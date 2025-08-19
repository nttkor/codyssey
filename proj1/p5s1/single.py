# 코드 설명:
# extract_file_from_zip 함수:
# ZIP 파일에서 특정 파일을 추출하여 그 내용을 반환합니다. zipfile.ZipFile을 사용하여 ZIP 파일을 열고, open() 메서드로 파일을 읽습니다. 파일이 존재하지 않으면 None을 반환합니다.
# read_password_from_zip 함수:
# ZIP 파일에서 password.txt 파일을 읽고, 그 내용을 caesar_cipher_decode() 함수에 전달하여 암호를 해독합니다.
# caesar_cipher_decode 함수:
# 앞서 설명한 카이사르 암호를 해독하는 함수입니다.
# 사용 방법:
# 암호화된 텍스트가 포함된 password.txt 파일을 encrypted.zip이라는 이름의 ZIP 파일로 압축한 후, 이 ZIP 파일을 처리합니다.
# caesar_cipher_decode 함수가 암호를 해독하고, result.txt에 결과를 저장합니다.

# 예시:

# ZIP 파일 구조:
# encrypted.zip
# password.txt (여기에 암호화된 텍스트가 포함)
# 이 코드는 password.txt 파일이 ZIP 파일에 포함되어 있다고 가정하고 그 파일을 추출하여 카이사르 암호를 해독하는 방식입니다. ZIP 파일을 다룰 때는 zipfile 모듈을 사용하여 파일을 열고, 필요한 파일을 읽어들일 수 있습니t.

import zipfile
import string

def caesar_cipher_decode(target_text):
    # 알파벳을 기준으로 한 카이사르 암호 해독
    alphabet = string.ascii_lowercase  # 소문자 알파벳
    decoded_results = []  # 결과를 저장할 리스트
    
    # 카이사르 암호를 풀기 위한 최대 시프트는 26이므로 26번 시프트
    for shift in range(1, 27):  # 자리수는 1부터 26까지
        decoded_text = []
        
        for char in target_text:
            if char.isalpha():  # 알파벳인 경우만 처리
                # 소문자인지 대문자인지 확인
                if char.islower():
                    new_char = alphabet[(alphabet.index(char) - shift) % 26]
                elif char.isupper():
                    new_char = alphabet[(alphabet.index(char.lower()) - shift) % 26].upper()
                decoded_text.append(new_char)
            else:
                decoded_text.append(char)  # 알파벳이 아닌 문자는 그대로 추가
        
        decoded_text = ''.join(decoded_text)  # 리스트를 문자열로 변환
        decoded_results.append((shift, decoded_text))  # 결과에 자리수와 함께 추가
    
    # 해독된 결과 출력
    for shift, decoded_text in decoded_results:
        print(f'자리수 {shift}: {decoded_text}')
        
        # 사전에서 단어가 일치하는지 확인
        if is_valid_word(decoded_text):
            print(f"암호가 해독되었습니다: {decoded_text}")
            save_result(decoded_text)  # result.txt에 저장
            break  # 해독되었으면 반복을 멈춘다.

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
