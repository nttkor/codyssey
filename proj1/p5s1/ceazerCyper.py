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

    # 2. password.txt 암호환된 문장 읽기
    try:
        with open("password.txt", "r", encoding="utf-8") as f:
            encrypted_text = f.read().strip()
    except FileNotFoundError:
        print("found_password.txt 파일이 없습니다.")
        return


    # 4. result.txt가 있으면 사전 단어로 사용
    dictionary_words = []
    results = []
    if os.path.exists("result.txt"):
        with open("result.txt", "r", encoding="utf-8") as f:
            dictionary_words = f.read().split()
        print(f"[사전 로드] {len(dictionary_words)}개 단어 사용")


    # 6. 모든 shift 결과 출력 (사전 단어 포함 시 강조 표시)
    print("=== 모든 shift 결과 ===")
    #사전 단어 설정
    dict_set = set(word.lower() for word in dictionary_words)
    for shift in range(26):
        decoded = caesar_cipher_decode(encrypted_text, shift)
        results.append(decoded) #카이사르 디코딩된 문장 추가
        highlight_words = []
        for word in decoded.split():
            if dictionary_words:
                if word.lower() in dict_set:
                    highlight_words.append(f"\033[7m{word}\033[0m") #사전에 있는 단어 하이라이트 시키기
                else:
                    highlight_words.append(word)
        
        print(f"[shift={shift}]", *highlight_words)

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
            decoded_text = results[choice]
            # ANSI 코드 제거 후 파일 저장
            with open("result.txt", "w", encoding="utf-8") as f:
                f.write(decoded_text)
            print(f"shift={choice} 결과가 result.txt 파일에 저장 완료!")
            break
        else:
            print("0부터 25 사이의 숫자를 입력하세요.")


if __name__ == "__main__":
    main()
