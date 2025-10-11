import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic
from PyQt6.QtGui import QFont

# ============================================================
# 현재 스크립트 폴더로 이동
# ============================================================
os.chdir(os.path.dirname(__file__))

# ============================================================
# Qt UI 파일 로드
# ============================================================
try:
    form_class = uic.loadUiType("calculator.ui")[0]
except FileNotFoundError:
    print("❌ UI 파일(calculator.ui)을 찾을 수 없습니다.")
    sys.exit(1)


# ============================================================
# Calculator 클래스 — 계산 로직
# ============================================================
class Calculator:
    """
    사칙연산, %, +/- 등 계산 로직 처리
    MainWindow에서 연산을 위임받아 수행
    """

    def __init__(self):
        self.reset()

    def reset(self):
        """계산 상태 초기화"""
        self.num = ""          # 현재 입력 숫자
        self.op1 = None        # 첫 번째 피연산자
        self.op2 = None        # 두 번째 피연산자
        self.operator = None   # 현재 연산자
        self.result = 0.0      # 마지막 결과

    # -------------------------------
    # 사칙연산
    # -------------------------------
    def add(self):
        self.op1 += self.op2

    def subtract(self):
        self.op1 -= self.op2

    def multiply(self):
        self.op1 *= self.op2

    def divide(self):
        if self.op2 == 0:
            return "Error"
        self.op1 /= self.op2

    # -------------------------------
    # 부가 기능
    # -------------------------------
    def percent(self):
        """퍼센트 연산"""
        if self.num:
            self.num = str(float(self.num) / 100)
        elif self.op1 is not None:
            self.op1 /= 100

    def negative_positive(self):
        """부호 반전"""
        if self.num:
            if self.num.startswith("-"):
                self.num = self.num[1:]
            else:
                self.num = "-" + self.num

    def equal(self):
        """= 버튼 연산 처리"""
        if self.op1 is not None and self.num:
            self.op2 = float(self.num)

            if self.operator == "+":
                self.add()
            elif self.operator == "-":
                self.subtract()
            elif self.operator == "X":
                self.multiply()
            elif self.operator == "/":
                res = self.divide()
                if res == "Error":
                    return "Error"
            elif self.operator == "%":
                self.op2 = self.op1 * (self.op2 / 100)
                self.add()

            # 결과 반올림
            self.result = round(self.op1, 10)

            # 연속 계산 준비
            self.op1 = self.result
            self.num = ""
            self.operator = None

            return self.result

        return "Error"


# ============================================================
# MainWindow 클래스 — UI 처리 및 이벤트
# ============================================================
class MainWindow(QMainWindow, form_class):
    """
    PyQt6 계산기 GUI
    Calculator 객체를 통해 모든 연산 수행
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.calc = Calculator()
        self.equals_pressed = False  # = 마지막 눌림 여부

        # 초기 화면
        self.led.setText("0")
        self.set_display_font_size("0")

        # 숫자 버튼 연결
        for i in range(10):
            getattr(self, f"btn_{i}").clicked.connect(
                lambda _, x=str(i): self.input_number(x)
            )
        self.btn_decimal.clicked.connect(lambda: self.input_number("."))

        # 연산자 버튼 연결
        self.btn_plus.clicked.connect(lambda: self.input_operator("+"))
        self.btn_minus.clicked.connect(lambda: self.input_operator("-"))
        self.btn_multiply.clicked.connect(lambda: self.input_operator("X"))
        self.btn_divide.clicked.connect(lambda: self.input_operator("/"))
        self.btn_percent.clicked.connect(self.handle_percent)
        self.btn_plus_minus.clicked.connect(self.handle_negative_positive)

        # 기능 버튼
        self.btn_equals.clicked.connect(self.handle_equal)
        self.btn_ac.clicked.connect(self.handle_reset)
        self.btn_mode.clicked.connect(self.handle_reset)

    # ============================================================
    # 디스플레이 폰트 자동 조절
    # ============================================================
    def set_display_font_size(self, text: str):
        font = QFont()
        font.setBold(True)
        length = len(text)
        font_size = 48 if length <= 10 else int(480 / length)
        font.setPointSize(font_size)
        self.led.setFont(font)

    # ============================================================
    # 숫자 입력 처리
    # ============================================================
    def input_number(self, digit: str):
        """
        숫자 또는 소수점 입력
        = 이후 새 입력이면 초기화
        """
        if self.equals_pressed:
            self.handle_reset()

        if digit == "." and "." in self.calc.num:
            return

        if self.led.text() == "0" and digit != ".":
            self.led.clear()

        self.calc.num += digit
        self.led.setText(self.calc.num)
        self.set_display_font_size(self.calc.num)

    # ============================================================
    # 연산자 입력 처리 (연속 입력 포함)
    # ============================================================
    def input_operator(self, op: str):
        """
        연산자 입력 처리
        - 숫자 입력 후 연산자: 계산 수행 후 새 연산자 저장
        - 연속 연산자 입력: 마지막 연산자로 교체
        """
        self.equals_pressed = False

        if self.calc.num:
            if self.calc.op1 is None:
                self.calc.op1 = float(self.calc.num)
            else:
                self.calc.op2 = float(self.calc.num)
                res = self.calc.equal()
                if res == "Error":
                    self.led.setText("Error")
                    return
            self.calc.operator = op
            self.calc.num = ""

        else:
            # 연산자 연속 입력 시 operator만 교체
            if self.calc.op1 is not None:
                self.calc.operator = op

            # 첫 입력 '-'일 때 음수 처리
            elif op == "-" and self.calc.op1 is None:
                self.calc.num = "-"
        
        # 화면 업데이트
        if self.calc.op1 is not None:
            op1_display = int(self.calc.op1) if self.calc.op1.is_integer() else self.calc.op1
            self.led.setText(f"{op1_display} {self.calc.operator}")
            self.set_display_font_size(self.led.text())
        elif self.calc.num:
            self.led.setText(self.calc.num)
            self.set_display_font_size(self.calc.num)

    # ============================================================
    # = 버튼 처리
    # ============================================================
    def handle_equal(self):
        result = self.calc.equal()

        if result == "Error":
            self.led.setText("Error")
            self.equals_pressed = True
            return

        display_text = str(int(result)) if float(result).is_integer() else str(result)
        self.led.setText(display_text)
        self.set_display_font_size(display_text)
        self.equals_pressed = True

    # ============================================================
    # AC / MODE 처리
    # ============================================================
    def handle_reset(self):
        self.calc.reset()
        self.led.setText("0")
        self.set_display_font_size("0")
        self.equals_pressed = False

    # ============================================================
    # +/- 버튼 처리
    # ============================================================
    def handle_negative_positive(self):
        if self.calc.num:
            self.calc.negative_positive()
            self.led.setText(self.calc.num)
        elif self.calc.op1 is not None and self.calc.operator is None:
            self.calc.op1 = -self.calc.op1
            self.led.setText(str(self.calc.op1))
        else:
            self.calc.num = "-0"
            self.led.setText(self.calc.num)
        self.set_display_font_size(self.led.text())

    # ============================================================
    # % 버튼 처리
    # ============================================================
    def handle_percent(self):
        self.calc.percent()
        if self.calc.num:
            self.led.setText(self.calc.num)
        elif self.calc.op1 is not None:
            text = str(int(self.calc.op1)) if float(self.calc.op1).is_integer() else str(self.calc.op1)
            self.led.setText(text)
        self.set_display_font_size(self.led.text())


# ============================================================
# 메인 실행
# ============================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
