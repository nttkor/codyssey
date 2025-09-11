import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton
from PyQt6.QtGui import QPainter

class HelloWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        quit_btn = QPushButton("종료", self) #버튼 객체 생성
        # clicked : QPushButton이 눌렸을 때 발생하는 시그널(signal), PyQt의 이벤트 시스템에서 버튼 동작을 알리는 역할
        # connect() : 시그널을 슬롯(slot, 동작) 에 연결하는 메서드, 연결된 슬롯이 시그널 발생 시 자동으로 호출됨
        # QApplication.quit : PyQt에서 애플리케이션을 종료하는 정적 메서드, 호출되면 이벤트 루프(app.exec())를 종료하고 프로그램을 종료
        quit_btn.clicked.connect(QApplication.quit)

        # 창 크기
        self.resize(400, 300)

        # 버튼 크기
        btn_width, btn_height = 80, 30

        # 버튼 위치 (아래쪽 중앙)
        x = (self.width() - btn_width) // 2
        y = self.height() - btn_height - 20  # 아래쪽 여백 20
        quit_btn.setGeometry(x, y, btn_width, btn_height)

    def paintEvent(self, a0):
        painter = QPainter(self)
        painter.drawText(self.rect().width() // 2,
                         self.rect().height() // 2,
                         "Hello!")

app = QApplication(sys.argv)
window = HelloWidget()
window.setWindowTitle("Hello Paint Example")
window.show()
app.exec()
