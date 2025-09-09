import sys
import os
import math
from PyQt6 import QtWidgets, uic, QtGui

# 현재 스크립트 경로로 이동
os.chdir(os.path.dirname(__file__))

# UI 파일 로드
CalculatorUI, _ = uic.loadUiType("calculator.ui")
EngineeringUI, _ = uic.loadUiType("engineering.ui")

# ---------------- Calculator Window ----------------
class CalculatorWindow(QtWidgets.QMainWindow, CalculatorUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # UI 초기화
        self.stack = []     # 계산 입력 스택
        self.setup_connections()  # 버튼 이벤트 연결

        # UI 버튼 텍스트 교정
        if hasattr(self, 'btn_backspace'):
            self.btn_backspace.setText("⌫")  # 백스페이스 기호
        if hasattr(self, 'btn_multiply'):
            self.btn_multiply.setText("X")   # 곱하기 기호
        if hasattr(self, 'btn_divide'):
            self.btn_divide.setText("÷")     # 나누기 기호

    def setup_connections(self):
        # 숫자 버튼 연결
        for i in range(10):
            btn = getattr(self, f'btn_{i}', None)
            if btn:
                btn.clicked.connect(lambda checked, n=str(i): self.add_input(n))

        # 연산자 버튼 연결
        ops = ['plus', 'minus', 'multiply', 'divide']
        symbols = {'plus':'+', 'minus':'-', 'multiply':'X', 'divide':'÷'}  # LED 표시용 기호
        for op in ops:
            btn = getattr(self, f'btn_{op}', None)
            if btn:
                btn.clicked.connect(lambda checked, s=symbols[op]: self.add_input(s))

        # 기타 버튼 연결
        if hasattr(self, 'btn_decimal'):
            self.btn_decimal.clicked.connect(lambda: self.add_input('.'))
        if hasattr(self, 'btn_equals'):
            self.btn_equals.clicked.connect(self.calculate)
        if hasattr(self, 'btn_backspace'):
            self.btn_backspace.clicked.connect(self.backspace)
        if hasattr(self, 'btn_mode'):
            self.btn_mode.clicked.connect(self.open_engineering)

    def add_input(self, text):
        # 입력된 텍스트를 스택에 추가
        self.stack.append(text)
        self.update_led()  # LED 갱신

    def update_led(self):
        # 스택 내용을 LED 표시용 문자열로 변환
        display_text = ''.join(self.stack)
        # 이미 X, ÷로 저장되므로 변환 필요 없음
        font_size = 24
        if len(display_text) > 10:
            font_size = int(480 / len(display_text))  # 글자 수에 따라 폰트 크기 조정
        self.led.setFont(QtGui.QFont("Arial", font_size))
        self.led.setText(display_text)

    def calculate(self):
        try:
            # X, ÷를 파이썬 연산자 * / 로 변환
            expr = ''.join(self.stack).replace('X','*').replace('÷','/')
            result = eval(expr)  # 계산 수행
            self.stack = list(str(result))
            self.update_led()
        except Exception:
            self.led.setText("Error")
            self.stack = []

    def backspace(self):
        # 스택이 비어있으면 리턴
        if not self.stack:
            return
        last = self.stack.pop()  # 마지막 입력 제거
        # 숫자 또는 소수점이면 한 자리 삭제
        if last.isdigit() or last=='.':
            pass
        else:
            # 함수명/연산자면 전체 삭제
            while self.stack and self.stack[-1].isalpha():
                self.stack.pop()
        self.update_led()

    def open_engineering(self):
        # 엔지니어링 모드로 전환
        self.eng_window = EngineeringWindow()
        self.eng_window.show()
        self.close()


# ---------------- Engineering Window ----------------
class EngineeringWindow(QtWidgets.QMainWindow, EngineeringUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # UI 초기화
        self.stack = []     # 계산 입력 스택
        self.setup_connections()  # 버튼 이벤트 연결

        # UI 버튼 텍스트 교정
        if hasattr(self, 'btn_backspace'):
            self.btn_backspace.setText("⌫")  # 백스페이스 기호
        if hasattr(self, 'btn_multiply'):
            self.btn_multiply.setText("X")   # 곱하기 기호
        if hasattr(self, 'btn_divide'):
            self.btn_divide.setText("÷")     # 나누기 기호

    def setup_connections(self):
        # 숫자 버튼 연결
        for i in range(10):
            btn = getattr(self, f'btn_{i}', None)
            if btn:
                btn.clicked.connect(lambda checked, n=str(i): self.add_input(n))

        # 연산자 버튼 연결
        ops = ['plus','minus','multiply','divide']
        symbols = {'plus':'+', 'minus':'-', 'multiply':'X', 'divide':'÷'}  # LED 표시용 기호
        for op in ops:
            btn = getattr(self, f'btn_{op}', None)
            if btn:
                btn.clicked.connect(lambda checked, s=symbols[op]: self.add_input(s))

        # 함수 버튼 연결
        funcs = ['sin','cos','tan','sinh','cosh','tanh','ln','log10','x_squared','x_cubed','x_power_y','e_power_x','10_power_x']
        for f in funcs:
            btn = getattr(self, f'btn_{f}', None)
            if btn:
                btn.clicked.connect(lambda checked, name=f: self.add_input(name+'('))

        # 기타 버튼 연결
        if hasattr(self, 'btn_decimal'):
            self.btn_decimal.clicked.connect(lambda: self.add_input('.'))
        if hasattr(self, 'btn_equals'):
            self.btn_equals.clicked.connect(self.calculate)
        if hasattr(self, 'btn_backspace'):
            self.btn_backspace.clicked.connect(self.backspace)
        if hasattr(self, 'btn_mode'):
            self.btn_mode.clicked.connect(self.open_calculator)

    def add_input(self, text):
        # 입력된 텍스트를 스택에 추가
        self.stack.append(text)
        self.update_led()  # LED 갱신

    def update_led(self):
        # 스택 내용을 LED 표시용 문자열로 변환
        display_text = ''.join(self.stack)
        font_size = 24
        if len(display_text) > 10:
            font_size = int(480 / len(display_text))  # 글자 수에 따라 폰트 크기 조정
        self.led.setFont(QtGui.QFont("Arial", font_size))
        self.led.setText(display_text)

    def calculate(self):
        try:
            # X, ÷를 파이썬 연산자 * / 로 변환
            expr = ''.join(self.stack).replace('X','*').replace('÷','/')
            result = eval(expr)  # 계산 수행
            self.stack = list(str(result))
            self.update_led()
        except Exception:
            self.led.setText("Error")
            self.stack = []

    def backspace(self):
        # 스택이 비어있으면 리턴
        if not self.stack:
            return
        last = self.stack.pop()
        # 숫자 또는 소수점이면 한 자리 삭제
        if last.isdigit() or last=='.':
            pass
        else:
            # 함수명/연산자면 전체 삭제
            while self.stack and self.stack[-1].isalpha():
                self.stack.pop()
        self.update_led()

    def open_calculator(self):
        # 일반 계산기로 전환
        self.calc_window = CalculatorWindow()
        self.calc_window.show()
        self.close()


# ---------------- Main ----------------
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CalculatorWindow()  # 기본 창은 일반 계산기
    window.show()
    sys.exit(app.exec())
