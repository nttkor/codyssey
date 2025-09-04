import zipfile
import string
import itertools
import multiprocessing
import sys
import time
import os
'''
password_worker는 (worker_id, password, status_dict)를 받아 비밀번호를 시도하고 결과 없으면 None 반환
시도할 때마다 status_dict에 (시도 개수, 마지막 시도한 비밀번호)를 기록
monitor_status 프로세스가 1초마다 화면을 클리어하고 현재 시간 + 각 프로세스 상태 출력 (스크롤 없이 한 화면에서 덮어씀)
비밀번호 생성기는 generate_passwords_letters_then_digits()로 순서대로 소문자/숫자 조합 생성
각 비밀번호는 worker_id를 idx % NUM_WORKERS로 나눠 순환 배분
암호 해제 성공하면 해독 내용 출력하고 파일 저장 후 종료
'''
zip_filename = 'emergency_storage_key.zip'
target_file = 'password.txt'

def try_password(zip_file, filename, password):
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.setpassword(password.encode())
            if filename in zip_ref.namelist():
                with zip_ref.open(filename) as file:
                    return file.read().decode('utf-8')
    except:
        return None

def password_worker(args):
    """
    args = (worker_id, password, status_dict)
    """
    worker_id, password, status_dict = args
    content = try_password(zip_filename, target_file, password)
    # 상태 업데이트
    if worker_id in status_dict:
        count, _ = status_dict[worker_id]
        status_dict[worker_id] = (count + 1, password)
    else:
        status_dict[worker_id] = (1, password)
    if content:
        return (worker_id, password, content)
    return None

def generate_passwords_letters_then_digits():
    letters = string.ascii_lowercase
    digits = string.digits
    length = 6

    for num_digits in range(length + 1):
        num_letters = length - num_digits
        for letter_part in itertools.product(letters, repeat=num_letters):
            for digit_part in itertools.product(digits, repeat=num_digits):
                yield ''.join(letter_part + digit_part)

def caesar_cipher_decode(text):
    alphabet = string.ascii_lowercase
    for shift in range(1, 27):
        decoded = []
        for char in text:
            if char.isalpha():
                idx = alphabet.index(char.lower())
                shifted = alphabet[(idx - shift) % 26]
                decoded.append(shifted.upper() if char.isupper() else shifted)
            else:
                decoded.append(char)
        print(f'Shift {shift}: {"".join(decoded)}')

def monitor_status(status_dict, num_workers):
    """
    1초마다 시간과 각 프로세스 상태 출력 (덮어쓰기)
    """
    try:
        while True:
            time.sleep(1)
            # 커서 맨 위로 이동 (ANSI escape code)
            os.system('cls' if os.name == 'nt' else 'clear')  # 화면 전체 클리어 (더 깔끔)
            print(f"현재 시간: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            for i in range(num_workers):
                if i in status_dict:
                    count, last_pw = status_dict[i]
                    print(f"프로세스 {i}: 시도한 암호 개수={count}, 마지막 시도 암호={last_pw}")
                else:
                    print(f"프로세스 {i}: 아직 시작하지 않음")
            print("\n(암호 해제 중...)")
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    NUM_WORKERS = 6
    manager = multiprocessing.Manager()
    status_dict = manager.dict()

    pool = multiprocessing.Pool(NUM_WORKERS)

    # 비밀번호 생성 제너레이터
    pw_generator = generate_passwords_letters_then_digits()

    # 결과 저장용 변수
    found = None

    # 모니터 프로세스 실행
    monitor_proc = multiprocessing.Process(target=monitor_status, args=(status_dict, NUM_WORKERS))
    monitor_proc.daemon = True
    monitor_proc.start()

    def generate_args():
        """
        비밀번호 생성기에 worker_id와 상태 딕셔너리 같이 넘겨줌
        worker_id는 라운드로 순환시키기 위해 idx%NUM_WORKERS 사용
        """
        idx = 0
        for pw in pw_generator:
            yield (idx % NUM_WORKERS, pw, status_dict)
            idx += 1

    # imap_unordered로 비밀번호 하나씩 병렬 시도
    for res in pool.imap_unordered(password_worker, generate_args()):
        if res:
            worker_id, password, content = res
            print(f"\n암호 해제 성공! 비밀번호: {password}\n")
            caesar_cipher_decode(content)
            with open("passwd.txt", "w", encoding="utf-8") as f:
                f.write(content)
            found = True
            break

    pool.terminate()
    pool.join()
    monitor_proc.terminate()

    if not found:
        print("비밀번호를 찾지 못했습니다.")
