import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic

class MinimalApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # minimal_calculator.ui 파일을 로드합니다.
        uic.loadUi("caculator1.ui", self)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MinimalApp()
    window.show()
    sys.exit(app.exec())
