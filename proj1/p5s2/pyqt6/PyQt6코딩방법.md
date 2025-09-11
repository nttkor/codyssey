PyQt는  Python에서 windows기반 프로그래밍이 가능하게 해주는 패키지입니다. 여러가지 클래스를 포함하고 있습니다.
---

# PyQt6 핵심 정리

## 1. PyQt6 구조

* **PyQt6** = Python에서 Qt6(C++ GUI 라이브러리)를 쓰게 해주는 패키지
* 주요 모듈:

  * `QtWidgets` → 버튼, 라벨, 창 등 **GUI 위젯**
  * `QtCore` → 이벤트 루프, 타이머, 시그널/슬롯 등 핵심 기능
  * `QtGui` → 색상, 폰트, 이미지 등 그래픽 처리
* 모듈은 실제로 \*\*C++ 라이브러리(.so/.pyd)\*\*를 감싸는 Python 확장 모듈

---

## 2. 창(Window) 만들기

* PyQt에서 “창”이 될 수 있는 객체는 **QWidget 계열 클래스** 최상위 부모 클래스

  * `QWidget` → 기본 창
  * `QMainWindow` → 메뉴/상태바, 중앙 위젯 구조
  * `QLabel`, `QPushButton` → 단독으로도 창이 될 수 있음 (보통은 자식 위젯으로 사용)
* `show()` → 창을 화면에 표시하는 요청 paintEvent발생
* `app.exec()` → 이벤트 루프 실행, 창이 유지되고 이벤트 처리 가능, 이게 없으면 바로 종료됨. 무한루프를 만드는 것

---

## 3. 이벤트 처리

* PyQt는 **이벤트 기반**:

  1. OS에서 이벤트 발생 (마우스, 키보드, WM\_PAINT 등)
  2. QApplication 이벤트 루프가 이벤트를 받아 위젯으로 전달
  3. 위젯이 `paintEvent`, `mousePressEvent` 등으로 처리
  4. 시그널/슬롯 메커니즘으로 사용자 정의 함수 실행 가능

---

## 4. Import 방법

좋아요 😄
그럼 간단하게 PyQt6에서 **QtCore와 QtWidgets를 함께 쓰면서 필요한 상수/클래스를 정리**해 드릴게요.

---

# PyQt6 기본 import 정리

```python
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QMainWindow
from PyQt6.QtCore import Qt  # Alignment, Key, Orientation 등 상수
from PyQt6.QtGui import QFont  # 글꼴, 색상, 그림 그리기
```

## 1️⃣ QtWidgets 주요 클래스

| 클래스                      | 용도                    |
| ------------------------ | --------------------- |
| QApplication             | 앱 실행, 이벤트 루프          |
| QWidget                  | 기본 창 / 위젯             |
| QMainWindow              | 메뉴, 툴바, 상태바 지원하는 기본 창 |
| QLabel                   | 텍스트/이미지 표시 위젯         |
| QPushButton              | 버튼 위젯                 |
| QLineEdit                | 한 줄 텍스트 입력            |
| QTextEdit                | 여러 줄 텍스트 입력           |
| QComboBox                | 드롭다운 선택               |
| QCheckBox / QRadioButton | 체크박스 / 라디오 버튼         |

---

## 2️⃣ QtCore.Qt 주요 상수

| 상수                                            | 용도         |
| --------------------------------------------- | ---------- |
| AlignmentFlag.AlignCenter                     | 텍스트 중앙 정렬  |
| AlignmentFlag.AlignLeft / AlignRight          | 좌/우 정렬     |
| Key.Key\_Escape / Key.Key\_Enter              | 키보드 이벤트 처리 |
| Orientation.Horizontal / Orientation.Vertical | 방향 지정      |
| MouseButton.LeftButton / RightButton          | 마우스 클릭 이벤트 |

---

## 3️⃣ QtGui 주요 클래스

| 클래스              | 용도                      |
| ---------------- | ----------------------- |
| QFont            | 폰트 설정                   |
| QColor           | 색상 설정                   |
| QPixmap / QImage | 이미지 처리                  |
| QPainter         | 화면 그리기, paintEvent에서 사용 |

---

### ✅ 정리

* **위젯 클래스** → `QtWidgets`
* **상수/플래그/이벤트 관련** → `QtCore.Qt`
* **그래픽/폰트/이미지** → `QtGui`
* **실무에서는 혼합 사용 + IDE 자동완성 활용**

---

원하면 제가 이 구조를 반영해서 **QMainWindow + 중앙 QLabel + 버튼 클릭 이벤트까지 포함한 샘플 코드**를 바로 만들어 보여드릴 수도 있어요.
그럼 import부터 이벤트까지 한눈에 이해 가능하게 됩니다.

만들어드릴까요?


---

Windows 띄우기
'''python

from PyQt6.QtWidgets import QApplication, QWidget
import sys

# 모든 PyQt 애플리케이션은 QApplication 인스턴스가 반드시 1개 필요함.
# sys.argv를 넣으면 명령줄 인자를 처리할 수 있음.
# 만약 명령줄 인자를 쓰지 않을 거라면 QApplication([])로 해도 무방. import sys도 필요없음
app = QApplication(sys.argv) 
window = QWidget() # QWidget 객체 생성 → 이게 기본 윈도우(창)가 됨. 다른 자식객체 만들어도 됨
window.show()  # ⚠️ 중요: 그리기 요청 처리 (paintEvent)
#QApplication의 객체 app
# 이벤트 루프 실행 (GUI 프로그램은 무조건 필요), 창을 닫으면 종료됨.
app.exec() # paintEvent요청처리해서 윈도우를 띄워주고 이벤트 폴링및 이벤트핸들링처리
'''
## Print Hello 프로그램
'''python
# 다른 위젯(QMainWindow, QLabel, QPushButton 등)을 바로 메인 창으로 써도 됩니다.
# 이번에는 QMainWindow를 사용해서 "Hello!"를 표시해 보겠습니다.
# QMainWindow는 QWidget보다 조금 더 고급 창으로, 메뉴바, 상태바, 툴바 같은 걸 붙일 수 있는 기본 구조를 이미 가지고 있어요.
# 그래서 setCentralWidget()을 이용해서 중앙에 위젯을 올려주면 됩니다.

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel 
import sys

app = QApplication(sys.argv)

# QMainWindow 객체 생성
window = QMainWindow()
window.setWindowTitle("QMainWindow 예제")  # 창 제목
window.resize(400, 300)  # 창 크기 (가로 400, 세로 300)

# QLabel 생성 (텍스트 표시 위젯)
label = QLabel("Hello!", window)
label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 텍스트 가운데 정렬

# QMainWindow 중앙에 QLabel 배치
window.setCentralWidget(label)

# 창 보이기
window.show()

# 이벤트 루프 실행
app.exec()
'''