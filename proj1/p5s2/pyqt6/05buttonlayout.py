from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
import sys

class HelloWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        label = QLabel("Hello!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 중앙 정렬

        quit_btn = QPushButton("종료")
        quit_btn.clicked.connect(QApplication.quit)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(quit_btn)
        self.setLayout(layout)

app = QApplication(sys.argv)
window = HelloWidget()
window.resize(400, 300)
window.setWindowTitle("Hello Layout Text Example")
window.show()
app.exec()
