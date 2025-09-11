import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtGui import QPainter, QBrush, QColor
from PyQt6.QtCore import Qt

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.radius = 50  # 초기 원 크기
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # 텍스트 라벨
        self.label = QLabel("원 크기 조절")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        # stretch 추가 → 라벨 위쪽 고정, 원과 버튼 공간은 아래로 밀림
        layout.addStretch()
        # 버튼 생성
        btn_layout = QHBoxLayout()
        plus_btn = QPushButton("+")
        minus_btn = QPushButton("-")
        plus_btn.clicked.connect(self.increase_radius)
        minus_btn.clicked.connect(self.decrease_radius)
        btn_layout.addStretch()
        btn_layout.addWidget(plus_btn)
        btn_layout.addWidget(minus_btn)
        btn_layout.addStretch()

        layout.addLayout(btn_layout)
        self.setLayout(layout)

        self.resize(400, 300)
        self.setWindowTitle("Circle Size Control")

    def increase_radius(self):
        self.radius += 10
        self.update()  # paintEvent 다시 호출

    def decrease_radius(self):
        if self.radius > 10:
            self.radius -= 10
            self.update()  # paintEvent 다시 호출

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.rect()
        center_x = rect.width() // 2
        center_y = rect.height() // 2
        painter.setBrush(QBrush(QColor("blue")))
        painter.drawEllipse(center_x - self.radius, center_y - self.radius,
                            self.radius * 2, self.radius * 2)

app = QApplication(sys.argv)
window = Window()
window.show()
app.exec()
