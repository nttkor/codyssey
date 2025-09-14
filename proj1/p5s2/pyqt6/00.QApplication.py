from PyQt6.QtWidgets import QApplication, QWidget
import sys

# 모든 PyQt 애플리케이션은 QApplication 인스턴스가 반드시 1개 필요함.
# sys.argv를 넣으면 명령줄 인자를 처리할 수 있음.
# 만약 명령줄 인자를 쓰지 않을 거라면 QApplication([])로 해도 무방.
app = QApplication(sys.argv)
app.exec() # paintEvent요청처리해서 윈도우를 띄워줌

# 여기 아래 코드는 이벤트 루프가 종료되기 전까지 실행되지 않음.
# 즉, 창을 닫아 애플리케이션이 종료된 후에만 도달함.
# 윈도우객체 생성및 show를 안했기 대문에 아무것도 안보임 Ctrl=Z로 강제 멈춰야함