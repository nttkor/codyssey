# -*- coding: utf-8 -*-
"""
Engineering Calculator - PyQt6 자동 연결 버전
"""

import sys, os, math
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMainWindow, QLineEdit

SIG_DIGITS = 16
FIXED_DECIMALS = None

def fmt_number(x: float) -> str:
    if x is None: return ""
    if math.isfinite(x) and abs(x - int(x)) < 1e-12: return str(int(x))
    if FIXED_DECIMALS is not None: return f"{x:.{FIXED_DECIMALS}f}"
    return f"{x:.{SIG_DIGITS}g}"

# ---------------- Core Engine ----------------

class Calculator:
    def __init__(self):
        self.memory = 0.0
        self.last_result = None

    def mem_clear(self): self.memory = 0.0
    def mem_recall(self): return self.memory
    def mem_add(self, x: float):
        if x is not None and math.isfinite(x): self.memory += x
    def mem_sub(self, x: float):
        if x is not None and math.isfinite(x): self.memory -= x

    def apply_function(self, name: str, x: float, angle_mode_rad: bool) -> float:
        raise NotImplementedError

    def apply_postfix(self, op: str, a: float) -> float:
        raise NotImplementedError

    def const_value(self, name: str) -> float:
        raise NotImplementedError

    def evaluate_expr(self, s: str, angle_mode_rad: bool) -> float:
        try:
            s = s.replace('π', str(math.pi)).replace('x','*').replace('÷','/')
            return eval(s)
        except:
            raise ValueError("invalid expression")

class EngineeringCalculator(Calculator):
    def __init__(self):
        super().__init__()
        self.angle_mode_rad = False

    def const_value(self, name: str) -> float:
        if name == 'pi': return math.pi
        raise ValueError(f"unknown const: {name}")

    def apply_function(self, name: str, x: float, angle_mode_rad: bool) -> float:
        trig = {'sin': math.sin, 'cos': math.cos, 'tan': math.tan}
        hyp  = {'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh}
        if name in trig:
            if not angle_mode_rad: x = math.radians(x)
            return trig[name](x)
        if name in hyp:
            return hyp[name](x)
        raise ValueError(f"unsupported function: {name}")

    def apply_postfix(self, op: str, a: float) -> float:
        ops = {'²': lambda x:x*x, '³': lambda x:x*x*x, '%': lambda x:x*0.01}
        return ops[op]

# ---------------- UI ----------------

class MainWindow(QMainWindow):
    FUNC_HEADERS = ("sinh(", "cosh(", "tanh(", "sin(", "cos(", "tan(")
    VALUE_TAILS = set('0123456789)') | {'π','²','³','%'}

    def __init__(self):
        super().__init__()
        ui_path = "engineering.ui"
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ui_path)
        uic.loadUi(ui_path, self)

        self.le_expr: QLineEdit = self.findChild(QLineEdit, "le_expr")
        self.le_result: QLineEdit = self.findChild(QLineEdit, "le_result")

        self.engine = EngineeringCalculator()
        self._pending_clear = False

    # ---------- Helper ----------
    def _text(self) -> str: return self.le_expr.text() or ""
    def _set_text(self,s:str): self.le_expr.setText(s)
    def _append(self,s:str): self._set_text(self._text()+s)
    def _tail(self)->str: t=self._text(); return t[-1] if t else ""
    def _is_digit_tail(self)->bool: c=self._tail(); return '0'<=c<='9'
    def _is_value_tail(self)->bool: c=self._tail(); return bool(c) and (c in self.VALUE_TAILS)
    def _clear_if_pending(self):
        if self._pending_clear: self._set_text(""); self.le_result.setText(""); self._pending_clear=False
    def _maybe_mul(self):
        if self._is_value_tail(): self._append("x")
    def _seed_ans_then(self, s:str=""):
        if self._pending_clear: self._set_text("Ans"); self._pending_clear=False
        if s: self._append(s)
    def _auto_closed_expr(self, expr:str)->str:
        opens=0
        for ch in expr:
            if ch=='(': opens+=1
            elif ch==')' and opens>0: opens-=1
        return expr + (')'*opens)

    # ---------- 숫자 / 점 ----------
    def on_btnn_0_clicked(self): self._clear_if_pending(); self._append("0")
    def on_btnn_1_clicked(self): self._clear_if_pending(); self._append("1")
    def on_btnn_2_clicked(self): self._clear_if_pending(); self._append("2")
    def on_btnn_3_clicked(self): self._clear_if_pending(); self._append("3")
    def on_btnn_4_clicked(self): self._clear_if_pending(); self._append("4")
    def on_btnn_5_clicked(self): self._clear_if_pending(); self._append("5")
    def on_btnn_6_clicked(self): self._clear_if_pending(); self._append("6")
    def on_btnn_7_clicked(self): self._clear_if_pending(); self._append("7")
    def on_btnn_8_clicked(self): self._clear_if_pending(); self._append("8")
    def on_btnn_9_clicked(self): self._clear_if_pending(); self._append("9")
    def on_btnn_dot_clicked(self):
        self._clear_if_pending()
        t=self._text();i=len(t)-1;seg=""
        while i>=0 and (('0'<=t[i]<='9') or t[i]=='.'): seg=t[i]+seg;i-=1
        if '.' not in seg: self._append('.')

    # ---------- 삼각/쌍곡 함수 ----------
    def on_btnf_sin_clicked(self): self._clear_if_pending(); self._maybe_mul(); self._append("sin(")
    def on_btnf_cos_clicked(self): self._clear_if_pending(); self._maybe_mul(); self._append("cos(")
    def on_btnf_tan_clicked(self): self._clear_if_pending(); self._maybe_mul(); self._append("tan(")
    def on_btnf_sinh_clicked(self): self._clear_if_pending(); self._maybe_mul(); self._append("sinh(")
    def on_btnf_cosh_clicked(self): self._clear_if_pending(); self._maybe_mul(); self._append("cosh(")
    def on_btnf_tanh_clicked(self): self._clear_if_pending(); self._maybe_mul(); self._append("tanh(")

    # ---------- 상수 / 후위연산 ----------
    def on_btnf_pi_clicked(self): self._clear_if_pending(); self._maybe_mul(); self._append("π")
    def on_btnf_pow2_clicked(self): self._seed_ans_then(""); self._append("²")
    def on_btnf_pow3_clicked(self): self._seed_ans_then(""); self._append("³")

    # ---------- 사칙연산 ----------
    def on_btno_plus_clicked(self): self._seed_ans_then("+")
    def on_btno_minus_clicked(self): self._seed_ans_then("-")
    def on_btno_mul_clicked(self): self._seed_ans_then("x")
    def on_btno_div_clicked(self): self._seed_ans_then("÷")
    def on_btno_open_paren_clicked(self): self._clear_if_pending(); self._append("x(" if self._is_digit_tail() else "(")
    def on_btno_close_paren_clicked(self): self._clear_if_pending(); self._append(")")

    # ---------- 시스템 ----------
    def on_btns_ac_clicked(self): self._pending_clear=False; self._set_text(""); self.le_result.setText("")
    def on_btns_del_clicked(self):
        s=self._text()
        for h in self.FUNC_HEADERS:
            if s.endswith(h): self._set_text(s[:-len(h)]); return
        self._set_text(s[:-1])
    def on_btno_percent_clicked(self): 
        self._clear_if_pending()
        if self._is_digit_tail(): self._append("%")
    def on_btno_rad_clicked(self): self.engine.angle_mode_rad = not self.engine.angle_mode_rad

    # ---------- 평가 ----------
    def on_btno_equal_clicked(self):
        expr_display = self._text()
        try:
            val = self.engine.evaluate_expr(self._auto_closed_expr(expr_display), self.engine.angle_mode_rad)
            self.engine.last_result = val
            self.le_result.setText(fmt_number(val))
        except Exception:
            self.engine.last_result = None
            self.le_result.setText("Error")
        self._pending_clear = True

# ---------- Main ----------

def main():

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow(); w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()