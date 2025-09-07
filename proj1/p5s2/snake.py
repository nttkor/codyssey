from PyQt6.QtCore import Qt  # QtCore.Qt를 올바르게 import
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QMainWindow, QFrame, QApplication
import random


class SnakeGame(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Snake Game")
        self.setGeometry(100, 100, 400, 400)

        self.gameBoard = GameBoard(self)  # 게임 보드를 메인 윈도우에 추가
        self.setCentralWidget(self.gameBoard)
        self.show()


class GameBoard(QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.board_width = 40
        self.board_height = 40
        self.cell_size = 10
        self.snake = [(10, 10)]  # 초기 뱀 위치
        self.food = self.random_food()  # 초기 음식 위치
        self.direction = Qt.Key_Right  # 초기 방향: 오른쪽
        self.isGameOver = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateGame)
        self.timer.start(100)  # 100ms마다 게임 업데이트

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.isGameOver:
            self.drawGameOver(painter)
            return

        self.drawSnake(painter)
        self.drawFood(painter)

    def drawSnake(self, painter):
        painter.setBrush(QColor(0, 255, 0))  # 초록색 뱀
        for x, y in self.snake:
            painter.drawRect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)

    def drawFood(self, painter):
        painter.setBrush(QColor(255, 0, 0))  # 빨간색 음식
        x, y = self.food
        painter.drawRect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)

    def drawGameOver(self, painter):
        painter.setPen(QColor(255, 0, 0))  # 빨간색 글씨
        painter.setFont("Arial")
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Game Over")

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Left and self.direction != Qt.Key_Right:
            self.direction = Qt.Key_Left
        elif key == Qt.Key_Right and self.direction != Qt.Key_Left:
            self.direction = Qt.Key_Right
        elif key == Qt.Key_Up and self.direction != Qt.Key_Down:
            self.direction = Qt.Key_Up
        elif key == Qt.Key_Down and self.direction != Qt.Key_Up:
            self.direction = Qt.Key_Down

    def updateGame(self):
        if self.isGameOver:
            return

        head_x, head_y = self.snake[0]

        # 새로운 머리 위치 계산
        if self.direction == Qt.Key_Left:
            head_x -= 1
        elif self.direction == Qt.Key_Right:
            head_x += 1
        elif self.direction == Qt.Key_Up:
            head_y -= 1
        elif self.direction == Qt.Key_Down:
            head_y += 1

        # 새로운 머리 위치가 벽에 부딪히면 게임 오버
        if head_x < 0 or head_x >= self.board_width or head_y < 0 or head_y >= self.board_height or (head_x, head_y) in self.snake:
            self.isGameOver = True
            self.update()  # 게임 오버 상태로 화면 업데이트
            return

        # 뱀의 머리를 새로운 위치에 추가
        new_head = (head_x, head_y)
        self.snake = [new_head] + self.snake[:-1]  # 뱀이 이동하며 몸통이 따라옴

        # 음식을 먹었을 경우, 몸 길이 증가
        if new_head == self.food:
            self.snake.append(self.snake[-1])  # 뱀 길이 증가
            self.food = self.random_food()  # 새로운 음식 생성

        self.update()

    def random_food(self):
        # 새로운 위치에 음식을 생성 (뱀의 위치와 겹치지 않도록)
        while True:
            food_x = random.randint(0, self.board_width - 1)
            food_y = random.randint(0, self.board_height - 1)
            if (food_x, food_y) not in self.snake:
                return (food_x, food_y)


def main():
    app = QApplication([])
    window = SnakeGame()
    app.exec()


if __name__ == '__main__':
    main()
