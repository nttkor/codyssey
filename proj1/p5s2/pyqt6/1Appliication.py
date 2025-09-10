
# 👉 핵심 포인트:
# QApplication은 프로그램당 반드시 하나만 있어야 함.
# show()를 호출해야 창이 보임 (안 하면 백그라운드에서만 존재).
# app.exec()이 이벤트 루프 → 여기서 프로그램이 계속 실행되다가 창을 닫으면 종료됨.
# 혹시 이 코드를 기반으로 버튼 추가라든지 레이아웃 적용 예제도 만들어 드릴까요?

# sys.argv를 사용하려면 sys 모듈이 필요함 (명령줄 인자 처리용)
from PyQt6.QtWidgets import QApplication, QWidget
import sys

# 모든 PyQt 애플리케이션은 QApplication 인스턴스가 반드시 1개 필요함.
# sys.argv를 넣으면 명령줄 인자를 처리할 수 있음.
# 만약 명령줄 인자를 쓰지 않을 거라면 QApplication([])로 해도 무방.
app = QApplication(sys.argv)

# QWidget 객체 생성 → 이게 기본 윈도우(창)가 됨.
window = QWidget()
window.show()  # ⚠️ 중요: 그리기 요청 처리 (paintEvent)
#QApplication의 객체 app
# 이벤트 루프 실행 (GUI 프로그램은 무조건 필요)
app.exec() # paintEvent요청처리해서 윈도우를 띄워줌

# 여기 아래 코드는 이벤트 루프가 종료되기 전까지 실행되지 않음.
# 즉, 창을 닫아 애플리케이션이 종료된 후에만 도달함.
