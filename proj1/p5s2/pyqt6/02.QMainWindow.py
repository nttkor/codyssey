# 다른 위젯(QMainWindow, QLabel, QPushButton 등)을 바로 메인 창으로 써도 됩니다.
# 이번에는 QMainWindow를 사용해서 "Hello!"를 표시해 보겠습니다.
# QMainWindow는 QWidget보다 조금 더 고급 창으로, 메뉴바, 상태바, 툴바 같은 걸 붙일 수 있는 기본 구조를 이미 가지고 있어요.
# 그래서 setCentralWidget()을 이용해서 중앙에 위젯을 올려주면 됩니다.

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
import sys

app = QApplication(sys.argv)

# QMainWindow 객체 생성
window = QMainWindow()
window.setWindowTitle("QMainWindow 예제")  # 창 제목
window.resize(400, 300)  # 창 크기 (가로 400, 세로 300)

# QLabel 생성 (텍스트 표시 위젯)
label = QLabel("Hello!", window)
label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 텍스트 가운데 정렬

# QMainWindow 중앙에 QLabel 배치
window.setCentralWidget(label)

# 창 보이기
window.show()

# 이벤트 루프 실행
app.exec()
