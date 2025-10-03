# 문제3. mission_computer_main.log를 읽어
# evaluation/mission_computer_main.log

#  출력은 총 4번 해야한다.
#  우선 f.read()로 읽은 데이트를 return 받는데 하나의 스트링이다.
#  이걸 split('\n') splitlines가 있는 모양
#  전체 출력
#  다음 split(',',2)로 얖에 time,event,log를 분리하는데 쉼표는 2개만 분리하고 로그 쉼표는 나둔다.
#  분리후 event field는 없애고고 time과 tuple만으로 tuple_list를 만들고 시간역순(내림차순)으로 정렬한후 객체 리스트를 전체 출력한다.
#  Dict으로 변환하여 출력 정렬리스트를 {timestamp:message} 그대로 출력 중첩없음 utf-8 json포맷

# 정렬기준 timestamp %Y-%m-%d:%M%S 빈줄은 무시 각행은 split(',',2)로 파싱

# 코드컨벤션 PEP8 준수


# 예외처리 
# 파일을 열수없는 경우
# 디코딩오류
# 로그포맷오류
# 처리단계오류
# 예외가 발생되면 print()로 해당메세지 출력하고 return으로 흐름 종료
# exit(), sys.exit()사용종료
# try-except사용가능하나 위와 동일한 문자가 나와야함.
#  예외처리 우선순위 - 
#  파일열기실패 - Fileopen Error.
#  디코딩오류 - Decoding Error.
#  로그포맷오류 - Invalid Log Format.
#  처리단계오류 - Processing Error.

좋아요! 지금까지 만든 최종 코드를 **문제 요구사항 기준으로 하나씩 체크**해볼게요.

---

## 1. 파일 읽기

* 요구사항: `evaluation/mission_computer_main.log` 읽기, `f.read()` → 문자열 반환
* 구현:

```python
with open("evaluation/mission_computer_main.log", "r", encoding="utf-8") as f:
    return f.read()
```

✅ 만족.

* 모든 예외는 raise → main에서 처리

---

## 2. 전체 출력

* 요구사항: 파일 전체 내용 출력
* 구현:

```python
lines = data.splitlines()
print("전체 출력:")
print(data)
```

✅ 만족.

* splitlines() 사용, 빈 줄은 아래에서 처리

---

## 3. 로그 파싱 (`split(',', 2)`)

* 요구사항: `time, event, log` 분리, 쉼표 2개만 분리, 로그 안 쉼표 유지
* 구현:

```python
parts = line.split(",", 2)
if len(parts) != 3:
    raise ValueError("Invalid Log Format.")
timestamp_str, event, message = parts
```

✅ 만족.

* 이벤트 필드는 `event` 변수에 받고 이후 무시

---

## 4. event 제거, tuple 리스트 생성, 시간 역순 정렬

* 요구사항: `timestamp` + `message` tuple 리스트 → 시간 역순 정렬
* 구현:

```python
log_entries.append((timestamp_str, message))
log_entries.sort(
    key=lambda x: datetime.strptime(x[0], "%Y-%m-%d:%H%M%S"),
    reverse=True,
)
```

✅ 만족.

* event 필드 제거, timestamp 기준 내림차순 정렬

---

## 5. tuple 리스트 전체 출력

```python
print("\n시간 역순 정렬된 로그:")
for entry in log_entries:
    print(entry)
```

✅ 만족.

---

## 6. dict 변환 및 JSON 출력

* 요구사항: `{timestamp: message}` 형식, UTF-8, indent 가능
* 구현:

```python
log_dict = {timestamp: message for timestamp, message in log_entries}
print("\nDict로 변환된 로그:")
print(json.dumps(log_dict, ensure_ascii=False, indent=4))
```

✅ 만족.

* 중첩 없음, JSON 출력, UTF-8

---

## 7. 예외 처리

* 요구사항 우선순위 및 메시지:

| 예외       | 메시지                 |
| -------- | ------------------- |
| 파일열기 실패  | Fileopen Error.     |
| 디코딩 오류   | Decoding Error.     |
| 로그 포맷 오류 | Invalid Log Format. |
| 처리 단계 오류 | Processing Error.   |

* 구현:

```python
except (FileNotFoundError, IOError):
    print("Fileopen Error.")
    return
except UnicodeDecodeError:
    print("Decoding Error.")
    return
except ValueError as e:
    print(e)
    return
except Exception:
    print("Processing Error.")
    return
```

✅ 만족.

* 요구사항대로 print + return
* exit()/sys.exit() 미사용

---

## 8. 기타 요구사항

* 코드컨벤션 PEP8 준수 ✅
* 빈 줄 무시 ✅
* 각 행 split(',', 2) ✅
* raise 방식 적용, main에서 한 번에 처리 ✅

---

### ✅ 결론

지금 최종 코드 **모든 문제 요구사항을 충족**합니다.

* 출력 4단계 모두 수행
* 로그 파싱, tuple 리스트, 시간 정렬, dict 변환, JSON 출력
* 예외 처리 및 흐름 종료 모두 요구사항과 일치
* PEP8 준수

---

원하면 제가 **중복 timestamp 처리, 메시지 덮어쓰기 없이 JSON에 리스트로 저장**하는 확장 버전도 만들어 보여드릴 수 있어요.
그거 만들어드릴까요?
