from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMainWindow, QApplication
import sys, os

class CalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # UI를 QMainWindow 대신 별도 QWidget에 로드
        ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "engineering.ui")
        self.ui = uic.loadUi(ui_path)   # self 대신 새 객체

        # QMainWindow의 centralWidget으로 설정
        self.setCentralWidget(self.ui)


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    app = QApplication(sys.argv)
    window = CalculatorApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
