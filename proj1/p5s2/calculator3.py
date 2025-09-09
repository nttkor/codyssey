# app.py
import sys, os, re
from pathlib import Path

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


def find_ui_path(name: str) -> str:
    """
    name: 'engineering.ui' or 'caculator.ui'
    1) 스크립트 폴더, 2) 현재 작업폴더, 3) /mnt/data 순서로 탐색
    """
    cand = [
        Path(__file__).parent / name,
        Path(os.getcwd()) / name,
        Path("/mnt/data") / name,
    ]
    for p in cand:
        if p.exists():
            return str(p)
    raise FileNotFoundError(f"UI not found: {name} (searched: {', '.join(map(str, cand))})")


class UIWindow(QMainWindow):
    """단순 UI 로더. led/QPushButton을 찾아 쓰기 좋게 보조 기능만 제공."""
    def __init__(self, ui_path: str):
        super().__init__()
        uic.loadUi(ui_path, self)
        self.ui_path = ui_path

        # led 찾기(우선 objectName='led', 아니면 첫 QLineEdit)
        self.led = getattr(self, "led", None)
        if self.led is None:
            qles = self.findChildren(QLineEdit)
            self.led = qles[0] if qles else None

        # led 기본 속성
        if self.led is not None:
            self.led.setReadOnly(True)
            self.led.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        # 모든 버튼 수집
        self.all_buttons: list[QPushButton] = self.findChildren(QPushButton)

    def find_mode_button(self) -> QPushButton | None:
        # 1) objectName 최우선
        for b in self.all_buttons:
            if b.objectName().lower() == "btn_mode":
                return b
        # 2) 텍스트로 추정 (mode)
        for b in self.all_buttons:
            if "mode" in b.text().lower():
                return b
        return None


class AppController:
    """
    - expression_buffer 문자열로 '표시만' 누적
    - engineering/basic 두 창을 만들고 show/hide 전환
    - 버튼 → 토큰 매핑: 숫자/연산자/함수/공학키를 가능한 한 자동 규칙으로 처리
    """
    def __init__(self):
        self.expression_buffer = ""

        # UI 로드
        self.ui_engineering = UIWindow(find_ui_path("engineering.ui"))
        self.ui_basic = UIWindow(find_ui_path("caculator.ui"))

        # 시작 모드는 engineering
        self.current = self.ui_engineering
        self.other = self.ui_basic
        self._apply_display("0")  # 초기 표시

        # 버튼 연결
        self._wire_window(self.ui_engineering)
        self._wire_window(self.ui_basic)

        # 모드 버튼
        self._connect_mode_button(self.ui_engineering)
        self._connect_mode_button(self.ui_basic)

        # 기본 창 표시
        self.ui_engineering.show()

    # -----------------------
    # 표시/폰트
    # -----------------------
    def _apply_display(self, text: str):
        if self.current.led is None:
            return
        if not text:
            text = "0"
        self.current.led.setText(text)
        self._fit_font(text)

    def _fit_font(self, text: str):
        # 길이에 따라 폰트 크기 동적 조절 (최소 12pt)
        length = max(1, len(text))
        if length <= 10:
            size = 48
        else:
            size = max(12, min(48, int(480 / length)))
        font = QFont()
        font.setBold(True)
        font.setPointSize(size)
        self.current.led.setFont(font)

    # -----------------------
    # 모드 전환
    # -----------------------
    def toggle_mode(self):
        # 현재 창 숨기고, 반대 창 보여주기 + 버퍼 동기화
        self.current.hide()
        self.current, self.other = self.other, self.current
        # 새 창에 버퍼 반영
        self._apply_display(self.expression_buffer if self.expression_buffer else "0")
        self.current.show()
        self.current.activateWindow()

    def _connect_mode_button(self, window: UIWindow):
        btn = window.find_mode_button()
        if btn:
            btn.clicked.connect(self.toggle_mode)

    # -----------------------
    # 버튼 연결
    # -----------------------
    def _wire_window(self, window: UIWindow):
        # 특수키 식별(객체명과 라벨 모두 사용)
        for b in window.all_buttons:
            name = b.objectName().lower()
            text = b.text().strip()

            # Mode는 따로 연결하므로 skip
            if name == "btn_mode" or "mode" in text.lower():
                continue

            # AC / Clear류
            if name.startswith("btn_ac") or text in {"AC", "C", "CE"}:
                b.clicked.connect(self.on_ac)
                continue

            # Backspace
            if "back" in name or text in {"⌫", "Back", "Backspace"}:
                b.clicked.connect(self.on_backspace)
                continue

            # =
            if text == "=" or name.endswith("equals"):
                b.clicked.connect(self.on_equal)
                continue

            # 일반 키: 토큰 생성 → on_token
            token = self._token_from_button(text, name)
            if token is not None:
                b.clicked.connect(lambda _=False, t=token: self.on_token(t))
            else:
                # 토큰 미매핑: 버튼 라벨 그대로 추가(표시만 목적이므로)
                b.clicked.connect(lambda _=False, t=text: self.on_token(t))

    # -----------------------
    # 토큰 규칙
    # -----------------------
    _func_like = {
        "sin", "cos", "tan", "sinh", "cosh", "tanh",
        "asin", "acos", "atan",
        "ln", "log", "log10", "rand", "abs",
    }

    _exact_map = {
        # 공학 특수
        "x²": "^2",
        "x³": "^3",
        "x^y": "^",
        "e^x": "e^",
        "10^x": "10^",
        "1/x": "1/(",
        "√x": "√(",
        "²√x": "2√(",
        "2√x": "2√(",
        "³√x": "3√(",
        "3√x": "3√(",
        "y√x": "√(",
        "x!": "!",
        # 상수/표식
        "π": "π",
        "e": "e",
        "+/-": "±",
        "±": "±",
        "%": "%",
        "(": "(",
        ")": ")",
        "+": "+",
        "-": "-",
        "/": "/",
        ".": ".",
        "×": "×",   # 곱 기호가 ×인 경우
        "X": "X",   # 곱 기호가 X인 경우
    }

    _simple_chars = set("0123456789+-/*().%")

    def _normalize_log_label(self, text: str) -> str:
        # log, log10, log₁₀ → log10 로 정규화
        t = text.lower()
        t = t.replace("log₁₀", "log10")
        return t

    def _token_from_button(self, text: str, object_name: str) -> str | None:
        # 1) 완전 일치 매핑
        if text in self._exact_map:
            return self._exact_map[text]

        # 2) 숫자/기본 기호
        if all(ch in self._simple_chars for ch in text) and len(text) == 1:
            return text

        # 3) 함수형 추정: (라벨이 영문/함수패턴) → "name("
        norm = self._normalize_log_label(text)
        # 알파/숫자/밑줄/지수 표기를 뺀 클린 문자열
        id_like = re.sub(r"[^a-z0-9_]", "", norm)
        if id_like in self._func_like:
            return f"{id_like}("

        # 4) 'deg/rad' 등은 버퍼 오염 방지를 위해 None 반환(표시만 하고 싶으면 여기서 문자열 지정)
        if id_like in {"deg", "rad"}:
            return None

        # 5) 나머지는 버튼 텍스트를 그대로(표시 목적)
        return text

    # -----------------------
    # 핸들러
    # -----------------------
    def on_token(self, token: str):
        self.expression_buffer += token
        self._apply_display(self.expression_buffer)

    def on_ac(self):
        self.expression_buffer = ""
        self._apply_display("0")

    def on_backspace(self):
        if self.expression_buffer:
            self.expression_buffer = self.expression_buffer[:-1]
        self._apply_display(self.expression_buffer if self.expression_buffer else "0")

    def on_equal(self):
        # 계산은 하지 않고 '='만 누적
        self.expression_buffer += "="
        self._apply_display(self.expression_buffer)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ctrl = AppController()
    sys.exit(app.exec())
