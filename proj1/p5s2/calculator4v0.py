import sys
import math
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QVBoxLayout, QLineEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class Calculator:
    """
    기본적인 계산기 기능을 제공하는 클래스입니다.
    """
    def __init__(self):
        self.result = 0

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b


class EngineeringCalculator(Calculator):
    """
    공학용 계산기 기능을 확장한 클래스입니다.
    기본적인 계산기 기능에 삼각 함수, 제곱, 세제곱 등을 추가합니다.
    """
    def __init__(self):
        super().__init__()

    # 삼각 함수 및 기타 수학 함수들
    def sin(self, angle):
        return math.sin(math.radians(angle))

    def cos(self, angle):
        return math.cos(math.radians(angle))

    def tan(self, angle):
        return math.tan(math.radians(angle))

    def sinh(self, angle):
        return math.sinh(math.radians(angle))

    def cosh(self, angle):
        return math.cosh(math.radians(angle))

    def tanh(self, angle):
        return math.tanh(math.radians(angle))

    def square(self, x):
        return x ** 2

    def cube(self, x):
        return x ** 3

    def pi(self):
        return math.pi


class EngineeringCalculatorUI(QWidget):
    """
    PyQt6를 사용하여 공학용 계산기 UI를 구현한 클래스입니다.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Engineering Calculator")
        self.setFixedSize(360, 600)
        self.calc = EngineeringCalculator()  # 계산기 인스턴스 생성
        self.init_ui()

    def init_ui(self):
        """
        계산기의 UI 구성과 버튼 배치를 설정하는 함수입니다.
        """
        # 디스플레이 설정
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)  # 입력 불가
        self.display.setFixedHeight(60)
        self.display.setFont(QFont("Arial", 24))

        # 버튼 레이아웃
        buttons = [
            ['7', '8', '9', '/', 'sin', 'cos'],
            ['4', '5', '6', '*', 'tan', 'sinh'],
            ['1', '2', '3', '-', 'cosh', 'tanh'],
            ['0', '.', '=', '+', 'x²', 'x³'],
            ['(', ')', 'C', 'pi', '%', 'MC']
        ]

        grid = QGridLayout()
        row = 0
        for btn_row in buttons:
            col = 0
            for btn_text in btn_row:
                button = QPushButton(btn_text)
                button.setFont(QFont("Arial", 14))
                button.setFixedSize(60, 60)
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
        버튼 클릭에 따라 해당 값을 화면에 누적하여 표시합니다.
        """
        sender = self.sender()
        btn_text = sender.text()

        if btn_text == 'C':  # 계산기 초기화
            self.display.clear()
        elif btn_text == '=':  # 계산 결과 출력
            self.calculate_result()
        elif btn_text == 'pi':  # 원주율 출력
            self.display.setText(str(self.calc.pi()))
        elif btn_text == 'x²':  # 제곱
            current_text = self.display.text()
            self.display.setText(str(self.calc.square(float(current_text))))
        elif btn_text == 'x³':  # 세제곱
            current_text = self.display.text()
            self.display.setText(str(self.calc.cube(float(current_text))))
        elif btn_text == 'MC':  # 메모리 초기화
            self.calc.result = 0
        else:
            # 숫자 및 연산자 버튼은 화면에 누적
            current_text = self.display.text()
            new_text = current_text + btn_text
            self.display.setText(new_text)

    def calculate_result(self):
        """
        입력된 수식을 계산하고 결과를 출력하는 함수입니다.
        """
        expression = self.display.text()

        try:
            # eval()을 사용하여 수식 계산
            result = eval(expression, {"__builtins__": None}, {"sin": self.calc.sin, "cos": self.calc.cos, 
                                                              "tan": self.calc.tan, "sinh": self.calc.sinh, 
                                                              "cosh": self.calc.cosh, "tanh": self.calc.tanh,
                                                              "pi": self.calc.pi, "x²": self.calc.square,
                                                              "x³": self.calc.cube})
            self.display.setText(f"{result:.6f}".rstrip('0').rstrip('.'))
        except Exception as e:
            # 계산 중 오류가 발생하면 "Error" 메시지 출력
            self.display.setText("Error")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc_ui = EngineeringCalculatorUI()
    calc_ui.show()
    sys.exit(app.exec())
