맞습니다 👍

Python에서 `dict` ↔ `JSON` 변환은 `json` 모듈을 씁니다.

---

### 1. dict → JSON 파일 쓰기 (`dump`)

```python
import json

data = {"name": "Alice", "age": 25, "is_student": False}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
```

👉 `json.dump(obj, file)`

* `obj`: 저장할 dict (또는 리스트 등 JSON 호환 객체)
* `file`: 열어둔 파일 객체
* `ensure_ascii=False`: 한글이 \uXXXX 로 안 깨지도록
* `indent=4`: 예쁘게 들여쓰기

---

### 2. JSON 파일 → dict 읽기 (`load`)

```python
with open("data.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)

print(loaded)         # {'name': 'Alice', 'age': 25, 'is_student': False}
print(type(loaded))   # <class 'dict'>
```

👉 `json.load(file)` 는 JSON 파일을 Python 객체(dict, list 등)로 변환합니다.

---

### 3. 문자열로 변환 (`dumps` / `loads`)

* 파일이 아니라 **문자열**로 다루고 싶을 때는 `dump` → `dumps`, `load` → `loads` 를 씁니다.

```python
s = json.dumps(data, ensure_ascii=False)
print(s)  # {"name": "Alice", "age": 25, "is_student": false}

d = json.loads(s)
print(d)  # {'name': 'Alice', 'age': 25, 'is_student': False}
```

---

✅ 정리

* **파일에 쓰기** → `json.dump(dict, file)`
* **파일에서 읽기** → `json.load(file)`
* **문자열 변환** → `json.dumps(dict)`, `json.loads(str)`

---

혹시 원하세요? 제가 dict을 json으로 저장하고 다시 불러오는 **짧은 예제 (한 파일로 완결)** 코드를 만들어드릴까요?
