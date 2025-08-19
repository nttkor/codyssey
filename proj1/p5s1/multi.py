
# 병렬 처리 설명:

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
# 변경 사항:

# generate_possible_passwords: itertools.product를 사용하여 가능한 모든 6자리 비밀번호 조합을 생성합니다. (소문자 알파벳과 숫자)

# read_password_from_zip: 각 비밀번호를 시도하면서 ZIP 파일을 열고, 성공할 경우 암호를 해독합니다.

# 암호 시도 출력: 어떤 비밀번호를 시도하는지 출력합니다.

# 작동 방식:

# 비밀번호 생성: generate_possible_passwords는 가능한 모든 6자리 비밀번호 조합을 생성합니다.

# 각각의 비밀번호를 ZIP 파일에 사용: 각 비밀번호로 password.txt를 추출하고, 성공하면 그 암호를 해독합니다.

# 비밀번호가 맞으면: 카이사르 암호를 해독하고, 해독된 결과를 출력합니다.

# 성능 최적화:

# 이 방법은 무차별 대입이므로 시간이 많이 걸릴 수 있습니다. 하지만 6자리 조합은 최대 36^6 (약 2.18억 개의 조합)입니다. 이를 몇 분 내에 처리할 수는 있지만, 속도 최적화를 위해 병렬 처리나 멀티스레딩을 사용할 수도 있습니다.

# 주의:

# 이 코드에서는 password.txt 파일이 암호화된 ZIP 파일에 들어 있다는 전제하에 작성되었습니다.

# 시간이 오래 걸릴 수 있습니다. 암호가 정확히 무엇인지를 모르고 모든 가능한 비밀번호를 시도해야 하기 때문에 많은 시간이 소요될 수 있습니다.

# 실행하는 환경이 충분한 자원을 제공하는지 확인해야 합니다.

# 변경 사항:

# save_to_passwd_txt: 해독된 password.txt 내용을 **passwd.txt**로 저장하는 함수입니다.

# decoded_text를 받아 passwd.txt 파일에 기록합니다.

# read_password_from_zip: password.txt를 해독한 후, 해독된 내용을 passwd.txt로 저장하도록 수정되었습니다.

# 실행 흐름:

# ZIP 파일을 열고, 가능한 모든 비밀번호를 시도하여 **password.txt**를 추출합니다.

# 비밀번호가 맞으면, password.txt 내용을 카이사르 암호로 해독하고 그 결과를 출력합니다.

# 암호가 해독되면, 해독된 내용을 **passwd.txt**로 저장합니다.

# 이제 passwd.txt 파일이 생성되며, 이 파일에 해독된 내용이 저장됩니다.

# 예시 출력:


import zipfile
import string
import itertools
import sys

def generate_possible_passwords():
    """가능한 모든 비밀번호(6자리 숫자+소문자)를 생성"""
    characters = string.ascii_lowercase + string.digits  # 소문자 알파벳 + 숫자
    return itertools.product(characters, repeat=6)  # 6자리 조합 생성

def extract_file_from_zip(zip_file, filename, password=None):
    """ZIP 파일에서 특정 파일을 추출하여 내용을 반환하는 함수 (암호화된 파일 처리)"""
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            # 암호화된 파일을 처리하기 위해 비밀번호 제공
            if password:
                zip_ref.setpassword(password.encode())  # 비밀번호 설정
            # ZIP 파일 내에 파일 목록 확인
            if filename in zip_ref.namelist():
                with zip_ref.open(filename) as file:
                    content = file.read().decode('utf-8')  # 파일 내용을 UTF-8로 디코딩
                    return content
            else:
                print(f'{filename} 파일이 ZIP에 없습니다.')
                return None
    except zipfile.BadZipFile:
        #print("ZIP 파일이 잘못되었습니다.")
        return None
    except RuntimeError as e:
        #print(f"암호화된 ZIP 파일을 열 때 오류 발생: {e}")
        return None
    except Exception as e:
        print(f'ZIP 파일 처리 중 오류 발생: {e}')
        return None

def save_to_passwd_txt(decoded_text):
    """해독된 내용을 passwd.txt 파일에 저장"""
    try:
        with open('passwd.txt', 'w') as passwd_file:
            passwd_file.write(decoded_text)
            print(f'암호가 해독되어 passwd.txt로 저장되었습니다: {decoded_text}')
    except Exception as e:
        print(f'파일 저장 중 오류 발생: {e}')

def read_password_from_zip(zip_file):
    """ZIP 파일에서 암호문이 담긴 password.txt 파일을 읽어오는 함수"""
    for password_tuple in generate_possible_passwords():
        password = ''.join(password_tuple)  # tuple을 문자열로 변환
        print(f"{password}",end=' ')  # 시도 중인 비밀번호 출력
        
        # 비밀번호로 파일을 추출 시도
        password_text = extract_file_from_zip(zip_file, 'password.txt', password)
        
        if password_text:
            print(f"암호가 해독되었습니다: {password}")
            caesar_cipher_decode(password_text)  # 카이사르 암호 해독
            save_to_passwd_txt(password_text)  # 해독된 내용을 passwd.txt로 저장
            break  # 성공하면 반복 종료

def caesar_cipher_decode(target_text):
    """카이사르 암호 해독 함수"""
    alphabet = string.ascii_lowercase
    decoded_text = []

    for shift in range(1, 27):  # 1부터 26까지 시프트
        shifted_text = []
        for char in target_text:
            if char.isalpha():
                if char.islower():
                    new_char = alphabet[(alphabet.index(char) - shift) % 26]
                elif char.isupper():
                    new_char = alphabet[(alphabet.index(char.lower()) - shift) % 26].upper()
                shifted_text.append(new_char)
            else:
                shifted_text.append(char)
        decoded_text.append(f'자리수 {shift}: {"".join(shifted_text)}')
    
    # 해독된 결과 출력
    for decoded in decoded_text:
        print(decoded)

if __name__ == "__main__":
    zip_filename = 'emergency_storage_key.zip'  # ZIP 파일 이름
    read_password_from_zip(zip_filename)  # ZIP 파일에서 암호문 읽기 및 해독
