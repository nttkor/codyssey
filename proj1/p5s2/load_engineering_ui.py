# -*- coding: utf-8 -*-
import sys
from PyQt6 import QtWidgets, uic

def main():
    app = QtWidgets.QApplication(sys.argv)
    w = uic.loadUi("engineering_renamed.ui")
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
