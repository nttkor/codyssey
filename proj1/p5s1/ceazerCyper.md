# 코드 개요 — 카이사르 암호 해독기 with ZIP 자동 해제 및 단어 사전 강조

## 목적

`emergency_storage_key.zip` 압축파일 안에 있는 암호화된 텍스트를 시저 암호(Caesar cipher) 방식으로 자동 또는 수동으로 해독하여 결과를 확인 및 저장하는 도구입니다.

---

## 주요 기능 및 흐름

1. **ZIP 비밀번호 읽기**

   * `password.txt` 파일에서 ZIP 파일 비밀번호를 읽음.

2. **ZIP 파일 해제 및 암호화된 텍스트 읽기**

   * `emergency_storage_key.zip` 내 첫 번째 파일을 비밀번호로 열어 암호화된 텍스트를 읽음.
   * 비밀번호가 틀리면 사용자에게 알기 쉽게 오류 메시지 출력.

3. **사전 단어 로드 (`result.txt`가 있으면)**

   * `result.txt`가 있으면 그 안의 단어들을 “사전 단어”로 불러와 이후 자동 해독 시 참고함.

4. **자동 해독 시도**

   * 시저 암호의 모든 가능한 shift (0\~25)를 적용하여 해독.
   * 사전 단어가 해독문 내에 포함되면 자동 탐지 성공 메시지 출력.

5. **모든 shift 결과 출력**

   * 사전 단어가 있으면, 해독 결과 내에서 사전 단어와 정확히 일치하는 단어들만 ANSI 반전 표시(강조)하여 보여줌.
   * 사전 단어가 없거나 자동 탐지 실패해도 모든 shift 결과는 항상 출력.

6. **사용자 수동 선택**

   * 사용자에게 shift 번호를 입력받아 선택한 해독 결과를 `result.txt`로 저장.
   * 저장 시 ANSI escape 코드 제거하여 파일에 깨끗한 텍스트 저장.
   * `q` 입력 시 종료 가능.

---

## 특징 및 장점

* **자동 및 수동 해독 병행**: 자동으로 사전 단어 포함 여부로 탐지하되, 최종 선택은 사람이 직접 가능
* **사전 단어 강조**: 결과 화면에서 사전 단어가 있는 부분을 시각적으로 쉽게 구분 가능
* **깔끔한 에러 처리**: 비밀번호 오류 시 복잡한 예외 대신 친절한 메시지 제공
* **ANSI 코드 사용**: 터미널에서 가독성 좋은 출력 지원
* **사용자 편의성**: shift 번호 재입력 가능 및 종료 명령 제공

---

## 실행 흐름 상세 설명

### 1. 작업 디렉토리 변경

```python
os.chdir(os.path.dirname(__file__))
```

* 스크립트가 위치한 폴더로 작업 디렉토리를 변경합니다.
* 이렇게 해야 `password.txt`, `emergency_storage_key.zip`, `result.txt` 같은 파일을 상대경로로 문제없이 읽고 쓸 수 있습니다.

---

### 2. ZIP 비밀번호 읽기 (`password.txt`)

```python
with open("password.txt", "r", encoding="utf-8") as f:
    zip_password = f.read().strip()
```

* 같은 디렉토리 내에 있는 `password.txt`에서 ZIP 압축 파일의 비밀번호를 읽어옵니다.
* 파일이 없으면 에러 메시지를 출력하고 프로그램을 종료합니다.

---

### 3. ZIP 파일 열기 및 압축 해제 (`emergency_storage_key.zip`)

```python
with zipfile.ZipFile("emergency_storage_key.zip") as zf:
    inner_files = zf.namelist()
    ...
    with zf.open(target_file, pwd=zip_password.encode()) as f:
        encrypted_text = f.read().decode("utf-8").strip()
```

* `emergency_storage_key.zip` 압축 파일을 엽니다.
* 내부에 포함된 파일 리스트를 불러오고, 첫 번째 파일을 해제 대상으로 지정합니다.
* ZIP 비밀번호를 사용해 내부 파일을 읽어옵니다.
* 비밀번호가 틀리거나 ZIP 파일이 없으면 적절한 오류 메시지를 출력하고 종료합니다.

---

### 4. 사전 단어 로드 (`result.txt`)

```python
if os.path.exists("result.txt"):
    with open("result.txt", "r", encoding="utf-8") as f:
        dictionary_words = f.read().split()
```

* 이전에 복호화한 결과를 저장한 `result.txt`가 있으면 그 파일을 읽어 단어들을 사전 단어 집합으로 사용합니다.
* 이 단어들은 이후 암호문 해독에 도움을 주는 기준으로 활용됩니다.

---

### 5. 자동 해독 시도

```python
if dictionary_words:
    shift_found, decoded_found = try_auto_decode(encrypted_text, dictionary_words)
    ...
```

* 0부터 25까지 모든 시프트(shift)를 시도하며 암호문을 복호화합니다.
* 복호화 결과에 사전 단어 중 4자 이상인 단어가 포함돼 있으면 자동 탐지 성공으로 간주하고 결과를 출력합니다.
* 자동 탐지가 성공해도 이후 모든 shift 결과는 계속 출력됩니다.

---

### 6. 모든 shift 결과 출력 및 사전 단어 강조

```python
for shift in range(26):
    decoded = caesar_cipher_decode(encrypted_text, shift)
    if dictionary_words:
        decoded = highlight_words(decoded, dictionary_words)
    print(f"[shift={shift}] {decoded}")
```

* 0부터 25까지 모든 시프트 값을 적용해 복호화 결과를 화면에 출력합니다.
* 사전 단어가 있으면 해당 단어를 ANSI 반전 색상 코드로 강조하여 가독성을 높입니다.
* 사용자에게 모든 가능한 결과를 보여주어 직접 확인할 수 있도록 합니다.

---

### 7. 사용자 입력으로 올바른 shift 선택 및 저장

```python
choice = input("올바른 shift 번호를 입력하세요 (종료: q): ").strip()
...
with open("result.txt", "w", encoding="utf-8") as f:
    f.write(remove_ansi(decoded_text))
```

* 사용자로부터 올바른 shift 번호(0\~25)를 입력받습니다.
* 입력이 `q`이면 프로그램을 종료합니다.
* 입력된 번호가 유효하면, 그 shift 결과를 ANSI 코드 없이 클린한 텍스트로 `result.txt`에 저장합니다.
* 저장 후 성공 메시지를 출력하고 종료합니다.

---

# 요약

1. **작업 디렉토리 이동** — 스크립트 위치 기준으로 이동
2. **비밀번호 읽기** — `password.txt`에서 ZIP 비밀번호 획득
3. **ZIP 파일 해제** — 비밀번호로 `emergency_storage_key.zip` 내부 파일 읽기
4. **사전 단어 로드** — 이전 복호화 결과 `result.txt`에서 단어 불러오기 (있으면)
5. **자동 해독 시도** — 사전 단어 포함 여부로 shift 자동 탐지 시도
6. **모든 시프트 결과 출력** — 사전 단어 포함 시 단어 강조 표시
7. **사용자 선택 및 결과 저장** — 올바른 shift 번호 선택 후 `result.txt` 갱신

---

필요하면 각 단계별 처리 코드도 같이 설명하거나 시각적으로 흐름도를 만들어 드릴 수 있어요!
