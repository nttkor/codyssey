import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QPainter, QBrush, QColor
from PyQt6.QtCore import Qt, QRect

class HelloWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 텍스트 (맨 위)
        self.label = QLabel("Hello!")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 종료 버튼 (아래 중앙)
        self.quit_btn = QPushButton("종료")
        self.quit_btn.clicked.connect(QApplication.quit)

        # 버튼 가로 중앙 배치
        h_layout = QHBoxLayout()
        h_layout.addStretch()
        h_layout.addWidget(self.quit_btn)
        h_layout.addStretch()

        # 전체 레이아웃
        layout = QVBoxLayout()
        layout.addWidget(self.label)  # 텍스트 위쪽
        layout.addStretch()           # 중간 여백
        layout.addLayout(h_layout)    # 버튼 아래쪽
        self.setLayout(layout)

        # 창 초기 크기
        self.resize(400, 300)

    def paintEvent(self, a0):
        # 중앙에 원 그리기
        painter = QPainter(self)
        rect = self.rect()
        center_x = rect.width() // 2
        center_y = rect.height() // 2
        radius = 50

        painter.setBrush(QBrush(QColor("blue")))  #안쪽을 채워줌
        painter.drawEllipse(center_x - radius, center_y - radius, radius*2, radius*2)

app = QApplication(sys.argv)
window = HelloWidget()
window.setWindowTitle("Text Top, Circle Center, Button Bottom")
window.show()
app.exec()
