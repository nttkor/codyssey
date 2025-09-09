import sys
import os
import math
import random
import re
from typing import Optional

from PyQt6 import uic
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QLineEdit,
    QPushButton,
)

# ---------------------------
# Calculator (기본) / EngineeringCalculator (상속)
# ---------------------------
class Calculator(QMainWindow):
    def __init__(self, ui_path: str = "calculator.ui"):
        super().__init__()
        # 별도의 스타일링 코드 없이 UI 파일로만 그리기
        uic.loadUi(ui_path, self)

        # LED 찾기 (ui에서 어떤 이름이라도 상관없게 자동 선택)
        self.led: QLineEdit = self._find_led()
        self.led.setReadOnly(True)

        # 상태
        self.memory = 0.0
        self.history: list[str] = []         # '=' 했던 수식들을 저장
        self.history_index: Optional[int] = None
        self.new_input = True                # 새 입력이면 화면 자동 클리어
        self.angle_mode = "rad"              # 'rad' 또는 'deg'

        # 버튼 자동 매핑 (모든 QPushButton을 찾아서 text()로 라우팅)
        self._map_buttons()

    # UI에서 QLineEdit을 찾아 반환
    def _find_led(self) -> QLineEdit:
        # 우선 흔한 이름들 체크
        for name in ("led", "LED", "display", "displayLineEdit"):
            if hasattr(self, name):
                widget = getattr(self, name)
                if isinstance(widget, QLineEdit):
                    return widget
        # fallback: 첫 번째 QLineEdit 자식
        qles = self.findChildren(QLineEdit)
        if qles:
            return qles[0]
        raise RuntimeError("LED(QLineEdit)를 찾을 수 없습니다. UI에 QLineEdit 하나를 추가하세요.")

    # 모든 QPushButton을 찾아서 text()를 key로 button_clicked에 연결
    def _map_buttons(self):
        buttons = self.findChildren(QPushButton)
        if not buttons:
            print("경고: 버튼을 찾지 못했습니다. UI에 QPushButton이 있어야 합니다.")
        for btn in buttons:
            text = btn.text()
            # lambda에서 기본값으로 text를 바인딩 (루프 변수 캡쳐 문제 방지)
            btn.clicked.connect(lambda checked=False, t=text: self.button_clicked(t))

    # 버튼 클릭 라우터
    def button_clicked(self, key: str):
        # '<-'이 아닌 버튼을 누르면 history 인덱스는 리셋
        if key != "<-":
            self.history_index = None

        # 즉시 처리되는 키들
        if key == "=":
            self.calculate()
            return

        if key == "<-":
            # 이전 수식 보여주기 (history에서 최근 순으로)
            if not self.history:
                QMessageBox.information(self, "Info", "이전 수식이 없습니다.")
                return
            if self.history_index is None:
                self.history_index = 0
            else:
                if self.history_index < len(self.history) - 1:
                    self.history_index += 1
            expr = self.history[-1 - self.history_index]
            self.led.setText(expr)
            self.new_input = True
            return

        # 메모리 기능
        if key == "mc":
            self.memory = 0.0
            return
        if key == "m+":
            try:
                val = self._eval_display_as_number()
                self.memory += val
            except Exception as e:
                QMessageBox.warning(self, "Memory Error", f"메모리에 더할 수 없습니다:\n{e}")
            return
        if key == "m-":
            try:
                val = self._eval_display_as_number()
                self.memory -= val
            except Exception as e:
                QMessageBox.warning(self, "Memory Error", f"메모리에서 뺄 수 없습니다:\n{e}")
            return
        if key == "mr":
            self.led.setText(self._format_number(self.memory))
            self.new_input = True
            return

        # 각도 모드 토글 (Rad <-> Deg). 버튼 텍스트가 'Rad'이면 'Deg'로 바뀌게 처리
        if key in ("Rad", "Deg"):
            self.angle_mode = "deg" if self.angle_mode == "rad" else "rad"
            # 버튼 표시도 바꿔준다 (있다면)
            self._set_button_text("Rad" if self.angle_mode == "rad" else "Deg",
                                  "Deg" if self.angle_mode == "rad" else "Rad")
            QMessageBox.information(self, "Angle Mode", f"각도 모드: {self.angle_mode}")
            return

        if key == "Mode":
            # 과제 범위 내에서는 Mode 동작을 구현하지 않음 (필요하면 여기에 추가)
            QMessageBox.information(self, "Mode", "Mode 버튼이 눌렸습니다.")
            return

        if key == "+/-":
            self._toggle_sign()
            return

        # 즉시 연산을 적용하는 단항 연산자들 (현재 화면의 값에 바로 적용)
        if key in ("x²", "x³", "1/x", "x!", "2√x", "3√x", "e^x", "10^x"):
            try:
                res = self._apply_unary_operator(key)
                self.led.setText(self._format_number(res))
                self.new_input = True
                # 수식 기록: 저장할 때는 문자열 수식이 아닌, 기존 표현을 기록해둔다.
                # (과제에서 '<-'로 이전 수식 보여주기 의도를 위해)
                # 여기서는 계산 전의 표현을 히스토리에 추가하지 않음.
            except Exception as e:
                QMessageBox.critical(self, "Error", f"연산 실패: {e}")
            return

        # 새 입력이면 화면을 지운다 (요구사항: '<-' 아닌 새로운 수식이 들어오면 전체 지우기)
        if self.new_input:
            self.led.clear()
            self.new_input = False

        # 기본 삽입 규칙 (숫자, 연산자, 함수 괄호 등)
        insertion = self._map_key_to_insert(key)
        if insertion is not None:
            self.led.insert(insertion)

    # 버튼 텍스트 바꿔주는 헬퍼 (Rad<->Deg 텍스트 교체 등)
    def _set_button_text(self, find_text: str, replace_text: str):
        for btn in self.findChildren(QPushButton):
            if btn.text() == find_text:
                btn.setText(replace_text)
                break

    # 마지막 숫자(또는 전체 화면)를 float로 평가
    def _eval_display_as_number(self) -> float:
        txt = self.led.text().strip()
        if txt == "":
            return 0.0
        val = self._safe_eval(txt)
        if not isinstance(val, (int, float)):
            raise ValueError("숫자가 아닙니다.")
        return float(val)

    # 단항 연산 (화면에 보이는 값을 바로 처리)
    def _apply_unary_operator(self, key: str):
        val = self._eval_display_as_number()
        if key == "x²":
            return val ** 2
        if key == "x³":
            return val ** 3
        if key == "1/x":
            if val == 0:
                raise ZeroDivisionError("0으로 나눌 수 없습니다.")
            return 1.0 / val
        if key == "x!":
            if val < 0 or int(val) != val:
                raise ValueError("정수 >= 0인 값만 팩토리얼 가능")
            return math.factorial(int(val))
        if key == "2√x":
            if val < 0:
                raise ValueError("음수의 제곱근은 실수 범위를 벗어납니다.")
            return val ** (1 / 2)
        if key == "3√x":
            return math.copysign(abs(val) ** (1 / 3), val)
        if key == "e^x":
            return math.exp(val)
        if key == "10^x":
            return 10 ** val
        raise NotImplementedError(key)

    # 키 -> 삽입 문자열 매핑 (함수는 '(' 포함해 삽입)
    def _map_key_to_insert(self, key: str) -> Optional[str]:
        m = {
            "π": "pi",
            "pi": "pi",
            "e": "e",
            "(": "(",
            ")": ")",
            "+": "+",
            "-": "-",
            "*": "*",
            "/": "/",
            ".": ".",
            "%": "/100",       # 간단 처리: 뒤에 붙이면 %로 간주
            "0": "0", "1": "1", "2": "2", "3": "3", "4": "4",
            "5": "5", "6": "6", "7": "7", "8": "8", "9": "9",
            "sin": "sin(",
            "cos": "cos(",
            "tan": "tan(",
            "sinh": "sinh(",
            "cosh": "cosh(",
            "tanh": "tanh(",
            "ln": "log(",
            "log₁₀": "log10(",
            "Rand": "random()",
            "EE": "e",   # 간단표현 (정교한 EE 입력은 별도 구현 필요)
            "^": "**",
            "x^y": "**",
        }
        return m.get(key, key)

    # 수식 평가 (안전한 eval)
    def _safe_eval(self, expr: str):
        # 허용된 네임스페이스 구성 (각도 모드 반영)
        env = {
            "pi": math.pi,
            "e": math.e,
            "abs": abs,
            "sqrt": math.sqrt,
            "log": math.log,
            "log10": math.log10,
            "factorial": math.factorial,
            "exp": math.exp,
            "random": random.random,
        }

        # 삼각함수: 각도 모드에 따라 래핑
        if self.angle_mode == "rad":
            env.update({
                "sin": math.sin,
                "cos": math.cos,
                "tan": math.tan,
                "sinh": math.sinh,
                "cosh": math.cosh,
                "tanh": math.tanh,
            })
        else:  # deg
            env.update({
                "sin": lambda x: math.sin(math.radians(x)),
                "cos": lambda x: math.cos(math.radians(x)),
                "tan": lambda x: math.tan(math.radians(x)),
                "sinh": math.sinh,
                "cosh": math.cosh,
                "tanh": math.tanh,
            })

        # 안전하게 eval: __builtins__ 제거
        try:
            # 작은 전처리: 쉼표(,)를 사용한 함수 인수 구분은 그대로 허용됨
            # 허용되지 않은 문자(예: 알파벳+숫자 조합 외 특수조작)는 eval이 알아서 에러를 냄
            result = eval(expr, {"__builtins__": None}, env)
        except ZeroDivisionError:
            raise
        except OverflowError:
            raise
        except Exception as e:
            # 재가공해서 상위에서 메시지 보여주도록 던짐
            raise ValueError(str(e))
        return result

    # '=' 눌렀을 때 계산
    def calculate(self):
        expr = self.led.text().strip()
        if expr == "":
            return
        # 저장: 사용자가 = 누르기 전 수식을 히스토리에 남김
        self.history.append(expr)
        try:
            val = self._safe_eval(expr)
            # 표현 형식 정리
            out = self._format_number(val)
            self.led.setText(out)
        except ZeroDivisionError:
            QMessageBox.critical(self, "Error", "0으로 나눌 수 없습니다.")
            self.led.setText("Error")
        except OverflowError:
            QMessageBox.critical(self, "Error", "숫자 범위(오버플로우)를 벗어났습니다.")
            self.led.setText("Error")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"잘못된 수식입니다:\n{e}")
            self.led.setText("Error")
        finally:
            self.new_input = True

    # 표시할 숫자 포맷: 정수면 int 형태로, 아니면 소수
    def _format_number(self, val):
        try:
            if isinstance(val, float) and val.is_integer():
                return str(int(val))
            return str(val)
        except Exception:
            return str(val)

    # +/- 토글: 마지막 피연산자(또는 전체 숫자)에 대해 부호 변경
    def _toggle_sign(self):
        s = self.led.text()
        if not s:
            self.led.setText("-")
            return
        # 마지막 연산자 위치 찾기
        m = max(s.rfind(op) for op in ["+", "-", "*", "/"])
        if m == -1:
            # 전체를 토글
            if s.startswith("-"):
                self.led.setText(s[1:])
            else:
                self.led.setText("-" + s)
        else:
            prefix = s[: m + 1]
            token = s[m + 1 :]
            # 이미 (-x) 형태면 풀어서 넣기
            if token.startswith("(-") and token.endswith(")"):
                token = token[2:-1]
            elif token.startswith("-"):
                token = token[1:]
            else:
                token = f"(-{token})"
            self.led.setText(prefix + token)

# 공학용 계산기: 현재는 Calculator 기능 전부 포함. 요구사항에 따라 추가 메소드 구현 가능.
class EngineeringCalculator(Calculator):
    def __init__(self, ui_path: str = "calculator.ui"):
        super().__init__(ui_path)
        # 추가 초기화가 필요하면 여기에 구현
        # (ex: 30가지 기능 목록을 메소드로 만들고 매핑)

# ---------------------------
# 실행
# ---------------------------
if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    app = QApplication(sys.argv)
    win = EngineeringCalculator("calculator.ui")
    win.show()
    sys.exit(app.exec())
