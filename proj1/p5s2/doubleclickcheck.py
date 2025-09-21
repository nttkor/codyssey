# -*- coding: utf-8 -*-
"""
Engineering Calculator - AutoConnect Version
uic.loadUiType 사용
"""

import sys, os
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMainWindow, QLineEdit

# ---------- uic.loadUiType ----------
ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "engineering.ui")
Ui_MainWindow, QtBaseClass = uic.loadUiType(ui_path)


class MainWindow(QMainWindow, Ui_MainWindow):
    VALUE_TAILS = set('0123456789)') | {'π','²','³','%'}

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # uic.loadUiType 구조에서는 setupUi 호출 필수

        # ---------- 라인에디트 ----------
        self.le_expr: QLineEdit = self.findChild(QLineEdit, "le_expr")
        self.le_result: QLineEdit = self.findChild(QLineEdit, "le_result")
        self._pending_clear = False

    # ---------- Helper ----------
    def _text(self) -> str: return self.le_expr.text() or ""
    def _set_text(self,s:str): self.le_expr.setText(s)
    def _append(self,s:str): self._set_text(self._text()+s)
    def _tail(self)->str: return self._text()[-1] if self._text() else ""
    def _is_digit_tail(self)->bool: return '0' <= self._tail() <= '9'
    def _clear_if_pending(self):
        if self._pending_clear:
            self._set_text("")
            self.le_result.setText("")
            self._pending_clear = False
    def _maybe_mul(self):
        if self._tail() in self.VALUE_TAILS:
            self._append("x")

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
        t = self._text(); seg = ""
        i = len(t)-1
        while i>=0 and (('0' <= t[i] <= '9') or t[i]=='.'):
            seg = t[i] + seg
            i -= 1
        if '.' not in seg: self._append(".")

    # ---------- 삼각/쌍곡 함수 ----------
    def on_btnf_sin_clicked(self): self._clear_if_pending(); self._maybe_mul(); self._append("sin(")
    def on_btnf_cos_clicked(self): self._clear_if_pending(); self._maybe_mul(); self._append("cos(")
    def on_btnf_tan_clicked(self): self._clear_if_pending(); self._maybe_mul(); self._append("tan(")
    def on_btnf_sinh_clicked(self): self._clear_if_pending(); self._maybe_mul(); self._append("sinh(")
    def on_btnf_cosh_clicked(self): self._clear_if_pending(); self._maybe_mul(); self._append("cosh(")
    def on_btnf_tanh_clicked(self): self._clear_if_pending(); self._maybe_mul(); self._append("tanh(")

    # ---------- 상수 / 후위연산 ----------
    def on_btnf_pi_clicked(self): self._clear_if_pending(); self._maybe_mul(); self._append("π")
    def on_btnf_pow2_clicked(self): self._append("²")
    def on_btnf_pow3_clicked(self): self._append("³")

    # ---------- 사칙연산 ----------
    def on_btno_plus_clicked(self): self._append("+")
    def on_btno_minus_clicked(self): self._append("-")
    def on_btno_mul_clicked(self): self._append("x")
    def on_btno_div_clicked(self): self._append("÷")
    def on_btno_open_paren_clicked(self): self._append("(")
    def on_btno_close_paren_clicked(self): self._append(")")

    # ---------- 시스템 ----------
    def on_btns_ac_clicked(self): self._set_text(""); self.le_result.setText("")
    def on_btns_del_clicked(self):
        s = self._text()
        if s.endswith(("sin(", "cos(", "tan(", "sinh(", "cosh(", "tanh(")):
            self._set_text(s[:-len(s.split('(')[-1])-1])
        else:
            self._set_text(s[:-1])

def main():
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
