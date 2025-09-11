from PyQt6.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
import sys

class MyButton(QPushButton):
    def __init__(self, label):
        super().__init__("클릭해봐요")
        self.label = label  # QLabel 참조 저장

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.label.setText("왼쪽 버튼 클릭")
        elif event.button() == Qt.MouseButton.RightButton:
            self.label.setText("오른쪽 버튼 클릭")
        elif event.button() == Qt.MouseButton.MiddleButton:
            self.label.setText("중간 버튼 클릭")
        super().mousePressEvent(event)  # 기본 동작 수행

class Window(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # 텍스트 라벨
        self.label = QLabel("Hello")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        # 버튼
        button = MyButton(self.label)
        layout.addWidget(button)

        self.setLayout(layout)

app = QApplication(sys.argv)
window = Window()
window.resize(400, 300)
window.setWindowTitle("Button Click Message")
window.show()
app.exec()
