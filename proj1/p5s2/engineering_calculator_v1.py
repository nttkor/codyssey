# -*- coding: utf-8 -*-
"""
engineering_calculator.py
=========================

개요
----
PyQt6 기반의 간단·견고한 공학용 계산기.

핵심 특징
- **UI 고정 전제**: 버튼 objectName 규칙(`btnn_*`, `btno_*`, `btnf_*`)을 이용해 자동 라우팅.
- **숫자/소수점/삼각·쌍곡**: 선점 매핑(람다 기본인자) + 나머지 버튼은 `do_<tail>` 규칙으로 자동 바인딩.
- **표시/평가 분리**: 화면에는 `x`, `÷` 등 사용하지만, 평가 전에 `*`, `/`로 변환.
- **파서**: 토큰화 → 단항 마이너스 보정 → 셔닝야드로 RPN → 스택 평가. (정규식 미사용)
- **공학 기능**: π, sin/cos/tan/sinh/cosh/tanh, 후위연산(²/³/%), Ans 이어 계산, 메모리(MC/MR/M+/M-).
- **각도 모드**: Deg 기본, Rad 토글 버튼으로 전환.
- **UX**: '=' 이후 다음 입력 정책(Ans 시드/표시 초기화), 암시적 곱셈(x), 함수 머리 DEL 통삭제, 괄호 자동 닫기.
- **표시**: 결과 숫자 포맷(유효숫자/고정 소수), 두 디스플레이 길이에 따라 폰트 자동 축소.

의존성
- PyQt6, math (표준 라이브러리만 사용)

주의
- UI에서 비활성화할 버튼은 **Qt Designer에서 enabled=false**로 설정해 코드 양을 최소화.
"""

import sys, os, math
from PyQt6 import uic, QtWidgets, QtCore
from PyQt6.QtWidgets import QMainWindow, QPushButton, QToolButton, QLineEdit
from PyQt6.QtGui import QFont, QFontMetrics

SIG_DIGITS = 16        # 기본 유효숫자 자릿수
FIXED_DECIMALS = None  # 고정 소수 자리수 (None이면 유효숫자 모드)

def fmt_number(x: float) -> str:
    """계산 결과를 보기 좋게 문자열로 포매팅한다.

    - 정수처럼 떨어지는 실수는 정수로 표시
    - FIXED_DECIMALS가 설정되면 고정 소수 자리수 적용
    - 그 외에는 SIG_DIGITS 유효숫자 모드 적용
    """
    if x is None:
        return ""
    if math.isfinite(x) and abs(x - int(x)) < 1e-12:
        return str(int(x))
    if FIXED_DECIMALS is not None:
        return f"{x:.{FIXED_DECIMALS}f}"
    return f"{x:.{SIG_DIGITS}g}"

# ---------------- Core Engine ----------------

class Calculator:
    """표준 계산 엔진(사칙/괄호/상수/함수/후위연산의 파서 + 평가)."""

    def __init__(self):
        """메모리와 마지막 결과(Ans)를 초기화한다."""
        self.memory = 0.0
        self.last_result = None  # Ans

    # ----- Memory API -----

    def mem_clear(self):
        """메모리를 0으로 초기화한다."""
        self.memory = 0.0

    def mem_recall(self) -> float:
        """메모리 값을 반환한다."""
        return self.memory

    def mem_add(self, x: float):
        """메모리에 x를 더한다(유효 실수만 반영)."""
        if x is not None and math.isfinite(x):
            self.memory += x

    def mem_sub(self, x: float):
        """메모리에서 x를 뺀다(유효 실수만 반영)."""
        if x is not None and math.isfinite(x):
            self.memory -= x

    # ----- Hook API (서브클래스 구현) -----

    def apply_function(self, name: str, x: float, angle_mode_rad: bool) -> float:
        """함수 호출 훅(sin/cos/tan/sinh/cosh/tanh 등). 서브클래스에서 구현."""
        raise NotImplementedError

    def apply_postfix(self, op: str, a: float) -> float:
        """후위 연산 훅(²/³/% 등). 서브클래스에서 구현."""
        raise NotImplementedError

    def const_value(self, name: str) -> float:
        """상수 값 훅(예: 'pi'). 서브클래스에서 구현."""
        raise NotImplementedError

    # ----- Pipeline -----

    def evaluate_expr(self, s: str, angle_mode_rad: bool) -> float:
        """표시식을 평가하여 숫자 결과를 반환한다.

        파이프라인:
        1) 토큰화
        2) 단항 마이너스 보정
        3) 셔닝야드로 RPN 변환
        4) RPN 스택 평가
        """
        if not s:
            raise ValueError("empty expression")
        tokens = self._fix_unary_minus(self._tokenize(s))
        rpn = self._to_rpn(tokens)
        return self._eval_rpn(rpn, angle_mode_rad)

    # ----- Tokenization -----

    def _tokenize(self, s: str):
        """문자열 s를 토큰 리스트로 변환한다(정규표현식 미사용)."""
        out, i, n = [], 0, len(s)
        is_digit = lambda ch: '0' <= ch <= '9'
        is_alpha = lambda ch: ('a' <= ch <= 'z') or ('A' <= ch <= 'Z')
        while i < n:
            ch = s[i]
            if ch in (' ', '\t'):
                i += 1; continue
            if is_digit(ch) or ch == '.':
                # 숫자(정수/실수)
                st, seen = i, (ch == '.'); i += 1
                while i < n:
                    c = s[i]
                    if is_digit(c): i += 1
                    elif c == '.':
                        if seen: break
                        seen = True; i += 1
                    else: break
                out.append(('NUM', float(s[st:i]))); continue
            if ch in '+-*/()':
                # 연산자/괄호
                out.append(('LPAREN','(') if ch=='(' else ('RPAREN',')') if ch==')' else ('OP', ch))
                i += 1; continue
            if ch == 'π':
                out.append(('CONST','pi')); i += 1; continue
            if ch in ('²','³','%'):
                out.append(('POST', ch)); i += 1; continue
            if is_alpha(ch):
                # 식별자 (함수/상수/Ans)
                st = i; i += 1
                while i < n and is_alpha(s[i]): i += 1
                low = s[st:i].lower()
                if low == 'pi': out.append(('CONST','pi'))
                elif low == 'ans': out.append(('CONST','ans'))
                else: out.append(('FUNC', low))
                continue
            raise ValueError(f"invalid char: {ch}")
        return out

    def _fix_unary_minus(self, tokens):
        """단항 마이너스를 이항으로 보정(식 시작/OP/LPAREN/FUNC 뒤 '-' → 0 - x)."""
        res, prev = [], 'START'
        for t, v in tokens:
            if t == 'OP' and v == '-' and prev in ('START','OP','LPAREN','FUNC'):
                res.append(('NUM', 0.0)); res.append(('OP','-')); prev = 'OP'; continue
            res.append((t, v))
            prev = t if t in ('NUM','CONST','RPAREN','POST','OP','LPAREN','FUNC') else 'OP'
        return res

    def _to_rpn(self, tokens):
        """셔닝야드 알고리즘으로 중위 → 후위(RPN) 변환."""
        out, st = [], []
        prec = {'+':1, '-':1, '*':2, '/':2}
        for tk in tokens:
            t, v = tk
            if t in ('NUM','CONST','POST'):
                out.append(tk)
            elif t == 'FUNC' or t == 'LPAREN':
                st.append(tk)
            elif t == 'RPAREN':
                while st and st[-1][0] != 'LPAREN':
                    out.append(st.pop())
                if not st:
                    raise ValueError("mismatched parenthesis")
                st.pop()  # '('
                if st and st[-1][0] == 'FUNC':
                    out.append(st.pop())
            elif t == 'OP':
                while st and st[-1][0] == 'OP' and prec[st[-1][1]] >= prec[v]:
                    out.append(st.pop())
                st.append(tk)
        while st:
            top = st.pop()
            if top[0] in ('LPAREN','RPAREN'):
                raise ValueError("mismatched parenthesis")
            out.append(top)
        return out

    def _eval_rpn(self, rpn, angle_mode_rad):
        """후위표기(RPN)를 스택으로 평가한다."""
        st=[]
        ops = {'+': lambda a,b: a+b, '-': lambda a,b: a-b, '*': lambda a,b: a*b, '/': lambda a,b: a/b}
        def need(n):
            if len(st) < n:
                raise ValueError("stack underflow")
        for t, v in rpn:
            if t == 'NUM':
                st.append(v)
            elif t == 'CONST':
                st.append(self.last_result if v=='ans' and self.last_result is not None
                          else (0.0 if v=='ans' else self.const_value(v)))
            elif t == 'OP':
                need(2); b = st.pop(); a = st.pop(); st.append(ops[v](a,b))
            elif t == 'FUNC':
                need(1); st.append(self.apply_function(v, st.pop(), angle_mode_rad))
            elif t == 'POST':
                need(1); st.append(self.apply_postfix(v, st.pop()))
        if len(st) != 1:
            raise ValueError("invalid expression")
        return st[0]

class EngineeringCalculator(Calculator):
    """공학 기능 구현(π, 삼각/쌍곡선 함수, 후위연산)."""

    def __init__(self):
        """기본 각도 모드는 Deg(=False)."""
        super().__init__()
        self.angle_mode_rad = False  # Deg 기본

    def const_value(self, name: str) -> float:
        """지원 상수 반환: 현재는 'pi'만."""
        if name == 'pi':
            return math.pi
        raise ValueError(f"unknown const: {name}")

    def apply_function(self, name: str, x: float, angle_mode_rad: bool) -> float:
        """함수 계산(sin/cos/tan/sinh/cosh/tanh). Deg 모드면 라디안 변환."""
        n = name.lower()
        trig = {'sin': math.sin, 'cos': math.cos, 'tan': math.tan}
        hyp  = {'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh}
        if n in trig:
            if not angle_mode_rad:
                x = math.radians(x)
            return trig[n](x)
        if n in hyp:
            return hyp[n](x)
        raise ValueError(f"function not supported: {name}")

    def apply_postfix(self, op: str, a: float) -> float:
        """후위 연산(², ³, %)을 계산한다."""
        ops = {'²': lambda x: x*x, '³': lambda x: x*x*x, '%': lambda x: x*0.01}
        try:
            return ops[op](a)
        except KeyError:
            raise ValueError(f"unknown postfix: {op}")

# ---------------- UI ----------------

class MainWindow(QMainWindow):
    """메인 윈도우: 표시/결과 디스플레이, 버튼 라우팅, UX 규칙을 관리한다."""

    FUNC_HEADERS = ("sinh(", "cosh(", "tanh(", "sin(", "cos(", "tan(")
    VALUE_TAILS = set('0123456789)') | {'π','²','³','%'}

    def __init__(self):
        """UI 로드, 디스플레이 바인딩, 자동 핸들러 라우팅을 설정한다."""
        super().__init__()
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "engineering.ui")
        uic.loadUi(ui_path, self) #`.ui` 로드: self에 위젯 바인딩

        opts = QtCore.Qt.FindChildOption.FindChildrenRecursively
        self.le_expr: QLineEdit = self.findChild(QLineEdit, "le_expr", opts)
        self.le_result: QLineEdit = self.findChild(QLineEdit, "le_result", opts)

        # 디스플레이 길이에 따른 폰트 자동 축소
        self.le_expr.textChanged.connect(lambda s: self._fit_font(self.le_expr, s))
        self.le_result.textChanged.connect(lambda s: self._fit_font(self.le_result, s))
        self._fit_font(self.le_expr, self.le_expr.text() or "")
        self._fit_font(self.le_result, self.le_result.text() or "")

        # 엔진/상태
        self.engine = EngineeringCalculator()
        self._pending_clear = False  # '=' 이후 입력 처리

        # ---------------- 핸들러 딕셔너리 구성 ----------------
        # 1) 모든 버튼 수집
        buttons = self.findChildren(QPushButton) # + self.findChildren(QToolButton)

        h = {}
        # 2) 선점: 숫자/점 (람다 기본인자로 late-binding 회피)
        h.update({f"btnn_{d}": (lambda d=d: self._append_digit(d)) for d in "0123456789"})
        h["btnn_dot"] = self._append_dot

        # 3) 선점: 삼각/쌍곡 입력 함수 (공통 처리 _insert_func)
        h.update({f"btnf_{n}": (lambda n=n: self._insert_func(n))
                  for n in ("sin","cos","tan","sinh","cosh","tanh")})

        # 4) 나머지 자동 매핑: objectName → on_btn_xxx_pressed
        # for b in buttons:
        #     name = b.objectName()
        #     if name in h:
        #         continue
        #     tail = name.split("_", 1)[-1]  # '_' 유무와 무관
        #     meth = getattr(self, f"on_btn_{tail}_pressed", None)
        #     if callable(meth):
        #         h[name] = meth

        self._handlers = h

        # # 5) 공용 클릭 라우팅(캡처로 late-binding 방지)
        for b in buttons:
            b.clicked.connect(lambda _=False, obj=b: self._handlers.get(obj.objectName(), lambda: None)())

        self._sync_rad_button_text()

    # ----- UI 유틸 -----

    def _fit_font(self, led: QLineEdit, text: str):
        """표시 길이에 따라 QLineEdit 폰트를 동적으로 줄인다."""
        length = max(1, len(text or ""))
        size = 48 if length<=19 else max(5, min(48, 900//length))
        f = led.font(); f.setBold(True); f.setPointSize(size); led.setFont(f)

    def _to_internal_expr(self, expr: str) -> str:
        """표시식을 평가용 기호로 치환한다(x/×→*, ÷→/)."""
        return expr.replace('×','*').replace('x','*').replace('÷','/')

    def _text(self) -> str:
        """현재 표시식 문자열을 반환한다."""
        return self.le_expr.text() or ""

    def _set_text(self, s: str):
        """표시식을 강제로 설정한다."""
        self.le_expr.setText(s)

    def _append(self, s: str):
        """표시식 뒤에 문자열 s를 덧붙인다."""
        self.le_expr.setText(self._text() + s)

    def _tail(self) -> str:
        """표시식의 마지막 문자(없으면 빈 문자열)를 반환한다."""
        t = self._text()
        return t[-1] if t else ""

    def _is_digit_tail(self) -> bool:
        """마지막 문자가 숫자인지 여부."""
        c = self._tail(); return '0' <= c <= '9'

    def _is_value_tail(self) -> bool:
        """마지막 문자가 '값'으로 간주되는지(숫자/닫는괄호/π/²/³/%) 여부."""
        c = self._tail(); return bool(c) and (c in self.VALUE_TAILS)

    def _maybe_mul(self):
        """값 뒤에 함수/π/여는 괄호가 오면 표시상 곱셈 x를 암시적으로 삽입한다."""
        if self._is_value_tail():
            self._append("x")

    def _clear_if_pending(self):
        """'=' 이후 첫 입력에 앞서 표시/결과를 초기화한다."""
        if self._pending_clear:
            self.le_expr.clear(); self.le_result.clear(); self._pending_clear = False

    def _seed_ans_then(self, s: str = ""):
        """'=' 직후 사칙/제곱 입력 시 Ans로 시드한 뒤 s를 덧붙인다."""
        if self._pending_clear:
            self.le_expr.setText("Ans"); self._pending_clear = False
        if s:
            self._append(s)

    # ----- 입력 핸들러 -----

    def _append_digit(self, d: str):
        """숫자 입력 처리."""
        self._clear_if_pending(); self._append(d)

    def _append_dot(self):
        """소수점 입력 처리(현재 숫자 세그먼트에 '.'가 없을 때만 삽입)."""
        self._clear_if_pending()
        t=self._text(); i=len(t)-1; seg=""
        while i>=0 and (('0'<=t[i]<='9') or t[i]=='.'):
            seg=t[i]+seg; i-=1
        if '.' not in seg:
            self._append(".")

    def _insert_func(self, name: str):
        """함수 입력 공통 처리: 암시적 곱셈 적용 후 'name('을 붙인다."""
        self._clear_if_pending(); self._maybe_mul(); self._append(name+"(")

    # ----- 버튼 메서드 (do_ → on_btn_ 변경) -----

    def on_btnc_pi_pressed(self):
        self._clear_if_pending()
        if self._is_value_tail(): self._append("x")
        self._append("π")

    def on_btnf_pow2_pressed(self):
        self._seed_ans_then("")
        if self._is_value_tail() or self._text()=="Ans":
            self._append("²")

    def on_btnf_pow3_pressed(self):
        self._seed_ans_then("")
        if self._is_value_tail() or self._text()=="Ans":
            self._append("³")

    def on_btnf_percent_pressed(self):
        self._clear_if_pending()
        if self._is_digit_tail():
            self._append("%")

    def on_btno_plus_pressed(self):  self._seed_ans_then("+")
    def on_btno_minus_pressed(self): self._seed_ans_then("-")
    def on_btno_mul_pressed(self):   self._seed_ans_then("x")
    def on_btno_div_pressed(self):   self._seed_ans_then("÷")

    def on_btno_open_paren_pressed(self):
        self._clear_if_pending()
        self._append("x(" if self._is_digit_tail() else "(")

    def on_btno_close_paren_pressed(self):
        self._clear_if_pending(); self._append(")")

    on_btn_open_pressed  = on_btno_open_paren_pressed
    on_btn_close_pressed = on_btno_close_paren_pressed

    def on_btns_ac_pressed(self):
        self._pending_clear=False; self._set_text(""); self.le_result.setText("")

    def on_btns_del_pressed(self):
        if self._pending_clear:
            self._pending_clear=False
        s=self._text()
        if not s:
            return
        for h in self.FUNC_HEADERS:
            if s.endswith(h):
                self._set_text(s[:-len(h)]); return
        self._set_text(s[:-1])

    def _auto_closed_expr(self, expr: str) -> str:
        opens = 0
        for ch in expr:
            if ch=='(':
                opens += 1
            elif ch==')' and opens>0:
                opens -= 1
        return expr + (")"*opens)

    def on_btno_equal_pressed(self):
        expr_display = self._text()
        try:
            val = self.engine.evaluate_expr(
                self._to_internal_expr(self._auto_closed_expr(expr_display)),
                self.engine.angle_mode_rad
            )
            self.engine.last_result = val
            self.le_result.setText(fmt_number(val))
        except Exception:
            self.engine.last_result = None
            self.le_result.setText("Error")
        self._pending_clear = True

    def on_btns_rad_pressed(self):
        self.engine.angle_mode_rad = not self.engine.angle_mode_rad
        self._sync_rad_button_text()

    def _sync_rad_button_text(self):
        opts = QtCore.Qt.FindChildOption.FindChildrenRecursively
        btn = (self.findChild(QPushButton, "btno_rad", opts) or
               self.findChild(QToolButton, "btno_rad", opts))
        if btn:
            btn.setText("Rad" if self.engine.angle_mode_rad else "Deg")

    def _current_value_for_memory(self):
        txt=(self.le_result.text() or "").strip()
        if txt and txt!="Error":
            try:
                return float(txt)
            except:
                pass
        expr=self._text()
        if not expr:
            return None
        try:
            e = self._to_internal_expr(self._auto_closed_expr(expr))
            return self.engine.evaluate_expr(e, self.engine.angle_mode_rad)
        except:
            return None

    def on_btns_m_c_pressed(self):
        self.engine.mem_clear()

    def on_btns_m_r_pressed(self):
        v=self.engine.mem_recall()
        if self._is_value_tail(): self._append("x")
        self._append(fmt_number(v))

    def on_btns_m_plus_pressed(self):
        self.engine.mem_add(self._current_value_for_memory())

    def on_btns_m_minus_pressed(self):
        self.engine.mem_sub(self._current_value_for_memory())



def main():
    """PyQt 애플리케이션 엔트리 포인트."""
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow(); w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
