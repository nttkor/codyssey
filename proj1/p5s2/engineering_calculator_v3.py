# -*- coding: utf-8 -*-
"""
engineering_calculator_eval_final.py
------------------------------------
PyQt6 공학용 계산기 (최종 완전 버전)
- 숫자 버튼/함수 버튼 개별 메서드
- eval 기반 계산
- 정규식 변환으로 후위 연산/기호 처리
- '=' 이후 처리, 암시적 곱셈, DEL 통삭제, 괄호 자동 닫기
- 메모리 기능, Deg/Rad 모드, Ans 유지
- 중복 클릭 연결 문제 제거
"""

import sys, os, math, re  # 표준 라이브러리
from PyQt6 import uic, QtWidgets, QtCore  # PyQt6 UI 모듈
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLineEdit  # UI 위젯

SIG_DIGITS = 16  # 유효 숫자 자리수
FIXED_DECIMALS = None  # 소수점 고정

def fmt_number(x: float) -> str:  # 숫자 포맷팅
    if x is None: return ""  # None → 빈 문자열
    if math.isfinite(x) and abs(x - int(x)) < 1e-12: return str(int(x))  # 정수형 처리
    if FIXED_DECIMALS is not None: return f"{x:.{FIXED_DECIMALS}f}"  # 고정 소수점
    return f"{x:.{SIG_DIGITS}g}"  # 일반 실수 포맷

# ---------------- Engine ----------------

class Calculator:  # 계산기 엔진
    def __init__(self):
        self.memory = 0.0  # 메모리 초기화
        self.last_result = None  # 마지막 결과 초기화

    def mem_clear(self): self.memory = 0.0  # 메모리 삭제
    def mem_recall(self): return self.memory  # 메모리 불러오기
    def mem_add(self, x):  # 메모리 더하기
        if x is not None and math.isfinite(x): self.memory += x
    def mem_sub(self, x):  # 메모리 빼기
        if x is not None and math.isfinite(x): self.memory -= x

    def evaluate_expr(self, expr: str, angle_mode_rad: bool):  # 수식 평가
        if not expr: raise ValueError("empty expression")  # 빈 문자열 체크
        # 정규식 변환
        expr = re.sub(r'²', '**2', expr)  # 제곱2 변환
        expr = re.sub(r'³', '**3', expr)  # 제곱3 변환
        expr = re.sub(r'%', '*0.01', expr)  # % → 0.01 곱
        expr = re.sub(r'[×x]', '*', expr)  # X → *
        expr = re.sub(r'÷', '/', expr)  # ÷ → /
        expr = re.sub(r'π', 'pi', expr)  # π → math.pi
        # 암시적 곱셈 처리
        expr = re.sub(r'(\d)(?=[a-zA-Z(π])', r'\1*', expr)
        expr = re.sub(r'(\))(?=\d)', r'\1*', expr)

        local_dict = {'pi': math.pi, 'Ans': self.last_result or 0.0}  # 상수, Ans
        if not angle_mode_rad:  # DEG 모드
            local_dict.update({
                'sin': lambda x: math.sin(math.radians(x)),  # DEG → RAD
                'cos': lambda x: math.cos(math.radians(x)),
                'tan': lambda x: math.tan(math.radians(x)),
            })
        else:  # RAD 모드
            local_dict.update({'sin': math.sin, 'cos': math.cos, 'tan': math.tan})
        local_dict.update({'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh})  # 쌍곡선

        try:
            val = eval(expr, {"__builtins__": None}, local_dict)  # 안전 eval
        except Exception:
            raise ValueError("invalid expression")  # 오류 처리
        return val  # 결과 반환

class EngineeringCalculator(Calculator):  # 공학용 확장
    def __init__(self):
        super().__init__()
        self.angle_mode_rad = False  # 기본 DEG 모드

# ---------------- UI ----------------

class MainWindow(QMainWindow):
    FUNC_HEADERS = ("sinh(", "cosh(", "tanh(", "sin(", "cos(", "tan(")  # 함수 헤더
    VALUE_TAILS = set('0123456789)') | {'π','²','³','%'}  # 값 끝 문자

    def __init__(self):
        super().__init__()
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "engineering.ui")  # UI 파일
        uic.loadUi(ui_path, self)  # UI 로드

        opts = QtCore.Qt.FindChildOption.FindChildrenRecursively
        self.le_expr: QLineEdit = self.findChild(QLineEdit, "le_expr", opts)  # 수식 입력
        self.le_result: QLineEdit = self.findChild(QLineEdit, "le_result", opts)  # 결과 표시
        self.le_expr.textChanged.connect(lambda s: self._fit_font(self.le_expr, s))  # 폰트 자동
        self.le_result.textChanged.connect(lambda s: self._fit_font(self.le_result, s))
        self._fit_font(self.le_expr, self.le_expr.text() or "")  # 초기 폰트
        self._fit_font(self.le_result, self.le_result.text() or "")

        self.engine = EngineeringCalculator()  # 엔진 생성
        self._pending_clear = False  # = 후 초기화 플래그

        self._sync_rad_button_text()  # RAD/DEG 표시

    # ---------------- UI 유틸 ----------------
    def _fit_font(self, led: QLineEdit, text: str):  # 폰트 크기 조정
        length = max(1, len(text or ""))
        size = 48 if length<=19 else max(5, min(48, 900//length))
        f = led.font(); f.setBold(True); f.setPointSize(size); led.setFont(f)
    def _text(self): return self.le_expr.text() or ""  # 수식 가져오기
    def _set_text(self, s): self.le_expr.setText(s)  # 수식 설정
    def _append(self, s): self.le_expr.setText(self._text()+s)  # 수식 추가
    def _tail(self): t=self._text(); return t[-1] if t else ""  # 마지막 문자
    def _is_digit_tail(self): return '0'<=self._tail()<='9'  # 숫자 끝 체크
    def _is_value_tail(self): return bool(self._tail()) and self._tail() in self.VALUE_TAILS  # 값 끝 체크
    def _maybe_mul(self):
        if self._is_value_tail(): self._append("*")  # 암시적 곱
    def _clear_if_pending(self):
        if self._pending_clear: self.le_expr.clear(); self.le_result.clear(); self._pending_clear=False  # = 후 클리어
    def _seed_ans_then(self, s=""):
        if self._pending_clear: self.le_expr.setText("Ans"); self._pending_clear=False  # Ans 삽입
        if s: self._append(s)  # 추가
    def _auto_closed_expr(self,expr):
        opens=0
        for ch in expr:
            if ch=='(': opens+=1  # 열린 괄호 카운트
            elif ch==')' and opens>0: opens-=1  # 닫힌 괄호 감소
        return expr + (")"*opens)  # 괄호 자동 닫기

    # ---------------- 숫자 버튼 ----------------
    def _append_digit(self,d): self._clear_if_pending(); self._append(d)  # 숫자 입력
    def _append_dot(self):
        self._clear_if_pending()
        t=self._text(); i=len(t)-1; seg=""
        while i>=0 and (('0'<=t[i]<='9') or t[i]=='.'): seg=t[i]+seg; i-=1
        if '.' not in seg: self._append(".")  # 소수점 입력

    def on_btnn_0_pressed(self): self._append_digit("0")  # 0 버튼
    def on_btnn_1_pressed(self): self._append_digit("1")  # 1 버튼
    def on_btnn_2_pressed(self): self._append_digit("2")
    def on_btnn_3_pressed(self): self._append_digit("3")
    def on_btnn_4_pressed(self): self._append_digit("4")
    def on_btnn_5_pressed(self): self._append_digit("5")
    def on_btnn_6_pressed(self): self._append_digit("6")
    def on_btnn_7_pressed(self): self._append_digit("7")
    def on_btnn_8_pressed(self): self._append_digit("8")
    def on_btnn_9_pressed(self): self._append_digit("9")
    def on_btnn_dot_pressed(self): self._append_dot()  # . 버튼

    # ---------------- 함수 버튼 ----------------
    def _insert_func(self,name): self._clear_if_pending(); self._maybe_mul(); self._append(name+"(")  # 함수 삽입
    def on_btnf_sin_pressed(self): self._insert_func("sin")
    def on_btnf_cos_pressed(self): self._insert_func("cos")
    def on_btnf_tan_pressed(self): self._insert_func("tan")
    def on_btnf_sinh_pressed(self): self._insert_func("sinh")
    def on_btnf_cosh_pressed(self): self._insert_func("cosh")
    def on_btnf_tanh_pressed(self): self._insert_func("tanh")

    # ---------------- 연산/괄호 ----------------
    def on_btnc_pi_pressed(self): self._clear_if_pending(); self._maybe_mul(); self._append("π")  # π 입력
    def on_btnf_pow2_pressed(self): self._seed_ans_then(""); self._append("²")  # 제곱2
    def on_btnf_pow3_pressed(self): self._seed_ans_then(""); self._append("³")  # 제곱3
    def on_btnf_percent_pressed(self): self._clear_if_pending(); self._append("%")  # % 입력
    def on_btno_plus_pressed(self): self._seed_ans_then("+")  # + 입력
    def on_btno_minus_pressed(self): self._seed_ans_then("-")  # - 입력
    def on_btno_mul_pressed(self): self._seed_ans_then("*")  # * 입력
    def on_btno_div_pressed(self): self._seed_ans_then("/")  # / 입력
    def on_btno_open_paren_pressed(self): self._clear_if_pending(); self._append("(" if not self._is_digit_tail() else "*(")  # ( 입력
    def on_btno_close_paren_pressed(self): self._clear_if_pending(); self._append(")")  # ) 입력
    on_btn_open_pressed = on_btno_open_paren_pressed  # 별칭
    on_btn_close_pressed = on_btno_close_paren_pressed  # 별칭

    def on_btns_ac_pressed(self): self._pending_clear=False; self._set_text(""); self.le_result.setText("")  # AC
    def on_btns_del_pressed(self):
        if self._pending_clear: self._pending_clear=False  # = 후 초기화
        s=self._text()
        for h in self.FUNC_HEADERS:  # 함수 전체 삭제
            if s.endswith(h): self._set_text(s[:-len(h)]); return
        self._set_text(s[:-1])  # 한 글자 삭제

    # ---------------- '=' ----------------
    def on_btno_equal_pressed(self):
        expr_display=self._text()  # 수식 가져오기
        try:
            val=self.engine.evaluate_expr(self._auto_closed_expr(expr_display),
                                          self.engine.angle_mode_rad)  # 계산
            self.engine.last_result=val  # Ans 저장
            self.le_result.setText(fmt_number(val))  # 결과 표시
        except:
            self.engine.last_result=None  # 오류시 Ans 초기화
            self.le_result.setText("Error")  # 에러 표시
        self._pending_clear=True  # 다음 입력시 클리어

    # ---------------- 각도 모드 ----------------
    def on_btns_rad_pressed(self):
        self.engine.angle_mode_rad = not self.engine.angle_mode_rad  # DEG/RAD 전환
        self._sync_rad_button_text()  # 버튼 텍스트 변경
    def _sync_rad_button_text(self):
        opts = QtCore.Qt.FindChildOption.FindChildrenRecursively
        btn = self.findChild(QPushButton,"btno_rad",opts)
        if btn: btn.setText("Rad" if self.engine.angle_mode_rad else "Deg")  # 버튼 표시

    # ---------------- Memory ----------------
    def _current_value_for_memory(self):
        txt=(self.le_result.text() or "").strip()  # 현재 결과
        if txt and txt!="Error":
            try: return float(txt)  # float 변환
            except: pass
        expr=self._text()
        if not expr: return None  # 빈 수식
        try: return self.engine.evaluate_expr(self._auto_closed_expr(expr),
                                             self.engine.angle_mode_rad)  # 계산
        except: return None
    def on_btns_m_c_pressed(self): self.engine.mem_clear()  # MC
    def on_btns_m_r_pressed(self): v=self.engine.mem_recall(); self._maybe_mul(); self._append(fmt_number(v))  # MR
    def on_btns_m_plus_pressed(self): self.engine.mem_add(self._current_value_for_memory())  # M+
    def on_btns_m_minus_pressed(self): self.engine.mem_sub(self._current_value_for_memory())  # M-

# ---------------- Entry ----------------

def main():
    app = QtWidgets.QApplication(sys.argv)  # 앱 생성
    w = MainWindow(); #윈도우 객체 생성
    w.show()  # 메인 윈도우 표시
    sys.exit(app.exec())  # 이벤트 루프

if __name__=="__main__":
    main()  # 실행
