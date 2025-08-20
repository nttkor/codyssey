import zipfile
import string
import itertools
import sys
import time
import threading

# 암호 생성: 6자리 소문자 + 숫자
def generate_possible_passwords():
    """가능한 모든 비밀번호(6자리 숫자+소문자)를 생성"""
    characters = string.ascii_lowercase + string.digits  # 소문자 알파벳 + 숫자
    return [''.join(p) for p in itertools.product(characters, repeat=6)]  # 리스트로 변환

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
def try_password(zip_file, password, point, result_list, lock):
    """주어진 비밀번호로 ZIP 파일을 추출해보고, 맞으면 결과를 출력하고 종료"""
    # 비밀번호 시도
    password_text = extract_file_from_zip(zip_file, 'password.txt', password)
    
    if password_text:
        # 암호가 성공적으로 해독되었을 때
        with lock:
            print(f"\n암호가 해독되었습니다: {password}")
            save_to_passwd_txt(password_text)  # 해독된 내용을 passwd.txt로 저장
            result_list.append(password)  # 성공한 비밀번호 리스트에 추가
        return True  # 성공 시 종료
        
    return False  # 실패 시 계속 진행

# 비밀번호를 멀티쓰레드로 시도하는 함수
def process_passwords(zip_file, passwords, result_list):
    """멀티쓰레드를 사용하여 암호들을 시도"""
    lock = threading.Lock()  # 멀티쓰레드에서 공유 자원을 안전하게 사용하기 위한 락
    threads = []
    point = 0  # 현재까지 처리된 암호의 인덱스
    
    # 진행 상태 출력 함수
    def update_progress(start_time, count):
        total_combinations = len(passwords)  # 총 암호 조합 수
        elapsed_time = time.time() - start_time  # 경과 시간
        remaining_combinations = total_combinations - count  # 남은 시도 횟수
        avg_time_per_attempt = elapsed_time / count if count > 0 else 0  # 평균 시도당 시간
        remaining_time = avg_time_per_attempt * remaining_combinations  # 남은 시간 계산
        
        # 남은 시간을 6자리로 고정, 초 단위로 표시
        remaining_seconds = int(remaining_time)  # 소수점 없는 정수로 변환
        sys.stdout.flush()  # 출력 버퍼를 즉시 비움
        sys.stdout.write(f"\r남은 시간: {remaining_seconds:06d}초    ")
       

    # 쓰레드 실행
    def worker():
        nonlocal point
        while point < len(passwords):
            password = passwords[point]
            point += 1  # 처리된 포인트 증가
            try_password(zip_file, password, point, result_list, lock)
            # 진행 상태 업데이트
            update_progress(start_time, point)
    
    # 쓰레드 수 설정: 32개 쓰레드로 작업을 나누어 처리
    num_threads = 32
    for _ in range(num_threads):
        thread = threading.Thread(target=worker)
        thread.start()
        threads.append(thread)
    
    # 모든 쓰레드가 끝날 때까지 대기
    for thread in threads:
        thread.join()

# 전체 실행 함수
def main():
    zip_filename = 'emergency_storage_key.zip'  # ZIP 파일 이름
    passwords = generate_possible_passwords()  # 가능한 모든 비밀번호 생성
    result_list = []  # 성공적인 비밀번호를 저장할 리스트

    start_time = time.time()  # 시작 시간 기록

    # 멀티쓰레드로 암호를 시도
    process_passwords(zip_filename, passwords, result_list)

    # 종료 시간 및 처리 시간 출력
    elapsed_time = time.time() - start_time
    print(f"\n전체 작업이 완료되었습니다. 소요 시간: {elapsed_time:.2f}초")
    if result_list:
        print(f"성공한 비밀번호: {result_list[0]}")
    else:
        print("암호를 찾지 못했습니다.")

if __name__ == "__main__":
    main()

