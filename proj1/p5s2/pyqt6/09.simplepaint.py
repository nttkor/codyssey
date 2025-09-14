import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt, QPoint

class PaintWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("간단한 Paint")
        self.resize(600, 400)
        self.points = []  # 그린 점 좌표를 저장

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # 클릭 시작점 저장
            self.points.append([event.position().toPoint()])  # 새로운 선 시작
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            # 현재 선에 점 추가
            self.points[-1].append(event.position().toPoint())
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(QColor("blue"))
        pen.setWidth(3)
        painter.setPen(pen)

        # 저장된 점들을 이어서 그림
        for line in self.points:
            if len(line) > 1:
                for i in range(len(line)-1):
                    painter.drawLine(line[i], line[i+1])

app = QApplication(sys.argv)
window = PaintWidget()
window.show()
app.exec()
