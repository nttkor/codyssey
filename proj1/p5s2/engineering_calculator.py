# ================================================================
# Engineering Calculator (문제 3: UI 입력 누적 / 문제 4 확장 준비)
# ================================================================
# [코드 원리]
# 1) PyQt6로 engineering.ui를 런타임 로드한다.
# 2) 버튼 배선은 두 단계로 처리한다.
#    (a) "라벨과 표시 토큰이 달라야 하는 예외"만 우선 하드코딩(bind_tok)
#        → 처리한 버튼은 handled 집합에 기록
#    (b) 그 외 모든 버튼은 라벨(text) 기반 자동 바인딩
#        - 함수 라벨(알파벳 시작 또는 'log₁₀')은 자동으로 '('를 덧붙임
#        - 숫자/기본 기호/괄호/점/등호는 라벨 그대로 토큰으로 누적
#        - EE 등 특수라도 라벨=토큰이면 그대로 사용
#        - mode/rad/2nd는 일단 pass
#        - Backspace는 핸들러 연결
# 3) '='은 현재(문제 3) 계산하지 않고 문자열 '='만 누적한다.
#    문제 4에서는 evaluate()와 연결하여 실제 계산으로 전환한다.
#
# [예외 목록 (ID → 토큰)]
# - btn_x_factorial → '!'
# - btn_x_squared   → '^2'
# - btn_x_cubed     → '^3'
# - btn_x_power_y   → '^'
# - btn_1_over_x    → '1/('
# - btn_2_root_x    → '√('
# - btn_3_root_x    → '∛('
# - btn_y_root_x    → 'y√x'   (표시만; 문제 4 파서에서 해석)
# - btn_10_power_x  → '10^('
# - btn_e_power_x   → 'e^('
#
# [자동 규칙 요약]
# - 함수라벨: 'sin' → 'sin(', 'Rand' → 'Rand(', 'log₁₀' → 'log₁₀('
# - 기본기호/숫자/괄호/점/등호: 라벨 그대로
# - 곱셈 라벨은 UI가 이미 'X'이므로 예외처리 불필요
# - EE: 라벨 그대로 'EE'
# - Backspace: on_backspace
# - mode/rad/2nd: pass
# - AC는 필요 시 on_clear에 연결(지금은 미사용)
# ================================================================

from __future__ import annotations

from pathlib import Path
from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit


class EngineeringCalculatorWindow(QMainWindow):
    """
    공학용 계산기 메인 윈도우 (문제 3 전용 입력 누적 UI).

    - 예외 매핑을 먼저 바인딩하고, 나머지는 라벨 기반으로 자동 바인딩한다.
    - 디스플레이 objectName은 'le_display'를 사용한다.
    - 표시 문자열 길이에 따라 폰트 크기를 자동으로 줄인다.
    - '='은 지금은 표시만 누적(문자열)한다. 문제 4에서 evaluate로 전환할 수 있다.
    - mode/rad/2nd는 현재 동작하지 않으며 람다 pass로 연결한다.
    """

    def __init__(self) -> None:
        """UI 로드, 디스플레이 초기화, 버튼 배선을 수행한다."""
        super().__init__()
        self._load_ui()
        self._init_display()
        self._wire_buttons()

    # ---------- UI 로드 ----------
    def _load_ui(self) -> None:
        """engineering.ui를 현재 파일과 같은 폴더에서 로드하고 표시창을 획득한다."""
        ui_path = Path(__file__).with_name('engineering.ui')
        self.ui = uic.loadUi(str(ui_path), self)

        self.display: QLineEdit | None = self.findChild(QLineEdit, 'le_display')
        if self.display is None:
            raise RuntimeError('QLineEdit "le_display"를 찾을 수 없습니다.')

        self.display.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.display.setReadOnly(True)

    # ---------- 디스플레이 ----------
    def _init_display(self) -> None:
        """버퍼를 '0'으로 세팅하고 폰트를 적용한다."""
        self._buffer = '0'
        self._apply_auto_font()
        self.display.setText(self._buffer)

    def _apply_auto_font(self) -> None:
        """버퍼 길이에 따라 폰트 크기를 12~48pt 범위에서 자동 조정한다."""
        length = max(1, len(self._buffer))
        size = 48 if length <= 18 else max(12, min(48, 870 // length))
        f = self.display.font() or QFont()
        f.setPointSize(int(size))
        f.setBold(True)
        self.display.setFont(f)

    def _set_text(self, s: str) -> None:
        """디스플레이 문자열을 갱신한다. 빈 문자열이면 '0'으로 대체한다."""
        if not s:
            s = '0'
        self._buffer = s
        self._apply_auto_font()
        self.display.setText(self._buffer)

    # ---------- 라벨 → 토큰 ----------
    @staticmethod
    def _token_from_label(label: str) -> str | None:
        """
        버튼 라벨에서 표시용 토큰을 생성한다. (문제 3: 표시 누적 전용)

        규칙:
        - 숫자/기본 연산/괄호/점/등호: 라벨 그대로
        - 함수(알파벳으로 시작하거나 'log₁₀'): 라벨 + '('
        - 대표 특수 라벨: 소수만 예외 매핑
        - 상수/부호: 그대로
        - 토글(mode/rad/2nd): None (pass)
        """
        t = (label or '').strip()
        if not t:
            return ''

        # 1) 한 글자 기본 토큰: 숫자/연산/괄호/점/등호
        if len(t) == 1 and (t.isdigit() or t in '+-/().%='):
            return t

        # 2) 함수: 알파벳 시작 or 'log₁₀' → label + '('
        if t == 'log₁₀' or t[:1].isalpha():
            return t + '('

        # 3) 대표 특수 라벨
        special = {
            'x²': '^2', 'x³': '^3', 'x^y': '^',
            '1/x': '1/(', '√x': '√(', '2√x': '√(', '3√x': '∛(',
            '10^x': '10^(', 'e^x': 'e^(', 'x!': '!', 'EE': 'EE',
            'y√x': 'y√x',
        }
        if t in special:
            return special[t]

        # 4) 상수/부호
        if t in {'π', 'e', '+/-', '±'}:
            return {'π': 'π', 'e': 'e', '+/-': '±', '±': '±'}[t]

        # 5) 토글류는 pass 처리
        if t.lower() in {'mode', 'rad', '2nd'}:
            return None

        # 6) 그 외: 라벨 그대로
        return t

    # ---------- 버튼 배선 ----------
    def _wire_buttons(self) -> None:
        """
        (1) 예외 케이스를 먼저 하드코딩으로 바인딩하고 handled에 기록한다.
        (2) 남은 버튼은 라벨(text) 기반으로 일괄 바인딩한다.
        """
        handled: set[str] = set()

        def bind(name: str, fn) -> None:
            btn = self.findChild(QPushButton, name)
            if btn:
                btn.clicked.connect(fn)
                handled.add(btn.objectName())

        def bind_tok(name: str, token: str) -> None:
            bind(name, lambda _, t=token: self.on_token(t))

        # ---- (1) 예외: 라벨과 토큰이 달라야 하는 것들 ----
        bind_tok('btn_x_factorial', '!')
        bind_tok('btn_x_squared', '^2')
        bind_tok('btn_x_cubed', '^3')
        bind_tok('btn_x_power_y', '^')
        bind_tok('btn_1_over_x', '1/(')
        bind_tok('btn_2_root_x', '√(')
        bind_tok('btn_3_root_x', '∛(')
        bind_tok('btn_y_root_x', 'y√x')   # 표시만 (문제 4에서 파서 처리)
        bind_tok('btn_10_power_x', '10^(')
        bind_tok('btn_e_power_x', 'e^(')

        # ---- 시스템: 동작 정의 ----
        bind('btn_backspace', self.on_backspace)
        bind('btn_equals',   lambda: self.on_token('='))  # 문제 3: 표시만
        bind('btn_mode',     lambda: None)  # pass
        bind('btn_rad',      lambda: None)  # pass
        bind('btn_2nd',      lambda: None)  # pass
        # AC를 쓰고 싶다면 아래 주석 해제
        # bind('btn_ac', self.on_clear)

        # ---- (2) 남은 버튼: 라벨 기반 일괄 바인딩 ----
        for btn in self.findChildren(QPushButton):
            name = btn.objectName() or ''
            if not name or name in handled:
                continue

            label = (btn.text() or '').strip()

            # 라벨로 Backspace/토글류 복구(혹시 빠졌을 경우)
            if label in {'⌫', 'Back', 'Backspace'}:
                btn.clicked.connect(self.on_backspace)
                handled.add(name)
                continue
            if label.lower() in {'mode', 'rad', '2nd'}:
                btn.clicked.connect(lambda: None)
                handled.add(name)
                continue

            tok = self._token_from_label(label)
            if tok is None:
                btn.clicked.connect(lambda: None)  # pass
            else:
                btn.clicked.connect(lambda _, t=tok: self.on_token(t))
            handled.add(name)

    # ---------- 핸들러 ----------
    def on_token(self, token: str) -> None:
        """토큰을 버퍼에 누적하고 디스플레이를 갱신한다."""
        if self._buffer == '0' and self._should_replace_zero(token):
            self._set_text(token)
        else:
            self._set_text(self._buffer + token)

    def _should_replace_zero(self, token: str) -> bool:
        """초기 '0' 상태에서 숫자/괄호/함수시작/상수/부호/소수점이면 대체."""
        if not token:
            return False
        if token[0].isdigit():
            return True
        if token[0] in {'.', '(', '±', 'π', 'e'}:
            return True
        if token.endswith('('):
            return True
        return False

    def on_backspace(self) -> None:
        """마지막 글자를 지우고, 비면 '0'으로 복구한다."""
        new_buf = self._buffer[:-1] if self._buffer else ''
        if not new_buf:
            new_buf = '0'
        self._set_text(new_buf)

    def on_clear(self) -> None:
        """전체 지움(AC)."""
        self._set_text('0')


def main() -> None:
    """PyQt 애플리케이션 엔트리포인트."""
    import sys
    app = QApplication(sys.argv)
    w = EngineeringCalculatorWindow()
    w.setWindowTitle('Engineering Calculator (UI-only)')
    w.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
