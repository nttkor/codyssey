#!/usr/bin/env python3
"""
door_hacking.py - 개선된 ZIP 파일 암호 해독 프로그램
ZipCrypto 헤더 검증을 활용한 고속 브루트포스 구현
크로스 플랫폼 지원 (Windows/Linux/Mac)
"""

import zipfile
import zlib
import struct
import time
import itertools
import platform
from multiprocessing import Pool, Queue, Manager, cpu_count
from datetime import datetime
import os
import sys
import string

# CRC32 테이블 초기화
CRC32_TABLE = []
for i in range(256):
    crc = i
    for _ in range(8):
        if crc & 1:
            crc = (crc >> 1) ^ 0xEDB88320
        else:
            crc = crc >> 1
    CRC32_TABLE.append(crc)

class ZipCryptoValidator:
    """ZipCrypto 빠른 검증을 위한 클래스"""
    
    def __init__(self):
        self.keys = [0x12345678, 0x23456789, 0x34567890]
    
    def reset_keys(self):
        """키를 초기 상태로 리셋"""
        self.keys = [0x12345678, 0x23456789, 0x34567890]
    
    def crc32_update(self, crc, byte):
        """CRC32 한 바이트 업데이트"""
        return CRC32_TABLE[(crc ^ byte) & 0xFF] ^ (crc >> 8)
    
    def update_keys(self, byte):
        """3개의 키 업데이트"""
        self.keys[0] = self.crc32_update(self.keys[0], byte)
        self.keys[1] = ((self.keys[1] + (self.keys[0] & 0xFF)) * 134775813 + 1) & 0xFFFFFFFF
        self.keys[2] = self.crc32_update(self.keys[2], (self.keys[1] >> 24) & 0xFF)
    
    def init_keys(self, password):
        """비밀번호로 키 초기화"""
        self.reset_keys()
        for byte in password:
            self.update_keys(byte)
    
    def decrypt_byte(self, enc_byte):
        """한 바이트 복호화"""
        temp = (self.keys[2] & 0xFFFF) | 2
        keystream = ((temp * (temp ^ 1)) >> 8) & 0xFF
        plain = enc_byte ^ keystream
        self.update_keys(plain)
        return plain
    
    def check_password_fast(self, password, encrypted_header, check_byte_expected):
        """헤더의 check byte로 빠른 검증 (1/256 정확도)"""
        self.init_keys(password.encode() if isinstance(password, str) else password)
        
        # 12바이트 헤더 복호화
        for i in range(11):
            self.decrypt_byte(encrypted_header[i])
        
        # 12번째 바이트 (check byte) 확인
        check_byte = self.decrypt_byte(encrypted_header[11])
        return check_byte == check_byte_expected

def get_zip_info(zip_path):
    """ZIP 파일에서 암호화 헤더와 CRC 정보 추출"""
    with open(zip_path, 'rb') as f:
        data = f.read()
    
    # ZIP 로컬 파일 헤더 찾기
    pos = data.find(b'PK\x03\x04')
    if pos == -1:
        raise ValueError("유효한 ZIP 파일이 아닙니다")
    
    # 헤더 파싱
    pos += 4  # 시그니처 건너뛰기
    version = struct.unpack('<H', data[pos:pos+2])[0]
    pos += 2
    flags = struct.unpack('<H', data[pos:pos+2])[0]
    pos += 2
    
    if not (flags & 0x1):  # 암호화 플래그 확인
        raise ValueError("암호화되지 않은 ZIP 파일입니다")
    
    method = struct.unpack('<H', data[pos:pos+2])[0]
    pos += 2
    mod_time = struct.unpack('<H', data[pos:pos+2])[0]
    pos += 2
    mod_date = struct.unpack('<H', data[pos:pos+2])[0]
    pos += 2
    crc32 = struct.unpack('<I', data[pos:pos+4])[0]
    pos += 4
    comp_size = struct.unpack('<I', data[pos:pos+4])[0]
    pos += 4
    uncomp_size = struct.unpack('<I', data[pos:pos+4])[0]
    pos += 4
    name_len = struct.unpack('<H', data[pos:pos+2])[0]
    pos += 2
    extra_len = struct.unpack('<H', data[pos:pos+2])[0]
    pos += 2
    
    # 파일명과 extra 필드 건너뛰기
    pos += name_len + extra_len
    
    # 암호화된 헤더 12바이트
    encrypted_header = data[pos:pos+12]
    
    # Check byte 계산 (bit 3 확인)
    if flags & 0x8:  # Data descriptor 사용
        check_byte = (mod_time >> 8) & 0xFF
    else:
        check_byte = (crc32 >> 24) & 0xFF
    
    return encrypted_header, check_byte, crc32

def generate_password_chunks(num_workers=8):
    """워커 수에 맞게 암호 공간을 균등 분할"""
    chars = string.ascii_lowercase  # 'abcdefghijklmnopqrstuvwxyz'
    digits = string.digits         # '0123456789'
    
    # 전체 조합 수 계산
    # 1. 순수 알파벳 6자: 26^6
    # 2. 알파벳 5자 + 숫자 1자: 6 * 26^5 * 10 (위치별)
    # 3. 알파벳 4자 + 숫자 2자: 15 * 26^4 * 10^2 (위치별)
    
    total_alpha_6 = 26**6
    total_alpha_5_digit_1 = 6 * (26**5) * 10
    total_alpha_4_digit_2 = 15 * (26**4) * (10**2)
    
    total_combinations = total_alpha_6 + total_alpha_5_digit_1 + total_alpha_4_digit_2
    chunk_size = total_combinations // num_workers
    
    chunks = []
    current_count = 0
    
    # 1. 순수 알파벳 6자리 분할
    alpha_chunk_size = total_alpha_6 // num_workers
    for i in range(num_workers):
        start_idx = i * alpha_chunk_size
        end_idx = (i + 1) * alpha_chunk_size if i < num_workers - 1 else total_alpha_6
        chunks.append(('alpha_6', start_idx, end_idx))
    
    return chunks

def password_generator_chunk(pattern_type, start_idx, end_idx):
    """지정된 범위의 암호 조합 생성"""
    chars = string.ascii_lowercase
    digits = string.digits
    
    if pattern_type == 'alpha_6':
        # 순수 알파벳 6자리
        count = 0
        for combo in itertools.product(chars, repeat=6):
            if start_idx <= count < end_idx:
                yield ''.join(combo)
            count += 1
            if count >= end_idx:
                break
    
    elif pattern_type == 'alpha_5_digit_1':
        # 알파벳 5자 + 숫자 1자
        count = 0
        for pos in range(6):  # 숫자가 들어갈 위치
            for combo in itertools.product(chars, repeat=5):
                for digit in digits:
                    if start_idx <= count < end_idx:
                        password = list(''.join(combo))
                        password.insert(pos, digit)
                        yield ''.join(password[:6])
                    count += 1
                    if count >= end_idx:
                        return
    
    elif pattern_type == 'alpha_4_digit_2':
        # 알파벳 4자 + 숫자 2자
        count = 0
        for pos1 in range(6):
            for pos2 in range(pos1 + 1, 6):
                for combo in itertools.product(chars, repeat=4):
                    for d1 in digits:
                        for d2 in digits:
                            if start_idx <= count < end_idx:
                                password = list(''.join(combo))
                                password.insert(pos1, d1)
                                password.insert(pos2, d2)
                                yield ''.join(password[:6])
                            count += 1
                            if count >= end_idx:
                                return

def smart_password_generator():
    """통계적으로 가능성이 높은 순서로 암호 생성"""
    chars = string.ascii_lowercase
    digits = string.digits
    
    # 1. 흔한 패턴부터 (일반적인 암호 패턴)
    common_starts = ['pass', 'test', 'admin', 'user', 'temp']
    
    # 흔한 패턴 우선 시도
    for start in common_starts:
        remaining_len = 6 - len(start)
        if remaining_len > 0:
            for combo in itertools.product(chars + digits, repeat=remaining_len):
                yield start + ''.join(combo)
    
    # 👉 여기서 순서 변경!
    # 2. 끝에 숫자가 오는 패턴 (예: passw1, hello3, abcde9 등)
    for digit_count in [1]:  # 숫자 1개 먼저
        alpha_count = 6 - digit_count
        for alpha_combo in itertools.product(chars, repeat=alpha_count):
            for digit_combo in itertools.product(digits, repeat=digit_count):
                password = ''.join(alpha_combo) + ''.join(digit_combo)
                if not any(password.startswith(start) for start in common_starts):
                    yield password
    
    # 3. 끝에 숫자가 2개 오는 패턴 (예: test12, hello34 등)
    for digit_count in [2]:
        alpha_count = 6 - digit_count
        for alpha_combo in itertools.product(chars, repeat=alpha_count):
            for digit_combo in itertools.product(digits, repeat=digit_count):
                password = ''.join(alpha_combo) + ''.join(digit_combo)
                if not any(password.startswith(start) for start in common_starts):
                    yield password
    
    # 4. 중간에 숫자가 있는 패턴
    for digit_pos in range(1, 5):  # 첫 자리와 마지막 자리 제외
        for alpha_combo in itertools.product(chars, repeat=5):
            for digit in digits:
                password = list(''.join(alpha_combo))
                password.insert(digit_pos, digit)
                password_str = ''.join(password[:6])
                if not any(password_str.startswith(start) for start in common_starts):
                    yield password_str
    
    # 5. 마지막으로 순수 알파벳 (사전 순서)
    for combo in itertools.product(chars, repeat=6):
        password = ''.join(combo)
        if not any(password.startswith(start) for start in common_starts):
            yield password


def worker_process_improved(args):
    """개선된 워커 프로세스 - 문자+숫자 비율별 검색"""
    worker_id, zip_path, encrypted_header, check_byte, queue, total_workers = args
    validator = ZipCryptoValidator()
    count = 0
    start_time = time.time()
    last_print_time = start_time
    
    print(f"[워커 {worker_id}/{total_workers}] 문자+숫자 조합 검색 시작", flush=True)
    
    # 워커별로 다른 시작점 사용 (인터리빙 방식)
    password_gen = smart_password_generator()
    
    # 워커 ID에 따라 시작 오프셋 설정
    skip_count = 0
    for password in password_gen:
        # 워커별 인터리빙 (N번째마다 처리)
        if skip_count % total_workers != worker_id:
            skip_count += 1
            continue
            
        count += 1
        skip_count += 1
        
        # 진행상황 출력 (2만개마다 또는 5초마다)
        current_time = time.time()
        if count % 200000 == 0 or (current_time - last_print_time) >= 5:
            elapsed = current_time - start_time
            speed = count / elapsed if elapsed > 0 else 0
            print(f"[wid {worker_id}] {elapsed:.0f}: {password} | {count/1000:.0f}K | {speed:.0f} pw/s", flush=True)
            last_print_time = current_time
        
        # 빠른 헤더 검증
        if validator.check_password_fast(password, encrypted_header, check_byte):
            # 실제 ZIP 파일로 최종 검증
            try:
                with zipfile.ZipFile(zip_path) as zf:
                    zf.extractall(pwd=password.encode())
                print(f"\n🎉 [성공!] 워커 {worker_id}가 암호 발견: {password}", flush=True)
                queue.put(password)
                return password
            except:
                # False positive - 계속 검색
                #print(f"[워커 {worker_id}] False positive: {password} (계속 검색...)", flush=True)
                pass
    
    elapsed = time.time() - start_time
    print(f"[워커 {worker_id}] 완료: 총 {count:,}개 검사 (소요시간: {elapsed:.1f}초)", flush=True)
    return None

def unlock_zip(zip_path='emergency_storage_key.zip', max_workers=None):
    """
    ZIP 파일 암호 해독 함수 (개선 버전)
    
    Args:
        zip_path: 해독할 ZIP 파일 경로
        max_workers: 최대 워커 수 (None이면 CPU 코어 수)
    
    Returns:
        str: 찾은 비밀번호 또는 None
    """
    print("="*60)
    print("개선된 ZIP 암호 해독 프로그램 시작")
    print("="*60)
    print(f"대상 파일: {os.path.abspath(zip_path)}")
    print(f"시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"시스템 정보: {platform.system()} {platform.release()}")
    
    # ZIP 파일 정보 추출
    try:
        encrypted_header, check_byte, crc32 = get_zip_info(zip_path)
        print(f"✓ 암호화 헤더 추출 완료")
        print(f"  - CRC32: 0x{crc32:08X}")
        print(f"  - Check byte: 0x{check_byte:02X}")
    except Exception as e:
        print(f"✗ 오류: {e}")
        return None
    
    # 멀티프로세싱 설정
    if max_workers is None:
        max_workers = min(cpu_count(), 8)  # 최적 성능을 위해 8개로 제한
    
    print(f"✓ 사용할 워커 수: {max_workers}")
    print(f"✓ 검색 전략: 스마트 패턴 기반 (흔한 암호부터)")
    print("-"*60)
    
    start_time = time.time()
    manager = Manager()
    result_queue = manager.Queue()
    
    # 작업 분배
    tasks = []
    for worker_id in range(max_workers):
        tasks.append((worker_id, zip_path, encrypted_header, check_byte, result_queue, max_workers))
    
    # 병렬 처리
    with Pool(processes=max_workers) as pool:
        print("스마트 브루트포스 공격 시작...")
        print("우선순위: 흔한 패턴 → 순수 알파벳 → 숫자 조합")
        print("-"*60)
        
        # 비동기 실행
        results = pool.map_async(worker_process_improved, tasks)
        
        # 결과 대기
        found_password = None
        try:
            while not results.ready():
                if not result_queue.empty():
                    found_password = result_queue.get()
                    pool.terminate()
                    pool.join()
                    break
                time.sleep(0.1)
            
            if found_password is None and not result_queue.empty():
                found_password = result_queue.get()
                
        except KeyboardInterrupt:
            print("\n사용자에 의해 중단되었습니다.")
            pool.terminate()
            pool.join()
            return None
    
    # 결과 출력
    elapsed_time = time.time() - start_time
    print("-"*60)
    print(f"종료 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"총 소요 시간: {elapsed_time:.2f}초")
    
    if found_password:
        print(f"✓ 암호 해독 성공: '{found_password}'")
        
        # 암호를 파일로 저장
        try:
            with open('password.txt', 'w', encoding='utf-8') as f:
                f.write(found_password)
            print(f"✓ 암호가 password.txt 파일로 저장되었습니다")
        except Exception as e:
            print(f"✗ 파일 저장 실패: {e}")
        
        return found_password
    else:
        print("✗ 지정된 조건에서 암호를 찾지 못했습니다")
        print("힌트: 암호가 더 복잡하거나 다른 패턴일 수 있습니다")
        return None

def find_zip_file():
    """ZIP 파일을 자동으로 찾기"""
    zip_filename = 'emergency_storage_key.zip'
    
    # 가능한 경로들
    search_paths = [
        '.',  # 현재 디렉토리
        '..',  # 상위 디렉토리
        os.path.join('..', '..'),
        'Codyssey/proj1/p5s1',
        '../Codyssey/proj1/p5s1',
        '../../Codyssey/proj1/p5s1',
        'proj1/p5s1',
        '../proj1/p5s1',
        'p5s1',
        '../p5s1',
    ]
    
    # OS별 추가 경로
    home_dir = os.path.expanduser('~')
    if platform.system() == 'Windows':
        search_paths.extend([
            os.path.join(home_dir, 'Codyssey', 'proj1', 'p5s1'),
            os.path.join('C:', 'Codyssey', 'proj1', 'p5s1'),
            os.path.join(home_dir, 'Documents', 'Codyssey', 'proj1', 'p5s1'),
            os.path.join(home_dir, 'Desktop', 'Codyssey', 'proj1', 'p5s1'),
        ])
    else:  # Linux/Mac
        search_paths.extend([
            os.path.join('/home', os.environ.get('USER', ''), 'Codyssey', 'proj1', 'p5s1'),
            os.path.join(home_dir, 'Codyssey', 'proj1', 'p5s1'),
        ])
    
    # 파일 검색
    for path in search_paths:
        full_path = os.path.join(path, zip_filename)
        if os.path.exists(full_path):
            return os.path.abspath(full_path)
    
    return None

def main():
    """메인 함수"""
    print("ZIP 암호 해독 도구 v2.0")
    print("=" * 30)
    
    # ZIP 파일 찾기
    zip_file = find_zip_file()
    if not zip_file:
        print(f"✗ 오류: emergency_storage_key.zip 파일을 찾을 수 없습니다")
        print(f"현재 디렉토리: {os.getcwd()}")
        print(f"디렉토리 내용:")
        try:
            for item in os.listdir('.'):
                print(f"  - {item}")
        except:
            print("  (디렉토리 읽기 실패)")
        return 1
    
    print(f"✓ 대상 파일 발견: {zip_file}")
    
    # 파일 크기 확인
    try:
        file_size = os.path.getsize(zip_file)
        print(f"✓ 파일 크기: {file_size:,} bytes")
    except:
        print("✗ 파일 크기 확인 실패")
    
    # 암호 해독 실행
    password = unlock_zip(zip_file)
    
    if password:
        print(f"\n🎉 최종 결과: 암호는 '{password}' 입니다!")
        
        # 압축 해제 테스트
        try:
            with zipfile.ZipFile(zip_file) as zf:
                zf.extractall(pwd=password.encode())
                print("✓ 파일 압축 해제 성공")
                
                # 압축 해제된 파일 목록
                extracted_files = zf.namelist()
                print(f"✓ 추출된 파일 ({len(extracted_files)}개):")
                for filename in extracted_files:
                    print(f"  - {filename}")
                    
        except Exception as e:
            print(f"✗ 압축 해제 실패: {e}")
        
        return 0
    else:
        print("\n💔 암호를 찾지 못했습니다.")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n프로그램이 사용자에 의해 중단되었습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"\n예상치 못한 오류가 발생했습니다: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)