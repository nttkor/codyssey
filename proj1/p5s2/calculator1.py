# 표준 라이브러리 불러오기
import sys  # 프로그램 종료용 (sys.exit)
import os   # 파일 경로 변경용 (UI 파일 불러올 때 사용)

# PyQt6 관련 모듈 불러오기
from PyQt6.QtWidgets import QApplication, QMainWindow  # GUI 기본 클래스
from PyQt6 import uic  # Qt Designer로 만든 .ui 파일을 불러오기 위한 모듈
from PyQt6.QtGui import QFont  # 글꼴 크기 조절용 클래스

# 현재 실행 중인 파이썬 파일이 있는 디렉토리로 작업 경로를 변경
os.chdir(os.path.dirname(__file__))

# Qt Designer로 만든 calculator.ui 파일을 불러옴
form_class = uic.loadUiType("calculator.ui")[0]  # UI 클래스 로드
# 역할: .ui 파일(Qt Designer로 만든 GUI 파일)을 Python 클래스 형태로 동적으로 로드합니다.
# 반환값이 튜플입니다:
# form_class → UI 안의 위젯과 레이아웃 정의 클래스
# base_class → 보통 QMainWindow나 QDialog 같은 기본 Qt 윈도우 클래스


# 메인 윈도우 클래스 정의 (QMainWindow + 불러온 UI 클래스 상속)
class MainWindow(QMainWindow, form_class):
    def __init__(self):
        # 부모 클래스 초기화 (PyQt 내부 동작 초기화)
        super().__init__()
        # UI 파일 적용 (버튼, 디스플레이 등 연결됨)
        self.setupUi(self)

        # 디스플레이(led) 초기화 — 처음에는 "0" 표시
        self.led.setText("0")
        
        # QFont 객체 한 번만 생성하고 재사용
        self.display_font = QFont()
        self.display_font.setBold(True)
        self.led.setFont(self.display_font)

        # 초기 글꼴 크기 설정 (문자 길이에 맞게)
        self.set_display_font_size("0")

        # --------------------------
        # 숫자 버튼 연결 (0~9)
        # getattr(self, f"btn_{i}") → btn_0, btn_1 ... btn_9 버튼 객체를 동적으로 가져옴
        # lambda를 사용해 각 숫자 버튼 클릭 시 show_text("숫자") 실행
        for i in range(10):
            getattr(self, f"btn_{i}").clicked.connect(lambda _, x=str(i): self.show_text(x))

        # 소수점 버튼 (.)
        self.btn_decimal.clicked.connect(lambda: self.show_text("."))

        # --------------------------
        # 연산자 버튼들 연결
        # 실제 계산은 하지 않고, 눌린 기호만 표시창에 출력함
        self.btn_plus.clicked.connect(lambda: self.show_text("+"))
        self.btn_minus.clicked.connect(lambda: self.show_text("-"))
        self.btn_multiply.clicked.connect(lambda: self.show_text("×"))
        self.btn_divide.clicked.connect(lambda: self.show_text("÷"))
        self.btn_percent.clicked.connect(lambda: self.show_text("%"))
        self.btn_plus_minus.clicked.connect(lambda: self.show_text("±"))
        self.btn_equals.clicked.connect(lambda: self.show_text("="))

        # --------------------------
        # AC 버튼 (초기화 기능)
        self.btn_ac.clicked.connect(self.handle_reset)
        # mode 버튼은 현재는 AC와 동일한 기능으로 연결
        self.btn_mode.clicked.connect(self.handle_reset)

    # --------------------------
    # 버튼이 눌릴 때 그 문자를 표시하는 메서드
    def show_text(self, text):
        """눌린 버튼의 문자를 이어 붙여서 표시"""
        current = self.led.text()          # 현재 표시된 글자 가져오기
        if current == "0":
            self.led.setText(text)         # 처음 0이면 새 글자로 대체
        else:
            self.led.setText(current + text)  # 기존 글자 뒤에 이어 붙이기
        self.set_display_font_size(self.led.text())  # 글자 길이에 맞춰 글꼴 조정

    # --------------------------
    # 글꼴 크기를 자동 조정하는 메서드
    def set_display_font_size(self, text):
        """입력된 문자열 길이에 따라 글꼴 크기를 동적으로 조절"""
        length = len(text)       # 문자열 길이 확인

        # 길이에 따라 글꼴 크기 자동 조정 (기본은 48pt)
        if length <= 10:
            self.display_font.setPointSize(48)  # 10자리 이하 → 큰 글씨 유지
        else:
            self.display_font.setPointSize(int(480 / length))  # 길어질수록 작게 조정

        # 계산된 글꼴 크기를 디스플레이에 적용
        self.led.setFont(self.display_font)

    # --------------------------
    # AC 버튼이 눌렸을 때 디스플레이 초기화
    def handle_reset(self):
        """AC 버튼 눌렀을 때 화면 초기화"""
        self.led.setText("0")                # 표시창을 "0"으로 리셋
        self.set_display_font_size("0")      # 글꼴 크기도 다시 기본 크기로

# --------------------------
# 프로그램이 직접 실행될 때만 아래 코드 실행
if __name__ == "__main__":
    app = QApplication(sys.argv)  # QApplication 객체 생성 (PyQt 필수)
    window = MainWindow()         # 메인 윈도우 인스턴스 생성
    window.show()                 # 윈도우 화면에 표시
    sys.exit(app.exec())          # 이벤트 루프 실행 (GUI 유지)
