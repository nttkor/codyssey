'''
주요 변경 사항

사칙연산:
add(), subtract(), multiply(), divide() 메소드를 Calculator 클래스에 추가합니다.
기타 기능:
reset(): 계산기 초기화 (디스플레이 클리어).
negative-positive(): 부호 변경 (음수/양수).
percent(): 퍼센트 계산 (100으로 나누기).
equal(): 결과 계산 및 디스플레이.
소수점:
소수점 버튼은 한번만 입력되도록 구현합니다.
폰트 크기 조정 (보너스):
계산 결과가 길어지면 폰트 크기가 자동으로 줄어들도록 구현합니다.
소수점 반올림 (보너스):
소수점 이하 6자리까지 입력되면 반올림된 값만 출력하도록 구현합니다.
'''
'''
Calculator 클래스를 만든다.
Calculator 클래스에 사칙 연산을 담당할 메소드인 add(), subtract(), multiply(), divide() 를 추가하고 동작할 수 있게 기능을 구현한다.
Calculator 클래스에 추가로 초기화 및 음수양수, 퍼센트 등을 담당할 reset(), negative-positive(), percent() 메소드를 추가하고 기능을 구현한다.
숫자키를 누를 때 마다 화면에 숫자가 누적된다.
소수점 키를 누르면 소수점이 입력된다. 단 이미 소수점이 입력되어 있는 상태에서는 추가로 입력되지 않는다.
Calculator 클래스에 결과를 출력할 equal() 메소드를 추가하고 기능을 구현한다.
UI의 각 버튼과 Calculator 클래스를 연결해서 완전한 동작을 구현한다.
완성된 코드는 calculator.py 로 저장한다.
'''

import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class Calculator:
    """
    Calculator 클래스는 사칙 연산, 부호 변경, 퍼센트 계산 등의 기능을 포함한 계산기를 구현합니다.
    """
    def __init__(self):
        self.current_input = ""  # 현재 입력값
        self.result = None  # 계산 결과 초기값
        self.last_operator = None  # 마지막 연산자
        self.is_decimal = False  # 소수점 여부 체크

    def reset(self):
        """
        계산기를 초기화하고 입력값을 초기 상태로 되돌립니다.
        """
        self.current_input = ""
        self.result = None
        self.last_operator = None
        self.is_decimal = False

    def negative_positive(self):
        """
        입력값의 부호를 변경합니다. (음수 <-> 양수)
        """
        if self.current_input:
            if self.current_input.startswith('-'):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input

    def percent(self):
        """
        현재 입력값을 100으로 나눠서 퍼센트로 계산합니다.
        """
        if self.current_input:
            try:
                self.current_input = str(float(self.current_input) / 100)
            except ValueError:
                self.current_input = "Error"

    def add(self):
        """
        덧셈 연산자를 설정합니다.
        """
        self.calculate()
        self.last_operator = "+"
        self.current_input = ""

    def subtract(self):
        """
        뺄셈 연산자를 설정합니다.
        """
        self.calculate()
        self.last_operator = "-"
        self.current_input = ""

    def multiply(self):
        """
        곱셈 연산자를 설정합니다.
        """
        self.calculate()
        self.last_operator = "*"
        self.current_input = ""

    def divide(self):
        """
        나눗셈 연산자를 설정합니다.
        """
        self.calculate()
        self.last_operator = "/"
        self.current_input = ""

    def equal(self):
        """
        결과를 계산하고 디스플레이에 표시합니다.
        """
        self.calculate()
        if self.result is not None:
            self.current_input = str(self.result)
        else:
            self.current_input = "Error"

    def calculate(self):
        """
        연산을 계산합니다. `self.last_operator`에 따라 덧셈, 뺄셈, 곱셈, 나눗셈을 처리합니다.
        """
        if self.result is None:
            self.result = float(self.current_input)
        else:
            if self.last_operator == "+":
                self.result += float(self.current_input)
            elif self.last_operator == "-":
                self.result -= float(self.current_input)
            elif self.last_operator == "*":
                self.result *= float(self.current_input)
            elif self.last_operator == "/":
                try:
                    self.result /= float(self.current_input)
                except ZeroDivisionError:
                    self.result = "Error"


class CalculatorApp(QWidget):
    """
    PyQt6 기반의 계산기 UI 클래스입니다.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enhanced Calculator (PyQt6)")
        self.setFixedSize(350, 500)
        self.calc = Calculator()  # 계산기 객체 생성
        self.init_ui()  # UI 초기화

    def init_ui(self):
        """
        계산기의 UI를 설정하는 함수입니다. 버튼 배치, 글꼴, 크기 등을 설정합니다.
        """
        # 디스플레이 영역
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFixedHeight(60)
        self.display.setFont(QFont("Arial", 24))

        # 버튼 레이아웃 (아이폰 계산기 스타일)
        buttons = [
            ['C', '+/-', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=',]
        ]

        grid = QGridLayout()
        row = 0
        for btn_row in buttons:
            col = 0
            for btn_text in btn_row:
                button = QPushButton(btn_text)
                button.setFont(QFont("Arial", 16))
                button.setFixedSize(70, 70)
                if btn_text == '0':
                    button.setFixedSize(140, 70)
                    grid.addWidget(button, row, col, 1, 2)
                    col += 1
                else:
                    grid.addWidget(button, row, col)
                button.clicked.connect(self.button_clicked)
                col += 1
            row += 1

        # 메인 레이아웃
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.display)
        main_layout.addLayout(grid)

        self.setLayout(main_layout)

    def button_clicked(self):
        """
        버튼 클릭 시 호출되는 함수입니다.
        """
        sender = self.sender()
        btn_text = sender.text()

        if btn_text == 'C':  # 계산기 초기화
            self.calc.reset()
            self.display.setText("")
        elif btn_text == '+/-':  # 부호 변경
            self.calc.negative_positive()
            self.display.setText(self.calc.current_input)
        elif btn_text == '%':  # 퍼센트 계산
            self.calc.percent()
            self.display.setText(self.calc.current_input)
        elif btn_text == '=':  # 결과 계산
            self.calc.equal()
            self.display.setText(self.calc.current_input)
            self.adjust_font_size()
        elif btn_text in '0123456789':  # 숫자 입력
            self.calc.current_input += btn_text
            self.display.setText(self.calc.current_input)
        elif btn_text == '.':  # 소수점 처리
            if not self.calc.is_decimal:
                self.calc.current_input += btn_text
                self.calc.is_decimal = True
                self.display.setText(self.calc.current_input)
        elif btn_text == '+':  # 덧셈
            self.calc.add()
        elif btn_text == '-':  # 뺄셈
            self.calc.subtract()
        elif btn_text == '*':  # 곱셈
            self.calc.multiply()
        elif btn_text == '/':  # 나눗셈
            self.calc.divide()

    def adjust_font_size(self):
        """
        결과 출력에 맞게 폰트 크기를 자동 조정합니다.
        소수점 6자리 이하로 반올림하여 출력합니다.
        """
        try:
            result = float(self.calc.current_input)
            if abs(result) > 999999:
                self.display.setFont(QFont("Arial", 12))
            elif len(str(result)) > 9:
                self.display.setFont(QFont("Arial", 18))
            else:
                self.display.setFont(QFont("Arial", 24))

            # 소수점 이하 6자리 반올림
            self.display.setText(f"{result:.6f}".rstrip('0').rstrip('.'))

        except ValueError:
            self.display.setFont(QFont("Arial", 24))
            self.display.setText("Error")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc = CalculatorApp()
    calc.show()
    sys.exit(app.exec())
