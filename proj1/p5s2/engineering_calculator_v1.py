# -*- coding: utf-8 -*-
"""
engineering_calculator_textbind.py
- Minimal & robust: bind all buttons by their VISIBLE TEXT (no objectName rules needed).
- No try/except.
- Chooses UI file by existence: engineering_renamed.ui -> engineering.ui.
- Supports QPushButton and QToolButton.
- ENABLE_EVAL toggles very simple evaluation on '='.
"""

import sys
import math
from pathlib import Path
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMainWindow, QPushButton, QToolButton, QLineEdit

# ---- config ----
CANDIDATES = ["engineering_renamed.ui", "engineering.ui"]
UI_FILE = next((f for f in CANDIDATES if Path(f).exists()), CANDIDATES[-1])
ENABLE_EVAL = True  # True to enable very simple evaluation

# functions that should append "(" automatically
FUNC_WITH_PAREN = {
    "sin","cos","tan","asin","acos","atan",
    "sinh","cosh","tanh",
    "ln","log","log₁₀","log10","sqrt","abs","floor","ceil",
    "pow","rand","exp","ee"
}

class Calculator:
    def __init__(self):
        self.current = ""

    def clear(self):
        self.current = ""

    def append(self, s: str):
        self.current += s

    def set(self, s: str):
        self.current = s

    def get(self) -> str:
        return self.current


class EngineeringApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_FILE, self)  # assume top-level QMainWindow

        self.display: QLineEdit = self.findChild(QLineEdit, "le_display")

        self.calc = Calculator()

        # bind all buttons by text only
        for btn in self.findChildren(QPushButton):
            btn.clicked.connect(lambda _, b=btn: self.on_clicked(b.text()))
        for btn in self.findChildren(QToolButton):
            btn.clicked.connect(lambda _, b=btn: self.on_clicked(b.text()))

        self.refresh()

    def refresh(self):
        self.display.setText(self.calc.get())

    def on_clicked(self, t: str):
        t = t.strip()
        if not t:
            return
        low = t.lower()

        if low == "ac":
            self.calc.clear()
            self.refresh()
            return

        if t == "=":
            if ENABLE_EVAL:
                self.evaluate_now()
            else:
                self.calc.append(t)
                self.refresh()
            return

        # auto "( " for common functions
        if low in FUNC_WITH_PAREN:
            self.calc.append(t if t.endswith("(") else (t + "("))
        else:
            self.calc.append(t)

        self.refresh()

    def evaluate_now(self):
        expr = self.calc.get()
        # normalize a few tokens
        expr = expr.replace("×", "*").replace("x", "*").replace("÷", "/")
        expr = expr.replace("π", "pi").replace("√", "sqrt").replace("log₁₀", "log10")

        # balance parentheses (naive)
        opens, closes = expr.count("("), expr.count(")")
        if opens > closes:
            expr += ")" * (opens - closes)

        safe = {k: getattr(math, k) for k in ("sin","cos","tan","sinh","cosh","tanh","sqrt","log","log10","exp","pi","e")}
        def square(x): return x*x
        def cube(x): return x*x*x
        def inv(x): return 1.0/x
        def fact(x): return math.factorial(int(x))
        safe.update({"square":square, "cube":cube, "inv":inv, "fact":fact})

        result = eval(expr, {"__builtins__": {}}, safe)
        self.calc.set(str(result))
        self.refresh()


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = EngineeringApp()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
