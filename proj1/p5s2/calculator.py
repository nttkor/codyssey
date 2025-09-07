import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLineEdit
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class Calculator(QWidget):
    """
    이 클래스는 PyQt6를 사용하여 간단한 계산기를 구현한 클래스입니다.
    계산기 UI는 아이폰 스타일을 따라 디자인되었으며,
    사용자가 버튼을 클릭할 때마다 해당 버튼의 값이 입력창에 나타납니다.
    """
    def __init__(self):
        """
        생성자 함수로, 계산기 UI를 초기화하고 기본 설정을 합니다.
        """
        super().__init__()
        self.setWindowTitle("iPhone Style Calculator (PyQt6)")  # 창 제목 설정
        self.setFixedSize(300, 400)  # 창 크기 고정
        self.init_ui()  # UI 초기화 함수 호출

    def init_ui(self):
        """
        계산기의 UI를 설정하는 함수입니다. 버튼 배치, 글꼴, 크기 등을 설정합니다.
        """
        # 디스플레이 영역: 계산 결과를 표시할 텍스트 입력창
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)  # 오른쪽 정렬
        self.display.setReadOnly(True)  # 텍스트 입력 불가 (읽기 전용)
        self.display.setFixedHeight(60)  # 높이 고정
        self.display.setFont(QFont("Arial", 24))  # 글꼴과 크기 설정

        # 버튼 배치 배열 (아이폰 계산기와 유사한 배치)
        buttons = [
            ['C', '+/-', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]

        # 버튼 그리드 배치
        grid = QGridLayout()
        row = 0
        for btn_row in buttons:
            col = 0
            for btn_text in btn_row:
                # 각 버튼 생성
                button = QPushButton(btn_text)
                button.setFont(QFont("Arial", 16))  # 글꼴 크기 설정
                button.setFixedSize(60, 60)  # 버튼 크기 설정
                if btn_text == '0':  # '0' 버튼은 두 칸을 차지
                    button.setFixedSize(130, 60)
                    grid.addWidget(button, row, col, 1, 2)  # 1행 2열에 걸쳐 배치
                    col += 1  # 한 칸 건너뛰기
                else:
                    grid.addWidget(button, row, col)  # 일반 버튼 배치
                button.clicked.connect(self.button_clicked)  # 버튼 클릭 시 이벤트 연결
                col += 1  # 다음 열로 이동
            row += 1  # 다음 행으로 이동

        # 메인 레이아웃 설정
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.display)  # 디스플레이 위젯 추가
        main_layout.addLayout(grid)  # 버튼 그리드 레이아웃 추가

        self.setLayout(main_layout)  # 레이아웃 설정

    def button_clicked(self):
        """
        버튼이 클릭되었을 때 호출되는 함수입니다.
        클릭된 버튼의 텍스트에 따라 적절한 동작을 수행합니다.
        """
        sender = self.sender()  # 클릭된 버튼을 가져옴
        btn_text = sender.text()  # 버튼의 텍스트(숫자/기호)를 얻음

        if btn_text == 'C':  # 'C'는 입력을 초기화
            self.display.clear()  # 디스플레이를 초기화
        elif btn_text == '=':  # '='은 수식 계산
            self.evaluate_expression()  # 수식 계산 함수 호출
        elif btn_text == '+/-':  # '+/-'는 부호를 변경
            self.toggle_sign()  # 부호 변경 함수 호출
        elif btn_text == '%':  # '%'는 퍼센트 계산
            self.percentage()  # 퍼센트 계산 함수 호출
        else:
            current_text = self.display.text()  # 현재 디스플레이 텍스트 가져오기
            self.display.setText(current_text + btn_text)  # 버튼 텍스트를 디스플레이에 추가

    def toggle_sign(self):
        """
        텍스트의 부호를 변경하는 함수입니다.
        예를 들어, +3 -> -3, -3 -> +3 으로 변경됩니다.
        """
        text = self.display.text()
        if text:
            try:
                # 부호가 있으면 제거, 없으면 추가
                if text.startswith('-'):
                    self.display.setText(text[1:])
                else:
                    self.display.setText('-' + text)
            except:
                self.display.setText("Error")  # 오류 처리

    def percentage(self):
        """
        현재 디스플레이에 있는 숫자를 100으로 나누어 퍼센트를 계산합니다.
        예: 50 -> 0.5
        """
        try:
            value = float(self.display.text())  # 텍스트를 실수로 변환
            self.display.setText(str(value / 100))  # 100으로 나누어 계산 결과 표시
        except:
            self.display.setText("Error")  # 오류 처리

    def evaluate_expression(self):
        """
        현재 디스플레이에 있는 수식을 계산하여 결과를 디스플레이에 표시합니다.
        이때, `eval()`을 사용하여 간단한 사칙연산을 처리합니다.
        """
        try:
            result = eval(self.display.text())  # 수식을 계산
            self.display.setText(str(result))  # 계산된 결과 표시
        except:
            self.display.setText("Error")  # 오류 처리

if __name__ == "__main__":
    """
    프로그램의 엔트리 포인트입니다.
    QApplication 객체를 생성하고, 계산기 UI를 표시한 뒤 이벤트 루프를 시작합니다.
    """
    app = QApplication(sys.argv)  # 애플리케이션 객체 생성
    calc = Calculator()  # 계산기 객체 생성
    calc.show()  # 계산기 UI 표시
    sys.exit(app.exec())  # 이벤트 루프 시작
