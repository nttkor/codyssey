import sys
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QBrush
from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsEllipseItem, QLabel

class BrickBreakerGame(QMainWindow):
    def __init__(self):
        super().__init__()

        # 기본 설정
        self.setWindowTitle("벽돌깨기 게임")
        self.setGeometry(100, 100, 800, 600)  # 윈도우 크기 수정 (높이를 적절하게 수정)

        # 게임 객체 초기화
        self.initGame()

    def initGame(self):
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(0, 0, 800, 600)  # 뷰 크기도 변경
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # 수평 스크롤 비활성화
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # 수직 스크롤 비활성화

        self.paddle_width = 100
        self.paddle_height = 20
        self.ball_radius = 10
        self.score = 0

        # 라켓 초기 위치 (화면 아래에서 약간 띄워서 보이게)
        self.paddle = QGraphicsRectItem(350, 550, self.paddle_width, self.paddle_height)  # 라켓을 화면 아래에서 띄움
        self.paddle.setBrush(QBrush(QColor(255, 0, 0)))  # 라켓 색상
        self.scene.addItem(self.paddle)

        # 공 초기 위치 (라켓 바로 위에 위치)
        self.ball = QGraphicsEllipseItem(self.paddle.x() + self.paddle_width // 2 - self.ball_radius, self.paddle.y() - self.ball_radius * 2, self.ball_radius * 2, self.ball_radius * 2)
        self.ball.setBrush(QBrush(QColor(0, 255, 0)))  # 공 색상
        self.scene.addItem(self.ball)

        # 총알 (공) 속도 초기화
        self.ball_dx = 3  # 공의 가로 속도
        self.ball_dy = -3  # 공의 세로 속도

        # 벽돌 설정
        self.bricks = []
        self.createBricks()

        # 키 이벤트 처리
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # 타이머 설정 (게임 업데이트)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateGame)
        self.timer.start(16)  # 약 60 FPS

        # 점수 레이블
        self.score_label = QLabel(f"점수: {self.score}", self)
        self.score_label.setGeometry(700, 10, 100, 30)

        # 게임 화면 크기 설정 (스크롤 방지)
        self.scene.setSceneRect(0, 0, 800, 600)  # 화면 크기 고정

    def createBricks(self):
        # 벽돌 생성
        brick_width = 60
        brick_height = 30
        margin = 10
        rows = 5
        columns = 10
        colors = [QColor(255, 0, 0), QColor(0, 255, 0), QColor(0, 0, 255), QColor(255, 165, 0), QColor(255, 255, 0)]

        for row in range(rows):
            for col in range(columns):
                brick = QGraphicsRectItem(col * (brick_width + margin), row * (brick_height + margin), brick_width, brick_height)
                brick.setBrush(QBrush(colors[(row + col) % len(colors)]))
                self.scene.addItem(brick)
                self.bricks.append(brick)

    def keyPressEvent(self, event):
        key = event.key()

        # 왼쪽, 오른쪽 키로 라켓 이동
        if key == Qt.Key_Left:
            if self.paddle.x() > 0:
                self.paddle.moveBy(-15, 0)  # 라켓을 왼쪽으로 이동
        elif key == Qt.Key_Right:
            if self.paddle.x() + self.paddle_width < self.width():
                self.paddle.moveBy(15, 0)  # 라켓을 오른쪽으로 이동

    def updateGame(self):
        # 공 이동
        self.ball.moveBy(self.ball_dx, self.ball_dy)

        # 벽에 튕기기 (상단 벽)
        if self.ball.y() <= 0:
            self.ball_dy = -self.ball_dy

        # 바닥에 닿으면 게임 오버
        if self.ball.y() + self.ball_radius * 2 >= self.height():
            self.gameOver()

        # 라켓과 공의 충돌 체크
        if self.paddle.collidesWithItem(self.ball):
            self.ball_dy = -self.ball_dy

        # 벽돌과 공의 충돌 체크
        for brick in self.bricks:
            if brick.collidesWithItem(self.ball):
                self.ball_dy = -self.ball_dy
                self.scene.removeItem(brick)  # 벽돌 제거
                self.bricks.remove(brick)  # 벽돌 리스트에서 제거
                self.score += 10
                self.score_label.setText(f"점수: {self.score}")
                break

        # 공이 화면 밖으로 나가면 다시 초기화
        if self.ball.x() < 0 or self.ball.x() + self.ball_radius * 2 > self.width():
            self.ball_dx = 0

        if self.ball.y() < 0:
            self.ball_dy = -self.ball_dy

    def gameOver(self):
        # 게임 오버 처리
        self.timer.stop()
        self.score_label.setText(f"게임 오버! 최종 점수: {self.score}")
        self.ball.setPos(self.width() / 2 - self.ball_radius, self.height() / 2 - self.ball_radius)

    def mousePressEvent(self, event):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = BrickBreakerGame()
    game.show()

    # 게임 시작 시 자동으로 공 발사
    game.ball_dx = 3  # 45도 각도로 발사되는 방향 (가로)
    game.ball_dy = -3  # 45도 각도로 발사되는 방향 (세로)

    sys.exit(app.exec())
