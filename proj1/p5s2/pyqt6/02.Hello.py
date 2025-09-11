import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QFont
from PyQt6.QtCore import Qt

class HelloWidget(QWidget):
    def paintEvent(self, a0):  #2번째 인자를 a0으로 해야 경고가 없어짐
        painter = QPainter(self)
        # painter.setFont(QFont("Arial", 24)) #폰트지정
        painter.drawText(self.rect().width()//2 ,self.rect().height()//2, "Hello!")  #rect을 안사용하고 단순하게 좌표로
        # painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Hello!")         # 텍스트 가운데 정렬

app = QApplication(sys.argv)  # sys.argv없어도 됨
window = HelloWidget() #HelloWidget의 객체만들기
window.resize(400, 300) #window사이즈 지정
window.setWindowTitle("Hello Paint Example")  #타이틀 지정
window.show() # paintEvent발생
app.exec() #이벤트 대기 처리, 표시
