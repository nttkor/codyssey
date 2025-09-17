# -*- coding: utf-8 -*-
"""
engineering_calculator.py
(inheritance-compliant + auto font fit + rich docstrings/comments)

요약
- Calculator: 기본 계산(숫자/사칙/괄호/Ans) + 토큰화 → 샌딩-야드 → RPN 평가. 공학 기능 훅 3개만 선언.
- EngineeringCalculator: 공학 기능(π, sin/cos/tan/sinh/cosh/tanh, x²/x³/% 등) 구현.
- UI(MainWindow):
  - 표시식: 곱셈 'x', 나눗셈 '÷' (평가 직전에 '*' '/'로 변환)
  - '=' 이후: + - x ÷, x²/x³ 입력 시 le_expr에 자동 'Ans'로 시드하고 이어 계산(결과창은 유지)
               함수(sin~)는 새 식 시작(표시 초기화 후 함수 입력)
  - '(' 은 숫자 뒤에서 자동으로 'x(' 삽입
  - '%' 는 숫자 뒤 후위 연산자(해당 숫자 × 0.01)
  - DEL: 공학 함수 머리(sin(, cos(, tan(, sinh(, cosh(, tanh()는 통삭제, ²/³/%는 1글자 삭제
  - 2nd/Rand/± 비활성
  - Deg 기본(버튼으로 Rad/Deg 전환)
  - 두 디스플레이(le_expr, le_result) 길이에 따라 폰트 자동 축소(≤19: 48pt, 그 이상: 800/len, 최소 12pt)

주의
- 외부 라이브러리 금지(표시/수학은 PyQt6, math만 사용).
- 정규표현식(re) 미사용.
"""

import sys
import os
import math
from PyQt6 import uic, QtWidgets, QtCore
from PyQt6.QtWidgets import QMainWindow, QPushButton, QToolButton, QLineEdit
from PyQt6.QtGui import QFont


# ---------- 표시 형식(숫자) 설정 ----------
SIG_DIGITS = 12        # 유효숫자 모드 기본값(필요시 15~16까지 올리기 가능. float 한계 고려)
FIXED_DECIMALS = None  # 고정 소수점 자리수. e.g., 6 설정 시 항상 소수점 6자리로 표시. None이면 유효숫자 모드 사용.


def fmt_number(x: float) -> str:
    """결과 숫자 포매팅.

    - 정수처럼 떨어지면 정수로 표시
    - FIXED_DECIMALS가 지정되면 고정 소수점 자리수로 표시
    - 아니면 유효숫자(SIG_DIGITS)로 표시
    """
    if x is None:
        return ""
    # 거의 정수인 경우(부동오차 방지용 임계)
    if math.isfinite(x) and abs(x - int(x)) < 1e-12:
        return str(int(x))
    # 고정 소수점 모드
    if FIXED_DECIMALS is not None:
        return f"{x:.{FIXED_DECIMALS}f}"
    # 유효숫자 모드
    return f"{x:.{SIG_DIGITS}g}"


class Token:
    """평가기 내부에서 쓰는 토큰 객체.

    속성:
        t (str): 토큰 타입('NUM','CONST','OP','FUNC','POST','LPAREN','RPAREN')
        v (Any): 토큰 값(숫자/기호/이름 등)
    """
    def __init__(self, t, v=None):
        self.t = t
        self.v = v


class Calculator:
    """기본 계산기.

    역할:
        - '숫자/사칙/괄호/Ans' 중심의 파싱/평가를 담당
        - 공학 함수/상수/후위연산은 하위 클래스가 구현하도록 훅 제공
    """

    def __init__(self):
        """메모리 및 Ans(마지막 결과) 초기화."""
        self.memory = 0.0
        self.last_result = None  # Ans

    # ---------- 메모리 ----------
    def mem_clear(self):
        """메모리를 0으로 초기화."""
        self.memory = 0.0

    def mem_recall(self) -> float:
        """메모리 값을 반환."""
        return self.memory

    def mem_add(self, x: float):
        """메모리에 x를 더함."""
        if x is not None and math.isfinite(x):
            self.memory += x

    def mem_sub(self, x: float):
        """메모리에서 x를 뺌."""
        if x is not None and math.isfinite(x):
            self.memory -= x

    # ---------- 공학 훅 (서브클래스 구현 대상) ----------
    def apply_function(self, name: str, x: float, angle_mode_rad: bool) -> float:
        """함수 호출 훅. 예: sin, cos, tan, sinh, cosh, tanh 등.

        Args:
            name: 함수명(소문자 추천)
            x: 피연산자
            angle_mode_rad: True=라디안, False=도(deg)

        Returns:
            float: 계산 결과

        Raises:
            NotImplementedError: 하위 클래스에서 구현해야 함
        """
        raise NotImplementedError("apply_function must be implemented in subclass")

    def apply_postfix(self, op: str, a: float) -> float:
        """후위 연산자 훅. 예: ², ³, %.

        Args:
            op: 후위 연산자 기호('²','³','%' 등)
            a: 피연산자

        Returns:
            float: 계산 결과

        Raises:
            NotImplementedError: 하위 클래스에서 구현해야 함
        """
        raise NotImplementedError("apply_postfix must be implemented in subclass")

    def const_value(self, name: str) -> float:
        """상수 값 훅. 예: 'pi'.

        Args:
            name: 상수명

        Returns:
            float: 상수값

        Raises:
            NotImplementedError: 하위 클래스에서 구현해야 함
        """
        raise NotImplementedError("const_value must be implemented in subclass")

    # ---------- 평가 파이프라인 ----------
    def evaluate_expr(self, s: str, angle_mode_rad: bool) -> float:
        """표시식을 받아 최종 숫자로 평가.

        파이프라인:
            1) 토큰화
            2) 단항 마이너스 보정
            3) 샌딩-야드 알고리즘으로 RPN 변환
            4) RPN 스택 평가
        """
        if not s:
            raise ValueError("empty expression")
        tokens = self._tokenize(s)
        tokens = self._fix_unary_minus(tokens)
        rpn = self._to_rpn(tokens)
        return self._eval_rpn(rpn, angle_mode_rad)

    # ---------- 토큰화 ----------
    def _tokenize(self, s: str):
        """입력 문자열을 토큰 리스트로 변환(re 미사용)."""
        tokens = []
        i, n = 0, len(s)

        def is_digit(ch): return '0' <= ch <= '9'
        def is_alpha(ch): return ('a' <= ch <= 'z') or ('A' <= ch <= 'Z')

        while i < n:
            ch = s[i]

            # 공백 무시
            if ch in (' ', '\t'):
                i += 1
                continue

            # 숫자(정수/실수)
            if is_digit(ch) or ch == '.':
                start = i
                seen_dot = (ch == '.')
                i += 1
                while i < n:
                    c = s[i]
                    if is_digit(c):
                        i += 1
                    elif c == '.':
                        if seen_dot:
                            break
                        seen_dot = True
                        i += 1
                    else:
                        break
                tokens.append(Token('NUM', float(s[start:i])))
                continue

            # 연산자/괄호
            if ch in '+-*/()':
                if ch == '(':
                    tokens.append(Token('LPAREN', '('))
                elif ch == ')':
                    tokens.append(Token('RPAREN', ')'))
                else:
                    tokens.append(Token('OP', ch))
                i += 1
                continue

            # π
            if ch == 'π':
                tokens.append(Token('CONST', 'pi'))
                i += 1
                continue

            # 후위 연산자(², ³, %)
            if ch in ('²', '³', '%'):
                tokens.append(Token('POST', ch))
                i += 1
                continue

            # 식별자(함수/상수/Ans)
            if is_alpha(ch):
                start = i
                i += 1
                while i < n and is_alpha(s[i]):
                    i += 1
                name = s[start:i]
                low = name.lower()
                if low == 'pi':
                    tokens.append(Token('CONST', 'pi'))
                elif low == 'ans':
                    tokens.append(Token('CONST', 'ans'))
                else:
                    tokens.append(Token('FUNC', low))
                continue

            # 그 외
            raise ValueError(f"invalid char: {ch}")

        return tokens

    def _fix_unary_minus(self, tokens):
        """단항 마이너스를 이항으로 보정(예: -x → 0-x)."""
        res = []
        prev_type = 'START'
        for tk in tokens:
            if tk.t == 'OP' and tk.v == '-':
                # 식 시작/연산자/왼괄호/함수 뒤의 '-'는 단항으로 간주
                if prev_type in ('START', 'OP', 'LPAREN', 'FUNC'):
                    res.append(Token('NUM', 0.0))
                    res.append(Token('OP', '-'))
                else:
                    res.append(tk)
                prev_type = 'OP'
                continue

            res.append(tk)
            if tk.t in ('NUM', 'CONST'):
                prev_type = tk.t
            elif tk.t in ('RPAREN', 'POST'):
                prev_type = tk.t
            elif tk.t in ('OP', 'LPAREN', 'FUNC'):
                prev_type = tk.t
            else:
                prev_type = 'OP'
        return res

    def _to_rpn(self, tokens):
        """샌딩-야드 알고리즘으로 중위 표기 → 후위 표기(RPN) 변환."""
        out = []
        st = []

        def prec(op):
            if op in ('+', '-'):
                return 1
            if op in ('*', '/'):
                return 2
            return 0

        for tk in tokens:
            if tk.t in ('NUM', 'CONST'):
                out.append(tk)
            elif tk.t == 'POST':
                # 후위 연산자는 바로 출력(피연산자 다음에 나오므로)
                out.append(tk)
            elif tk.t == 'FUNC':
                st.append(tk)
            elif tk.t == 'LPAREN':
                st.append(tk)
            elif tk.t == 'RPAREN':
                # '(' 만날 때까지 pop
                while st and st[-1].t != 'LPAREN':
                    out.append(st.pop())
                if not st:
                    raise ValueError("mismatched parenthesis")
                st.pop()  # '(' 제거
                # 괄호 닫힌 직후 함수가 있으면 출력 (f(x) 형태)
                if st and st[-1].t == 'FUNC':
                    out.append(st.pop())
            elif tk.t == 'OP':
                while st and st[-1].t == 'OP' and prec(st[-1].v) >= prec(tk.v):
                    out.append(st.pop())
                st.append(tk)
            else:
                raise ValueError("unknown token type")

        # 스택에 남은 연산자/함수 정리
        while st:
            top = st.pop()
            if top.t in ('LPAREN', 'RPAREN'):
                raise ValueError("mismatched parenthesis")
            out.append(top)

        return out

    def _eval_rpn(self, rpn, angle_mode_rad: bool) -> float:
        """RPN(후위 표기)을 스택으로 평가."""
        st = []

        def need(n):
            if len(st) < n:
                raise ValueError("stack underflow")

        for tk in rpn:
            if tk.t == 'NUM':
                st.append(tk.v)
            elif tk.t == 'CONST':
                if tk.v == 'ans':
                    st.append(self.last_result if (self.last_result is not None) else 0.0)
                else:
                    st.append(self.const_value(tk.v))
            elif tk.t == 'OP':
                need(2)
                b = st.pop()
                a = st.pop()
                if tk.v == '+':
                    st.append(a + b)
                elif tk.v == '-':
                    st.append(a - b)
                elif tk.v == '*':
                    st.append(a * b)
                elif tk.v == '/':
                    st.append(a / b)
                else:
                    raise ValueError("unknown op")
            elif tk.t == 'FUNC':
                need(1)
                x = st.pop()
                st.append(self.apply_function(tk.v, x, angle_mode_rad))
            elif tk.t == 'POST':
                need(1)
                a = st.pop()
                st.append(self.apply_postfix(tk.v, a))
            else:
                raise ValueError("unknown token in rpn")

        if len(st) != 1:
            raise ValueError("invalid expression")
        return st[0]


class EngineeringCalculator(Calculator):
    """공학용 계산기: Calculator의 훅을 실제 구현(rad/deg 지원 포함)."""

    def __init__(self):
        """기본 각도 모드: Deg(=False)."""
        super().__init__()
        self.angle_mode_rad = False  # False=Deg, True=Rad

    # ----- 상수 -----
    def const_value(self, name: str) -> float:
        """지원 상수 반환. 현재는 π만 지원."""
        if name == 'pi':
            return math.pi
        raise ValueError(f"unknown const: {name}")

    # ----- 함수 -----
    def apply_function(self, name: str, x: float, angle_mode_rad: bool) -> float:
        """삼각/쌍곡선 함수 계산(rad/deg 변환 포함)."""
        n = name.lower()
        if n in ('sin', 'cos', 'tan'):
            # Deg 모드면 라디안으로 바꿔서 계산
            if not angle_mode_rad:
                x = math.radians(x)
            if n == 'sin':
                return math.sin(x)
            if n == 'cos':
                return math.cos(x)
            return math.tan(x)
        if n == 'sinh':
            return math.sinh(x)
        if n == 'cosh':
            return math.cosh(x)
        if n == 'tanh':
            return math.tanh(x)
        raise ValueError(f"function not supported: {name}")

    # ----- 후위 연산 -----
    def apply_postfix(self, op: str, a: float) -> float:
        """후위 연산자 계산: x², x³, %, 등."""
        if op == '²':
            return a * a
        if op == '³':
            return a * a * a
        if op == '%':
            return a * 0.01
        raise ValueError(f"unknown postfix: {op}")


class MainWindow(QMainWindow):
    """PyQt6 메인 윈도우.

    - engineering.ui를 로드하고, 각 버튼을 동적으로 바인딩
    - le_expr(표시식), le_result(결과) 관리
    - '=' 이후 이어 계산(Ans 시드), 함수·괄호 입력 규칙, 메모리, 각도 모드 토글
    - 글자 수에 따른 폰트 자동 축소
    """

    # 구현된 공학 기능 목록(미구현 버튼은 비활성/회색 처리)
    ENABLED_FUNCS = {"sin", "cos", "tan", "sinh", "cosh", "tanh", "pi", "pow2", "pow3", "percent"}
    # DEL 시 함수 머리를 한 번에 지우기 위해 사용하는 접미사 후보
    FUNC_HEADERS = ["sinh(", "cosh(", "tanh(", "sin(", "cos(", "tan("]
    # 값이 끝날 수 있는 문자(암시적 곱셈 판단 등)
    VALUE_TAILS = set('0123456789)') | {'π', '²', '³', '%'}

    def __init__(self):
        """UI 로드 및 초기 연결."""
        super().__init__()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(base_dir, "engineering.ui")
        uic.loadUi(ui_path, self)

        # UI 요소 가져오기
        opts = QtCore.Qt.FindChildOption.FindChildrenRecursively
        self.le_expr: QLineEdit = self.findChild(QLineEdit, "le_expr", opts)
        self.le_result: QLineEdit = self.findChild(QLineEdit, "le_result", opts)

        # 글자 수에 따른 폰트 자동 축소: 시그널 연결 + 초기 1회 적용
        if self.le_expr:
            self.le_expr.textChanged.connect(lambda s: self._fit_font(self.le_expr, s))
            self._fit_font(self.le_expr, self.le_expr.text() or "")
        if self.le_result:
            self.le_result.textChanged.connect(lambda s: self._fit_font(self.le_result, s))
            self._fit_font(self.le_result, self.le_result.text() or "")

        # 엔진/상태
        self.engine = EngineeringCalculator()
        self.inv_mode = False
        self._pending_clear = False  # '=' 후 다음 입력 처리용 플래그

        # 버튼 바인딩 및 UI 상태 정리
        self._bind_all_buttons()
        self._disable_unimplemented_functions()
        self._disable_2nd_rand_plusminus()
        self._sync_rad_button_text()

    # ---------- 폰트 자동 조절 ----------
    def _fit_font(self, led: QLineEdit, text: str):
        """표시 길이에 따라 QLineEdit 폰트를 자동으로 줄임.

        규칙:
            - 길이 ≤ 19: 48pt 유지
            - 길이 > 19: size = max(12, min(48, int(800/length)))
        """
        length = max(1, len(text or ""))
        if length <= 19:
            size = 48
        else:
            size = max(5, min(48, int(900 // length)))
        font = led.font()
        font.setBold(True)
        font.setPointSize(size)
        led.setFont(font)

    # ---------- 표시식 → 내부식 ----------
    def _to_internal_expr(self, expr: str) -> str:
        """표시식 기호('x','×','÷')를 파서용 기호('*','/')로 변환."""
        return expr.replace('×', '*').replace('x', '*').replace('÷', '/')

    # ---------- '=' 이후 Ans 시드 ----------
    def _ans_seed_if_needed(self, want_ans: bool):
        """'=' 직후 입력 종류에 따라 le_expr 초기화/Ans 시드를 결정.

        Args:
            want_ans: 사칙/제곱처럼 직후에 'Ans'로 이어 계산해야 하는 경우 True.
                      함수처럼 새 식을 시작해야 하는 경우 False.
        """
        if not self._pending_clear:
            return
        if want_ans:
            # 결과창 유지 + 식만 Ans로 교체
            self.le_expr.setText("Ans")
            self._pending_clear = False
        else:
            # 함수류: 새 식 시작(표시/결과 모두 클리어)
            self.le_expr.clear()
            self.le_result.clear()
            self._pending_clear = False

    def _prepare_for_input(self, will_modify_expr: bool):
        """다음 입력이 표시식을 변경할 경우, '=' 이후 상태를 정리."""
        if will_modify_expr and self._pending_clear:
            self.le_expr.clear()
            self.le_result.clear()
            self._pending_clear = False

    # ---------- 버튼 바인딩 ----------
    def _bind_all_buttons(self):
        """UI 내 모든 QPushButton/QToolButton을 클릭 핸들러에 연결."""
        for w in self.findChildren(QPushButton) + self.findChildren(QToolButton):
            name = w.objectName()
            if not name:
                continue
            w.clicked.connect(lambda _=False, b=w: self.on_button_clicked(b))

    def _disable_unimplemented_functions(self):
        """미구현 공학 함수 버튼을 비활성화하고 회색 처리."""
        for w in self.findChildren(QPushButton) + self.findChildren(QToolButton):
            name = w.objectName() or ""
            if not name.startswith("btnf_"):
                continue
            key = name.split("_", 1)[1]
            key = self._alias(key)
            if key not in self.ENABLED_FUNCS:
                w.setEnabled(False)
                try:
                    old = w.styleSheet() or ""
                    w.setStyleSheet(old + "; color:#888;")
                except Exception:
                    pass

    def _disable_2nd_rand_plusminus(self):
        """2nd / Rand / ± 관련 버튼 비활성화 및 회색 처리."""
        candidates = self.findChildren(QPushButton) + self.findChildren(QToolButton)
        for w in candidates:
            nm = (w.objectName() or "").lower()
            tx = (getattr(w, "text", lambda: "")() or "").strip().lower()
            disable = False
            if ("2nd" in nm) or ("rand" in nm) or (tx in {"2nd", "rand"}):
                disable = True
            if ("plusminus" in nm) or ("pm" in nm) or ("±" in nm) or (tx in {"±", "+/-", "plus/minus"}):
                disable = True
            if disable:
                w.setEnabled(False)
                try:
                    old = w.styleSheet() or ""
                    w.setStyleSheet(old + "; color:#888;")
                except Exception:
                    pass

    # ---------- 텍스트 폴백 ----------
    def _key_from_text(self, txt):
        """objectName 매핑 실패 시 버튼 텍스트로 기능을 추정."""
        t = (txt or "").strip().lower()
        if not t:
            return None
        if len(t) == 1 and '0' <= t <= '9':
            return t
        if t in {"(", ")"}:
            return "open" if t == "(" else "close"
        if t in {"=", "eq"}:
            return "equal"
        if t in {"+", "add"}:
            return "plus"
        if t in {"-", "sub"}:
            return "minus"
        if t in {"*", "x", "×", "times"}:
            return "mul"
        if t in {"/", "÷", "divide"}:
            return "div"
        if t in {".", "·"}:
            return "dot"
        if t in {"%","percent"}:
            return "percent"
        if t in {"ac", "c", "clear"}:
            return "ac"
        if t in {"del", "⌫", "back", "bksp"}:
            return "del"
        if t in {"rad", "deg"}:
            return "rad"
        if t == "mc":
            return "m_c"
        if t == "mr":
            return "m_r"
        if t in {"m+", "madd"}:
            return "m_plus"
        if t in {"m-", "msub"}:
            return "m_minus"
        if t in {"sin", "cos", "tan", "sinh", "cosh", "tanh"}:
            return t
        if t in {"π", "pi"}:
            return "pi"
        if t in {"x²", "x^2", "x2"}:
            return "pow2"
        if t in {"x³", "x^3", "x3"}:
            return "pow3"
        return None

    # ---------- 클릭 디스패치 ----------
    def on_button_clicked(self, btn):
        """버튼 클릭 시 objectName 우선 → 텍스트 폴백으로 기능 호출."""
        name = btn.objectName() or ""
        key = None

        # objectName 기반 라우팅 (btnn_*, btnf_*, btno_* 등)
        if "_" in name:
            prefix, raw = name.split("_", 1)
            key = self._alias(raw)

            # 숫자/소수점
            if prefix == "btnn":
                if key and key.isdigit():
                    self._append_digit(key)
                    return
                if key in (".", "dot", "point", "decimal"):
                    self._append_dot()
                    return

            # 공학 함수
            if prefix == "btnf":
                handler = getattr(self, f"do_{key}", None)
                if callable(handler):
                    handler()
                    return

            # 연산/시스템
            handler = getattr(self, f"do_{key}", None)
            if callable(handler):
                handler()
                return

        # 텍스트 폴백
        tkey = self._key_from_text(getattr(btn, "text", lambda: "")())
        if tkey:
            handler = getattr(self, f"do_{tkey}", None)
            if callable(handler):
                handler()
                return

    # ---------- 별칭 ----------
    def _alias(self, key: str) -> str:
        """objectName 뒤 꼬리(raw)를 내부 핸들러 키로 통일."""
        k = (key or "").lower()
        if k in {"+", "add", "plus"}: return "plus"
        if k in {"-", "sub", "minus"}: return "minus"
        if k in {"*", "x", "×", "times", "mul"}: return "mul"
        if k in {"/", "÷", "div", "divide"}: return "div"
        if k in {"(", "open", "lparen"}: return "open"
        if k in {")", "close", "rparen"}: return "close"
        if k in {"=", "eq", "equal"}: return "equal"
        if k in {"dot", ".", "point", "decimal"}: return "dot"
        if k in {"mc", "m_c", "mclear"}: return "m_c"
        if k in {"mr", "m_r"}: return "m_r"
        if k in {"m+", "mplus", "m_add"}: return "m_plus"
        if k in {"m-", "mminus", "m_sub"}: return "m_minus"
        if k in {"pi", "π"}: return "pi"
        if k in {"x2", "square", "sqr", "pow2"}: return "pow2"
        if k in {"x3", "cube", "pow3"}: return "pow3"
        if k in {"percent", "%"}: return "percent"
        return k

    # ---------- 입력 유틸 ----------
    def _text(self) -> str:
        """현재 표시식 문자열을 반환."""
        return self.le_expr.text() or ""

    def _set_text(self, s: str):
        """표시식 문자열을 강제로 설정."""
        self.le_expr.setText(s)

    def _append(self, s: str):
        """표시식 문자열 뒤에 s를 덧붙임."""
        self.le_expr.setText(self._text() + s)

    def _ends_with_value(self) -> bool:
        """표시식이 '값'으로 끝나는지(숫자/π/괄호닫힘/제곱/%) 판단."""
        t = self._text()
        return bool(t) and (t[-1] in self.VALUE_TAILS)

    def _ends_with_digit(self) -> bool:
        """표시식이 숫자(0~9)로 끝나는지 판단."""
        t = self._text()
        return bool(t) and ('0' <= t[-1] <= '9')

    def _maybe_mul(self):
        """암시적 곱셈 처리. 값 뒤에 함수/π/괄호가 오면 'x'를 붙임(표시만)."""
        if self._ends_with_value():
            self._append("x")

    def _append_digit(self, d: str):
        """숫자 버튼 입력 처리."""
        self._prepare_for_input(True)
        self._append(d)

    def _append_dot(self):
        """소수점 입력 처리. 현재 숫자 세그먼트에 '.'가 이미 있으면 무시."""
        self._prepare_for_input(True)
        t = self._text()
        i = len(t) - 1
        seg = ""
        # 마지막 숫자 세그먼트만 검사
        while i >= 0 and (('0' <= t[i] <= '9') or t[i] == '.'):
            seg = t[i] + seg
            i -= 1
        if '.' in seg:
            return
        self._append(".")

    # ---------- 공학 함수/상수 ----------
    def insert_function(self, name: str):
        """함수 입력 공통 처리. '=' 직후면 새 식 시작, 암시적 곱셈 적용."""
        self._prepare_for_input(True)
        self._maybe_mul()
        self._append(name + "(")

    def do_sin(self): self.insert_function("sin")
    def do_cos(self): self.insert_function("cos")
    def do_tan(self): self.insert_function("tan")
    def do_sinh(self): self.insert_function("sinh")
    def do_cosh(self): self.insert_function("cosh")
    def do_tanh(self): self.insert_function("tanh")

    def do_pi(self):
        """π 입력(필요 시 암시적 곱셈)."""
        self._prepare_for_input(True)
        if self._ends_with_value():
            self._append("x")
        self._append("π")

    def do_pow2(self):
        """x² 후위 연산 입력('=' 직후면 Ans 시드)."""
        self._ans_seed_if_needed(want_ans=True)
        if self._ends_with_value() or self._text() == "Ans":
            self._append("²")

    def do_pow3(self):
        """x³ 후위 연산 입력('=' 직후면 Ans 시드)."""
        self._ans_seed_if_needed(want_ans=True)
        if self._ends_with_value() or self._text() == "Ans":
            self._append("³")

    # ---------- % (후위, 숫자 뒤만) ----------
    def do_percent(self):
        """퍼센트 후위 연산 입력(숫자 뒤에서만 허용)."""
        self._prepare_for_input(True)
        if self._ends_with_digit():
            self._append("%")

    # ---------- 일반 연산 ----------
    def do_plus(self):
        """더하기 입력('=' 직후면 Ans 시드)."""
        self._ans_seed_if_needed(want_ans=True)
        self._append("+")

    def do_minus(self):
        """빼기 입력('=' 직후면 Ans 시드)."""
        self._ans_seed_if_needed(want_ans=True)
        self._append("-")

    def do_mul(self):
        """곱하기 입력('=' 직후면 Ans 시드)."""
        self._ans_seed_if_needed(want_ans=True)
        self._append("x")  # 표시용 x

    def do_div(self):
        """나누기 입력('=' 직후면 Ans 시드)."""
        self._ans_seed_if_needed(want_ans=True)
        self._append("÷")  # 표시용 ÷

    def do_open(self):
        """여는 괄호 입력(숫자 뒤면 자동으로 'x(')."""
        self._prepare_for_input(True)
        if self._ends_with_digit():
            self._append("x(")
        else:
            self._append("(")

    def do_close(self):
        """닫는 괄호 입력."""
        self._prepare_for_input(True)
        self._append(")")

    # ---------- 시스템 ----------
    def do_ac(self):
        """모두 지우기(표시/결과/상태 초기화)."""
        self._pending_clear = False
        self._set_text("")
        self.le_result.setText("")

    def do_del(self):
        """한 글자 지우기. 함수 머리는 통삭제."""
        if self._pending_clear:
            self._pending_clear = False
        s = self._text()
        if not s:
            return
        # 함수 머리(sinh(, cosh(, ...)는 통삭제
        for header in sorted(self.FUNC_HEADERS, key=len, reverse=True):
            if s.endswith(header):
                self._set_text(s[:-len(header)])
                return
        # ²/³/%는 1글자 삭제
        if s.endswith("²") or s.endswith("³") or s.endswith("%"):
            self._set_text(s[:-1])
            return
        # 일반 1글자 삭제
        self._set_text(s[:-1])

    def _auto_closed_expr(self, expr: str) -> str:
        """왼·오른 괄호 수를 맞춰 자동으로 닫아 줌."""
        opens = 0
        for ch in expr:
            if ch == '(':
                opens += 1
            elif ch == ')':
                if opens > 0:
                    opens -= 1
        return expr + (")" * opens) if opens > 0 else expr

    def do_equal(self):
        """'=' 처리: 현재 표시식을 평가해 결과창에 표시하고 Ans에 저장.

        - 내부 평가 전 표시식을 '*','/'로 변환
        - 괄호 자동 닫기
        - 오류 발생 시 'Error' 표시
        - 다음 입력 특수처리 플래그(_pending_clear) 활성화
        """
        expr_display = self._text()
        try:
            to_eval = self._auto_closed_expr(expr_display)
            to_eval = self._to_internal_expr(to_eval)
            val = self.engine.evaluate_expr(to_eval, self.engine.angle_mode_rad)
            self.engine.last_result = val
            self.le_result.setText(fmt_number(val))
        except Exception:
            self.engine.last_result = None
            self.le_result.setText("Error")
        # '=' 이후 다음 입력 정책을 위한 플래그
        self._pending_clear = True

    # ---------- 각도 모드 ----------
    def do_rad(self):
        """Rad/Deg 토글. 버튼 텍스트 동기화."""
        self.engine.angle_mode_rad = not self.engine.angle_mode_rad
        self._sync_rad_button_text()

    def _sync_rad_button_text(self):
        """현재 각도 모드에 맞게 버튼 텍스트를 'Rad'/'Deg'로 설정."""
        btn = self.findChild((QPushButton, QToolButton), "btno_rad",
                             QtCore.Qt.FindChildOption.FindChildrenRecursively)
        if btn:
            btn.setText("Rad" if self.engine.angle_mode_rad else "Deg")

    # ---------- 메모리 ----------
    def _current_value_for_memory(self):
        """현재 결과창 또는 표시식을 평가해 메모리 연산에 사용할 숫자를 반환."""
        # 우선 결과창
        txt = (self.le_result.text() or "").strip()
        if txt and txt != "Error":
            try:
                return float(txt)
            except Exception:
                pass
        # 아니면 표시식 평가(실패 시 None)
        expr = self._text()
        if expr:
            try:
                expr2 = self._to_internal_expr(self._auto_closed_expr(expr))
                return self.engine.evaluate_expr(expr2, self.engine.angle_mode_rad)
            except Exception:
                return None
        return None

    def do_m_c(self):
        """MC: 메모리 클리어."""
        self.engine.mem_clear()

    def do_m_r(self):
        """MR: 메모리 값을 식에 붙임(필요 시 암시적 곱셈)."""
        self._prepare_for_input(True)
        v = self.engine.mem_recall()
        if self._ends_with_value():
            self._append("x")
        self._append(fmt_number(v))

    def do_m_plus(self):
        """M+: 현재 값(결과/표시식 평가)을 메모리에 더함."""
        v = self._current_value_for_memory()
        self.engine.mem_add(v)

    def do_m_minus(self):
        """M-: 현재 값(결과/표시식 평가)을 메모리에서 뺌."""
        v = self._current_value_for_memory()
        self.engine.mem_sub(v)


def main():
    """PyQt6 앱을 생성하고 메인 윈도우를 실행."""
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
