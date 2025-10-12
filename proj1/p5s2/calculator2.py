
# 표준 라이브러리 불러오기
import sys  # 파이썬 인터프리터 관련 모듈, 프로그램 종료용 sys.exit 사용
import os   # 운영체제 기능, 파일 경로 변경 등 사용
from PyQt6.QtWidgets import QApplication, QMainWindow  # PyQt6 GUI 위젯
from PyQt6 import uic  # Qt Designer로 만든 .ui 파일을 불러오기 위해 사용
from PyQt6.QtGui import QFont  # 화면 폰트 조절용

# --------------------------------------------
# UI 로드
# --------------------------------------------
os.chdir(os.path.dirname(__file__))  # 현재 스크립트 파일 위치로 작업 디렉토리 변경
try:
    form_class = uic.loadUiType("calculator.ui")[0]  # .ui 파일을 Python 클래스 형태로 로드
except FileNotFoundError:  
    print("❌ UI 파일(calculator.ui)을 찾을 수 없습니다.")  # 파일 없으면 알림
    sys.exit(1)  # 프로그램 종료

# --------------------------------------------
# 계산 오류 예외 클래스
# --------------------------------------------
class CalcError(Exception):  # 계산 도중 발생하는 오류 전용 예외 클래스
    """계산 중 발생한 오류를 처리하기 위한 사용자 정의 예외"""
    pass  # 기능 없이 상속만 사용

# --------------------------------------------
# 계산 로직 클래스
# --------------------------------------------
class Calculator:  
    """사칙연산, %, +/- 등 계산 기능 담당 클래스"""
    def __init__(self):
        self.reset()  # 객체 생성 시 초기 상태 설정

    def reset(self):
        """모든 상태 초기화"""
        self.num = ""        # 현재 입력 중인 숫자 문자열
        self.op1 = None      # 첫 번째 피연산자
        self.op2 = None      # 두 번째 피연산자
        self.operator = None # 현재 선택된 연산자
        self.result = 0.0    # 계산 결과

    def calculate(self):  
        # num → 현재 입력 중인 숫자 (문자열)
        # op1 → 첫 번째 피연산자이자 계산 결과 누적
        # op2 → 두 번째 피연산자 (현재 입력값)
        # operator → 현재 선택된 연산자
        """연산자에 따라 op1, op2 계산 수행"""
        if self.operator == "+": self.op1 += self.op2
        elif self.operator == "-": self.op1 -= self.op2
        elif self.operator == "X": self.op1 *= self.op2
        elif self.operator == "/":
            if self.op2 == 0: raise CalcError("0으로 나눌 수 없습니다.")  # 0으로 나누기 방지
            self.op1 /= self.op2
        elif self.operator == "%":  # 퍼센트 연산 처리
            self.op2 = self.op1 * (self.op2 / 100)
            self.op1 += self.op2
        else:
            raise CalcError("유효하지 않은 연산자입니다.")  # 지원하지 않는 연산자 처리

    def equal(self):
        """= 버튼 클릭 시 실제 계산 수행 및 결과 반환"""
        if self.op1 is None or not self.num: raise CalcError("입력이 불완전합니다.")  # 숫자가 없으면 오류
        self.op2 = float(self.num)  # 현재 입력 문자열을 float으로 변환
        self.calculate()  # 계산 수행 후 결과는 op1에 저장됨
        self.result = round(self.op1, 10)  # 소수점 10자리로 반올림
        self.op1 = self.result  # 연속 계산 가능하도록 op1 갱신
        self.num = ""  # 입력 초기화
        self.operator = None  # 연산자 초기화
        return self.result  # 최종 결과 반환

    def percent(self):
        """% 버튼 처리"""
        if self.num:  
            self.num = str(float(self.num)/100)  # 입력 중이면 num 값을 100으로 나눔
        elif self.op1 is not None:
            self.op1 /= 100  # 결과가 있으면 op1 값을 100으로 나눔

    def negative_positive(self):
        """+/- 버튼 처리: 현재 입력의 부호 반전"""
        if self.num:
            self.num = self.num[1:] if self.num.startswith("-") else "-" + self.num  # 부호 반전

# --------------------------------------------
# GUI 클래스
# --------------------------------------------
class MainWindow(QMainWindow, form_class):  
    """PyQt6 계산기 GUI 클래스"""
    def __init__(self):
        super().__init__()  
        self.setupUi(self)  # .ui 파일 UI 초기화 (버튼, 디스플레이 연결)
        
        self.calc = Calculator()  # 계산 로직 객체 생성
        self.equals_pressed = False  # 마지막으로 = 버튼 눌림 여부

        # QFont 객체 한 번만 생성 후 재사용
        self.display_font = QFont()  
        self.display_font.setBold(True)  # 볼드체 적용
        self.led.setFont(self.display_font)  # LED 디스플레이에 적용
        self.update_display("0")  # 초기 화면 0 표시

        # --------------------------
        # 숫자 버튼 (0~9) 클릭 시 input_number 연결
        for i in range(10):
            getattr(self, f"btn_{i}").clicked.connect(lambda _, x=str(i): self.input_number(x))
        self.btn_decimal.clicked.connect(lambda: self.input_number("."))  # 소수점 버튼

        # 사칙연산 버튼 연결
        self.btn_plus.clicked.connect(lambda: self.input_operator("+"))
        self.btn_minus.clicked.connect(lambda: self.input_operator("-"))
        self.btn_multiply.clicked.connect(lambda: self.input_operator("X"))
        self.btn_divide.clicked.connect(lambda: self.input_operator("/"))

        # 특수 기능 버튼 연결
        self.btn_percent.clicked.connect(self.handle_percent)  # % 버튼
        self.btn_plus_minus.clicked.connect(self.handle_negative_positive)  # +/- 버튼
        self.btn_equals.clicked.connect(self.handle_equal)  # = 버튼
        self.btn_ac.clicked.connect(self.handle_reset)  # AC 버튼
        self.btn_mode.clicked.connect(self.handle_reset)  # MODE 버튼도 초기화

    # ------------------------------
    # 화면 업데이트
    # ------------------------------
    def format_number(self, value):  
        """숫자를 int/float 형식에 맞게 문자열로 반환"""
        try:
            f = float(value)
        except Exception:
            return str(value)
        return str(int(f)) if f.is_integer() else str(f)  # 정수면 int로 변환

    def update_display(self, text: str):
        """LED 화면에 텍스트 표시 + 글꼴 크기 자동 조정"""
        self.led.setText(text)  # 화면에 텍스트 표시
        font_size = 48 if len(text) <= 10 else int(480 / len(text))  # 글자 길이에 따른 폰트 크기 계산
        self.display_font.setPointSize(font_size)  # 폰트 크기 적용
        self.led.setFont(self.display_font)  # LED 디스플레이에 적용

    # ------------------------------
    # 숫자 입력
    # ------------------------------
    def input_number(self, digit: str):
        if self.equals_pressed: self.handle_reset()  # = 이후 입력이면 초기화
        if digit == "." and "." in self.calc.num: return  # 이미 소수점 있으면 무시
        # 현재 입력값이 "0"이면 새 숫자로 대체 아니면 기존 숫자 뒤에 이어 붙이기
        self.calc.num = digit if self.calc.num=="0" and digit!="." else self.calc.num + digit  # 입력 갱신
        self.update_display(self.calc.num)  # 화면 갱신

    # ------------------------------
    # 연산자 입력
    # ------------------------------
    def input_operator(self, op: str):
        self.equals_pressed = False
        if self.calc.num:  
            # 첫 번째 숫자 없으면 op1 설정, 있으면 기존 계산 후 갱신
            self.calc.op1 = float(self.calc.num) if self.calc.op1 is None else self.calc.equal()
            self.calc.operator = op
            self.calc.num = ""  # 입력 초기화
        elif self.calc.op1 is not None:
            self.calc.operator = op  # 연속 연산자 입력
        elif op == "-":
            self.calc.num = "-"  # 첫 입력 음수 처리
        self.update_display(self.display_with_operator())  # 화면 갱신

    def display_with_operator(self):
        """연산자 포함 화면 문자열 생성"""
        if self.calc.op1 is not None:
            op1_display = self.format_number(self.calc.op1)
            operator = self.calc.operator or ""
            return f"{op1_display} {operator}".strip()
        return self.calc.num if self.calc.num else "0"

    # ------------------------------
    # = 버튼 처리
    # ------------------------------
    def handle_equal(self):
        try:
            result = self.calc.equal()  # 실제 계산 수행
        except CalcError as e:
            self.show_error(str(e))  # 오류 발생 시 처리
            return
        self.update_display(self.format_number(result))  # 결과 화면 표시
        self.equals_pressed = True  # 상태 갱신

    # ------------------------------
    # AC 버튼
    # ------------------------------
    def handle_reset(self):
        self.calc.reset()  # 계산 상태 초기화
        self.update_display("0")  # 화면 초기화
        self.equals_pressed = False  # 상태 초기화

    # ------------------------------
    # +/- 버튼
    # ------------------------------
    def handle_negative_positive(self):
        if self.calc.num:
            self.calc.negative_positive()  # 입력 숫자 부호 반전
        elif self.calc.op1 is not None and self.calc.operator is None:
            self.calc.op1 = -self.calc.op1  # 결과 부호 반전
        else:
            self.calc.num = "-0"  # 초기 상태 처리
        self.update_display(self.display_with_operator())  # 화면 갱신

    # ------------------------------
    # % 버튼
    # ------------------------------
    def handle_percent(self):
        self.calc.percent()  # 퍼센트 계산
        self.update_display(self.display_with_operator())  # 화면 갱신

    # ------------------------------
    # 오류 표시
    # ------------------------------
    def show_error(self, msg: str):
        self.update_display("Error")  # 화면에 Error 표시
        print(f"[오류] {msg}")  # 콘솔에 로그
        self.equals_pressed = True  # 상태 갱신

# --------------------------------------------
# 프로그램 시작점
# --------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)  # QApplication 객체 생성
    window = MainWindow()  # 메인 윈도우 객체 생성
    window.show()  # 창 표시
    sys.exit(app.exec())  # 이벤트 루프 시작 및 종료
