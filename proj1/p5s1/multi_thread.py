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

    # 진행 상태 출력 함수
    def update_progress(password, remaining_combinations):
        sys.stdout.write(f"\r시도 중인 암호: {password} 남은 시도 횟수: {remaining_combinations:06d}")
        sys.stdout.flush()  # 출력 버퍼를 즉시 비움

    # 비밀번호를 생성하고 바로 쓰레드를 실행
    def worker(password):
        with progress_lock:
            progress_data["count"] += 1
        try_password(zip_file, password, lock, progress_lock, progress_data)
        with progress_lock:
            # 1000번마다 진행 상태 출력
            if progress_data["count"] % 10000 == 0:  # 1000번에 한번 갱신
                remaining_combinations = total_combinations - progress_data["count"]  # 남은 시도 횟수
                update_progress(password, remaining_combinations)

    # 가능한 모든 비밀번호 생성
    for password_tuple in itertools.product(characters, repeat=6):
        password = ''.join(password_tuple)  # tuple을 문자열로 변환

        # 비밀번호를 시도하는 쓰레드를 생성
        thread = threading.Thread(target=worker, args=(password,))
        thread.start()  # 쓰레드 실행

        # 쓰레드가 일정 수 이상 실행되면 모든 쓰레드가 끝날 때까지 대기
        if progress_data["count"] % 32 == 0:  # 32개의 쓰레드가 실행될 때마다
            thread.join()  # 모든 쓰레드가 완료될 때까지 기다림

    # 모든 쓰레드가 완료될 때까지 대기
    while threading.active_count() > 1:  # main thread를 제외한 active thread 수
        pass

# 전체 실행 함수
def main():
    generate_and_process_passwords(zip_filename)

    # 종료 시간 및 처리 시간 출력
    print("\n전체 작업이 완료되었습니다.")

if __name__ == "__main__":
    main()
