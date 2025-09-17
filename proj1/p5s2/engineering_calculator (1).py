# -*- coding: utf-8 -*-
"""
engineering_calculator.py (rev4: '=' 후 다음 입력 시 클리어)

변경점
- '=' 누를 때 le_expr/le_result를 즉시 지우지 않음.
- 대신 내부 플래그 self._pending_clear = True 로 표시.
- 이후 "표현식을 변경하는" 다음 입력(숫자/소수점/연산자/괄호/함수/π/제곱/세제곱/MR)이 들어오면
  해당 입력을 처리하기 전에 le_expr, le_result 모두 클리어하고 플래그 해제.
- DEL은 예외: 플래그가 켜져 있어도 클리어하지 않고, 기존 수식을 편집할 수 있음(플래그 해제).

나머지 요구사항 유지
- 공학함수 즉시계산형 없음, 값 뒤 함수/π는 '*' 암시적 곱셈
- del은 sin(, cos(, tan(, sinh(, cosh(, tanh( 머리를 통째 삭제(고정 접미사 비교, re 미사용)
- 미구현 함수 비활성/회색
- 메모리 MC/MR/M+/M-, 라디안/디그리 토글
- 평가기: 샌딩-야드 + RPN (eval 미사용)
"""
import sys, os, math
from PyQt6 import uic, QtWidgets, QtCore
from PyQt6.QtWidgets import QMainWindow, QPushButton, QToolButton, QLineEdit


def fmt_number(x: float) -> str:
    if x is None:
        return ""
    if math.isfinite(x) and abs(x - int(x)) < 1e-12:
        return str(int(x))
    return ("{:.12g}".format(x))


class Token:
    def __init__(self, t, v=None):
        self.t = t
        self.v = v
    def __repr__(self):
        return f"Token({self.t!r},{self.v!r})"


class Calculator:
    def __init__(self):
        self.memory = 0.0
        self.last_result = None

    def mem_clear(self):
        self.memory = 0.0
    def mem_recall(self) -> float:
        return self.memory
    def mem_add(self, x: float):
        if x is not None and math.isfinite(x):
            self.memory += x
    def mem_sub(self, x: float):
        if x is not None and math.isfinite(x):
            self.memory -= x

    def evaluate_expr(self, s: str, angle_mode_rad: bool) -> float:
        if not s:
            raise ValueError("empty expression")
        tokens = self._tokenize(s)
        tokens = self._fix_unary_minus(tokens)
        rpn = self._to_rpn(tokens)
        val = self._eval_rpn(rpn, angle_mode_rad)
        return val

    def _tokenize(self, s: str):
        tokens = []
        i, n = 0, len(s)

        def is_digit(ch): return '0' <= ch <= '9'
        def is_alpha(ch): return ('a' <= ch <= 'z') or ('A' <= ch <= 'Z')

        while i < n:
            ch = s[i]
            if ch in (' ', '\t'):
                i += 1; continue

            if is_digit(ch) or ch == '.':
                start = i; seen_dot = (ch == '.'); i += 1
                while i < n:
                    c = s[i]
                    if is_digit(c): i += 1
                    elif c == '.':
                        if seen_dot: break
                        seen_dot = True; i += 1
                    else: break
                tokens.append(Token('NUM', float(s[start:i]))); continue

            if ch in '+-*/()':
                if ch == '(': tokens.append(Token('LPAREN','('))
                elif ch == ')': tokens.append(Token('RPAREN',')'))
                else: tokens.append(Token('OP', ch))
                i += 1; continue

            if ch == 'π':
                tokens.append(Token('CONST','pi')); i += 1; continue

            if ch in ('²','³'):
                tokens.append(Token('POST', ch)); i += 1; continue

            if is_alpha(ch):
                start = i; i += 1
                while i < n and is_alpha(s[i]): i += 1
                name = s[start:i].lower()
                if name == 'pi': tokens.append(Token('CONST','pi'))
                else: tokens.append(Token('FUNC', name))
                continue

            raise ValueError(f"invalid char: {ch}")
        return tokens

    def _fix_unary_minus(self, tokens):
        res = []; prev_type = 'START'
        for tk in tokens:
            if tk.t == 'OP' and tk.v == '-':
                if prev_type in ('START','OP','LPAREN','FUNC'):
                    res.append(Token('NUM', 0.0)); res.append(Token('OP', '-'))
                else:
                    res.append(tk)
                prev_type = 'OP'; continue
            res.append(tk)
            if tk.t in ('NUM','CONST'): prev_type = tk.t
            elif tk.t in ('RPAREN','POST'): prev_type = tk.t
            elif tk.t in ('OP','LPAREN','FUNC'): prev_type = tk.t
            else: prev_type = 'OP'
        return res

    def _to_rpn(self, tokens):
        out = []; st = []
        def prec(op):
            if op in ('+','-'): return 1
            if op in ('*','/'): return 2
            return 0
        for tk in tokens:
            if tk.t in ('NUM','CONST'): out.append(tk)
            elif tk.t == 'POST': out.append(tk)
            elif tk.t == 'FUNC': st.append(tk)
            elif tk.t == 'LPAREN': st.append(tk)
            elif tk.t == 'RPAREN':
                while st and st[-1].t != 'LPAREN': out.append(st.pop())
                if not st: raise ValueError("mismatched parenthesis")
                st.pop()
                if st and st[-1].t == 'FUNC': out.append(st.pop())
            elif tk.t == 'OP':
                while st and st[-1].t == 'OP' and prec(st[-1].v) >= prec(tk.v): out.append(st.pop())
                st.append(tk)
            else: raise ValueError("unknown token type")
        while st:
            top = st.pop()
            if top.t in ('LPAREN','RPAREN'): raise ValueError("mismatched parenthesis")
            out.append(top)
        return out

    def _eval_rpn(self, rpn, angle_mode_rad: bool) -> float:
        st = []
        def need(n):
            if len(st) < n: raise ValueError("stack underflow")
        for tk in rpn:
            if tk.t == 'NUM': st.append(tk.v)
            elif tk.t == 'CONST':
                if tk.v == 'pi': st.append(math.pi)
                else: raise ValueError("unknown const")
            elif tk.t == 'OP':
                need(2); b = st.pop(); a = st.pop()
                if tk.v == '+': st.append(a + b)
                elif tk.v == '-': st.append(a - b)
                elif tk.v == '*': st.append(a * b)
                elif tk.v == '/': st.append(a / b)
                else: raise ValueError("unknown op")
            elif tk.t == 'FUNC':
                need(1); x = st.pop(); name = tk.v
                if name in ('sin','cos','tan'):
                    if not angle_mode_rad: x = math.radians(x)
                    if name == 'sin': st.append(math.sin(x))
                    elif name == 'cos': st.append(math.cos(x))
                    else: st.append(math.tan(x))
                elif name == 'sinh': st.append(math.sinh(x))
                elif name == 'cosh': st.append(math.cosh(x))
                elif name == 'tanh': st.append(math.tanh(x))
                else: raise ValueError("function not supported")
            elif tk.t == 'POST':
                need(1); a = st.pop()
                if tk.v == '²': st.append(a * a)
                elif tk.v == '³': st.append(a * a * a)
                else: raise ValueError("unknown postfix")
            else: raise ValueError("unknown token in rpn")
        if len(st) != 1: raise ValueError("invalid expression")
        return st[0]


class EngineeringCalculator(Calculator):
    def __init__(self):
        super().__init__()
        self.angle_mode_rad = True  # True=Rad, False=Deg


class MainWindow(QMainWindow):
    ENABLED_FUNCS = {"sin","cos","tan","sinh","cosh","tanh","pi","pow2","pow3"}
    FUNC_HEADERS = ["sinh(", "cosh(", "tanh(", "sin(", "cos(", "tan("]
    VALUE_TAILS = set('0123456789)') | {'π', '²', '³'}

    def __init__(self):
        super().__init__()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(base_dir, "engineering.ui")
        uic.loadUi(ui_path, self)

        opts = QtCore.Qt.FindChildOption.FindChildrenRecursively
        self.le_expr: QLineEdit = self.findChild(QLineEdit, "le_expr", opts)
        self.le_result: QLineEdit = self.findChild(QLineEdit, "le_result", opts)

        self.engine = EngineeringCalculator()
        self.inv_mode = False  # 라벨만 유지
        self._pending_clear = False  # '=' 후 다음 입력에서 클리어

        self._bind_all_buttons()
        self._disable_unimplemented_functions()
        self._sync_rad_button_text()

    # ----------------- 공통: 다음 입력에서 클리어 처리 -----------------
    def _prepare_for_input(self, will_modify_expr: bool):
        """
        will_modify_expr=True 인 입력(숫자/점/연산/괄호/함수/π/제곱/세제곱/MR 등) 전에 호출.
        self._pending_clear 가 True면 le_expr, le_result를 비우고 플래그 해제.
        DEL은 will_modify_expr=False로 호출하여 기존 수식을 유지/편집 가능.
        """
        if will_modify_expr and self._pending_clear:
            self.le_expr.clear()
            self.le_result.clear()
            self._pending_clear = False

    # ----------------- 바인딩 -----------------
    def _bind_all_buttons(self):
        for w in self.findChildren(QPushButton) + self.findChildren(QToolButton):
            name = w.objectName()
            if not name: continue
            w.clicked.connect(lambda _=False, b=w: self.on_button_clicked(b))

    def _disable_unimplemented_functions(self):
        for w in self.findChildren(QPushButton) + self.findChildren(QToolButton):
            name = w.objectName() or ""
            if not name.startswith("btnf_"): continue
            key = name.split("_",1)[1]
            key = self._alias(key)
            if key not in self.ENABLED_FUNCS:
                w.setEnabled(False)
                try:
                    old = w.styleSheet() or ""
                    w.setStyleSheet(old + "; color:#888;")
                except Exception:
                    pass

    # ----------------- 디스패치 -----------------
    def on_button_clicked(self, btn):
        name = btn.objectName() or ""
        if "_" not in name: return
        prefix, key = name.split("_",1)
        key = self._alias(key)

        # 숫자/소수점
        if prefix == "btnn":
            if key.isdigit(): self._append_digit(key); return
            if key in (".","dot","point","decimal"): self._append_dot(); return

        # 공학 함수
        if prefix == "btnf":
            handler = getattr(self, f"do_{key}", None)
            if callable(handler): handler(); return

        # 연산/시스템 포함
        handler = getattr(self, f"do_{key}", None)
        if callable(handler): handler(); return

        if key in ("plus","minus","mul","div","open","close","equal"):
            getattr(self, f"do_{key}")()

    # ----------------- 별칭 -----------------
    def _alias(self, key: str) -> str:
        k = key.lower()
        if k in {"+","add","plus"}: return "plus"
        if k in {"-","sub","minus"}: return "minus"
        if k in {"*","x","times","mul"}: return "mul"
        if k in {"/","÷","div","divide"}: return "div"
        if k in {"(","open","lparen"}: return "open"
        if k in {")","close","rparen"}: return "close"
        if k in {"=","eq","equal"}: return "equal"
        if k in {"dot",".","point","decimal"}: return "dot"
        if k in {"mc","m_c","mclear"}: return "m_c"
        if k in {"mr","m_r"}: return "m_r"
        if k in {"m+","mplus","m_add"}: return "m_plus"
        if k in {"m-","mminus","m_sub"}: return "m_minus"
        if k in {"pi","π"}: return "pi"
        if k in {"x2","square","sqr","pow2"}: return "pow2"
        if k in {"x3","cube","pow3"}: return "pow3"
        return k

    # ----------------- 입력 구성 -----------------
    def _text(self) -> str: return self.le_expr.text() or ""
    def _set_text(self, s: str): self.le_expr.setText(s)
    def _append(self, s: str): self.le_expr.setText(self._text() + s)
    def _ends_with_value(self) -> bool:
        t = self._text()
        return bool(t) and (t[-1] in self.VALUE_TAILS)

    def _maybe_mul(self):
        if self._ends_with_value():
            self._append("*")

    def _append_digit(self, d: str):
        self._prepare_for_input(True)
        self._append(d)

    def _append_dot(self):
        self._prepare_for_input(True)
        t = self._text(); i = len(t)-1; seg = ""
        while i >= 0 and (('0' <= t[i] <= '9') or t[i] == '.'):
            seg = t[i] + seg; i -= 1
        if '.' in seg: return
        self._append(".")

    # ----------------- 공학 함수/상수 -----------------
    def insert_function(self, name: str):
        self._prepare_for_input(True)
        self._maybe_mul()
        self._append(name + "(")

    def do_sin(self):  self.insert_function("sin")
    def do_cos(self):  self.insert_function("cos")
    def do_tan(self):  self.insert_function("tan")
    def do_sinh(self): self.insert_function("sinh")
    def do_cosh(self): self.insert_function("cosh")
    def do_tanh(self): self.insert_function("tanh")

    def do_pi(self):
        self._prepare_for_input(True)
        if self._ends_with_value():
            self._append("*")
        self._append("π")

    def do_pow2(self):
        self._prepare_for_input(True)
        if self._ends_with_value():
            self._append("²")

    def do_pow3(self):
        self._prepare_for_input(True)
        if self._ends_with_value():
            self._append("³")

    # ----------------- 일반 연산 -----------------
    def do_plus(self):  self._prepare_for_input(True); self._append("+")
    def do_minus(self): self._prepare_for_input(True); self._append("-")
    def do_mul(self):   self._prepare_for_input(True); self._append("*")
    def do_div(self):   self._prepare_for_input(True); self._append("/")
    def do_open(self):  self._prepare_for_input(True); self._append("(")
    def do_close(self): self._prepare_for_input(True); self._append(")")

    # ----------------- 시스템 -----------------
    def do_ac(self):
        # AC는 무조건 전부 초기화
        self._pending_clear = False
        self._set_text("")
        self.le_result.setText("")

    def do_del(self):
        # DEL은 다음입력시클리어를 해제하고, 즉시 클리어하지 않음
        if self._pending_clear:
            self._pending_clear = False
        s = self._text()
        if not s: return
        for header in sorted(self.FUNC_HEADERS, key=len, reverse=True):
            if s.endswith(header):
                self._set_text(s[:-len(header)]); return
        if s.endswith("²") or s.endswith("³"):
            self._set_text(s[:-1]); return
        self._set_text(s[:-1])

    def do_equal(self):
        expr = self._text()
        try:
            val = self.engine.evaluate_expr(expr, self.engine.angle_mode_rad)
            self.engine.last_result = val
            self.le_result.setText(fmt_number(val))
        except Exception:
            self.engine.last_result = None
            self.le_result.setText("Error")
        # 여기서는 expr/result를 지우지 않음.
        # 다음 입력이 표현식을 변경하려고 할 때 클리어되도록 플래그만 세팅
        self._pending_clear = True

    # ----------------- 각도 모드 -----------------
    def do_rad(self):
        self.engine.angle_mode_rad = not self.engine.angle_mode_rad
        self._sync_rad_button_text()
    def _sync_rad_button_text(self):
        btn = self.findChild((QPushButton, QToolButton), "btno_rad",
                             QtCore.Qt.FindChildOption.FindChildrenRecursively)
        if btn:
            btn.setText("Rad" if self.engine.angle_mode_rad else "Deg")

    # ----------------- 메모리 -----------------
    def _current_value_for_memory(self):
        txt = (self.le_result.text() or "").strip()
        if txt and txt != "Error":
            try: return float(txt)
            except Exception: pass
        expr = self._text()
        if expr:
            try: return self.engine.evaluate_expr(expr, self.engine.angle_mode_rad)
            except Exception: return None
        return None

    def do_m_c(self):
        self.engine.mem_clear()

    def do_m_r(self):
        # MR은 표현식을 "변경"하므로 next-input 클리어 대상으로 취급
        self._prepare_for_input(True)
        v = self.engine.mem_recall()
        if self._ends_with_value(): self._append("*")
        self._append(fmt_number(v))

    def do_m_plus(self):
        v = self._current_value_for_memory()
        self.engine.mem_add(v)

    def do_m_minus(self):
        v = self._current_value_for_memory()
        self.engine.mem_sub(v)


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
