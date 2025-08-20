# 코드 설명

# extract_file_from_zip 함수:

# ZIP 파일에서 주어진 password.txt 파일을 추출하고 비밀번호를 맞추면 그 내용을 반환합니다. 비밀번호가 틀리면 None을 반환합니다.

# save_to_passwd_txt 함수:

# 비밀번호를 풀었을 때 그 내용을 password.txt 파일에 저장합니다.

# try_password 함수:

# 주어진 비밀번호로 ZIP 파일을 추출해 보고, 맞으면 비밀번호를 저장하고 종료합니다.

# unlock_zip 함수:

# 가능한 모든 6자리 비밀번호 조합을 생성하고, 멀티스레드를 사용하여 비밀번호를 시도합니다.

# 각 비밀번호 조합에 대해 worker 함수가 쓰레드로 실행됩니다.

# 진행 상태는 실시간으로 콘솔에 출력됩니다.

# main 함수:

# unlock_zip 함수를 호출하여 ZIP 파일의 암호를 풀기 시작합니다.

# 작업이 완료되면 "전체 작업이 완료되었습니다."라는 메시지가 출력됩니다.

# 암호 추출을 시작합니다...
# 시도 횟수: 15000 남은 횟수: 2176768336 경과 시간: 45.00초
# ...
# 시도 횟수: 2176782336 남은 횟수: 0 경과 시간: 1234.56초
# 암호가 해독되었습니다: abc123
# 암호가 해독되어 password.txt로 저장되었습니다.
# 전체 작업이 완료되었습니다.

import zipfile
import string
import itertools
import time
import threading
import sys

# 시간을 시, 분, 초 형식으로 변환하는 함수
def format_time(seconds):
    """초 단위 시간을 시, 분, 초 형식으로 변환"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

# ZIP 파일에서 비밀번호로 파일을 추출하는 함수
def extract_file_from_zip(zip_file, filename, password=None):
    """ZIP 파일에서 특정 파일을 추출하여 내용을 반환하는 함수 (암호화된 파일 처리)"""
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            if password:
                zip_ref.setpassword(password.encode())  # 비밀번호 설정
            if filename in zip_ref.namelist():
                with zip_ref.open(filename) as file:
                    content = file.read().decode('utf-8')  # 파일 내용을 UTF-8로 디코딩
                    return content
            else:
                return None
    except RuntimeError:  # 비밀번호가 틀렸을 때 발생하는 오류
        return None  # 비밀번호가 틀리면 None을 리턴하고 계속 진행
    except Exception:  # 그 외의 예외 발생 시 처리
        return None  # 그 외 오류 발생 시 None 리턴

# 암호를 찾았을 때 파일에 저장하는 함수
def save_to_passwd_txt(decoded_text):
    """해독된 내용을 password.txt 파일에 저장"""
    try:
        with open('password.txt', 'w') as passwd_file:
            passwd_file.write(decoded_text)
            print(f'암호가 해독되어 password.txt로 저장되었습니다.')
    except Exception as e:
        print(f'파일 저장 중 오류 발생: {e}')

# 비밀번호를 시도하는 함수 (멀티쓰레드에서 호출)
def try_password(zip_file, password, lock, progress_lock, progress_data):
    """주어진 비밀번호로 ZIP 파일을 추출해보고, 맞으면 결과를 출력하고 종료"""
    password_text = extract_file_from_zip(zip_file, 'password.txt', password)
    
    if password_text:
        with lock:
            print(f"\n암호가 해독되었습니다: {password}")
            save_to_passwd_txt(password_text)  # 해독된 내용을 password.txt로 저장
        return True  # 성공 시 종료
        
    return False  # 실패 시 계속 진행

# 비밀번호를 생성하면서 멀티쓰레드를 실행하는 함수
def unlock_zip(zip_file):
    """비밀번호를 생성하면서 멀티쓰레드를 실행"""
    characters = string.ascii_lowercase + string.digits  # 소문자 알파벳 + 숫자
    total_combinations = 36 ** 6  # 가능한 6자리 비밀번호의 조합 수
    lock = threading.Lock()  # 멀티쓰레드에서 공유 자원을 안전하게 사용하기 위한 락
    progress_lock = threading.Lock()  # 진행 상태 업데이트를 위한 락
    progress_data = {"count": 0, "start_time": time.time(), "last_update": time.time()}  # 진행 상태 추적

    active_threads = 0  # 현재 진행 중인 쓰레드 수
    max_threads = 1024  # 최대 쓰레드 수

    # 진행 상태 출력 함수
    def update_progress():
        nonlocal progress_data
        elapsed_time = time.time() - progress_data["start_time"]
        remaining_combinations = total_combinations - progress_data["count"]  # 남은 시도 횟수

        # 초당 시도 횟수 (속도) 추정
        if elapsed_time > 0:
            attempts_per_second = progress_data["count"] / elapsed_time
        else:
            attempts_per_second = 0

        # 예상 남은 시간 (초 단위)
        if attempts_per_second > 0:
            remaining_time = remaining_combinations / attempts_per_second
        else:
            remaining_time = 0

        # 경과 시간과 예상 시간을 시, 분, 초 형식으로 출력
        elapsed_time_str = format_time(elapsed_time)
        remaining_time_str = format_time(remaining_time)

        sys.stdout.write(f"\r시도 횟수: {progress_data['count']} 남은 횟수: {remaining_combinations} 경과 시간: {elapsed_time_str} 예상 시간: {remaining_time_str}")
        sys.stdout.flush()  # 출력 버퍼를 즉시 비움

    # 비밀번호를 생성하고 바로 쓰레드를 실행
    def worker(password):
        nonlocal active_threads
        with progress_lock:
            progress_data["count"] += 1
        try_password(zip_file, password, lock, progress_lock, progress_data)
        with progress_lock:
            active_threads -= 1
        if progress_data["count"] % 10000 == 0:
            with progress_lock:
                update_progress()

    # 가능한 모든 비밀번호 생성
    for password_tuple in itertools.product(characters, repeat=6):
        password = ''.join(password_tuple)  # tuple을 문자열로 변환

        # 쓰레드를 시작하는 조건
        while active_threads >= max_threads:
            time.sleep(0.1)  # 쓰레드가 끝날 때까지 기다림 (최대 1024개 쓰레드가 실행 중일 때)

        # 비밀번호를 시도하는 쓰레드를 생성
        thread = threading.Thread(target=worker, args=(password,))
        thread.start()
        with progress_lock:
            active_threads += 1  # 활성화된 쓰레드 수 증가

    # 모든 쓰레드가 완료될 때까지 대기
    while threading.active_count() > 1:  # main thread를 제외한 active thread 수
        time.sleep(0.1)

# 전체 실행 함수
def main():
    zip_filename = 'emergency_storage_key.zip'  # ZIP 파일 이름
    print("암호 추출을 시작합니다...")
    unlock_zip(zip_filename)  # 암호 추출 함수 호출

    # 종료 시간 및 처리 시간 출력
    print("\n전체 작업이 완료되었습니다.")

if __name__ == "__main__":
    main()
