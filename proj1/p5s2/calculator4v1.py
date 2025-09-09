# calculator4.py
# ------------------------------------------------------------
# 목적:
# - PyQt6 통합형(MainWindow 내부) 계산기 컨트롤러
# - engineering.ui / caculator.ui를 show/hide 전환
# - 공학 함수(EngineeringCalculator)와 UI 버튼 이벤트 연결
# - 삼각/쌍곡삼각/제곱/세제곱/π 등 단항은 즉시 계산
# - x^y는 이항 연산: 1항 저장 → '='에서 계산
# - MC/MR/M+/M-/MS, DEG/RAD, AC, ⌫, %, ± 처리
# - 예외/범위/정의역 오류는 "Error" 표시(콘솔 경고/프린트 없음)
# ------------------------------------------------------------

import sys, os, re, math
from pathlib import Path
from typing import Optional, Callable

# PyQt6: Qt Designer .ui를 로드하고, 위젯/시그널(이벤트)을 관리하기 위해 import
from PyQt6 import uic  # uic.loadUi 로 .ui 파일을 런타임에 로드
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit  # 핵심 위젯
from PyQt6.QtCore import Qt  # 정렬/플래그 등 상수
from PyQt6.QtGui import QFont  # 표시 폰트 크기/스타일 제어

# 공학 계산 로직(표준 라이브러리 + math만 사용)
from engineering_calculator import EngineeringCalculator


def find_ui_path(name: str) -> str:
    """engineering.ui / caculator.ui 경로 탐색 유틸.
    - __file__ 기준, 현재 작업 디렉토리, /mnt/data 3곳을 우선탐색
    - FileNotFoundError 발생 시 초기 실행에서 즉시 알림
    """
    roots = [Path(__file__).parent, Path(os.getcwd()), Path("/mnt/data")]
    for r in roots:
        p = r / name
        if p.exists():
            return str(p)
    raise FileNotFoundError(f"UI not found: {name}  (searched: {', '.join(map(str, roots))})")


class UIWindow(QMainWindow):
    """uic로 로드된 QMainWindow 컨테이너.
    - led 디스플레이(QLineEdit) 참조/설정
    - 모든 QPushButton 수집
    - 모드 버튼 탐색 유틸 제공
    """
    def __init__(self, ui_path: str):
        super().__init__()
        # PyQt6: Qt Designer로 만든 .ui를 런타임에 로드하여 이 QMainWindow 인스턴스에 적용
        uic.loadUi(ui_path, self)
        self.ui_path = ui_path

        # 디스플레이 역할의 QLineEdit 찾기: objectName='led'가 있으면 우선 사용
        self.led: Optional[QLineEdit] = getattr(self, "led", None)
        if self.led is None:
            # led가 명시되어 있지 않다면 첫 번째 QLineEdit를 led로 사용
            qles = self.findChildren(QLineEdit)
            self.led = qles[0] if qles else None

        if self.led:
            # 사용자가 직접 타이핑하지 않도록 읽기 전용
            self.led.setReadOnly(True)
            # 숫자 전자계산기와 유사하게 우측 정렬 + 수직 중앙정렬
            self.led.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        # 창 내부의 모든 QPushButton 수집(자동 배선에 사용)
        self.buttons: list[QPushButton] = self.findChildren(QPushButton)

    def find_mode_button(self) -> Optional[QPushButton]:
        """Mode 버튼 탐색:
        - objectName 'btn_mode'를 우선
        - 대안: 텍스트에 'mode' 포함
        """
        for b in self.buttons:
            if b.objectName().lower() == "btn_mode":
                return b
        for b in self.buttons:
            if "mode" in b.text().lower():
                return b
        return None


class MainWindow:
    """통합형 컨트롤러.
    - 두 UI(engineering/basic) show/hide 전환
    - 버튼 → 공학 엔진 메서드 연결
    - 상태(이항 연산 op1/operator/awaiting_second) 관리
    - 디스플레이/폰트/에러 표기 관리
    """
    def __init__(self):
        # 공학용 계산 엔진(삼각/쌍곡/제곱/세제곱/π 등 구현 + 예외/범위 검사 포함)
        self.calc = EngineeringCalculator()

        # 상태 변수
        self.expression_str: str = ""     # (옵션) 문자열 누적용 버퍼
        self.op1: Optional[float] = None  # 이항 연산의 첫 번째 피연산자
        self.operator: Optional[str] = None  # "POW" 등
        self.awaiting_second: bool = False  # 두 번째 피연산자 입력 대기 플래그

        # PyQt6: UI 로드(두 창을 모두 띄워두고 show/hide로 전환)
        self.win_engineering = UIWindow(find_ui_path("engineering.ui"))
        self.win_basic = UIWindow(find_ui_path("caculator.ui"))

        # 현재 보이는 창 포인터
        self.current = self.win_engineering
        self.other = self.win_basic

        # 초기 디스플레이 세팅
        self._apply_display("0")

        # 모든 버튼을 자동 배선(신호/슬롯 연결)
        self._wire_window(self.win_engineering)
        self._wire_window(self.win_basic)

        # Mode 버튼은 전용 핸들러에 연결
        self._connect_mode_button(self.win_engineering)
        self._connect_mode_button(self.win_basic)

        # 시작 시 엔지니어링 창 표시
        self.current.show()

    # ---------- 라벨 정규화 ----------
    def _normalize_label(self, raw: str) -> str:
        """버튼 라벨의 다양한 표기를 표준 키로 정규화.
        - 예: ×/X/* → '*', x²/x^2 → 'x^2', π/pi → 'π', log/log₁₀ → 'log10', 등
        - 정규화된 키는 이후 매핑/분기에 사용
        """
        s = (raw or "").strip()
        s_low = s.lower()

        # 곱셈 기호 통일
        if s in {"×", "X", "*"}: return "*"

        # 제곱/세제곱 통일
        if s_low in {"x²", "x^2", "x2", "x**2"}: return "x^2"
        if s_low in {"x³", "x^3", "x3", "x**3"}: return "x^3"

        # 거듭제곱(이항)
        if s_low in {"x^y", "^", "pow"}: return "x^y"

        # 루트류
        if s in {"√x", "√", "sqrt"}: return "√x"
        if s_low in {"²√x", "2√x", "2root"}: return "2√x"
        if s_low in {"³√x", "3√x", "3root"}: return "3√x"
        if s_low in {"y√x", "nthroot", "n√x"}: return "y√x"

        # 원주율/상수
        if s in {"π", "pi", "PI"}: return "π"
        if s_low in {"e", "const e", "ℯ"}: return "e"

        # 로그/ln
        if s_low in {"ln"}: return "ln"
        if s_low in {"log", "log10", "log₁₀", "lg"}: return "log10"

        # 역수
        if s_low in {"1/x", "x^-1", "x⁻¹"}: return "1/x"

        # 팩토리얼
        if s_low in {"x!", "n!", "!"}: return "x!"

        # 각도 모드
        if s_low in {"deg", "degree"}: return "DEG"
        if s_low in {"rad", "radian"}: return "RAD"

        # 부호/퍼센트/등호/삭제/클리어
        if s in {"+/-", "±"}: return "±"
        if s == "%": return "%"
        if s == "=": return "="
        if s in {"⌫", "back", "backspace"}: return "⌫"
        if s in {"AC", "C", "CE"}: return "AC"

        # 메모리 키
        if s_low in {"mc"}: return "MC"
        if s_low in {"mr"}: return "MR"
        if s_low in {"m+"}: return "M+"
        if s_low in {"m-"}: return "M-"
        if s_low in {"ms", "mem", "store"}: return "MS"

        # 사칙/괄호/점 그대로 허용
        if s in {"+", "-", "/", "(", ")", ".", "%"}: return s

        # 숫자 그대로 허용
        if re.fullmatch(r"\d+", s): return s

        # 나머지는 원문(또는 소문자) 그대로 반환
        return s

    # ---------- 표시 & 폰트 ----------
    def _apply_display(self, text: str):
        """현재 창의 led 텍스트와 폰트를 갱신.
        - 빈 문자열이면 '0'으로 표시
        - 길이에 따라 폰트 크기를 자동 조절(최소 12pt)
        """
        if not text:
            text = "0"
        if self.current.led:
            self.current.led.setText(text)
            self._fit_font(text)

    def _fit_font(self, text: str):
        """표시 글자 수에 따라 폰트 크기 동적 조절."""
        n = max(1, len(text))
        size = 48 if n <= 10 else max(12, int(480 / n))
        f = QFont()
        f.setBold(True)
        f.setPointSize(size)
        self.current.led.setFont(f)

    def _get_display_value(self) -> float:
        """led의 문자열을 float로 안전 파싱.
        - 'π'는 math.pi로 대체
        - 숫자 이외 문자가 섞인 경우, 가장 앞의 숫자 토큰만 파싱 시도
        - 파싱 실패 시 0.0
        """
        s = self.current.led.text() if self.current.led else "0"
        s = s.strip()
        if s in {"", "Error"}:
            return 0.0
        try:
            return float(s)
        except ValueError:
            if s == "π":
                return float(self.calc.const_pi())
            # 숫자 패턴만 추출(예: '12 +' 같은 상황 구제)
            m = re.search(r"[-+]?\d+(\.\d+)?([eE][-+]?\d+)?", s)
            if m:
                try:
                    return float(m.group(0))
                except Exception:
                    pass
            return 0.0

    def _show_result(self, val: float):
        """결과 표시.
        - 0 근사치는 0.0으로 스냅
        - 최대 12 유효자리로 표시(과학적 표기 허용)
        """
        if abs(val) < 1e-12:
            val = 0.0
        s = f"{val:.12g}"
        self._apply_display(s)

    def _show_error(self):
        """에러를 led에 표기."""
        self._apply_display("Error")

    # ---------- 모드 전환 ----------
    def toggle_mode(self):
        """Mode 버튼: 현재 보이는 창을 숨기고, 다른 창을 표시.
        - show/hide 전환만 수행(UI는 수정하지 않음)
        - 기존 표시 텍스트를 새 창에도 동기화
        """
        # 현재 창 숨김
        self.current.hide()
        # 포인터 스왑
        self.current, self.other = self.other, self.current
        # 표시 텍스트를 새 창에 반영
        txt = self.other.led.text() if self.other.led else "0"
        self._apply_display(txt)
        # 새 창 표시 및 포커스
        self.current.show()
        self.current.activateWindow()

    def _connect_mode_button(self, w: UIWindow):
        """Mode 버튼을 toggle_mode에 연결."""
        btn = w.find_mode_button()
        if btn:
            # PyQt6: clicked 시그널을 슬롯(toggle_mode)과 연결
            btn.clicked.connect(self.toggle_mode)

    # ---------- 버튼 배선 ----------
    def _wire_window(self, w: UIWindow):
        """해당 창의 모든 버튼을 기능별 핸들러에 자동 배선.
        - 정규화된 라벨 기준으로 분기(특수키/이항/단항/일반 입력)
        - PyQt6: clicked.connect(슬롯) 형태로 연결
        """
        for b in w.buttons:
            name = b.objectName().strip().lower()  # 오브젝트명(보조 힌트)
            raw_label = b.text().strip()           # 원 라벨
            label = self._normalize_label(raw_label)  # 정규화 라벨

            # Mode는 전용 핸들러에서 연결하므로 여기서 건너뜀
            if name == "btn_mode" or "mode" in raw_label.lower():
                continue

            # 특수키들(클리어/등호/백스페이스/메모리/각도/부호/퍼센트)
            if label == "AC" or name.startswith("btn_ac"):
                b.clicked.connect(self._on_ac); continue
            if label == "=" or name.endswith("equals"):
                b.clicked.connect(self._on_equals); continue
            if label == "⌫" or "back" in name:
                b.clicked.connect(self._on_backspace); continue
            if label in {"MC", "MR", "M+", "M-", "MS"}:
                b.clicked.connect(lambda _=False, t=label: self._on_memory(t)); continue
            if label in {"DEG", "RAD"}:
                b.clicked.connect(lambda _=False, t=label: self._on_angle_mode(t)); continue
            if label == "±":
                b.clicked.connect(self._on_negate); continue
            if label == "%":
                b.clicked.connect(self._on_percent); continue

            # 이항 연산(x^y) → '='에서 평가
            if label == "x^y":
                b.clicked.connect(lambda _=False: self._on_binary_op("POW")); continue

            # 나머지 버튼은 단항/일반 입력 핸들러로
            b.clicked.connect(lambda _=False, t=label, n=name: self._on_generic_input(t, n))

    # ---------- 특수키 핸들러 ----------
    def _on_ac(self):
        """AC/C/CE: 모든 상태 초기화 + 디스플레이 0."""
        self.expression_str = ""
        self.op1 = None
        self.operator = None
        self.awaiting_second = False
        self._apply_display("0")

    def _on_backspace(self):
        """⌫: led 끝 문자 1개 삭제(문자 단위)."""
        if not self.current.led:
            return
        s = self.current.led.text()
        if s and s != "0":
            s = s[:-1]
        self._apply_display(s if s else "0")

    def _on_memory(self, key: str):
        """MC/MR/M+/M-/MS 처리.
        - 공학 엔진의 메모리 레지스터 사용
        - 예외 발생 시 'Error' 표시
        """
        try:
            if key == "MC":
                self.calc.memory_clear()
            elif key == "MR":
                v = self.calc.memory_recall()
                self._show_result(v)
            elif key == "M+":
                self.calc.memory_add(self._get_display_value())
            elif key == "M-":
                self.calc.memory_sub(self._get_display_value())
            elif key == "MS":
                self.calc.memory_store(self._get_display_value())
        except ValueError:
            self._show_error()

    def _on_angle_mode(self, label: str):
        """DEG/RAD: 각도 모드 설정(삼각/쌍곡삼각에 반영)."""
        try:
            self.calc.set_angle_mode(label.upper())  # 'DEG' or 'RAD'
        except ValueError:
            self._show_error()

    def _on_negate(self):
        """±: 현재 표시값의 부호 반전."""
        v = self._get_display_value()
        self._show_result(-v)

    def _on_percent(self):
        """%: 현재 표시값을 100으로 나눔(표시 전용 간단 처리)."""
        v = self._get_display_value()
        self._show_result(v / 100.0)

    def _on_binary_op(self, opcode: str):
        """이항 연산 시작: op1 저장 후 두 번째 피연산자 대기."""
        self.op1 = self._get_display_value()
        self.operator = opcode
        self.awaiting_second = True
        # 두 번째 입력을 받기 위해 디스플레이를 비워줌
        self._apply_display("0")

    def _on_equals(self):
        """'=': 대기 중인 이항 연산을 평가."""
        if self.operator is None:
            return
        try:
            cur = self._get_display_value()
            if self.operator == "POW":
                # x^y 계산
                res = self.calc.pow_xy(self.op1, cur)
            else:
                # 확장 여지(다른 이항 연산 추가 시)
                return
            self._show_result(res)
            # 체인 연산을 위해 op1에 결과 유지, 상태 해제
            self.op1 = res
            self.awaiting_second = False
            self.operator = None
        except ValueError:
            # 공학 엔진에서 Range/Domain/ZeroDiv/Undefined 등 발생 시
            self._show_error()
            self.operator = None
            self.awaiting_second = False

    # ---------- 일반 입력/단항 함수 ----------
    def _on_generic_input(self, label: str, obj_name: str):
        """단항/상수는 즉시 계산, 그 외(숫자/연산자/괄호 등)는 표시만 누적.
        - label은 _normalize_label()을 거친 표준 키
        - obj_name은 'btn_sin' 같은 오브젝트명으로 보조 힌트
        """
        # 단항/상수 매핑 테이블(정규화 키 기준)
        unary_map: dict[str, Callable[[float], float] | Callable[[], float]] = {
            # 필수 구현(공학 엔진)
            "sin":   lambda x: self.calc.sin(x),
            "cos":   lambda x: self.calc.cos(x),
            "tan":   lambda x: self.calc.tan(x),
            "sinh":  lambda x: self.calc.sinh(x),
            "cosh":  lambda x: self.calc.cosh(x),
            "tanh":  lambda x: self.calc.tanh(x),
            "x^2":   lambda x: self.calc.square(x),
            "x^3":   lambda x: self.calc.cube(x),
            "π":     lambda _x=None: self.calc.const_pi(),
            # 선택 구현(있으면 바로 사용 가능)
            "ln":     lambda x: self.calc.ln(x),
            "log10":  lambda x: self.calc.log10(x),
            "√x":     lambda x: self.calc.sqrt(x),
            "2√x":    lambda x: self.calc.nth_root(x, 2),
            "3√x":    lambda x: self.calc.nth_root(x, 3),
            # "y√x":  → 별도 입력 흐름이 필요하므로 이번 단계에서는 보류
            "1/x":    lambda x: self.calc.reciprocal(x),
            "abs":    lambda x: self.calc.abs_val(x),
            "e^x":    lambda x: self.calc.exp(x),
            "10^x":   lambda x: self.calc.ten_pow(x),
            "x!":     lambda x: self.calc.factorial(x),
            "e":      lambda _x=None: math.e,  # 상수 e 허용
        }

        key = label  # 정규화된 키

        # 오브젝트명이 힌트이면 보조 사용(예: btn_sin → 'sin')
        if key not in unary_map and obj_name.startswith("btn_"):
            hint = obj_name[4:]
            if hint in unary_map:
                key = hint

        # 1) 단항/상수: 현재 표시값에 대해 즉시 계산/표시
        if key in unary_map and unary_map[key] is not None:
            try:
                cur = self._get_display_value()
                fn = unary_map[key]
                # 상수(π, e) 같은 인자 없는 함수도 있으므로 인자 수에 따라 호출
                res = fn(cur) if fn.__code__.co_argcount == 1 else fn()
                self._show_result(res)
            except ValueError:
                # 공학 엔진에서 발생한 예외(정의역/범위/분모0 등)는 일괄 Error 표시
                self._show_error()
            return

        # 2) 나머지(숫자/연산자/괄호 등)는 문자열로만 누적(= 또는 전용 핸들러에서 계산)
        if not self.current.led:
            return
        s = self.current.led.text()
        # 이전에 '0' 표기였거나, 'Error'였거나, 이항 두 번째 입력 시작이면 초기화
        if s == "0" or s == "Error" or self.awaiting_second:
            s = ""
            self.awaiting_second = False
        # 정규화된 라벨 그대로 이어 붙여 표시
        self._apply_display(s + label)


if __name__ == "__main__":
    # PyQt6: 애플리케이션 인스턴스 생성(이벤트 루프 관리)
    app = QApplication(sys.argv)
    # MainWindow(통합형 컨트롤러) 생성 → 내부에서 UI 로드/배선/표시
    mw = MainWindow()
    # 이벤트 루프 진입(앱 종료 시까지 블로킹)
    sys.exit(app.exec())
