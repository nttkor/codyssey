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
'''
CRC32는 순환 중복 검사로, 데이터의 일관성을 확인하는 데 사용됩니다. 
이 테이블은 암호화된 데이터를 빠르게 복호화하기 위해 사용됩니다. 
ZIP 파일에서 ZipCrypto 방식의 복호화 시 CRC32 값이 중요하기 때문에, 
이 테이블을 이용해 복호화 효율성을 높입니다.
'''
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
        # IP 암호화에 사용되는 3개의 키입니다
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
        for byte in password:  #암호 글자수 만큼 update
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
    
    # ZIP 파일의 모든 파일 엔트리
    pos = data.find(b'PK\x03\x04')
    if pos == -1:
        raise ValueError("유효한 ZIP 파일이 아닙니다")
    
    # 헤더 파싱
    pos += 4  # 시그니처 건너뛰기
    # struct.unpack() 함수는 바이너리 데이터(바이트)를 특정 형식의 파이썬 값으로 변환하는 데 사용됩니다. <I와 <H는 그 변환 형식을 지정하는 포맷 문자열입니다.
    # H (부호 없는 2바이트 정수)
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
    # I (부호 없는 4바이트 정수)
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
    
    # 암호화 헤더 위치 계산: 파일명과 extra 필드 건너뛰기
    #로컬 파일 헤더는 고정된 길이를 가지지 않고, 파일명 길이(name_len)와 추가 필드 길이(extra_len)에 따라 그 길이가 달라집니다.
    pos += name_len + extra_len
    
    # 계산된 위치에서 12바이트를 읽어 암호화 헤더를 추출합니다.
    encrypted_header = data[pos:pos+12]
    
    # Check byte 계산 (bit 3 확인)
    # ZIP 파일의 압축 정보는 파일 데이터 뒤에 붙는 **데이터 디스크립터(Data Descriptor)**에 저장될 수도 있습니다. 이 플래그는 그 사용 여부를 나타냅니다.
    if flags & 0x8:  # Data descriptor 사용
        # check byte는 파일 수정 시간(mod_time)의 상위 1바이트에서 가져옵니다 ((mod_time >> 8) & 0xFF).
        check_byte = (mod_time >> 8) & 0xFF
    else:
        # crc32 값의 상위 1바이트에서 가져옵니다 ((crc32 >> 24) & 0xFF). 이 코드는 crc32 값을 24비트 오른쪽으로 이동시켜 상위 8비트(1바이트)만 남기는 연산입니다.
        check_byte = (crc32 >> 24) & 0xFF
    # 마지막으로, 함수는 추출한 12바이트 암호화 헤더(encrypted_header), 계산된 예상 check byte, 그리고 파일의 crc32 값을 튜플 형태로 반환합니다. 이 값들은 이후 브루트포스 워커 프로세스에서 사용됩니다.
    return encrypted_header, check_byte, crc32


def smart_password_generator():

    """통계적으로 가능성이 높은 순서로 암호 생성"""
    chars = string.ascii_lowercase
    digits = string.digits
    
    # 1. 흔한 패턴부터 (일반적인 암호 패턴) 제너레이터함수이기때문에 하니씩 리턴되고 멈춤
    common_starts = ['pass', 'test', 'admin', 'user', 'temp']
    
    # 흔한 패턴 우선 시도
    for start in common_starts:
        remaining_len = 6 - len(start)
        if remaining_len > 0:
            for combo in itertools.product(chars + digits, repeat=remaining_len):
                #yield를 사용하여 제너레이터로 동작 
                yield start + ''.join(combo)
    

    # 3. 끝에 숫자가 2개 오는 패턴 (예: test12, hello34 등)
    for digit_count in [2]:
        alpha_count = 6 - digit_count
        for alpha_combo in itertools.product(chars, repeat=alpha_count):
            for digit_combo in itertools.product(digits, repeat=digit_count):
                password = ''.join(alpha_combo) + ''.join(digit_combo)
                if not any(password.startswith(start) for start in common_starts):
                    yield password
    
    # 👉 여기서 순서 변경!
    # 2. 끝에 숫자가 오는 패턴 (예: passw1, hello3, abcde9 등)
    for digit_count in [1]:  # 숫자 1개 먼저
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
    '''
    개선된 워커 프로세스 - 문자+숫자 비율별 검색"
    worker_id: 각 워커를 구분하는 고유 ID입니다.
    zip_path: 암호를 해독할 ZIP 파일의 경로입니다.
    encrypted_header, check_byte: ZIP 파일에서 추출한 암호화 정보입니다. 이를 통해 실제 파일을 풀지 않고도 암호가 맞는지 빠르게 검증할 수 있습니다.
    queue: 암호를 찾았을 때 메인 프로세스에 결과를 전달하기 위한 **공유 큐(Queue)**입니다.
    total_workers: 전체 워커의 수입니다.
    '''
    worker_id, zip_path, encrypted_header, check_byte, queue, total_workers = args
    validator = ZipCryptoValidator() # 클래스의 인스턴스를 생성하여 암호 검증에 필요한 준비를 합니다. 이 객체는 각 워커마다 독립적으로 존재합니다.
    count = 0
    start_time = time.time()
    last_print_time = start_time
    
    print(f"[워커 {worker_id}/{total_workers}] 문자+숫자 조합 검색 시작", flush=True)
    
    # 워커별로 다른 시작점 사용 (인터리빙 방식)
    #  워커가 검색할 암호 조합을 규칙에 따라 생성합니다
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
                #성공시 암호를 공유큐에 넣는다
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
    '''
    공유 메모리 역할: Queue는 여러 프로세스가 안전하게 데이터를 주고받을 수 있는 통로 역할을 합니다.
    데이터 넣기: 암호 해독에 성공한 자식 프로세스는 자신이 찾은 암호를 result_queue.put() 메서드를 사용하여 큐에 넣습니다.
    데이터 가져오기: 메인 프로세스(부모 프로세스)는 result_queue.get()을 사용하여 큐에서 데이터를 가져옵니다.
    즉, 암호를 찾은 자식 프로세스가 직접 found_password 변수에 값을 저장하는 것이 아니라, 공유된 큐에 암호를 넣으면, 메인 프로세스가 그 값을 큐에서 꺼내와 자신의 found_password 변수에 할당하는 방식입니다.
    이러한 **큐(Queue)나 파이프(Pipe)**와 같은 IPC(Inter-Process Communication) 메커니즘을 사용해야만 독립적인 메모리 공간을 가진 프로세스 간에 데이터를 주고받을 수 있습니다.
    '''
    result_queue = manager.Queue() 
    
    # 작업 분배
    tasks = []
    for worker_id in range(max_workers):
        tasks.append((worker_id, zip_path, encrypted_header, check_byte, result_queue, max_workers))
    
    # 병렬 처리 Pool : Python의 multiprocessing 모듈에 있는 클래스로, 여러 개의 프로세스를 묶어 병렬로 작업을 처리할 수 있게 해줍니다.
    with Pool(processes=max_workers) as pool:
        print("스마트 브루트포스 공격 시작...")
        print("우선순위: 흔한 패턴 → 순수 알파벳 → 숫자 조합")
        print("-"*60)
        
        # 비동기 실행, 이는 모든 작업이 완료될 때까지 기다리지 않고 다음 코드를 실행할 수 있다는 뜻입니다.
        results = pool.map_async(worker_process_improved, tasks)
        
        # 결과 대기
        found_password = None
        try:
            #큐에 새로운 데이터(즉, 찾아낸 암호)가 있는지 지속적으로 확인합니다.
            while not results.ready():
                if not result_queue.empty():
                    found_password = result_queue.get() # 큐에서 암호를 가져옵니다
                    pool.terminate()
                    pool.join()
                    break
                time.sleep(0.1)
            # 하나의 워커 프로세스가 암호를 찾아서 큐에 put()한 동시에, 다른 모든 워커 프로세스가 작업을 완료했습니다.
            # 메인 프로세스가 results.ready()가 True가 되어 while 루프가 종료되었지만, result_queue.empty() 조건문이 실행되기 직전이라 break되지 못했습니다.
            # 이럴경우  큐에서 최종 결과를 가져오도록 합니다.
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


def main():
    """메인 함수"""
    os.chdir(os.path.dirname(__file__))
    print("ZIP 암호 해독 도구 v2.0")
    print("=" * 30)
    
    # 암호 해독 실행
    zip_file = 'emergency_storage_key.zip'
    #zip 암호를 푸는 메인함수
    password = unlock_zip(zip_file)
    
    if password:
        print(f"\n🎉 최종 결과: 암호는 '{password}' 입니다!")
        
        # 압축 해제 테스트
        try:
            with zipfile.ZipFile(zip_file) as zf:  #zipfile 객체를 만들어
                zf.extractall(pwd=password.encode())  # 암호를 byte로 변환후 zip파일내용의 암호화를 푼다.
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


