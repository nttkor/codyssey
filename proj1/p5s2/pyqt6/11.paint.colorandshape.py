import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt, QPoint, QRect

class PaintWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini Paint")
        self.resize(600, 400)

        self.shapes = []  # 그린 도형 저장
        self.current_color = QColor("black")
        self.current_tool = "pen"  # 초기 도구: pen

        self.start_point = None  # 도형 시작점

        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.addStretch()  # 그림 공간 확보

        # 색상 버튼
        color_layout = QHBoxLayout()
        colors = ["white", "red", "yellow", "blue", "black"]
        for color in colors:
            btn = QPushButton(color.capitalize())
            btn.setStyleSheet(f"background-color: {color};")
            btn.clicked.connect(lambda checked, c=color: self.set_color(c))
            color_layout.addWidget(btn)
        main_layout.addLayout(color_layout)

        # 도구 버튼
        tool_layout = QHBoxLayout()
        tools = ["pen", "line", "rect", "circle"]
        for tool in tools:
            btn = QPushButton(tool.capitalize())
            btn.clicked.connect(lambda checked, t=tool: self.set_tool(t))
            tool_layout.addWidget(btn)
        main_layout.addLayout(tool_layout)

        self.setLayout(main_layout)

    def set_color(self, color_name):
        self.current_color = QColor(color_name)

    def set_tool(self, tool_name):
        self.current_tool = tool_name

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_point = event.position().toPoint()
            if self.current_tool == "pen":
                # pen은 즉시 저장
                self.shapes.append({"tool": "pen", "points": [self.start_point], "color": self.current_color})
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            if self.current_tool == "pen" and self.shapes:
                self.shapes[-1]["points"].append(event.position().toPoint())
                self.update()

    def mouseReleaseEvent(self, event):
        if self.start_point is None:
            return
        end_point = event.position().toPoint()
        if self.current_tool in ["line", "rect", "circle"]:
            self.shapes.append({"tool": self.current_tool,
                                "start": self.start_point,
                                "end": end_point,
                                "color": self.current_color})
        self.start_point = None
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        for shape in self.shapes:
            pen = QPen(shape["color"])
            pen.setWidth(3)
            painter.setPen(pen)

            if shape["tool"] == "pen":
                pts = shape["points"]
                if len(pts) > 1:
                    for i in range(len(pts)-1):
                        painter.drawLine(pts[i], pts[i+1])
            elif shape["tool"] == "line":
                painter.drawLine(shape["start"], shape["end"])
            elif shape["tool"] == "rect":
                rect = QRect(shape["start"], shape["end"])
                painter.drawRect(rect)
            elif shape["tool"] == "circle":
                rect = QRect(shape["start"], shape["end"])
                painter.drawEllipse(rect)

app = QApplication(sys.argv)
window = PaintWidget()
window.show()
app.exec()
