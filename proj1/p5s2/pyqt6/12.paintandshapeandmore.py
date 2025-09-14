import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt, QPoint, QRect

class MiniPaint(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini Paint")
        self.resize(700, 500)

        self.shapes = []  # 저장된 도형
        self.current_color = QColor("black")
        self.current_tool = "pen"
        self.current_width = 3
        self.start_point = None
        self.temp_shape = None  # 미리보기용 도형

        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.addStretch()  # 그림 영역 확보

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

        # 선 굵기
        width_layout = QHBoxLayout()
        width_label = QLabel("선 굵기:")
        self.width_spin = QSpinBox()
        self.width_spin.setRange(1, 20)
        self.width_spin.setValue(self.current_width)
        self.width_spin.valueChanged.connect(self.set_width)
        width_layout.addWidget(width_label)
        width_layout.addWidget(self.width_spin)
        main_layout.addLayout(width_layout)

        # Clear 버튼
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self.clear_canvas)
        main_layout.addWidget(clear_btn)

        self.setLayout(main_layout)

    def set_color(self, color_name):
        self.current_color = QColor(color_name)

    def set_tool(self, tool_name):
        self.current_tool = tool_name

    def set_width(self, w):
        self.current_width = w

    def clear_canvas(self):
        self.shapes.clear()
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_point = event.position().toPoint()
            if self.current_tool == "pen":
                self.shapes.append({"tool": "pen", "points": [self.start_point],
                                    "color": self.current_color, "width": self.current_width})
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            if self.current_tool == "pen" and self.shapes:
                self.shapes[-1]["points"].append(event.position().toPoint())
            elif self.current_tool in ["line", "rect", "circle"]:
                # 드래그 중 미리보기
                self.temp_shape = {"tool": self.current_tool,
                                   "start": self.start_point,
                                   "end": event.position().toPoint(),
                                   "color": self.current_color,
                                   "width": self.current_width}
            self.update()

    def mouseReleaseEvent(self, event):
        if self.start_point is None:
            return
        end_point = event.position().toPoint()
        if self.current_tool in ["line", "rect", "circle"]:
            self.shapes.append({"tool": self.current_tool,
                                "start": self.start_point,
                                "end": end_point,
                                "color": self.current_color,
                                "width": self.current_width})
            self.temp_shape = None
        self.start_point = None
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        # 저장된 도형 그리기
        for shape in self.shapes:
            pen = QPen(shape["color"], shape["width"])
            painter.setPen(pen)
            if shape["tool"] == "pen":
                pts = shape["points"]
                for i in range(len(pts)-1):
                    painter.drawLine(pts[i], pts[i+1])
            elif shape["tool"] == "line":
                painter.drawLine(shape["start"], shape["end"])
            elif shape["tool"] == "rect":
                painter.drawRect(QRect(shape["start"], shape["end"]))
            elif shape["tool"] == "circle":
                painter.drawEllipse(QRect(shape["start"], shape["end"]))

        # 미리보기 도형
        if self.temp_shape:
            pen = QPen(self.temp_shape["color"], self.temp_shape["width"], Qt.PenStyle.DotLine)
            painter.setPen(pen)
            shape = self.temp_shape
            if shape["tool"] == "line":
                painter.drawLine(shape["start"], shape["end"])
            elif shape["tool"] == "rect":
                painter.drawRect(QRect(shape["start"], shape["end"]))
            elif shape["tool"] == "circle":
                painter.drawEllipse(QRect(shape["start"], shape["end"]))

app = QApplication(sys.argv)
window = MiniPaint()
window.show()
app.exec()
