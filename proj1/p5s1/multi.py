# multiprocessing.Pool:
# multiprocessing.Pool을 사용하여 CPU 코어 수만큼 프로세스 풀을 생성하고, 각 자리수(1부터 26까지)를 병렬로 처리합니다.
# pool.starmap 함수는 각 자리수에 대해 caesar_cipher_decode_segment 함수를 실행합니다. 이 방식은 여러 프로세서에서 병렬로 작업을 처리하여 속도를 크게 향상시킬 수 있습니다.
# caesar_cipher_decode_segment 함수:
# shift와 target_text를 받아 해당 자리수만큼 암호를 해독하는 함수입니다.
# 이 함수는 병렬로 실행되며, 결과가 반환되면 주 함수에서 출력하고, 사전에서 단어가 발견되면 파일에 저장합니다.
# 프로세스 수:
# cpu_count()를 사용하여 시스템에서 사용할 수 있는 CPU 코어 수 만큼 프로세스를 생성합니다. 이 방식은 멀티 코어 시스템에서 성능을 극대화합니다.
# 최적화 효과:
# 병렬 처리를 사용하면 여러 프로세서가 동시에 자리수를 풀기 때문에, 전체 시간이 크게 단축될 수 있습니다.
# 예를 들어, 12시간이 걸리는 작업이 1시간 이내로 처리될 수 있습니다 (CPU 코어 수에 따라 달라짐).
# 이 방법은 텍스트 길이가 길거나 많은 자리수를 테스트해야 하는 경우에 매우 효과적입니다.
import zipfile
import string
import multiprocessing

def caesar_cipher_decode_segment(shift, target_text):
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
    # 멀티프로세싱을 사용하여 자리수를 병렬로 처리
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())  # CPU 코어 수 만큼 프로세스 풀 생성
    shifts = range(1, 27)
    results = pool.starmap(caesar_cipher_decode_segment, [(shift, target_text) for shift in shifts])

    for shift, decoded_text in results:
        print(f'자리수 {shift}: {decoded_text}')
        
        # 사전에서 단어가 일치하는지 확인
        if is_valid_word(decoded_text):
            print(f"암호가 해독되었습니다: {decoded_text}")
            save_result(decoded_text)  # result.txt에 저장
            pool.close()
            pool.join()
            break

def is_valid_word(decoded_text):
    # 단어 사전을 활용하여 일치하는지 체크 (단어 목록을 만들어서 체크)
    dictionary = ["hello", "world", "test", "password"]  # 예시 사전
    decoded_words = decoded_text.split()  # 공백을 기준으로 분리
    for word in decoded_words:
        if word.lower() in dictionary:
            return True  # 사전에서 단어가 존재하면 True
    return False  # 존재하지 않으면 False

def save_result(decoded_text):
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
