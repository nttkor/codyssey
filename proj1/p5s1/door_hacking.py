#!/usr/bin/env python3
"""
특징 및 장점
자동 및 수동 해독 병행: 자동으로 사전 단어 포함 여부로 탐지하되, 최종 선택은 사람이 직접 가능
사전 단어 강조: 결과 화면에서 사전 단어가 있는 부분을 시각적으로 쉽게 구분 가능
깔끔한 에러 처리: 비밀번호 오류 시 복잡한 예외 대신 친절한 메시지 제공
ANSI 코드 사용: 터미널에서 가독성 좋은 출력 지원
사용자 편의성: shift 번호 재입력 가능 및 종료 명령 제공
"""

import os
import zipfile
import re


def caesar_cipher_decode(target_text, shift):
    """
    카이사르 암호 해독 함수
    - 주어진 텍스트에 대해 지정한 shift만큼 알파벳을 뒤로 이동시켜 복호화
    - 대소문자 구분하며 알파벳 이외 문자는 변경하지 않음
    """
    decoded = ""
    for ch in target_text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            decoded += chr((ord(ch) - base - shift) % 26 + base)
        else:
            decoded += ch
    return decoded


def highlight_words(text, dictionary_words):
    """
    사전 단어와 정확히 일치하는 단어만 반전(ANSI escape) 처리하는 함수
    - 대소문자 구분 없이 단어 단위로 비교
    - 일치하는 단어는 터미널에서 반전되어 강조됨
    """
    dict_set = set(word.lower() for word in dictionary_words)

    def replacer(match):
        word = match.group(0)
        if word.lower() in dict_set:
            return f"\033[7m{word}\033[0m"
        else:
            return word

    # 단어 경계(\b)로 분리하여 정확히 단어만 매칭
    pattern = re.compile(r'\b\w+\b', re.UNICODE)
    return pattern.sub(replacer, text)


def try_auto_decode(target_text, dictionary_words):
    """
    사전 단어를 이용해 자동 해독 시도
    - shift 값을 0부터 25까지 적용해 복호화 결과를 생성
    - 복호화 결과에 4자 이상인 사전 단어가 포함되면 자동 탐지 성공으로 간주
    - 성공 시 shift와 복호화된 텍스트를 반환
    - 실패 시 (None, None) 반환
    """
    for shift in range(26):
        decoded = caesar_cipher_decode(target_text, shift)
        for word in dictionary_words:
            if len(word) <= 3:
                continue
            if word.lower() in decoded.lower():
                print(f"[자동 탐지] shift={shift}, '{word}' 발견!")
                print("해독 결과:", decoded)
                return shift, decoded
    return None, None


def remove_ansi(text):
    """
    ANSI escape 코드 제거 함수
    - 파일 저장 시 터미널용 색상 코드가 포함되지 않도록 클린업
    """
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    return ansi_escape.sub('', text)


def main():
    # 1. 현재 스크립트 위치로 작업 디렉토리 변경
    os.chdir(os.path.dirname(__file__))

    # 2. password.txt에서 ZIP 비밀번호 읽기
    try:
        with open("password.txt", "r", encoding="utf-8") as f:
            zip_password = f.read().strip()
    except FileNotFoundError:
        print("password.txt 파일이 없습니다.")
        return

    # 3. emergency_storage_key.zip 열기 및 압축 해제 시도
    try:
        with zipfile.ZipFile("emergency_storage_key.zip") as zf:
            inner_files = zf.namelist()
            if not inner_files:
                print("ZIP 안에 파일이 없습니다.")
                return
            target_file = inner_files[0]
            print(f"[ZIP 해제] 내부 파일: {target_file}")

            # ZIP 비밀번호로 압축 파일 열기
            with zf.open(target_file, pwd=zip_password.encode()) as f:
                encrypted_text = f.read().decode("utf-8").strip()
    except RuntimeError as e:
        if 'Bad password' in str(e):
            print(f"❌ ZIP 비밀번호 '{zip_password}' 가 틀렸습니다.")
            return
        else:
            raise
    except FileNotFoundError:
        print("emergency_storage_key.zip 파일이 없습니다.")
        return

    # 4. result.txt가 있으면 사전 단어로 사용
    dictionary_words = []
    if os.path.exists("result.txt"):
        with open("result.txt", "r", encoding="utf-8") as f:
            dictionary_words = f.read().split()
        print(f"[사전 로드] {len(dictionary_words)}개 단어 사용")

    # 5. 사전 단어로 자동 해독 시도 (성공해도 계속 모든 shift 출력)
    if dictionary_words:
        shift_found, decoded_found = try_auto_decode(encrypted_text, dictionary_words)
        if decoded_found:
            print("✅ 자동 해독 성공! result.txt 갱신 가능 (사용자 선택 대기)")
        else:
            shift_found, decoded_found = None, None
    else:
        shift_found, decoded_found = None, None

    # 6. 모든 shift 결과 출력 (사전 단어 포함 시 강조 표시)
    print("=== 모든 shift 결과 ===")
    results = []
    for shift in range(26):
        decoded = caesar_cipher_decode(encrypted_text, shift)
        if dictionary_words:
            decoded = highlight_words(decoded, dictionary_words)
        results.append((shift, decoded))
        print(f"[shift={shift}] {decoded}")

    # 7. 사용자로부터 shift 번호 선택받아 결과 저장 (반복 가능)
    while True:
        choice = input("올바른 shift 번호를 입력하세요 (종료: q): ").strip()
        if choice.lower() == 'q':
            print("종료합니다.")
            break
        if not choice.isdigit():
            print("숫자를 입력해야 합니다.")
            continue
        choice = int(choice)
        if 0 <= choice < 26:
            decoded_text = results[choice][1]
            # ANSI 코드 제거 후 파일 저장
            with open("result.txt", "w", encoding="utf-8") as f:
                f.write(remove_ansi(decoded_text))
            print(f"shift={choice} 결과가 result.txt 파일에 저장 완료!")
            break
        else:
            print("0부터 25 사이의 숫자를 입력하세요.")


if __name__ == "__main__":
    main()
