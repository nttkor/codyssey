import sys  # 시스템 관련 기능을 사용할 수 있도록 sys 모듈을 임포트합니다.
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit  # PyQt6의 위젯 관련 모듈들을 임포트합니다.
from PyQt6.QtCore import Qt  # PyQt6에서 Qt 클래스의 기능을 사용하기 위해 임포트합니다.

# 클래스 정의
class EngineeringCalculator(QWidget):  # QWidget을 상속받는 계산기 클래스를 정의합니다.
    def __init__(self):
        super().__init__()  # 부모 클래스인 QWidget의 초기화 메서드를 호출합니다.

        # 윈도우 크기 고정: 400x800 크기로 창을 고정합니다.
        self.setWindowTitle("Engineering Calculator")  # 윈도우 제목을 설정합니다.
        self.setFixedSize(400, 800)  # 윈도우의 크기를 고정하여 크기를 변경할 수 없게 합니다.

        # LED 디스플레이 설정 (디스플레이는 화면 상단에 고정되어야 합니다)
        self.display = QLineEdit(self)  # QLineEdit 위젯을 생성하여 텍스트를 입력할 수 있는 디스플레이를 만듭니다.
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)  # 텍스트를 오른쪽 정렬로 설정합니다.
        self.display.setReadOnly(True)  # 디스플레이는 읽기 전용으로 설정하여 사용자가 직접 수정할 수 없게 합니다.
        self.display.setStyleSheet("font-size: 50px; background-color: black; color: white;")  # 디스플레이의 스타일을 설정합니다.
        self.display.setFixedHeight(200)  # 디스플레이의 높이를 200px로 고정합니다.

        self.angle_unit = 'deg'  # 기본 각도 단위를 'deg'로 설정합니다.
        self.init_ui()  # UI 초기화 메서드를 호출합니다.

    def init_ui(self):
        grid_layout = QGridLayout()  # QGridLayout을 사용하여 버튼을 그리드 형태로 배치할 수 있도록 설정합니다.

        # 버튼 레이아웃: 두 개의 그룹으로 나누어 각 그룹에 버튼들을 배치합니다.
        buttons_top = [  # 위쪽 그룹 (디스플레이 아래 5줄의 버튼들)
            ['(', ')', 'mc', 'm+', 'm-', 'mr'],
            ['2nd', 'x²', 'x³', 'x^y', 'e^x', '10^x'],
            ['1/x', '2√x', '3√x', 'y√x', 'ln', 'log₁₀'],
            ['x!', 'sin', 'cos', 'tan', 'e', 'EE'],
            ['Rand', 'sinh', 'cosh', 'tanh', 'π', 'Rad']
        ]
        
        buttons_bottom = [  # 아래쪽 그룹 (디스플레이 아래 5줄의 버튼들)
            ['<-', '+/-', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['Mode', '0', '.', '=']
        ]

        # LED 디스플레이를 맨 위에 추가
        grid_layout.addWidget(self.display, 0, 0, 1, 6)  # 첫 번째 행에 디스플레이를 추가하고, 6열을 차지하도록 설정합니다.

        # 위 5줄의 버튼 추가
        for row_idx, row in enumerate(buttons_top, 1):  # 버튼을 위 그룹에서 하나씩 추가합니다.
            for col_idx, button_text in enumerate(row):  # 각 행의 버튼을 차례대로 추가합니다.
                button = QPushButton(button_text)  # QPushButton을 생성하여 텍스트를 버튼에 할당합니다.
                button.setStyleSheet("font-size: 20px; background-color: #444; color: white;")  # 버튼의 스타일을 설정합니다.
                button.clicked.connect(self.button_clicked)  # 버튼을 클릭했을 때 호출될 메서드를 연결합니다.
                grid_layout.addWidget(button, row_idx, col_idx)  # 버튼을 그리드 레이아웃에 추가합니다.

        # 아래 5줄의 버튼 추가
        for row_idx, row in enumerate(buttons_bottom, 6):  # 버튼을 아래 그룹에서 하나씩 추가합니다.
            for col_idx, button_text in enumerate(row):  # 각 행의 버튼을 차례대로 추가합니다.
                button = QPushButton(button_text)  # QPushButton을 생성하여 텍스트를 버튼에 할당합니다.
                button.setStyleSheet("font-size: 20px; background-color: #444; color: white;")  # 버튼의 스타일을 설정합니다.
                button.clicked.connect(self.button_clicked)  # 버튼을 클릭했을 때 호출될 메서드를 연결합니다.
                grid_layout.addWidget(button, row_idx, col_idx)  # 버튼을 그리드 레이아웃에 추가합니다.

        # 그리드 레이아웃에 각 버튼의 크기 설정 (열 비율)
        grid_layout.setColumnStretch(0, 1)  # 0번째 열의 너비를 균등하게 조정합니다.
        grid_layout.setColumnStretch(1, 1)  # 1번째 열의 너비를 균등하게 조정합니다.
        grid_layout.setColumnStretch(2, 1)  # 2번째 열의 너비를 균등하게 조정합니다.
        grid_layout.setColumnStretch(3, 1)  # 3번째 열의 너비를 균등하게 조정합니다.
        grid_layout.setColumnStretch(4, 1)  # 4번째 열의 너비를 균등하게 조정합니다.
        grid_layout.setColumnStretch(5, 1)  # 5번째 열의 너비를 균등하게 조정합니다.

        # 버튼들이 화면을 꽉 채우도록 비율 맞추기 (행 비율)
        for i in range(1, 10):  # 각 행의 높이를 균등하게 조정합니다.
            grid_layout.setRowStretch(i, 1)

        self.setLayout(grid_layout)  # 계산기의 레이아웃을 설정합니다.

    def button_clicked(self):
        button = self.sender()  # 클릭된 버튼을 가져옵니다.
        button_text = button.text()  # 버튼에 있는 텍스트를 가져옵니다.

        if button_text == "=":
            # "=" 버튼이 클릭되었을 때 계산 결과를 화면에 표시합니다.
            self.calculate_result()
        elif button_text == "Rad" or button_text == "Deg":
            # Rad/deg 단위를 변경하는 버튼이 클릭되었을 때 호출됩니다.
            self.switch_angle_unit(button_text)
        else:
            current_text = self.display.text()  # 현재 디스플레이에 표시된 텍스트를 가져옵니다.
            new_text = current_text + button_text  # 버튼의 텍스트를 디스플레이에 추가합니다.
            self.display.setText(new_text)  # 새로운 텍스트를 디스플레이에 표시합니다.

    def calculate_result(self):
        try:
            current_text = self.display.text()  # 디스플레이에 표시된 텍스트를 가져옵니다.
            result = eval(current_text)  # 수식을 계산합니다 (eval 함수는 문자열을 파이썬 코드로 실행합니다).
            self.display.setText(str(result))  # 계산 결과를 디스플레이에 표시합니다.
        except Exception as e:
            self.display.setText("Error")  # 계산 오류가 발생하면 "Error"를 표시합니다.

    def switch_angle_unit(self, button_text):
        if button_text == "Rad":
            self.angle_unit = "rad"  # Rad로 변경합니다.
            self.display.setText("Rad Mode")  # 화면에 "Rad Mode"를 표시합니다.
        elif button_text == "Deg":
            self.angle_unit = "deg"  # Deg로 변경합니다.
            self.display.setText("Deg Mode")  # 화면에 "Deg Mode"를 표시합니다.

if __name__ == '__main__':
    app = QApplication(sys.argv)  # QApplication 객체를 생성하여 PyQt6 애플리케이션을 실행합니다.
    window = EngineeringCalculator()  # EngineeringCalculator 객체를 생성하여 계산기 창을 만듭니다.
    window.show()  # 계산기 창을 화면에 표시합니다.
    sys.exit(app.exec())  # 이벤트 루프를 실행하여 애플리케이션을 실행합니다.
