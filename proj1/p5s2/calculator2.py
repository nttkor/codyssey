import sys # 시스템 관련 기능을 사용하기 위해 sys 모듈을 불러옵니다.
import os # 파일 경로 관련 기능을 사용하기 위해 os 모듈을 불러옵니다.
from PyQt6.QtWidgets import QApplication, QMainWindow # PyQt6의 주요 위젯 클래스를 불러옵니다.
from PyQt6 import uic # Qt Designer로 만든 UI 파일을 로드하는 기능을 불러옵니다.
from PyQt6.QtCore import Qt # Qt 모듈의 상수들을 불러옵니다.
from PyQt6.QtGui import QFont # 폰트 관련 기능을 사용하기 위해 QFont를 불러옵니다.

# 현재 스크립트가 있는 디렉토리로 작업 경로를 변경합니다.
os.chdir(os.path.dirname(__file__))

# UI 파일(caculator.ui)을 로드합니다. 파일이 없으면 오류 메시지를 출력하고 종료합니다.
try:
    form_class = uic.loadUiType("caculator.ui")[0]
except FileNotFoundError:
    print("UI 파일(caculator.ui)을 찾을 수 없습니다. 경로를 확인해주세요.")
    sys.exit(1)

class Calculator:
    """계산 로직을 담당하는 클래스입니다."""
    def __init__(self):
        # 현재 입력되는 숫자를 저장하는 변수
        self.num = ""
        # 첫 번째 피연산자를 저장하는 변수
        self.op1 = None
        # 두 번째 피연산자를 저장하는 변수
        self.op2 = None
        # 연산자를 저장하는 변수
        self.operator = None
        # 최종 결과를 저장하는 변수
        self.result = 0.0

    def reset(self):
        """모든 계산기 상태를 초기화합니다."""
        self.num = ""
        self.op1 = None
        self.op2 = None
        self.operator = None
        self.result = 0.0

    def add(self):
        """더하기 연산을 수행합니다."""
        self.op1 += self.op2

    def subtract(self):
        """빼기 연산을 수행합니다."""
        self.op1 -= self.op2

    def multiply(self):
        """곱하기 연산을 수행합니다."""
        self.op1 *= self.op2

    def divide(self):
        """나누기 연산을 수행합니다. 0으로 나누는 경우를 처리합니다."""
        if self.op2 == 0:
            return "Error"
        self.op1 /= self.op2

    def percent(self):
        """퍼센트 연산을 수행합니다. op1 또는 num에 적용됩니다."""
        if self.op1 is not None:
            self.op1 /= 100
        elif self.num:
            self.num = str(float(self.num) / 100)

    def negative_positive(self):
        """현재 입력된 숫자의 부호를 변경합니다."""
        if self.num:
            if self.num.startswith('-'):
                self.num = self.num[1:]
            else:
                self.num = '-' + self.num

    def equal(self):
        """최종 계산을 수행하고 결과를 반환합니다."""
        if self.op1 is not None and self.num:
            # num 변수의 값을 op2에 실수형으로 저장합니다.
            self.op2 = float(self.num)
            
            # operator 변수에 따라 적절한 연산을 호출합니다.
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
                # 퍼센트 연산은 op1에 (op1 * (op2 / 100))을 더하는 방식으로 처리합니다.
                self.op2 = self.op1 * (self.op2 / 100)
                self.add()

            # 최종 결과를 소수점 6자리에서 반올림합니다.
            self.result = round(self.op1, 6)
            
            # 계산 후 상태를 초기화하고 결과를 op1에 저장합니다.
            self.op1 = self.result
            self.op2 = None
            self.operator = None
            self.num = ""
            return self.result
        
        return "Error"

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        # UI 설정을 초기화합니다.
        self.setupUi(self)

        # 계산 로직을 담당하는 Calculator 클래스의 인스턴스를 생성합니다.
        self.calc = Calculator()
        
        # `=` 버튼이 눌렸는지 추적하는 UI 상태 변수
        self.equals_pressed = False
        
        # 디스플레이를 초기화하고 초기 폰트 크기를 설정합니다.
        self.led.setText("0")
        self.set_display_font_size("0")
        
        # 각 버튼을 해당 기능을 수행하는 메서드에 연결합니다.
        self.btn_0.clicked.connect(lambda: self.input_number("0"))
        # 숫자 버튼 연결 (반복되므로 주석 생략)
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
        # 연산자 버튼 연결 (반복되므로 주석 생략)
        self.btn_minus.clicked.connect(lambda: self.input_operator("-"))
        self.btn_multiply.clicked.connect(lambda: self.input_operator("X"))
        self.btn_divide.clicked.connect(lambda: self.input_operator("/"))
        self.btn_percent.clicked.connect(self.handle_percent)
        self.btn_plus_minus.clicked.connect(self.handle_negative_positive)
        self.btn_equals.clicked.connect(self.handle_equal)
        self.btn_ac.clicked.connect(self.handle_reset)
        self.btn_mode.clicked.connect(self.handle_reset) # 임시로 AC와 동일 기능

    def set_display_font_size(self, text):
        """텍스트 길이에 따라 폰트 크기를 동적으로 조절합니다."""
        font = QFont()
        font.setBold(True)
        length = len(text)
        
        if length > 10:
            # 11자리부터는 단순 비율로 폰트 크기를 계산합니다.
            font_size = int(480 / length)
            font.setPointSize(font_size)
        else:
            # 10자리까지는 기본 폰트 크기 48pt를 유지합니다.
            font.setPointSize(48)
        
        self.led.setFont(font)

    def input_number(self, digit):
        """숫자 버튼 클릭을 처리합니다."""
        # `=` 이후에 숫자를 입력하면 초기화합니다.
        if self.equals_pressed:
            self.handle_reset()
        
        # 소수점 중복 입력을 방지합니다.
        if digit == "." and "." in self.calc.num:
            return

        # '0'이 표시된 상태에서 새로운 숫자를 입력하면 '0'을 지웁니다.
        if self.led.text() == "0" and digit != ".":
            self.led.clear()

        # 현재 숫자에 새 숫자를 추가하고 디스플레이를 업데이트합니다.
        self.calc.num += digit
        self.led.setText(self.calc.num)
        self.set_display_font_size(self.calc.num)

    def input_operator(self, op):
        """연산자 버튼 클릭을 처리합니다."""
        self.equals_pressed = False
        
        # 현재 숫자가 입력된 상태일 때
        if self.calc.num:
            # op1이 비었다면 num을 op1에 저장합니다.
            if self.calc.op1 is None:
                self.calc.op1 = float(self.calc.num)
            else:
                # op1이 있다면 중간 계산을 수행합니다.
                self.calc.op2 = float(self.calc.num)
                self.calc.equal()
            
            # 연산자를 저장하고 num을 초기화합니다.
            self.calc.operator = op
            self.calc.num = ""
            # 디스플레이에 op1과 연산자를 표시합니다.
            self.led.setText(f"{self.calc.op1} {self.calc.operator}")
            self.set_display_font_size(self.led.text())

        # 현재 숫자가 입력되지 않은 상태일 때 (연속 연산자 입력)
        else:
            # op1, operator가 비어있고 '-'가 입력되면 음수 처리를 시작합니다.
            if op == "-" and self.calc.operator is None and self.calc.op1 is None:
                self.calc.num = "-"
                self.led.setText("-")
                return

            # 이미 연산자가 있다면, 새로운 연산자로 변경합니다.
            if self.calc.operator:
                if op != "-" and op != "+":
                    self.calc.operator = op
                    self.led.setText(f"{self.calc.op1} {self.calc.operator}")
            # op1은 있지만 연산자가 없을 때, 연산자를 설정합니다.
            elif self.calc.op1 is not None:
                self.calc.operator = op
                self.led.setText(f"{self.calc.op1} {self.calc.operator}")

    def handle_equal(self):
        """등호(=) 버튼 클릭을 처리합니다."""
        # Calculator 클래스의 equal() 메서드를 호출하여 결과를 받습니다.
        result = self.calc.equal()
        if result == "Error":
            # 에러 발생 시 에러 메시지를 표시하고 초기화합니다.
            self.led.setText("Error")
            self.handle_reset()
        else:
            # 결과를 디스플레이에 표시하고 폰트 크기를 조절합니다.
            self.led.setText(str(result))
            self.set_display_font_size(str(result))
            # `=` 버튼이 눌렸음을 기록합니다.
            self.equals_pressed = True

    def handle_reset(self):
        """AC 버튼 클릭을 처리합니다."""
        # Calculator 클래스의 reset() 메서드를 호출하여 상태를 초기화합니다.
        self.calc.reset()
        # 디스플레이를 "0"으로 초기화하고 폰트 크기를 재설정합니다.
        self.led.setText("0")
        self.set_display_font_size("0")
        self.equals_pressed = False

    def handle_negative_positive(self):
        """+/- 버튼 클릭을 처리합니다."""
        # Calculator 클래스의 negative_positive() 메서드를 호출합니다.
        self.calc.negative_positive()
        # 변경된 숫자를 디스플레이에 표시하고 폰트 크기를 조절합니다.
        self.led.setText(self.calc.num)
        self.set_display_font_size(self.calc.num)

    def handle_percent(self):
        """% 버튼 클릭을 처리합니다."""
        # num 또는 op1에 퍼센트 연산을 적용하고 결과를 표시합니다.
        if self.calc.num:
            self.calc.percent()
            self.led.setText(self.calc.num)
            self.set_display_font_size(self.calc.num)
        elif self.calc.op1 is not None:
            self.calc.percent()
            self.led.setText(str(self.calc.op1))
            self.set_display_font_size(str(self.calc.op1))

if __name__ == '__main__':
    # QApplication 인스턴스를 생성합니다.
    app = QApplication(sys.argv)
    # MainWindow 인스턴스를 생성합니다.
    window = MainWindow()
    # 윈도우를 화면에 표시합니다.
    window.show()
    # 이벤트 루프를 실행합니다.
    sys.exit(app.exec())