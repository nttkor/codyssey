# -*- coding: utf-8 -*-
"""
engineering_calculator.py (trimmed: fixed-UI, no defensive guards)

- 고정 UI 전제: 널가드/폴백 제거, 버튼 라우팅 단순화
- 기능: 사칙/괄호/Ans/π/sin~tanh/x²/x³/%/Rad↔Deg/메모리/암시적 곱셈/오토 폰트/함수머리 DEL/괄호 자동닫기
"""

import sys, os, math
from PyQt6 import uic, QtWidgets, QtCore
from PyQt6.QtWidgets import QMainWindow, QPushButton, QToolButton, QLineEdit

SIG_DIGITS = 12
FIXED_DECIMALS = None

def fmt_number(x: float) -> str:
    if x is None: return ""
    if math.isfinite(x) and abs(x - int(x)) < 1e-12: return str(int(x))
    if FIXED_DECIMALS is not None: return f"{x:.{FIXED_DECIMALS}f}"
    return f"{x:.{SIG_DIGITS}g}"

class Token:
    def __init__(self, t, v=None): self.t, self.v = t, v

class Calculator:
    def __init__(self):
        self.memory = 0.0
        self.last_result = None

    # memory
    def mem_clear(self): self.memory = 0.0
    def mem_recall(self): return self.memory
    def mem_add(self, x): 
        if x is not None and math.isfinite(x): self.memory += x
    def mem_sub(self, x): 
        if x is not None and math.isfinite(x): self.memory -= x

    # hooks
    def apply_function(self, name, x, angle_mode_rad): raise NotImplementedError
    def apply_postfix(self, op, a): raise NotImplementedError
    def const_value(self, name): raise NotImplementedError

    # evaluate
    def evaluate_expr(self, s: str, angle_mode_rad: bool) -> float:
        if not s: raise ValueError("empty expression")
        tokens = self._fix_unary_minus(self._tokenize(s))
        rpn = self._to_rpn(tokens)
        return self._eval_rpn(rpn, angle_mode_rad)

    # tokenize
    def _tokenize(self, s: str):
        out, i, n = [], 0, len(s)
        is_digit = lambda ch: '0' <= ch <= '9'
        is_alpha = lambda ch: ('a' <= ch <= 'z') or ('A' <= ch <= 'Z')
        while i < n:
            ch = s[i]
            if ch in (' ','\t'): i+=1; continue
            if is_digit(ch) or ch=='.':
                st, seen = i, (ch=='.'); i+=1
                while i<n:
                    c=s[i]
                    if is_digit(c): i+=1
                    elif c=='.':
                        if seen: break
                        seen=True; i+=1
                    else: break
                out.append(Token('NUM', float(s[st:i]))); continue
            if ch in '+-*/()':
                out.append(Token('LPAREN' if ch=='(' else 'RPAREN' if ch==')' else 'OP', ch)); i+=1; continue
            if ch=='π': out.append(Token('CONST','pi')); i+=1; continue
            if ch in ('²','³','%'): out.append(Token('POST', ch)); i+=1; continue
            if is_alpha(ch):
                st=i; i+=1
                while i<n and is_alpha(s[i]): i+=1
                low=s[st:i].lower()
                if low=='pi': out.append(Token('CONST','pi'))
                elif low=='ans': out.append(Token('CONST','ans'))
                else: out.append(Token('FUNC', low))
                continue
            raise ValueError(f"invalid char: {ch}")
        return out

    def _fix_unary_minus(self, tokens):
        res, prev = [], 'START'
        for tk in tokens:
            if tk.t=='OP' and tk.v=='-' and prev in ('START','OP','LPAREN','FUNC'):
                res.append(Token('NUM',0.0)); res.append(Token('OP','-')); prev='OP'; continue
            res.append(tk)
            prev = tk.t if tk.t in ('NUM','CONST','RPAREN','POST','OP','LPAREN','FUNC') else 'OP'
        return res

    def _to_rpn(self, tokens):
        out, st = [], []
        prec = lambda op: 1 if op in ('+','-') else 2 if op in ('*','/') else 0
        for tk in tokens:
            t = tk.t
            if t in ('NUM','CONST'): out.append(tk)
            elif t=='POST': out.append(tk)
            elif t=='FUNC': st.append(tk)
            elif t=='LPAREN': st.append(tk)
            elif t=='RPAREN':
                while st and st[-1].t!='LPAREN': out.append(st.pop())
                if not st: raise ValueError("mismatched parenthesis")
                st.pop()
                if st and st[-1].t=='FUNC': out.append(st.pop())
            elif t=='OP':
                while st and st[-1].t=='OP' and prec(st[-1].v)>=prec(tk.v): out.append(st.pop())
                st.append(tk)
        while st:
            top=st.pop()
            if top.t in ('LPAREN','RPAREN'): raise ValueError("mismatched parenthesis")
            out.append(top)
        return out

    def _eval_rpn(self, rpn, angle_mode_rad):
        st=[]
        def need(n): 
            if len(st)<n: raise ValueError("stack underflow")
        for tk in rpn:
            t=tk.t
            if t=='NUM': st.append(tk.v)
            elif t=='CONST': st.append(self.last_result if tk.v=='ans' and self.last_result is not None else (0.0 if tk.v=='ans' else self.const_value(tk.v)))
            elif t=='OP':
                need(2); b=st.pop(); a=st.pop()
                st.append(a+b if tk.v=='+' else a-b if tk.v=='-' else a*b if tk.v=='*' else a/b)
            elif t=='FUNC':
                need(1); st.append(self.apply_function(tk.v, st.pop(), angle_mode_rad))
            elif t=='POST':
                need(1); st.append(self.apply_postfix(tk.v, st.pop()))
        if len(st)!=1: raise ValueError("invalid expression")
        return st[0]

class EngineeringCalculator(Calculator):
    def __init__(self):
        super().__init__()
        self.angle_mode_rad = False  # Deg 기본

    def const_value(self, name):
        if name=='pi': return math.pi
        raise ValueError(f"unknown const: {name}")

    def apply_function(self, name, x, angle_mode_rad):
        n=name.lower()
        if n in ('sin','cos','tan'):
            if not angle_mode_rad: x = math.radians(x)
            return math.sin(x) if n=='sin' else math.cos(x) if n=='cos' else math.tan(x)
        if n=='sinh': return math.sinh(x)
        if n=='cosh': return math.cosh(x)
        if n=='tanh': return math.tanh(x)
        raise ValueError(f"function not supported: {name}")

    def apply_postfix(self, op, a):
        if op=='²': return a*a
        if op=='³': return a*a*a
        if op=='%': return a*0.01
        raise ValueError(f"unknown postfix: {op}")

class MainWindow(QMainWindow):
    FUNC_HEADERS = ["sinh(", "cosh(", "tanh(", "sin(", "cos(", "tan("]
    VALUE_TAILS = set('0123456789)') | {'π','²','³','%'}

    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "engineering.ui")
        uic.loadUi(ui_path, self)

        self.le_expr: QLineEdit = self.findChild(QLineEdit, "le_expr", QtCore.Qt.FindChildOption.FindChildrenRecursively)
        self.le_result: QLineEdit = self.findChild(QLineEdit, "le_result", QtCore.Qt.FindChildOption.FindChildrenRecursively)

        self.le_expr.textChanged.connect(lambda s: self._fit_font(self.le_expr, s))
        self.le_result.textChanged.connect(lambda s: self._fit_font(self.le_result, s))
        self._fit_font(self.le_expr, self.le_expr.text() or "")
        self._fit_font(self.le_result, self.le_result.text() or "")

        self.engine = EngineeringCalculator()
        self._pending_clear = False

        # 버튼 일괄 바인딩(고정 UI: 모든 버튼은 핸들러에 존재)
        buttons = self.findChildren(QPushButton) + self.findChildren(QToolButton)
        self._handlers = {
            # 시스템
            "btns_ac": self.do_ac,
            "btns_del": self.do_del,
            "btno_equal": self.do_equal,
            "btno_rad": self.do_rad,

            # 메모리
            "btns_m_c": self.do_m_c,
            "btns_m_r": self.do_m_r,
            "btns_m_plus": self.do_m_plus,
            "btns_m_minus": self.do_m_minus,

            # 사칙/괄호/퍼센트
            "btno_plus": self.do_plus,
            "btno_minus": self.do_minus,
            "btno_mul": self.do_mul,     # 표시용 x
            "btno_div": self.do_div,     # 표시용 ÷
            "btno_open_paren": self.do_open,
            "btno_close_paren": self.do_close,
            "btno_percent": self.do_percent,  # % (후위)

            # 숫자/소수점
            "btnn_dot": self._append_dot,
            "btnn_0": lambda: self._append_digit("0"),
            "btnn_1": lambda: self._append_digit("1"),
            "btnn_2": lambda: self._append_digit("2"),
            "btnn_3": lambda: self._append_digit("3"),
            "btnn_4": lambda: self._append_digit("4"),
            "btnn_5": lambda: self._append_digit("5"),
            "btnn_6": lambda: self._append_digit("6"),
            "btnn_7": lambda: self._append_digit("7"),
            "btnn_8": lambda: self._append_digit("8"),
            "btnn_9": lambda: self._append_digit("9"),

            # 공학 상수/후위연산/함수(구현된 것만 연결)
            "btnf_pi": self.do_pi,
            "btnf_pow2": self.do_pow2,   # x²
            "btnf_pow3": self.do_pow3,   # x³
            "btnf_sin": lambda: self._insert_func("sin"),
            "btnf_cos": lambda: self._insert_func("cos"),
            "btnf_tan": lambda: self._insert_func("tan"),
            "btnf_sinh": lambda: self._insert_func("sinh"),
            "btnf_cosh": lambda: self._insert_func("cosh"),
            "btnf_tanh": lambda: self._insert_func("tanh"),
        }

        # 나머지(미구현: 2nd, Rand, ±, EE, e^x, ln, log10, x^y, y√x, 2√x, 3√x, 1/x, e 등)는 매핑 생략 → 클릭해도 무동작(코드 간결 유지)
        for b in buttons:
            b.clicked.connect(lambda _=False, obj=b: self._handlers.get(obj.objectName(), lambda: None)())
        self._sync_rad_button_text()
        # disable_ids = [
        # # 특수 버튼
        # "btno_sign", "btns_2nd", "btns_rand",

        # # 공학 함수 중 비활성화할 것들 ui에서 설정할것 (고정 UI 전제)
        # 'btno_sign',     'btnf_log10',        'btnf_fact',        'btnf_invx',
        # 'btnf_ex',        'btnf_ee',        'btnf_yrootx',        'btnf_10pow',
        # 'btnf_sqrt3',        'btnf_sqrt2',         'btno_percent',        'btnf_e',
        # 'btns_2nd', 'btnf_ln',         'btnf_xpowy',        'btnf_fact', 'btnf_EE', 'btnf_pow_y'
        # ]
        # # 특정 버튼 비활성화 (UI 고정 전제)
        # for name in disable_ids:
        #     w = self.findChild((QPushButton, QToolButton), name,
        #                     QtCore.Qt.FindChildOption.FindChildrenRecursively)
        #     if w:
        #         w.setEnabled(False)
        #         w.setStyleSheet((w.styleSheet() or "") + "; color:#888;")

    # --- UI helpers
    def _fit_font(self, led: QLineEdit, text: str):
        length = max(1, len(text or ""))
        size = 48 if length <= 19 else max(5, min(48, 900 // length))
        f = led.font(); f.setBold(True); f.setPointSize(size); led.setFont(f)

    def _to_internal_expr(self, expr: str) -> str:
        return expr.replace('×','*').replace('x','*').replace('÷','/')

    def _text(self): return self.le_expr.text() or ""
    def _set_text(self, s: str): self.le_expr.setText(s)
    def _append(self, s: str): self.le_expr.setText(self._text() + s)

    def _ends_with_value(self):
        t=self._text(); return bool(t) and (t[-1] in self.VALUE_TAILS)
    def _ends_with_digit(self):
        t=self._text(); return bool(t) and ('0'<=t[-1]<='9')
    def _maybe_mul(self): 
        if self._ends_with_value(): self._append("x")

    # --- 입력
    def _append_digit(self, d: str):
        if self._pending_clear: self.le_expr.clear(); self.le_result.clear(); self._pending_clear=False
        self._append(d)

    def _append_dot(self):
        if self._pending_clear: self.le_expr.clear(); self.le_result.clear(); self._pending_clear=False
        t=self._text(); i=len(t)-1; seg=""
        while i>=0 and (('0'<=t[i]<='9') or t[i]=='.'): seg=t[i]+seg; i-=1
        if '.' not in seg: self._append(".")

    # --- 공학
    def _insert_func(self, name: str):
        if self._pending_clear: self.le_expr.clear(); self.le_result.clear(); self._pending_clear=False
        self._maybe_mul(); self._append(name+"(")

    def do_pi(self):
        if self._pending_clear: self.le_expr.clear(); self.le_result.clear(); self._pending_clear=False
        if self._ends_with_value(): self._append("x"); self._append("π")

    def do_pow2(self):
        if self._pending_clear: self.le_expr.setText("Ans"); self._pending_clear=False
        if self._ends_with_value() or self._text()=="Ans": self._append("²")

    def do_pow3(self):
        if self._pending_clear: self.le_expr.setText("Ans"); self._pending_clear=False
        if self._ends_with_value() or self._text()=="Ans": self._append("³")

    def do_percent(self):
        if self._pending_clear: self.le_expr.clear(); self.le_result.clear(); self._pending_clear=False
        if self._ends_with_digit(): self._append("%")

    # --- 사칙/괄호
    def do_plus(self):
        if self._pending_clear: self.le_expr.setText("Ans"); self._pending_clear=False
        self._append("+")
    def do_minus(self):
        if self._pending_clear: self.le_expr.setText("Ans"); self._pending_clear=False
        self._append("-")
    def do_mul(self):
        if self._pending_clear: self.le_expr.setText("Ans"); self._pending_clear=False
        self._append("x")
    def do_div(self):
        if self._pending_clear: self.le_expr.setText("Ans"); self._pending_clear=False
        self._append("÷")
    def do_open(self):
        if self._pending_clear: self.le_expr.clear(); self.le_result.clear(); self._pending_clear=False
        self._append("x(" if self._ends_with_digit() else "(")
    def do_close(self):
        if self._pending_clear: self.le_expr.clear(); self.le_result.clear(); self._pending_clear=False
        self._append(")")

    # --- 시스템
    def do_ac(self):
        self._pending_clear=False; self._set_text(""); self.le_result.setText("")
    def do_del(self):
        if self._pending_clear: self._pending_clear=False
        s=self._text()
        if not s: return
        for header in ("sinh(", "cosh(", "tanh(", "sin(", "cos(", "tan("):
            if s.endswith(header): self._set_text(s[:-len(header)]); return
        self._set_text(s[:-1])

    def _auto_closed_expr(self, expr: str) -> str:
        opens=0
        for ch in expr:
            if ch=='(' : opens+=1
            elif ch==')' and opens>0: opens-=1
        return expr + (")"*opens if opens>0 else "")

    def do_equal(self):
        expr_display = self._text()
        try:
            to_eval = self._to_internal_expr(self._auto_closed_expr(expr_display))
            val = self.engine.evaluate_expr(to_eval, self.engine.angle_mode_rad)
            self.engine.last_result = val
            self.le_result.setText(fmt_number(val))
        except Exception:
            self.engine.last_result = None
            self.le_result.setText("Error")
        self._pending_clear = True

    # --- 각도
    def do_rad(self):
        self.engine.angle_mode_rad = not self.engine.angle_mode_rad
        self._sync_rad_button_text()

    def _sync_rad_button_text(self):
        btn = self.findChild((QPushButton, QToolButton), "btno_rad",
                             QtCore.Qt.FindChildOption.FindChildrenRecursively)
        btn.setText("Rad" if self.engine.angle_mode_rad else "Deg")

    # --- 메모리
    def _current_value_for_memory(self):
        txt=(self.le_result.text() or "").strip()
        if txt and txt!="Error":
            try: return float(txt)
            except: pass
        expr=self._text()
        if expr:
            try:
                return self.engine.evaluate_expr(self._to_internal_expr(self._auto_closed_expr(expr)),
                                                 self.engine.angle_mode_rad)
            except: return None
        return None

    def do_m_c(self): self.engine.mem_clear()
    def do_m_r(self):
        v=self.engine.mem_recall()
        if self._ends_with_value(): self._append("x")
        self._append(fmt_number(v))
    def do_m_plus(self): self.engine.mem_add(self._current_value_for_memory())
    def do_m_minus(self): self.engine.mem_sub(self._current_value_for_memory())

def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow(); w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
