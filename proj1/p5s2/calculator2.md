좋아요 😄
지금 코드를 **실행 순서대로, 특히 계산 부분을 중심으로** 자세히 설명해드릴게요.
UI 연결, 버튼 입력, 연산 흐름, 결과 처리까지 순서대로 정리합니다.

---

## 1️⃣ 프로그램 시작

```python
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
```

* `QApplication(sys.argv)` → PyQt6 GUI 앱 생성, 이벤트 루프 준비
* `MainWindow()` → GUI 클래스 객체 생성, UI 초기화(`setupUi`)
* `window.show()` → 창 화면 표시
* `app.exec()` → 이벤트 루프 시작, 버튼 클릭 등 모든 이벤트 처리

이 시점에서 **GUI 창이 뜨고 버튼이 모두 연결된 상태**입니다.

---

## 2️⃣ MainWindow 초기화 (`__init__`)

```python
self.calc = Calculator()  # 계산기 객체 생성
self.equals_pressed = False  # = 마지막 눌림 여부
self.update_display("0")  # 초기 화면 0 표시
```

* `Calculator()` → 계산 상태 초기화

  * `num=""`, `op1=None`, `op2=None`, `operator=None`, `result=0.0`
* 화면 초기값 `0` 설정, 폰트 자동 조절

### 버튼 연결

* 숫자 버튼 (0~9) → `input_number()`
* 소수점 버튼 → `input_number('.')`
* 연산자 버튼 (+, -, X, /) → `input_operator()`
* 특수 버튼 (% → `handle_percent()`, +/- → `handle_negative_positive()`)
* = 버튼 → `handle_equal()`
* AC / MODE 버튼 → `handle_reset()`

> 여기서 **GUI와 계산 로직(Calculator)**이 연결되었습니다.

---

## 3️⃣ 숫자 입력 (`input_number()`)

```python
if self.equals_pressed: self.handle_reset()
if digit == "." and "." in self.calc.num: return
self.calc.num = digit if self.calc.num=="0" and digit!="." else self.calc.num + digit
self.update_display(self.calc.num)
```

* = 버튼 이후 새 입력이면 초기화
* 이미 소수점이 있으면 중복 방지
* 입력 숫자를 문자열로 누적 (`self.calc.num`)
* 화면에 갱신 (`update_display()` → 폰트 자동 조절 포함)

> 즉, **사용자가 1, 2, 3 누르면 `num='123'`**이 됩니다.

---

## 4️⃣ 연산자 입력 (`input_operator()`)

```python
if self.calc.num:
    self.calc.op1 = float(self.calc.num) if self.calc.op1 is None else self.calc.equal()
    self.calc.operator = op
    self.calc.num = ""
elif self.calc.op1 is not None:
    self.calc.operator = op
elif op == "-":
    self.calc.num = "-"
self.update_display(self.display_with_operator())
```

* 숫자를 입력한 상태에서 연산자 클릭:

  1. `op1`이 없으면 → `num`을 `float`로 변환 → `op1`에 저장
  2. `op1`이 이미 있으면 → **연속 연산 수행** (`equal()` 호출)

     * 이전 계산 결과를 `op1`에 갱신
* `operator`에 연산자 저장
* `num` 초기화 → 다음 숫자 입력 준비
* 화면 갱신 → `op1 operator` 표시

> 여기서 **연산부 계산 흐름**이 시작됩니다.

---

## 5️⃣ = 버튼 입력 (`handle_equal()`)

```python
try:
    result = self.calc.equal()
except CalcError as e:
    self.show_error(str(e))
    return
self.update_display(self.format_number(result))
self.equals_pressed = True
```

* `equal()` 호출 → **실제 계산 수행**
* 오류 발생 시 → 화면에 `Error` 표시
* 정상 계산 시 → 결과 화면 표시
* `equals_pressed = True` → 다음 입력 시 초기화 신호

---

## 6️⃣ Calculator 계산 로직 (`equal()` → `calculate()`)

### 6-1. 입력 확인

```python
if self.op1 is None or not self.num: raise CalcError("입력이 불완전합니다.")
self.op2 = float(self.num)
```

* `op1`이 없거나 숫자를 입력하지 않으면 오류
* 입력 숫자를 `float`로 변환 → `op2`에 저장

---

### 6-2. 실제 연산 (`calculate()`)

```python
if self.operator == "+": self.op1 += self.op2
elif self.operator == "-": self.op1 -= self.op2
elif self.operator == "X": self.op1 *= self.op2
elif self.operator == "/":
    if self.op2 == 0: raise CalcError("0으로 나눌 수 없습니다.")
    self.op1 /= self.op2
elif self.operator == "%":
    self.op2 = self.op1 * (self.op2 / 100)
    self.op1 += self.op2
```

* 연산자별로 op1과 op2를 계산
* `/` → 0 나누기 방지
* `%` → `op1 * (op2 / 100)` 후 더하기
* 결과는 **op1에 저장** → 연속 계산 가능

---

### 6-3. 결과 저장 및 반환

```python
self.result = round(self.op1, 10)
self.op1 = self.result
self.num = ""
self.operator = None
return self.result
```

* 소수점 10자리 반올림
* `op1`에 결과 저장 → 다음 연산 가능
* 입력 초기화, 연산자 초기화
* 결과 반환 → GUI에서 화면 갱신

---

## 7️⃣ +/- 버튼 (`handle_negative_positive()`)

```python
if self.calc.num:
    self.calc.negative_positive()
elif self.calc.op1 is not None and self.calc.operator is None:
    self.calc.op1 = -self.calc.op1
else:
    self.calc.num = "-0"
self.update_display(self.display_with_operator())
```

* 입력 중 숫자 → 부호 반전
* 계산된 결과 → 부호 반전
* 초기 상태 → `-0` 표시

---

## 8️⃣ % 버튼 (`handle_percent()`)

```python
self.calc.percent()
self.update_display(self.display_with_operator())
```

* 입력 중 숫자 → 100으로 나누기
* 계산 결과 → 100으로 나누기
* 화면 갱신

---

## 🔹 정리: 계산 흐름

1. **숫자 입력** → `num`에 누적
2. **연산자 입력** → `op1` 저장, 연속 연산 시 `equal()` 호출
3. **두 번째 숫자 입력** → `num`에 누적
4. **= 버튼 입력** → `equal()` 호출

   * `op2 = float(num)` → 연산 수행 → `op1`에 결과 저장
5. **화면 갱신** → `update_display()`
6. **연속 연산** → `op1`은 결과 유지, 다음 연산 준비

> 즉, **실제 계산은 Calculator 클래스의 `equal()` → `calculate()`**에서 수행되며,
> UI는 단순히 `num`, `op1`, `op2`, `operator` 상태를 반영하고 화면에 표시하는 역할만 합니다.

---

원하면 제가 **실제 계산 예제 시나리오** (예: `12 + 3 X 2 =`)를
각 버튼 누를 때 상태(`op1`, `op2`, `num`, `operator`)가 어떻게 바뀌는지
표로 만들어서 보여드릴 수도 있습니다.

혹시 그걸 만들어드릴까요?
좋아요 😎 그럼 예제 시나리오로 **`12 + 3 × 2 =`**를 기준으로 **각 버튼 누를 때 상태 변화**를 표로 보여드릴게요.

---

## 버튼 입력 시 상태 변화

| 버튼 | `num` | `op1` | `op2` | `operator` | `result` | 화면 표시 |
| -- | ----- | ----- | ----- | ---------- | -------- | ----- |
| 1  | "1"   | None  | None  | None       | 0.0      | 1     |
| 2  | "12"  | None  | None  | None       | 0.0      | 12    |
| +  | ""    | 12.0  | None  | "+"        | 0.0      | 12 +  |
| 3  | "3"   | 12.0  | None  | "+"        | 0.0      | 3     |
| ×  | ""    | 15.0  | None  | "X"        | 15.0     | 15 X  |
| 2  | "2"   | 15.0  | None  | "X"        | 15.0     | 2     |
| =  | ""    | 30.0  | 2.0   | None       | 30.0     | 30    |

---

### 단계별 설명

1. **숫자 입력** (`1` → `2`)

   * `num`에 숫자 누적
   * `op1`은 아직 없음
   * 화면: 입력한 숫자 그대로 표시

2. **연산자 입력** (`+`)

   * `op1 = float(num)` → 12.0 저장
   * `operator = "+"`
   * `num` 초기화
   * 화면: `12 +` 표시

3. **두 번째 숫자 입력** (`3`)

   * `num = "3"`
   * 화면: 3 표시

4. **연속 연산 입력** (`×`)

   * `op2 = float(num) = 3`
   * `calculate()` 호출 → 12 + 3 = 15
   * `op1 = result = 15`
   * `operator = "X"`
   * `num` 초기화
   * 화면: `15 X` 표시

5. **세 번째 숫자 입력** (`2`)

   * `num = "2"`
   * 화면: 2 표시

6. **= 버튼**

   * `op2 = float(num) = 2`
   * `calculate()` 호출 → 15 × 2 = 30
   * `result = op1 = 30`
   * `num` 초기화, `operator` 초기화
   * 화면: 30 표시

---

### 🔹 핵심 포인트

* `num` : **현재 입력 중인 숫자**
* `op1` : **첫 번째 피연산자 또는 이전 결과**
* `op2` : **두 번째 피연산자 (연산 수행 시)**
* `operator` : **현재 연산자**
* **연속 연산 시** `equal()` 호출 → 이전 계산 결과를 `op1`에 저장

---

원하면 제가 이걸 **그림으로 시각화**해서
각 단계에 `num`, `op1`, `op2`, `operator`, `화면 표시`를 한눈에 보여주는 **상태 다이어그램**으로 만들어 드릴 수도 있어요.

그림으로 만들어드릴까요?


