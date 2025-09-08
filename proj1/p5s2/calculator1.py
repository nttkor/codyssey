import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic
from PyQt6.QtCore import Qt

# 디렉토리 변경
os.chdir(os.path.dirname(__file__))

# UI 파일 로드
try:
    form_class = uic.loadUiType("caculator.ui")[0]
except FileNotFoundError:
    print("UI 파일(caculator.ui)을 찾을 수 없습니다. 경로를 확인해주세요.")
    sys.exit(1)

class Calculator(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 변수 초기화
        self.num = ""
        self.op1 = None
        self.op2 = None
        self.operator = None
        self.equals_pressed = False
        self.is_negative = False
        
        # 디스플레이 초기화
        self.led.setText("0")
        
        # 버튼 연결
        self.btn_0.clicked.connect(lambda: self.input_number("0"))
        self.btn_1.clicked.connect(lambda: self.input_number("1"))
        self.btn_2.clicked.connect(lambda: self.input_number("2"))
        self.btn_3.clicked.connect(lambda: self.input_number("3"))
        self.btn_4.clicked.connect(lambda: self.input_number("4"))
        self.btn_5.clicked.connect(lambda: self.input_number("5"))
        self.btn_6.clicked.connect(lambda: self.input_number("6"))
        self.btn_7.clicked.connect(lambda: self.input_number("7"))
        self.btn_8.clicked.connect(lambda: self.input_number("8"))
        self.btn_9.clicked.connect(lambda: self.input_number("9"))
        self.btn_decimal.clicked.connect(lambda: self.input_number("."))
        
        self.btn_plus.clicked.connect(lambda: self.input_operator("+"))
        self.btn_minus.clicked.connect(lambda: self.input_operator("-"))
        self.btn_multiply.clicked.connect(lambda: self.input_operator("X"))
        self.btn_divide.clicked.connect(lambda: self.input_operator("/"))
        self.btn_percent.clicked.connect(lambda: self.input_operator("%"))
        self.btn_plus_minus.clicked.connect(self.toggle_sign)
        self.btn_equals.clicked.connect(self.calculate_result)
        self.btn_ac.clicked.connect(self.all_clear)
        self.btn_mode.clicked.connect(self.all_clear) # 임시로 AC와 동일 기능

    def input_number(self, digit):
        if self.equals_pressed:
            self.all_clear()
        
        # 소수점 중복 입력 방지
        if digit == "." and "." in self.num:
            return
        
        # 디스플레이 초기화
        if self.led.text() == "0" and digit != ".":
            self.led.clear()
        
        # 숫자 누적 및 디스플레이 업데이트
        self.num += digit
        self.led.setText(self.num)

    def input_operator(self, op):
        self.equals_pressed = False
        self.is_negative = False
        
        if self.num:
            if self.op1 is None:
                self.op1 = float(self.num)
            else:
                self.op2 = float(self.num)
                self.calculate()
            
            self.operator = op
            self.num = ""
            self.led.setText(f"{self.op1} {self.operator}")

        else: # num이 비어있는 상태
            # 음수 처리를 위한 단독 - 입력
            if op == "-" and self.operator is None:
                self.num = "-"
                self.led.setText("-")
                return

            # 연속 연산자 처리
            if self.operator:
                # 다음 숫자가 음수임을 나타내는 - 입력
                if op == "-":
                    self.led.setText(f"{self.op1} {self.operator} -")
                    self.is_negative = True
                # 연산자 변경
                else:
                    self.operator = op
                    self.led.setText(f"{self.op1} {self.operator}")
            # op1이 있고 연산자가 없는 상태에서 연산자 입력
            elif self.op1 is not None:
                self.operator = op
                self.led.setText(f"{self.op1} {self.operator}")
            
    def calculate_result(self):
        if self.op1 is not None and self.num:
            try:
                self.op2 = float(self.num)
                self.calculate()
                self.led.setText(str(self.op1))
                self.equals_pressed = True
            except (ValueError, TypeError):
                self.led.setText("Error")
                self.all_clear()
        elif self.op1 is not None: # op2가 없는 상태에서 =를 누를 경우
            self.operator = None
            self.equals_pressed = True
            self.led.setText(str(self.op1))
        else: # 숫자가 없는 상태에서 =를 누를 경우
            self.all_clear()

    def calculate(self):
        if self.op1 is not None and self.op2 is not None:
            if self.operator == "+":
                self.op1 += self.op2
            elif self.operator == "-":
                self.op1 -= self.op2
            elif self.operator == "X":
                self.op1 *= self.op2
            elif self.operator == "/":
                if self.op2 != 0:
                    self.op1 /= self.op2
                else:
                    self.led.setText("Error")
                    self.all_clear()
                    return
            elif self.operator == "%":
                self.op1 %= self.op2
            
            # 소수점 처리
            self.op1 = round(self.op1, 3)
            self.op2 = None
            self.operator = None
            self.num = ""

    def toggle_sign(self):
        if self.num:
            if self.num.startswith('-'):
                self.num = self.num[1:]
            else:
                self.num = '-' + self.num
            self.led.setText(self.num)
        
    def all_clear(self):
        self.num = ""
        self.op1 = None
        self.op2 = None
        self.operator = None
        self.equals_pressed = False
        self.is_negative = False
        self.led.setText("0")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calculator()
    calc.show()
    sys.exit(app.exec())