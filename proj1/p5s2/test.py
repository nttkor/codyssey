import sys
import math
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QLineEdit, QPushButton, QGridLayout, QVBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt


# 1️⃣ 계산 엔진
class CalculatorEngine:
    def __init__(self):
        self.constants = {'π': math.pi, 'e': math.e}
        self.functions = {
            'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
            'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
            'ln': math.log, 'log': math.log10, '√': math.sqrt, 'x!': math.factorial
        }

    def evaluate(self, expression):
        try:
            # 상수 치환
            for key, val in self.constants.items():
                expression = expression.replace(key, f'({val})')
            # 함수 처리
            for func in self.functions:
                if func in expression:
                    expression = expression.replace(func, f'self.functions["{func}"]')
            result = eval(expression)
            return result
        except Exception as e:
            return f"Error: {e}"


# 2️⃣ 입력 처리
class InputHandler:
    def __init__(self, display: QLineEdit, engine: CalculatorEngine):
        self.display = display
        self.engine = engine

    def append(self, text):
        self.display.setText(self.display.text() + text)

    def clear(self):
        self.display.clear()

    def delete(self):
        self.display.setText(self.display.text()[:-1])

    def calculate(self):
        expr = self.display.text()
        result = self.engine.evaluate(expr)
        self.display.setText(str(result))


# 3️⃣ UI 메인 윈도우
class CalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("공학용 계산기")
        self.setFixedSize(400, 500)

        self.engine = CalculatorEngine()
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.input_handler = InputHandler(self.display, self.engine)

        self._create_ui()
        self.show()

    def _create_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout()
        central.setLayout(main_layout)

        main_layout.addWidget(self.display)

        grid = QGridLayout()
        main_layout.addLayout(grid)

        buttons = [
            ['7', '8', '9', '/', 'AC'],
            ['4', '5', '6', '*', 'DEL'],
            ['1', '2', '3', '-', '('],
            ['0', '.', '=', '+', ')'],
            ['sin', 'cos', 'tan', 'π', 'e'],
            ['ln', 'log', '√', '^', 'x!']
        ]

        for r, row in enumerate(buttons):
            for c, btn_text in enumerate(row):
                btn = QPushButton(btn_text)
                btn.setFixedSize(70, 50)
                btn.clicked.connect(self._on_button_click)
                grid.addWidget(btn, r, c)

    def _on_button_click(self):
        sender = self.sender().text()
        if sender == 'AC':
            self.input_handler.clear()
        elif sender == 'DEL':
            self.input_handler.delete()
        elif sender == '=':
            self.input_handler.calculate()
        else:
            if sender == '^':
                sender = '**'  # 파이썬 지수 연산자
            self.input_handler.append(sender)


# 4️⃣ 실행
if __name__ == "__main__":
    app = QApplication(sys.argv)
    calc = CalculatorApp()
    sys.exit(app.exec())
