import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit
from PyQt6 import uic
import os

class EngineeringCalculator(QMainWindow):
    """
    공학용 계산기 애플리케이션 클래스입니다.
    """
    def __init__(self):
        super().__init__()

        # Qt Designer에서 생성한 UI 파일(caculator.ui)을 로드합니다.
        uic.loadUi("caculator.ui", self)
        
        # 디스플레이 역할을 하는 QLineEdit 위젯에 대한 참조를 저장합니다.
        self.display = self.findChild(QLineEdit, "led")

        # 모든 버튼에 대한 클릭 이벤트를 연결합니다.
        self.connect_buttons()

    def connect_buttons(self):
        """
        UI 파일의 모든 버튼을 기능과 연결합니다.
        """
        # 숫자 및 소수점 버튼 연결
        number_buttons = [
            self.btn_0, self.btn_1, self.btn_2, self.btn_3, self.btn_4,
            self.btn_5, self.btn_6, self.btn_7, self.btn_8, self.btn_9,
            self.btn_decimal
        ]
        for button in number_buttons:
            button.clicked.connect(lambda _, text=button.text(): self.append_to_display(text))
            
        # 연산자 버튼 연결
        operator_buttons = [
            self.btn_plus, self.btn_minus, self.btn_multiply, self.btn_divide,
            self.btn_percent
        ]
        for button in operator_buttons:
            button.clicked.connect(lambda _, text=button.text(): self.append_to_display(text))

        # 공학용 함수 및 기타 버튼 연결
        engineering_buttons = [
            self.btn_open_paren, self.btn_close_paren, self.btn_x_squared,
            self.btn_x_cubed, self.btn_x_power_y, self.btn_e_power_x,
            self.btn_10_power_x, self.btn_1_over_x, self.btn_2_root_x,
            self.btn_3_root_x, self.btn_y_root_x, self.btn_ln, self.btn_log10,
            self.btn_x_factorial, self.btn_sin, self.btn_cos, self.btn_tan,
            self.btn_e, self.btn_ee, self.btn_rand, self.btn_sinh, self.btn_cosh,
            self.btn_tanh, self.btn_pi, self.btn_rad, self.btn_plus_minus
        ]
        for button in engineering_buttons:
            button.clicked.connect(lambda _, text=button.text(): self.append_to_display(text))
            
        # 특수 기능 버튼 연결
        self.btn_backspace.clicked.connect(self.backspace)
        self.btn_ac.clicked.connect(self.clear_display)
        self.btn_equals.clicked.connect(self.equals) # 과제 요구사항에 따라 기능은 없지만 이벤트만 연결
        self.btn_mc.clicked.connect(self.clear_memory)
        self.btn_m_plus.clicked.connect(self.add_to_memory)
        self.btn_m_minus.clicked.connect(self.subtract_from_memory)
        self.btn_mr.clicked.connect(self.recall_memory)
        self.btn_2nd.clicked.connect(self.toggle_2nd_function)
        #self.btn_mode.clicked.connect(self.change_mode)
        
    def append_to_display(self, text):
        """
        버튼의 텍스트를 디스플레이에 추가합니다.
        """
        current_text = self.display.text()
        # sin, cos, tan 같은 함수 버튼은 괄호를 추가하여 함수형태로 표시합니다.
        if text in ['sin', 'cos', 'tan', 'sinh', 'cosh', 'tanh', 'ln', 'log₁₀']:
            self.display.setText(current_text + text + '(')
        else:
            self.display.setText(current_text + text)

    def backspace(self):
        """
        디스플레이의 마지막 글자를 지웁니다.
        """
        current_text = self.display.text()
        self.display.setText(current_text[:-1])

    def clear_display(self):
        """
        디스플레이의 모든 텍스트를 지웁니다.
        """
        self.display.clear()

    # 다음은 과제 요구사항에 따라 빈 함수로 남겨둔 기능들입니다.
    def equals(self):
        # '=' 버튼 클릭 시 아무것도 하지 않습니다.
        pass

    def clear_memory(self):
        pass
    
    def add_to_memory(self):
        pass

    def subtract_from_memory(self):
        pass

    def recall_memory(self):
        pass

    def toggle_2nd_function(self):
        pass

if __name__ == '__main__':
    # 스크립트 실행 시 작업 디렉터리를 스크립트가 있는 디렉터리로 변경합니다.
    os.chdir(os.path.dirname(__file__))
    app = QApplication(sys.argv)
    window = EngineeringCalculator()
    window.show()
    sys.exit(app.exec())
