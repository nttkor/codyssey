## 🧭 calculator1  실행 순서 요약

### ① `if __name__ == "__main__":` 부분 실행

```python
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
```

#### ▶ 순서

1. **`QApplication` 생성**

   * PyQt6에서 GUI 프로그램은 반드시 `QApplication` 객체가 먼저 있어야 해요.
   * 이게 있어야 버튼, 창, 폰트 등이 실제로 화면에 표시됩니다.

2. **`MainWindow()` 실행**

   * `MainWindow` 클래스의 **생성자 `__init__`** 가 자동으로 호출됩니다.
   * 여기서 버튼 연결, UI 세팅 등이 한 번에 설정됩니다.

3. **`window.show()`**

   * 실제 창을 화면에 띄웁니다.

4. **`app.exec()`**

   * 이벤트 루프 시작.
   * 이제부터 PyQt가 키보드/마우스 입력을 기다리고, 버튼을 누를 때마다 연결된 함수(`clicked.connect(...)`)를 호출합니다.

---

## 🪜 MainWindow 생성 시 실행 흐름

### ② `MainWindow.__init__()` 실행

```python
def __init__(self):
    super().__init__()
    self.setupUi(self)
```

* `super().__init__()` : 부모 클래스(QMainWindow, form_class)의 초기화 진행.
* `self.setupUi(self)` : `calculator.ui` 파일의 위젯(버튼, led 등)을 실제 코드 객체로 연결합니다.
  → 이 시점에 `btn_0`, `btn_1`, `led` 같은 속성이 생깁니다.

---

### ③ 표시 초기화

```python
self.led.setText("0")
self.set_display_font_size("0")
```

* 프로그램이 처음 실행되면 LED 창(`QLabel`)에 `"0"`이 표시됩니다.
* 동시에 폰트 크기도 숫자 길이에 맞춰 조정합니다.

---

### ④ 숫자 버튼 연결 루프

```python
for i in range(10):
    getattr(self, f"btn_{i}").clicked.connect(lambda _, x=str(i): self.show_text(x))
```

* `btn_0`부터 `btn_9`까지 자동으로 하나씩 불러와(`getattr`)
* 각각 클릭될 때 `show_text("해당 숫자")` 가 호출되도록 연결합니다.
  예: `btn_3` → 누르면 `self.show_text("3")` 실행.

---

### ⑤ 소수점 및 연산자 버튼 연결

```python
self.btn_decimal.clicked.connect(lambda: self.show_text("."))
self.btn_plus.clicked.connect(lambda: self.show_text("+"))
...
```

* 각각 클릭되면 해당 문자만 `show_text()`로 전달되어 LED에 표시됩니다.

---

### ⑥ AC(초기화) 및 모드 버튼 연결

```python
self.btn_ac.clicked.connect(self.handle_reset)
self.btn_mode.clicked.connect(self.handle_reset)
```

* `AC`나 `MODE` 버튼을 누르면 `handle_reset()` 실행 → LED를 `"0"`으로 되돌립니다.

---

## 🖱 버튼을 누를 때의 흐름

예를 들어 **“7 버튼”** 을 누르면:

1. PyQt 이벤트 루프가 클릭 신호를 감지
2. `btn_7.clicked` 에 연결된 람다가 실행됨

   ```python
   lambda _, x='7': self.show_text(x)
   ```
3. 결과적으로 `self.show_text("7")` 호출
4. `show_text()` 내부에서

   ```python
   self.led.setText("7")               # LED에 "7" 표시
   self.set_display_font_size("7")     # 폰트 크기 재조정
   ```
5. 결과: 화면의 표시창에 “7”이 나타남 🎉

---

## 🧹 AC 버튼을 누를 때

1. `btn_ac.clicked` → `self.handle_reset()` 실행
2. 내부에서

   ```python
   self.led.setText("0")
   self.set_display_font_size("0")
   ```
3. 화면이 다시 “0”으로 리셋됩니다.

---

## 🧩 전체 실행 순서 정리

| 단계 | 실행 코드                                           | 설명                  |
| -- | ----------------------------------------------- | ------------------- |
| 1  | `app = QApplication(sys.argv)`                  | GUI 앱 시작            |
| 2  | `window = MainWindow()`                         | 창 클래스 생성, 내부 초기화 수행 |
| 3  | `setupUi()`                                     | UI 파일에서 버튼·레이블 연결   |
| 4  | `led` 초기화                                       | "0" 표시, 폰트 크기 세팅    |
| 5  | `connect()`                                     | 각 버튼을 함수에 연결        |
| 6  | `window.show()`                                 | 창 띄우기               |
| 7  | `app.exec()`                                    | 이벤트 루프 시작           |
| 8  | (사용자 클릭 시) `show_text()` or `handle_reset()` 실행 | 표시 업데이트             |

---

원하신다면, 이 흐름을 **시각적 다이어그램 (예: 순서도나 이벤트 흐름 그림)** 으로도 만들어드릴 수 있어요.
그림으로 보는 게 이해 훨씬 빠른데, 만들어드릴까요?
