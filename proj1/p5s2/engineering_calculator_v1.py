import sys, os
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt
import math

os.chdir(os.path.dirname(__file__))

# ------------------- 기본 계산기 -------------------
class Calculator:
    def __init__(self):
        self.reset()

    def reset(self):
        self.num = ""      # 현재 입력 문자열
        self.op1 = None     # 첫 번째 피연산자
        self.op2 = None     # 두 번째 피연산자
        self.operator = None
        self.result = None

    def evaluate(self, expr: str):
        """입력 문자열(expr)을 안전하게 계산"""
        try:
            # eval 사용: 안전하게 숫자, + - * / ( ) 만 허용
            allowed_chars = "0123456789.+-*/()eπ"
            for ch in expr:
                if ch not in allowed_chars:
                    return "Math Error"
            # π, e 치환
            expr = expr.replace("π", str(math.pi)).replace("e", str(math.e))
            result = eval(expr)
            return round(result, 12)
        except ZeroDivisionError:
            return "Math Error"
        except OverflowError:
            return "Overflow"
        except Exception:
            return "Math Error"

# ------------------- 공학용 계산기 -------------------
class EngineeringCalculator(Calculator):
    def __init__(self):
        super().__init__()
        self.memory = 0.0

    # 삼각함수
    def calc_func(self, func_name, x):
        try:
            mapping = {
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "sinh": math.sinh,
                "cosh": math.cosh,
                "tanh": math.tanh,
            }
            return mapping[func_name](x)
        except:
            return "Math Error"

    # 제곱 / 세제곱 / 상수
    def square(self, x): return x**2
    def cube(self, x): return x**3
    def get_pi(self): return math.pi
    def get_e(self): return math.e

    # 메모리
    def memory_clear(self): self.memory = 0.0
    def memory_recall(self): return self.memory
    def memory_add(self, x): self.memory += x
    def memory_subtract(self, x): self.memory -= x

# ------------------- UI 연동 -------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("engineering.ui", self)
        self.calc = EngineeringCalculator()
        self._connect_signals()
        self.setFixedSize(self.size())

    def _connect_signals(self):
        button_map = {
            "btn_0":"0","btn_1":"1","btn_2":"2","btn_3":"3","btn_4":"4","btn_5":"5",
            "btn_6":"6","btn_7":"7","btn_8":"8","btn_9":"9",
            "btn_plus":"+","btn_minus":"-","btn_mul":"*","btn_div":"/",
            "btn_decimal":".","btn_equals":"=",
            "btn_plus_minus":"+/-","btn_pi":"π",
            "btn_x_squared":"x²","btn_x_cubed":"x³",
            "btn_sin":"sin","btn_cos":"cos","btn_tan":"tan",
            "btn_sinh":"sinh","btn_cosh":"cosh","btn_tanh":"tanh",
            "btn_mc":"MC","btn_mr":"MR","btn_m_plus":"M+","btn_m_minus":"M-",
            "btn_clear":"C","btn_del":"DEL"
        }

        for btn_name, text in button_map.items():
            btn = getattr(self, btn_name, None)
            if btn:
                btn.clicked.connect(lambda _, t=text: self.button_pressed(t))

    def button_pressed(self, text):
        try:
            if text in "0123456789.()+-*/":
                self.calc.num += text
                self.le_display.setText(self.calc.num)

            elif text == "C":
                self.calc.reset()
                self.le_display.setText("")

            elif text == "DEL":
                self.calc.num = self.calc.num[:-1]
                self.le_display.setText(self.calc.num)

            elif text == "+/-":
                # 마지막 숫자 토글
                import re
                nums = re.findall(r"[-]?\d+\.?\d*", self.calc.num)
                if nums:
                    last = nums[-1]
                    toggled = last[1:] if last.startswith('-') else '-' + last
                    self.calc.num = self.calc.num[:-len(last)] + toggled
                    self.le_display.setText(self.calc.num)

            elif text == "π":
                self.calc.num += "π"
                self.le_display.setText(self.calc.num)

            elif text == "x²":
                self.calc.num += "**2"
                self.le_display.setText(self.calc.num)

            elif text == "x³":
                self.calc.num += "**3"
                self.le_display.setText(self.calc.num)

            elif text in ["sin","cos","tan","sinh","cosh","tanh"]:
                # 입력창 숫자에 함수 적용
                self.calc.num = f"{text}({self.calc.num})"
                self.le_display.setText(self.calc.num)

            elif text == "=":
                expr = self.calc.num
                # 함수 계산 처리
                for f in ["sin","cos","tan","sinh","cosh","tanh"]:
                    if f in expr:
                        import re
                        matches = re.findall(f"{f}\((.*?)\)", expr)
                        for m in matches:
                            val = float(self.calc.evaluate(m))
                            res = self.calc.calc_func(f, val)
                            expr = expr.replace(f"{f}({m})", str(res))
                result = self.calc.evaluate(expr)
                self.le_display.setText(str(result))
                self.calc.num = str(result)

            # 메모리
            elif text == "MC":
                self.calc.memory_clear()
            elif text == "MR":
                self.calc.num += str(self.calc.memory_recall())
                self.le_display.setText(self.calc.num)
            elif text == "M+":
                self.calc.memory_add(float(self.calc.evaluate(self.calc.num)))
            elif text == "M-":
                self.calc.memory_subtract(float(self.calc.evaluate(self.calc.num)))

        except Exception:
            self.le_display.setText("Math Error")

# ------------------- 실행 -------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
