import sys, os
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt

# 실행 디렉토리 고정
os.chdir(os.path.dirname(__file__))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("engineering.ui", self)

        self._connect_signals()
        self.setFixedSize(self.size())  # 윈도우 크기 고정

    def _connect_signals(self):
        """
        버튼 이름 → 입력 텍스트 매핑
        """
        button_map = {
            # 숫자 버튼
            "btn_0": "0", "btn_1": "1", "btn_2": "2", "btn_3": "3",
            "btn_4": "4", "btn_5": "5", "btn_6": "6",
            "btn_7": "7", "btn_8": "8", "btn_9": "9",

            # 사칙연산
            "btn_plus": "+", "btn_minus": "-",
            "btn_mul": "*", "btn_div": "/",

            # 괄호, 소수점, 등호
            "btn_open_paren": "(", "btn_close_paren": ")",
            "btn_decimal": ".", "btn_equals": "=",

            # 부호, EE, 상수
            "btn_plus_minus": "+/-", "btn_ee": "EE",
            "btn_pi": "π", "btn_e": "e",

            # 제곱/루트
            "btn_x_squared": "x²", "btn_x_cubed": "x³",
            "btn_x_power_y": "x^y", "btn_2_root_x": "√",
            "btn_3_root_x": "∛", "btn_y_root_x": "y√x",

            # 로그
            "btn_log10": "log", "btn_ln": "ln",
            "btn_10_power_x": "10^x", "btn_e_power_x": "e^x",

            # 삼각함수
            "btn_sin": "sin", "btn_cos": "cos", "btn_tan": "tan",
            "btn_sinh": "sinh", "btn_cosh": "cosh", "btn_tanh": "tanh",

            # 역삼각함수
            "btn_asin": "asin", "btn_acos": "acos", "btn_atan": "atan",

            # 팩토리얼
            "btn_x_factorial": "x!",

            # 메모리 기능
            "btn_mc": "MC", "btn_mr": "MR", "btn_m_plus": "M+", "btn_m_minus": "M-",

            # 기타
            "btn_mode": "mode", "btn_clear": "C", "btn_del": "DEL"
        }

        for btn_name, text in button_map.items():
            btn = getattr(self, btn_name, None)
            if btn:
                btn.clicked.connect(lambda _, t=text: self.append_text(t))

    def append_text(self, text: str):
        """
        출력창에 글자 추가 (계산은 이후 구현)
        """
        current = self.le_display.text()  # 수정된 ID 반영
        self.le_display.setText(current + text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
