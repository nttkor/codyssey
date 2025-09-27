# -*- coding: utf-8 -*-
"""
engineering_calculator_eval.py
==============================

PyQt6 기반 공학용 계산기 - eval 버전
-----------------------------------

개요
----
- UI: PyQt6 + .ui 파일 로드
- 엔진: eval 기반으로 계산
    - 후위 연산: ² → **2, ³ → **3, % → *0.01
    - 표시식 기호: ×, x → *, ÷ → /
    - 함수: sin/cos/tan/sinh/cosh/tanh, 상수: pi, Ans
    - 각도 모드: Deg/Rad
- UX: '=' 이후 입력 정책, 암시적 곱셈(x), 함수 머리 DEL 통삭제, 괄호 자동 닫기
- 표시: 결과 포매팅, 폰트 자동 조절
- 메모리 기능: MC, MR, M+, M-

사용법
------
1. engineering.ui 파일과 동일 폴더에 위치
2. python engineering_calculator_eval.py 실행
3. UI 버튼 클릭으로 입력 및 계산
"""

import sys, os, math
from PyQt6 import uic, QtWidgets, QtCore
from PyQt6.QtWidgets import QMainWindow, QPushButton, QToolButton, QLineEdit

# 결과 표시 시 기본 유효숫자, 고정 소수점 여부
SIG_DIGITS = 16
FIXED_DECIMALS = None

def fmt_number(x: float) -> str:
    """계산 결과를 보기 좋게 문자열로 포맷
    
    - 정수처럼 떨어지는 실수는 정수로 표시
    - 고정 소수점(FIXED_DECIMALS) 설정 시 적용
    - 그 외는 SIG_DIGITS 유효숫자 모드
    """
    if x is None:
        return ""
    if math.isfinite(x) and abs(x - int(x)) < 1e-12:
        return str(int(x))
    if FIXED_DECIMALS is not None:
        return f"{x:.{FIXED_DECIMALS}f}"
    return f"{x:.{SIG_DIGITS}g}"

# ---------------- Engine ----------------

class Calculator:
    """eval 기반 계산기 엔진"""

    def __init__(self):
        """메모리와 마지막 결과(Ans) 초기화"""
        self.memory = 0.0
        self.last_result = None

    # ----- Memory API -----
    def mem_clear(self): self.memory = 0.0
    def mem_recall(self): return self.memory
    def mem_add(self, x):
        if x is not None and math.isfinite(x): self.memory += x
    def mem_sub(self, x):
        if x is not None and math.isfinite(x): self.memory -= x

    def evaluate_expr(self, expr: str, angle_mode_rad: bool):
        """표시식을 eval용 표현으로 변환 후 계산
        
        - 후위 연산 변환: ²→**2, ³→**3, %→*0.01
        - 표시 기호 변환: x,× → *, ÷ → /
        - 안전 eval: 함수, 상수, Ans만 로컬 딕셔너리로 허용
        - 각도 모드에 따라 trig 함수에 rad 변환 적용
        """
        if not expr: raise ValueError("empty expression")

        e = expr.replace('²','**2').replace('³','**3').replace('%','*0.01')
        e = e.replace('×','*').replace('x','*').replace('÷','/')

        # 안전하게 매핑할 함수와 상수
        local_dict = {'pi': math.pi, 'Ans': self.last_result or 0.0}
        if not angle_mode_rad:
            # Deg 모드면 rad 변환
            local_dict.update({
                'sin': lambda x: math.sin(math.radians(x)),
                'cos': lambda x: math.cos(math.radians(x)),
                'tan': lambda x: math.tan(math.radians(x)),
            })
        else:
            local_dict.update({
                'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
            })
        local_dict.update({
            'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh
        })

        try:
            val = eval(e, {"__builtins__": None}, local_dict)
        except Exception:
            raise ValueError("invalid expression")
        return val

class EngineeringCalculator(Calculator):
    """공학용 계산기 확장: 각도 모드 포함"""
    def __init__(self):
        super().__init__()
        self.angle_mode_rad = False  # Deg 기본

# ---------------- UI ----------------

class MainWindow(QMainWindow):
    """
    PyQt6 메인 윈도우
    ----------------
    - 표시식 입력: le_expr
    - 결과 표시: le_result
    - 버튼 이벤트: 자동 라우팅
    - UX: '=' 이후 처리, 암시적 곱셈, DEL 통삭제, 괄호 자동 닫기
    """
    FUNC_HEADERS = ("sinh(", "cosh(", "tanh(", "sin(", "cos(", "tan(")
    VALUE_TAILS = set('0123456789)') | {'π','²','³','%'}

    def __init__(self):
        """UI 로드, 버튼 라우팅, 디스플레이 폰트 조절"""
        super().__init__()
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "engineering.ui")
        uic.loadUi(ui_path, self)

        opts = QtCore.Qt.FindChildOption.FindChildrenRecursively
        self.le_expr: QLineEdit = self.findChild(QLineEdit, "le_expr", opts)
        self.le_result: QLineEdit = self.findChild(QLineEdit, "le_result", opts)

        # 표시 길이에 따른 폰트 자동 축소
        self.le_expr.textChanged.connect(lambda s: self._fit_font(self.le_expr, s))
        self.le_result.textChanged.connect(lambda s: self._fit_font(self.le_result, s))
        self._fit_font(self.le_expr, self.le_expr.text() or "")
        self._fit_font(self.le_result, self.le_result.text() or "")

        # 엔진 초기화
        self.engine = EngineeringCalculator()
        self._pending_clear = False  # '=' 이후 입력 초기화 플래그

        # ---------------- 버튼 라우팅 ----------------
        buttons = self.findChildren(QPushButton)
        h = {}
        # 숫자/점 버튼
        h.update({f"btnn_{d}": (lambda d=d: self._append_digit(d)) for d in "0123456789"})
        h["btnn_dot"] = self._append_dot
        # 함수 버튼
        h.update({f"btnf_{n}": (lambda n=n: self._insert_func(n))
                  for n in ("sin","cos","tan","sinh","cosh","tanh")})
        self._handlers = h

        # 버튼 클릭 시 공용 라우팅
        for b in buttons:
            b.clicked.connect(lambda _=False, obj=b: self._handlers.get(obj.objectName(), lambda: None)())

        self._sync_rad_button_text()

    # ---------------- UI 유틸 ----------------
    def _fit_font(self, led: QLineEdit, text: str):
        """텍스트 길이에 따라 폰트 크기 조정"""
        length = max(1, len(text or ""))
        size = 48 if length<=19 else max(5, min(48, 900//length))
        f = led.font(); f.setBold(True); f.setPointSize(size); led.setFont(f)

    def _text(self): return self.le_expr.text() or ""
    def _set_text(self, s): self.le_expr.setText(s)
    def _append(self, s): self.le_expr.setText(self._text()+s)
    def _tail(self): t=self._text(); return t[-1] if t else ""
    def _is_digit_tail(self): return '0'<=self._tail()<='9'
    def _is_value_tail(self): return bool(self._tail()) and self._tail() in self.VALUE_TAILS

    def _maybe_mul(self):
        """값 뒤에 함수/괄호 오면 암시적 곱셈 삽입"""
        if self._is_value_tail(): self._append("x")

    def _clear_if_pending(self):
        """'=' 이후 첫 입력 시 표시/결과 초기화"""
        if self._pending_clear:
            self.le_expr.clear(); self.le_result.clear(); self._pending_clear=False

    def _seed_ans_then(self, s=""):
        """'=' 직후 사칙/제곱 입력 시 Ans 시드 후 문자 덧붙임"""
        if self._pending_clear:
            self.le_expr.setText("Ans"); self._pending_clear=False
        if s: self._append(s)

    # ---------------- 입력 핸들러 ----------------
    def _append_digit(self,d): self._clear_if_pending(); self._append(d)
    def _append_dot(self):
        """현재 숫자 세그먼트에 '.' 없을 때만 추가"""
        self._clear_if_pending(); t=self._text(); i=len(t)-1; seg=""
        while i>=0 and (('0'<=t[i]<='9') or t[i]=='.'): seg=t[i]+seg;i-=1
        if '.' not in seg: self._append(".")
    def _insert_func(self,name): self._clear_if_pending(); self._maybe_mul(); self._append(name+"(")

    # ---------------- 버튼 메서드 ----------------
    def on_btnc_pi_pressed(self): self._clear_if_pending(); self._maybe_mul(); self._append("π")
    def on_btnf_pow2_pressed(self): self._seed_ans_then(""); self._append("²")
    def on_btnf_pow3_pressed(self): self._seed_ans_then(""); self._append("³")
    def on_btnf_percent_pressed(self): self._clear_if_pending(); self._append("%")
    def on_btno_plus_pressed(self):  self._seed_ans_then("+")
    def on_btno_minus_pressed(self): self._seed_ans_then("-")
    def on_btno_mul_pressed(self):   self._seed_ans_then("x")
    def on_btno_div_pressed(self):   self._seed_ans_then("÷")
    def on_btno_open_paren_pressed(self): self._clear_if_pending(); self._append("(" if not self._is_digit_tail() else "x(")
    def on_btno_close_paren_pressed(self): self._clear_if_pending(); self._append(")")
    on_btn_open_pressed = on_btno_open_paren_pressed
    on_btn_close_pressed = on_btno_close_paren_pressed

    def on_btns_ac_pressed(self): self._pending_clear=False; self._set_text(""); self.le_result.setText("")
    def on_btns_del_pressed(self):
        if self._pending_clear: self._pending_clear=False
        s=self._text()
        for h in self.FUNC_HEADERS:
            if s.endswith(h): self._set_text(s[:-len(h)]); return
        self._set_text(s[:-1])

    def _auto_closed_expr(self,expr):
        """열린 괄호 자동 닫기"""
        opens=0
        for ch in expr:
            if ch=='(': opens+=1
            elif ch==')' and opens>0: opens-=1
        return expr + (")"*opens)

    def on_btno_equal_pressed(self):
        """= 버튼 처리: eval 계산 후 결과 표시"""
        expr_display=self._text()
        try:
            val=self.engine.evaluate_expr(self._auto_closed_expr(expr_display),
                                          self.engine.angle_mode_rad)
            self.engine.last_result=val
            self.le_result.setText(fmt_number(val))
        except:
            self.engine.last_result=None
            self.le_result.setText("Error")
        self._pending_clear=True

    def on_btns_rad_pressed(self):
        """Deg/Rad 토글"""
        self.engine.angle_mode_rad = not self.engine.angle_mode_rad
        self._sync_rad_button_text()

    def _sync_rad_button_text(self):
        """Rad/Deg 버튼 텍스트 동기화"""
        opts = QtCore.Qt.FindChildOption.FindChildrenRecursively
        btn = (self.findChild(QPushButton,"btno_rad",opts) or
               self.findChild(QToolButton,"btno_rad",opts))
        if btn: btn.setText("Rad" if self.engine.angle_mode_rad else "Deg")

    # ---------------- Memory ----------------
    def _current_value_for_memory(self):
        txt=(self.le_result.text() or "").strip()
        if txt and txt!="Error":
            try: return float(txt)
            except: pass
        expr=self._text()
        if not expr: return None
        try: return self.engine.evaluate_expr(self._auto_closed_expr(expr),
                                             self.engine.angle_mode_rad)
        except: return None

    def on_btns_m_c_pressed(self): self.engine.mem_clear()
    def on_btns_m_r_pressed(self): v=self.engine.mem_recall(); self._maybe_mul(); self._append(fmt_number(v))
    def on_btns_m_plus_pressed(self): self.engine.mem_add(self._current_value_for_memory())
    def on_btns_m_minus_pressed(self): self.engine.mem_sub(self._current_value_for_memory())

# ---------------- Entry ----------------

def main():
    """PyQt6 애플리케이션 시작"""
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow(); w.show()
    sys.exit(app.exec())

if __name__=="__main__":
    main()
