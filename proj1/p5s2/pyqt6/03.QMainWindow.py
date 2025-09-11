import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class MainWindow(QMainWindow):
    '''
    다양한 widget 자식 클래스를 보여주기 위한 예제 굳이 이렇게 짤 필요는 없음
    '''
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Hello Example")
        self.resize(400, 300)

        # 중앙 위젯 생성
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # QVBoxLayout은 레이아웃 매니저(Layout Manager)
        #레이아웃 매니저가 자식 위젯(QLabel, QPushButton 등)을 부모 위젯(QMainWindow의 중앙 위젯) 크기에 맞춰 자동 배치
        layout = QVBoxLayout()
        #QVBoxLayout은 레이아웃 매니저(Layout Manager)
        # 레이아웃 매니저가 자식 위젯(QLabel, QPushButton 등)을 부모 위젯(QMainWindow의 중앙 위젯) 크기에 맞춰 자동 배치
        central_widget.setLayout(layout)

        # QLabel 생성
        self.label = QLabel("Hello!")
        self.label.setFont(QFont("Arial", 24))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        # QPushButton 생성
        button = QPushButton("Click Me")
        button.clicked.connect(self.change_text)
        layout.addWidget(button)

    def change_text(self):
        self.label.setText("Hello, PyQt6!")

# 앱 실행
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
