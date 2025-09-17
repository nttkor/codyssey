# -*- coding: utf-8 -*-
"""
engineering_calculator.py
- Loads a Qt Designer .ui (engineering_renamed.ui preferred; falls back to engineering.ui)
- Binds buttons using the agreed header scheme: btnn_, btno_, btnf_, btns_, btnk_
- Shows a simple, easy-to-read structure:
    Calculator -> EngineeringCalculator
- Memory buttons intentionally omitted per requirement.
- Actual evaluation can be toggled with ENABLE_EVAL. By default it's False (display-only).
"""

import sys
import re
import math
from typing import Callable, Dict, Optional
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QPushButton, QLineEdit, QWidget

# === Toggle: if True, pressing '=' will try to evaluate the display text (very basic).
ENABLE_EVAL = False


# -----------------------------
# Core calculator classes
# -----------------------------
class Calculator:
    """Base calculator with minimal state and helpers."""
    def __init__(self):
        self.current: str = ""

    def clear(self):
        self.current = ""

    def input_text(self, s: str):
        self.current += s

    def set_text(self, s: str):
        self.current = s

    def get_text(self) -> str:
        return self.current


class EngineeringCalculator(Calculator):
    """Scientific functions (math module only)."""

    # --- Trig ---
    def sin(self, x: float) -> float:
        return math.sin(x)

    def cos(self, x: float) -> float:
        return math.cos(x)

    def tan(self, x: float) -> float:
        return math.tan(x)

    # --- Hyperbolic ---
    def sinh(self, x: float) -> float:
        return math.sinh(x)

    def cosh(self, x: float) -> float:
        return math.cosh(x)

    def tanh(self, x: float) -> float:
        return math.tanh(x)

    # --- Powers ---
    def square(self, x: float) -> float:
        return x * x

    def cube(self, x: float) -> float:
        return x * x * x

    # --- Constants ---
    def pi(self) -> float:
        return math.pi

    def e(self) -> float:
        return math.e


# -----------------------------
# UI glue and event bindings
# -----------------------------
class EngineeringApp(QWidget):
    """
    Loads the .ui and wires up all QPushButtons.
    Button naming scheme:
        btnn_<...>  : numbers
        btno_<...>  : operators (add, sub, mul, div, eq, dot, lparen, rparen, percent, sign)
        btnf_<...>  : functions (sin, cos, tan, sinh, cosh, tanh, log, ln, sqrt, pow, exp, pow10, square, cube, inv, fact, etc.)
        btns_<...>  : system (ac, mode, 2nd, rad, ...)
        btnk_<...>  : constants (pi, e)
    """
    def __init__(self, ui_path: Optional[str] = None):
        super().__init__()

        # Load UI (prefer renamed file, else original)
        preferred = ui_path or "engineering_renamed.ui"
        fallback = "engineering.ui"
        try:
            self.ui = uic.loadUi(preferred, self)
        except Exception:
            self.ui = uic.loadUi(fallback, self)

        # display widget (assume objectName is le_display from the provided UI)
        self.display: Optional[QLineEdit] = self.findChild(QLineEdit, "le_display")
        if self.display is None:
            # try a few common names
            for name in ("display", "lineEdit", "input", "disp_main"):
                self.display = self.findChild(QLineEdit, name)
                if self.display:
                    break
        if self.display is None:
            raise RuntimeError("Display QLineEdit (le_display) not found in UI.")

        # model
        self.calc = EngineeringCalculator()

        # dispatcher maps
        self.handlers: Dict[str, Callable[[QPushButton], None]] = {
            "btnn": self.handle_number_like,
            "btno": self.handle_operator_like,
            "btnf": self.handle_function_like,
            "btns": self.handle_system,
            "btnk": self.handle_constant,
        }

        # wire all QPushButtons
        for btn in self.findChildren(QPushButton):
            name = btn.objectName() or ""
            # pick handler by header (split at first underscore)
            header = name.split("_", 1)[0] if "_" in name else name
            handler = self.handlers.get(header)
            if handler is not None:
                btn.clicked.connect(lambda _, b=btn, h=handler: h(b))

        # ensure display shows current state
        self.refresh_display()

    # --- UI helpers ---
    def append_to_display(self, s: str):
        self.calc.input_text(s)
        self.refresh_display()

    def set_display(self, s: str):
        self.calc.set_text(s)
        self.refresh_display()

    def refresh_display(self):
        self.display.setText(self.calc.get_text())

    # --- Handlers ---
    def handle_number_like(self, btn: QPushButton):
        """btnn_* -> append visible text directly (e.g., '7')."""
        self.append_to_display(btn.text())

    def handle_operator_like(self, btn: QPushButton):
        """
        btno_* -> append the operator text.
        Special cases:
            '='  -> evaluate (if ENABLE_EVAL), else ignore or just keep '='
            '+/-' or '±' -> toggle sign of the current number token (simple heuristic)
        """
        text = btn.text()
        if text in ("=",):
            if ENABLE_EVAL:
                self.try_evaluate()
            else:
                # just show '=' as literal or ignore; we append literal to keep Problem 3 behavior compatible
                self.append_to_display(text)
            return

        if text in ("+/-", "±"):
            self.toggle_sign()
            return

        self.append_to_display(text)

    def handle_function_like(self, btn: QPushButton):
        """
        btnf_* -> by default append 'label(' to help user continue typing.
        e.g., 'sin' -> 'sin(' ; 'log₁₀' -> 'log₁₀(' ; 'Rand' -> 'Rand('
        """
        label = btn.text().strip()
        # protect if label already ends with '('
        token = label if label.endswith("(") else (label + "(")
        self.append_to_display(token)

    def handle_system(self, btn: QPushButton):
        """
        btns_* -> minimal set:
            AC -> clear
            others (mode, 2nd, rad, etc.) are UI-only here.
        """
        label = btn.text().strip().lower()
        if label == "ac":
            self.calc.clear()
            self.refresh_display()
            return

        # For other system keys, append literal (keeps Problem 3 behavior simple)
        self.append_to_display(btn.text())

    def handle_constant(self, btn: QPushButton):
        """
        btnk_* -> 'π' or 'e' text appended as-is.
        """
        self.append_to_display(btn.text())

    # --- Utility actions ---
    def toggle_sign(self):
        """
        Very simple sign toggle: find the last number in the display and flip its sign by
        prefixing/removing a leading '-'.
        """
        s = self.calc.get_text()
        # match last numeric token (optional decimal, scientific E ignored for simplicity)
        m = list(re.finditer(r"(\-?\d+(?:\.\d+)?)", s))
        if not m:
            # no number -> just prefix a '-' at the end as a hint
            self.append_to_display("-")
            return
        start, end = m[-1].span()
        num = m[-1].group(1)
        if num.startswith("-"):
            new_num = num[1:]
        else:
            new_num = "-" + num
        new_s = s[:start] + new_num + s[end:]
        self.set_display(new_s)

    def try_evaluate(self):
        """
        Extremely basic evaluation (optional). Replaces some unicode operators with Python equivalents,
        maps common math function names to math. Use with caution; intended for quick demo only.
        """
        expr = self.calc.get_text()
        if not expr:
            return

        # normalize operators and tokens
        replacements = {
            "×": "*",
            "x": "*",   # per project decision, 'x' key means multiply
            "÷": "/",
            "π": "pi",
            "√": "sqrt",
            "log₁₀": "log10",
        }
        for k, v in replacements.items():
            expr = expr.replace(k, v)

        # close any unclosed '(' to reduce eval errors (naive)
        # count '(' and ')' and pad with ')' if needed
        opens = expr.count("(")
        closes = expr.count(")")
        if opens > closes:
            expr = expr + (")" * (opens - closes))

        # Build a safe namespace exposing only math and some aliases
        safe = {
            k: getattr(math, k)
            for k in ("sin", "cos", "tan", "sinh", "cosh", "tanh",
                      "sqrt", "log", "log10", "exp", "pi", "e")
        }
        # custom helpers
        def square(x): return x * x
        def cube(x): return x * x * x
        def inv(x): return 1.0 / x
        def fact(x): return math.factorial(int(x))

        safe.update({
            "square": square,
            "cube": cube,
            "inv": inv,
            "fact": fact,
        })

        try:
            result = eval(expr, {"__builtins__": {}}, safe)  # noqa: S307 (intentional, controlled env)
            self.set_display(str(result))
        except Exception:
            # keep it silent per "no warning messages"; show '=' effect as literal fallback
            self.append_to_display("=")


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = EngineeringApp()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
