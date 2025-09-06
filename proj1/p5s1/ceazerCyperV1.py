#!/usr/bin/env python3
import os
import zipfile
import re


def caesar_cipher_decode(target_text, shift):
    """카이사르 암호 해독"""
    decoded = ""
    for ch in target_text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            decoded += chr((ord(ch) - base - shift) % 26 + base)
        else:
            decoded += ch
    return decoded


def highlight_words(text, dictionary_words):
    """사전 단어를 반전(강조)시켜서 반환"""
    def replacer(match):
        word = match.group(0)
        return f"\033[7m{word}\033[0m"  # ANSI escape code로 반전 처리

    if not dictionary_words:
        return text

    # 단어별로 정규 표현식으로 감싸서 매칭
    for word in sorted(dictionary_words, key=len, reverse=True):
        pattern = re.compile(rf"\b({re.escape(word)})\b", flags=re.IGNORECASE)
        text = pattern.sub(replacer, text)
    return text


def try_auto_decode(target_text, dictionary_words):
    """사전 단어를 이용해 자동 해독 시도"""
    for shift in range(26):
        decoded = caesar_cipher_decode(target_text, shift)
        for word in dictionary_words:
            if word.lower() in decoded.lower() and len(word) > 3:
                print(f"[자동 탐지] shift={shift}, '{word}' 발견!")
                print("해독 결과:", decoded)
                return shift, decoded
    return None, None


def main():
    # 1. password.txt 에서 ZIP 비밀번호 읽기
    with open("password.txt", "r", encoding="utf-8") as f:
        zip_password = f.read().strip()

    # 2. emergency_storage_key.zip 열기
    with zipfile.ZipFile("emergency_storage_key.zip") as zf:
        inner_files = zf.namelist()
        if not inner_files:
            print("ZIP 안에 파일이 없습니다.")
            return
        target_file = inner_files[0]
        print(f"[ZIP 해제] 내부 파일: {target_file}")

        with zf.open(target_file, pwd=zip_password.encode()) as f:
            encrypted_text = f.read().decode("utf-8").strip()

    # 3. result.txt 가 있으면 → 그 안 단어들을 사전으로 사용
    dictionary_words = []
    if os.path.exists("result.txt"):
        with open("result.txt", "r", encoding="utf-8") as f:
            dictionary_words = f.read().split()
        print(f"[사전 로드] {len(dictionary_words)}개 단어 사용")

    # 4. 자동 해독 시도 (단, 자동 성공 여부와 관계없이 전부 출력함)
    auto_shift, auto_decoded = None, None
    if dictionary_words:
        auto_shift, auto_decoded = try_auto_decode(encrypted_text, dictionary_words)
        if auto_decoded:
            with open("result.txt", "w", encoding="utf-8") as f:
                f.write(auto_decoded)
            print("✅ 자동 해독 성공! result.txt 갱신 완료")

    # 5. 모든 shift 결과 출력 (사전 단어 강조 포함)
    print("\n=== 모든 shift 결과 ===")
    results = []
    for shift in range(26):
        decoded = caesar_cipher_decode(encrypted_text, shift)
        highlighted = highlight_words(decoded, dictionary_words)
        results.append((shift, decoded))
        print(f"[shift={shift}] {highlighted}")

    # 6. 사람이 shift 선택
    choice = input("\n올바른 shift 번호를 입력하세요: ")
    if choice.isdigit():
        choice = int(choice)
        if 0 <= choice < 26:
            decoded_text = results[choice][1]
            with open("result.txt", "w", encoding="utf-8") as f:
                f.write(decoded_text)
            print("✅ result.txt 파일에 저장 완료!")
        else:
            print("❌ 잘못된 번호입니다.")
    else:
        print("❌ 숫자를 입력해야 합니다.")


if __name__ == "__main__":
    main()
