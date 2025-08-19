import zipfile
import string
import multiprocessing
import time
import sys

def spinning_clock():
    """시계처럼 돌아가는 애니메이션"""
    spinner = ['-\\', '|', '/', '-', '\\', '|', '/']
    while True:
        for frame in spinner:
            sys.stdout.write(f'\r{frame}')  # 현재 줄에서 덮어쓰며 출력
            sys.stdout.flush()  # 출력 버퍼를 즉시 비움
            time.sleep(1)  # 1초 대기

def caesar_cipher_decode_segment(shift, target_text):
    """각 자리수를 풀어내는 작업"""
    alphabet = string.ascii_lowercase
    decoded_text = []

    for char in target_text:
        if char.isalpha():
            if char.islower():
                new_char = alphabet[(alphabet.index(char) - shift) % 26]
            elif char.isupper():
                new_char = alphabet[(alphabet.index(char.lower()) - shift) % 26].upper()
            decoded_text.append(new_char)
        else:
            decoded_text.append(char)

    return shift, ''.join(decoded_text)

def caesar_cipher_decode(target_text):
    """카이사르 암호 해독 함수, 진행 상태를 1분마다 출력"""
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    shifts = range(1, 27)
    results = []
    
    # 진행 상황을 출력할 시간 기록
    start_time = time.time()
    last_report_time = start_time

    for shift in shifts:
        results.append(pool.apply_async(caesar_cipher_decode_segment, (shift, target_text)))

    # 결과 처리 및 1분마다 진행상황 출력
    decoded_results = []
    total_shifts = len(shifts)
    
    # 시계 애니메이션을 별도의 쓰레드에서 실행
    from threading import Thread
    clock_thread = Thread(target=spinning_clock)
    clock_thread.daemon = True  # 메인 프로그램이 끝날 때 함께 종료되도록 설정
    clock_thread.start()

    for i, result in enumerate(results):
        shift, decoded_text = result.get()
        decoded_results.append((shift, decoded_text))
        
        # 1분마다 진행 상황 출력
        elapsed_time = time.time() - start_time
        if elapsed_time - last_report_time >= 60:  # 1분이 지난 경우
            percent_complete = (i + 1) / total_shifts * 100
            print(f"진행 상황: {percent_complete:.2f}% 완료")
            last_report_time = time.time()  # 마지막 보고 시간 갱신

    pool.close()
    pool.join()

    # 해독된 결과 출력 및 사전 확인
    for shift, decoded_text in decoded_results:
        print(f'자리수 {shift}: {decoded_text}')
        
        # 사전에서 단어가 일치하는지 확인
        if is_valid_word(decoded_text):
            print(f"암호가 해독되었습니다: {decoded_text}")
            save_result(decoded_text)  # result.txt에 저장
            break

def is_valid_word(decoded_text):
    """사전에서 단어가 존재하는지 확인"""
    dictionary = ["hello", "world", "test", "password"]  # 예시 사전
    decoded_words = decoded_text.split()  # 공백을 기준으로 분리
    for word in decoded_words:
        if word.lower() in dictionary:
            return True  # 사전에서 단어가 존재하면 True
    return False  # 존재하지 않으면 False

def save_result(decoded_text):
    """해독된 결과를 파일에 저장"""
    try:
        with open('result.txt', 'w') as result_file:
            result_file.write(decoded_text)
            print(f'결과가 result.txt에 저장되었습니다: {decoded_text}')
    except Exception as e:
        print(f'결과 저장 중 오류 발생: {e}')

def extract_file_from_zip(zip_file, filename):
    """ZIP 파일에서 특정 파일을 추출하여 내용을 반환하는 함수"""
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            # ZIP 파일 내에 파일 목록 확인
            if filename in zip_ref.namelist():
                with zip_ref.open(filename) as file:
                    content = file.read().decode('utf-8')  # 파일 내용을 UTF-8로 디코딩
                    return content
            else:
                print(f'{filename} 파일이 ZIP에 없습니다.')
                return None
    except zipfile.BadZipFile:
        print("ZIP 파일이 잘못되었습니다.")
        return None
    except Exception as e:
        print(f'ZIP 파일 처리 중 오류 발생: {e}')
        return None

def read_password_from_zip(zip_file):
    """ZIP 파일에서 암호문이 담긴 password.txt 파일을 읽어오는 함수"""
    password_text = extract_file_from_zip(zip_file, 'password.txt')
    if password_text:
        caesar_cipher_decode(password_text)  # 카이사르 암호 해독

if __name__ == "__main__":
    zip_filename = 'encrypted.zip'  # ZIP 파일 이름
    read_password_from_zip(zip_filename)  # ZIP 파일에서 암호문 읽기 및 해독
