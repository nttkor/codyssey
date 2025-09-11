import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QFont
from PyQt6.QtCore import Qt

class HelloWidget(QWidget):
    def paintEvent(self, a0):
        painter = QPainter(self)
        painter.setFont(QFont("Arial", 24))
        # 텍스트 가운데 정렬
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Hello!")

app = QApplication(sys.argv)

window = HelloWidget()
window.resize(400, 300)
window.setWindowTitle("Hello Paint Example")
window.show()

app.exec()
