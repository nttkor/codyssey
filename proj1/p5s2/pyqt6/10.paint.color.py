import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt

class PaintWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("간단한 Paint")
        self.resize(600, 400)
        self.points = []  # 그린 선들의 좌표와 색 저장
        self.current_color = QColor("black")  # 초기 색상

        # 레이아웃 (버튼을 아래쪽에)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.addStretch()  # 위쪽 그림 공간 확보

        # 색상 버튼 생성
        btn_layout = QHBoxLayout()
        colors = ["white", "red", "yellow", "blue", "black"]
        for color in colors:
            btn = QPushButton(color.capitalize())
            btn.setStyleSheet(f"background-color: {color};")
            btn.clicked.connect(lambda checked, c=color: self.set_color(c))
            btn_layout.addWidget(btn)

        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)

    def set_color(self, color_name):
        self.current_color = QColor(color_name)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # 클릭 시작점과 색 저장
            self.points.append({"line": [event.position().toPoint()], "color": self.current_color})
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton and self.points:
            self.points[-1]["line"].append(event.position().toPoint())
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        for item in self.points:
            pen = QPen(item["color"])
            pen.setWidth(3)
            painter.setPen(pen)
            line = item["line"]
            if len(line) > 1:
                for i in range(len(line)-1):
                    painter.drawLine(line[i], line[i+1])

app = QApplication(sys.argv)
window = PaintWidget()
window.show()
app.exec()
