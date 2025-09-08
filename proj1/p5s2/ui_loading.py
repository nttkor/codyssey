import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic

class CalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # calculator.ui 파일을 로드합니다.
        uic.loadUi("calculator.ui", self)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalculatorApp()
    window.show()
    sys.exit(app.exec())