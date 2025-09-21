import sys,os
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QDialog

# ui 파일 경로
UI_PATH = "test.ui"  # 실제 ui 파일 이름으로 바꿔주세요

class MyDialog(QDialog):
    def __init__(self):
        super().__init__()
        # UI 로드
        os.chdir(os.path.dirname(__file__))
        uic.loadUi(UI_PATH, self)
        
        # 버튼 클릭 시 함수 연결
        #self.btn_1.clicked.connect(self.on_btn_1_clicked)
    
    def on_btn_1_clicked(self):
        # lineEdit의 내용 읽어서 콘솔에 출력
        text = self.lineEdit.text()
        print(f"clicked 내용: {text}")
    
    def on_btn_1_pressed(self):
        # lineEdit의 내용 읽어서 콘솔에 출력
        text = self.lineEdit.text()
        print(f"pressed 내용: {text}")

    def on_btn_1_released(self):
        # lineEdit의 내용 읽어서 콘솔에 출력
        text = self.lineEdit.text()
        print(f"released 내용: {text}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = MyDialog()
    dialog.show()
    sys.exit(app.exec())
