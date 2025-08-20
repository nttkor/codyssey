
# 이 코드는 ZIP 파일을 열기 위한 비밀번호를 찾아내는 프로그램으로, 멀티쓰레딩을 사용하여 가능한 모든 6자리 비밀번호 조합을 빠르게 시도하는 방식입니다. 이제 각 주요 부분을 좀 더 자세히 분석해보겠습니다.

# ### 1. **주요 목적**

# * ZIP 파일을 열 때 필요한 비밀번호를 찾고, 해당 비밀번호로 'password.txt' 파일을 추출하여 그 내용을 `passwd.txt`로 저장하는 것이 목표입니다.

# ### 2. **주요 함수 설명**

# #### `extract_file_from_zip(zip_file, filename, password=None)`

# * **목적**: ZIP 파일에서 특정 파일(예: `password.txt`)을 추출하여 내용을 반환합니다.
# * **매개변수**:

#   * `zip_file`: ZIP 파일의 경로.
#   * `filename`: 추출할 파일의 이름(이 코드에서는 `password.txt`).
#   * `password`: 비밀번호.
# * **동작**:

#   * ZIP 파일을 읽고, 주어진 비밀번호로 파일을 추출하려 시도합니다.
#   * 비밀번호가 맞으면 파일의 내용을 UTF-8로 디코딩하여 반환합니다.
#   * 비밀번호가 틀리면 `RuntimeError`가 발생하며 `None`을 반환합니다.

# #### `save_to_passwd_txt(decoded_text)`

# * **목적**: 성공적으로 추출된 `password.txt`의 내용을 `passwd.txt` 파일에 저장합니다.
# * **매개변수**: `decoded_text`는 추출한 텍스트입니다.
# * **동작**:

#   * 텍스트를 `passwd.txt`에 저장하고, 완료 메시지를 출력합니다.

# #### `try_password(zip_file, password, lock, progress_lock, progress_data)`

# * **목적**: 주어진 비밀번호로 ZIP 파일을 추출하여 파일 내용을 추출해보는 함수입니다.
# * **매개변수**:

#   * `zip_file`: ZIP 파일 경로.
#   * `password`: 시도할 비밀번호.
#   * `lock`: 멀티쓰레딩에서의 동기화(공유 자원 보호)용 락.
#   * `progress_lock`: 진행 상태 업데이트를 위한 락.
#   * `progress_data`: 진행 상태 정보(진행된 시도 횟수 등).
# * **동작**:

#   * 주어진 비밀번호로 `password.txt`를 추출하려 시도하고, 성공하면 비밀번호와 함께 그 내용을 `passwd.txt`에 저장합니다.
#   * 성공 시 `True`를 반환하고, 실패 시 `False`를 반환합니다.

# #### `generate_and_process_passwords(zip_file)`

# * **목적**: 모든 가능한 비밀번호 조합을 생성하고, 각 비밀번호로 `try_password` 함수를 멀티쓰레딩으로 실행합니다.
# * **매개변수**: `zip_file`은 ZIP 파일의 경로입니다.
# * **동작**:

#   * `string.ascii_lowercase + string.digits`을 이용해 가능한 6자리 비밀번호 조합을 생성합니다.
#   * `itertools.product`를 사용하여 모든 가능한 조합을 생성합니다.
#   * 최대 1024개의 쓰레드가 동시에 실행될 수 있도록 설정하여, 비밀번호를 빠르게 시도합니다.
#   * 비밀번호가 맞는지 확인하고, 결과를 출력합니다.
#   * 진행 상황을 출력하는 함수(`update_progress`)도 포함되어 있으며, 10,000번 시도마다 현재 진행 상태를 출력합니다.

# #### `main()`

# * **목적**: 프로그램의 진입점으로, ZIP 파일의 비밀번호를 찾아내기 위한 전체 프로세스를 실행합니다.
# * **동작**:

#   * ZIP 파일이 저장된 디렉토리로 이동하고, `generate_and_process_passwords` 함수를 호출하여 비밀번호를 찾아냅니다.

# ### 3. **멀티쓰레딩**

# * **쓰레드 생성 및 관리**:

#   * 비밀번호의 각 조합에 대해 새로운 쓰레드를 생성하여 `worker` 함수에서 `try_password`를 호출합니다.
#   * 한 번에 실행되는 쓰레드의 수는 `max_threads`(1024개)로 제한됩니다. 이를 초과하지 않도록 쓰레드를 기다리게 하며, 최대치에 도달할 경우 0.1초씩 대기 후 새로운 쓰레드를 시작합니다.
#   * 진행 상태를 추적하여, 10,000번마다 진행 상황을 출력합니다.

# * **동기화**:

#   * 여러 쓰레드가 동시에 실행되므로, 공유 자원(예: `progress_data`, 출력 등)에 대해 동기화가 필요합니다. 이를 위해 `threading.Lock()`을 사용하여 각 쓰레드가 안전하게 자원에 접근하도록 합니다.

# ### 4. **보안 및 성능**

# * **보안**: 비밀번호를 추측하는 방식은 무차별 대입(brute-force) 방법으로, 가능한 모든 비밀번호 조합을 시도합니다. 이 방법은 비밀번호가 단순한 경우에는 유효할 수 있지만, 비밀번호가 길거나 복잡한 경우엔 시간이 많이 걸릴 수 있습니다.
# * **성능**: 멀티쓰레딩을 사용하여 비밀번호를 동시에 여러 개 시도하는 방식으로 성능을 최적화하고 있습니다. `max_threads` 값을 조정하여 최대 실행되는 쓰레드 수를 제한하고, 시스템 자원 과부하를 방지하려고 합니다.

# ### 5. **작동 예시**

# * 이 코드는 `emergency_storage_key.zip`라는 ZIP 파일을 열기 위해 6자리 비밀번호(소문자 + 숫자 조합)를 시도합니다.
# * 만약 비밀번호가 맞으면, `password.txt`에서 내용을 읽어 `passwd.txt`로 저장합니다.
# * 작업 중에는 진행 상태를 출력하며, 모든 작업이 완료되면 "전체 작업이 완료되었습니다."라는 메시지를 출력합니다.

# ### 개선 사항

# * **에러 처리**: 현재는 오류가 발생하면 그냥 `None`을 반환하는 방식으로 예외를 처리합니다. 더 구체적인 오류 메시지를 제공하거나, 비밀번호를 계속 시도하는 방식을 개선할 수 있습니다.
# * **성능 개선**: `max_threads`가 너무 크면 시스템에 과부하를 일으킬 수 있습니다. 이는 하드웨어에 따라 다르므로, `max_threads` 값을 자동으로 조정할 수 있는 기능을 추가할 수 있습니다.

# 이 프로그램은 짧고 간단한 비밀번호를 빠르게 찾는 데 유용하지만, 복잡한 비밀번호에는 시간이 많이 걸릴 수 있습니다.

# 주요 변경 사항

# 진행 상태 출력:

# 진행 상태는 한 줄에서 업데이트됩니다. sys.stdout.write()를 사용해 줄을 덮어쓰고, sys.stdout.flush()로 즉시 화면에 반영합니다.

# 진행 시간(진행 시간: 00:00), 남은 시도 횟수(남은 시도: 123456), 현재 활성화된 쓰레드 수(쓰레드 수: 10)를 실시간으로 출력합니다.

# 시간은 시분초로 표시됩니다.

# 최적화된 쓰레드 관리:

# 쓰레드를 시작할 때, 현재 활성화된 쓰레드 수가 max_threads(1024개) 이하일 경우만 새로운 쓰레드를 생성합니다.

# max_threads 값은 하드웨어 성능에 따라 동적으로 조정할 수 있지만, 코드에서는 최대 1024개로 설정했습니다. 필요에 따라 조정 가능합니다.

# 진행 시간 및 남은 시간 표시:

# 전체 진행 시간과 남은 시간을 계산하여 출력합니다.

# 진행된 시도 수와 남은 시도 수를 바탕으로 예상 종료 시간을 계산해 표시합니다.


import zipfile
import string
import itertools
import sys
import time
import threading

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
    """해독된 내용을 passwd.txt 파일에 저장"""
    try:
        with open('passwd.txt', 'w') as passwd_file:
            passwd_file.write(decoded_text)
            print(f'암호가 해독되어 passwd.txt로 저장되었습니다.')
    except Exception as e:
        print(f'파일 저장 중 오류 발생: {e}')

# 비밀번호를 시도하는 함수 (멀티쓰레드에서 호출)
def try_password(zip_file, password, lock, progress_lock, progress_data):
    """주어진 비밀번호로 ZIP 파일을 추출해보고, 맞으면 결과를 출력하고 종료"""
    # 비밀번호 시도
    password_text = extract_file_from_zip(zip_file, 'password.txt', password)
    
    if password_text:
        with lock:
            print(f"\n암호가 해독되었습니다: {password}")
            save_to_passwd_txt(password_text)  # 해독된 내용을 passwd.txt로 저장
        return True  # 성공 시 종료
        
    return False  # 실패 시 계속 진행

# 비밀번호를 생성하면서 멀티쓰레드를 실행하는 함수
def generate_and_process_passwords(zip_file):
    """비밀번호를 생성하면서 멀티쓰레드를 실행"""
    characters = string.ascii_lowercase + string.digits  # 소문자 알파벳 + 숫자
    total_combinations = 36 ** 6  # 가능한 6자리 비밀번호의 조합 수
    lock = threading.Lock()  # 멀티쓰레드에서 공유 자원을 안전하게 사용하기 위한 락
    progress_lock = threading.Lock()  # 진행 상태 업데이트를 위한 락
    progress_data = {"count": 0, "start_time": time.time()}  # 진행 상태 추적

    active_threads = 0  # 현재 진행 중인 쓰레드 수
    max_threads = 1024  # 최대 쓰레드 수

    # 진행 상태 출력 함수
    def update_progress():
        nonlocal progress_data, active_threads
        elapsed_time = time.time() - progress_data["start_time"]
        remaining_combinations = total_combinations - progress_data["count"]  # 남은 시도 횟수
        remaining_time = (elapsed_time / progress_data["count"] if progress_data["count"] > 0 else 0) * remaining_combinations
        remaining_time = int(remaining_time)
        minutes, seconds = divmod(remaining_time, 60)

        # 진행 정보 출력 (스크롤되지 않도록 기존 라인에서 덮어쓰기)
        sys.stdout.write(f"\r시도: {progress_data['count']}  남은 시도: {remaining_combinations}  진행 시간: {minutes:02}:{seconds:02}  쓰레드 수: {active_threads}")
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
    import os

    # 원하는 디렉토리 경로
    new_directory = '/home/mpeg4/Codyssey/proj1/p5s1'

    # 디렉토리 변경
    os.chdir(new_directory)

    # 현재 디렉토리 확인
    print("현재 디렉토리:", os.getcwd())
    print("암호 추출을 시작합니다...V2")
    zip_filename = 'emergency_storage_key.zip'  # ZIP 파일 이름
    generate_and_process_passwords(zip_filename)

    # 종료 시간 및 처리 시간 출력
    print("\n전체 작업이 완료되었습니다.")

if __name__ == "__main__":
    main()
