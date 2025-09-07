#!/usr/bin/python

"""
ZetCode PyQt6 tutorial

This is a Tetris game clone.

Author: Jan Bodnar
Website: zetcode.com
"""

import random  # 랜덤 수 생성 모듈
import sys     # 시스템 관련 모듈

# PyQt6의 다양한 클래스를 불러옴
from PyQt6.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QMainWindow, QFrame, QApplication


class Tetris(QMainWindow):
    """Tetris 게임의 메인 윈도우 클래스"""

    def __init__(self):
        super().__init__()  # 부모 클래스 초기화
        self.initUI()  # UI 초기화 메서드 호출

    def initUI(self):
        """애플리케이션 UI를 초기화"""
        self.tboard = Board(self)  # Board 객체 생성
        self.setCentralWidget(self.tboard)  # 중앙 위젯 설정

        self.statusbar = self.statusBar()  # 상태바 설정
        self.tboard.msg2Statusbar[str].connect(self.statusbar.showMessage)  # 상태 메시지 연결

        self.tboard.start()  # 게임 시작

        self.resize(360, 760)  # 윈도우 크기 설정
        self.center()  # 윈도우 중앙에 위치시키기
        self.setWindowTitle('Tetris')  # 윈도우 타이틀 설정
        self.show()  # 윈도우 표시

    def center(self):
        """윈도우를 화면 중앙에 배치"""
        qr = self.frameGeometry()  # 윈도우 크기 정보 가져오기
        cp = self.screen().availableGeometry().center()  # 화면 중앙 좌표 가져오기

        qr.moveCenter(cp)  # 윈도우를 중앙으로 이동
        self.move(qr.topLeft())  # 윈도우의 왼쪽 상단 좌표로 이동


class Board(QFrame):
    """테트리스 게임 보드 클래스"""

    msg2Statusbar = pyqtSignal(str)  # 상태바로 메시지를 보낼 신호

    BoardWidth = 10  # 보드 너비
    BoardHeight = 22  # 보드 높이
    Speed = 300  # 게임 속도 (밀리초)

    def __init__(self, parent):
        super().__init__(parent)  # 부모 클래스 초기화
        self.initBoard()  # 보드 초기화 메서드 호출

    def initBoard(self):
        """보드를 초기화"""
        self.timer = QBasicTimer()  # 기본 타이머 객체 생성
        self.isWaitingAfterLine = False  # 라인 삭제 후 대기 상태 여부

        self.curX = 0  # 현재 모양의 X 좌표
        self.curY = 0  # 현재 모양의 Y 좌표
        self.numLinesRemoved = 0  # 제거된 라인의 수
        self.board = []  # 보드 초기화

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)  # 포커스 정책 설정
        self.isStarted = False  # 게임 시작 여부
        self.isPaused = False  # 게임 일시 정지 여부
        self.clearBoard()  # 보드 클리어

    def shapeAt(self, x, y):
        """주어진 좌표에 있는 도형을 반환"""
        return self.board[(y * Board.BoardWidth) + x]

    def setShapeAt(self, x, y, shape):
        """주어진 좌표에 도형을 설정"""
        self.board[(y * Board.BoardWidth) + x] = shape

    def squareWidth(self):
        """각 사각형의 너비를 반환"""
        return self.contentsRect().width() // Board.BoardWidth

    def squareHeight(self):
        """각 사각형의 높이를 반환"""
        return self.contentsRect().height() // Board.BoardHeight

    def start(self):
        """게임을 시작"""
        if self.isPaused:  # 게임이 일시 정지 상태라면 시작하지 않음
            return

        self.isStarted = True  # 게임 시작 상태로 변경
        self.isWaitingAfterLine = False  # 라인 삭제 후 대기 상태 초기화
        self.numLinesRemoved = 0  # 제거된 라인 수 초기화
        self.clearBoard()  # 보드 초기화

        self.msg2Statusbar.emit(str(self.numLinesRemoved))  # 상태바에 초기 라인 수 표시

        self.newPiece()  # 새로운 도형 생성
        self.timer.start(Board.Speed, self)  # 타이머 시작

    def pause(self):
        """게임을 일시 정지"""
        if not self.isStarted:  # 게임이 시작되지 않았다면 정지하지 않음
            return

        self.isPaused = not self.isPaused  # 일시 정지 상태 토글

        if self.isPaused:
            self.timer.stop()  # 타이머 정지
            self.msg2Statusbar.emit("paused")  # 상태바에 'paused' 표시
        else:
            self.timer.start(Board.Speed, self)  # 타이머 시작
            self.msg2Statusbar.emit(str(self.numLinesRemoved))  # 상태바에 라인 수 표시

        self.update()  # 화면 갱신

    def paintEvent(self, event):
        """게임 도형들을 그리는 메서드"""
        painter = QPainter(self)  # QPainter 객체 생성
        rect = self.contentsRect()  # 콘텐츠 영역 가져오기

        boardTop = rect.bottom() - Board.BoardHeight * self.squareHeight()  # 보드의 상단 좌표 계산

        # 보드에 있는 모든 도형을 그림
        for i in range(Board.BoardHeight):
            for j in range(Board.BoardWidth):
                shape = self.shapeAt(j, Board.BoardHeight - i - 1)  # 현재 좌표에 있는 도형

                if shape != Tetrominoe.NoShape:
                    self.drawSquare(painter,
                                    rect.left() + j * self.squareWidth(),
                                    boardTop + i * self.squareHeight(), shape)  # 도형 그리기

        # 현재 모양이 있다면 그리기
        if self.curPiece.shape() != Tetrominoe.NoShape:
            for i in range(4):
                x = self.curX + self.curPiece.x(i)
                y = self.curY - self.curPiece.y(i)
                self.drawSquare(painter, rect.left() + x * self.squareWidth(),
                            boardTop + (Board.BoardHeight - y - 1) * self.squareHeight(),
                            self.curPiece.shape())  # 현재 도형 그리기

    def keyPressEvent(self, event):
        """키 이벤트를 처리하는 메서드"""
        if not self.isStarted or self.curPiece.shape() == Tetrominoe.NoShape:
            super(Board, self).keyPressEvent(event)  # 부모 클래스의 기본 이벤트 처리
            return

        key = event.key()  # 누른 키 값

        if key == Qt.Key.Key_P:  # P키: 일시 정지
            self.pause()
            return

        if self.isPaused:  # 게임이 일시 정지 상태일 때는 아무 것도 처리하지 않음
            return

        elif key == Qt.Key.Key_Left.value:  # 왼쪽 화살표 키: 왼쪽으로 이동
            self.tryMove(self.curPiece, self.curX - 1, self.curY)

        elif key == Qt.Key.Key_Right.value:  # 오른쪽 화살표 키: 오른쪽으로 이동
            self.tryMove(self.curPiece, self.curX + 1, self.curY)

        elif key == Qt.Key.Key_Down.value:  # 아래 화살표 키: 아래로 회전
            self.tryMove(self.curPiece.rotateRight(), self.curX, self.curY)

        elif key == Qt.Key.Key_Up.value:  # 위 화살표 키: 위로 회전
            self.tryMove(self.curPiece.rotateLeft(), self.curX, self.curY)

        elif key == Qt.Key.Key_Space.value:  # 스페이스 키: 빠르게 떨어뜨리기
            self.dropDown()

        elif key == Qt.Key.Key_D.value:  # D키: 한 줄 아래로 떨어뜨리기
            self.oneLineDown()

        else:
            super(Board, self).keyPressEvent(event)  # 다른 키는 기본 이벤트 처리

    def timerEvent(self, event):
        """타이머 이벤트를 처리하는 메서드"""
        if event.timerId() == self.timer.timerId():  # 타이머 이벤트인지 확인
            if self.isWaitingAfterLine:
                self.isWaitingAfterLine = False  # 라인 삭제 후 대기 상태 해제
                self.newPiece()  # 새로운 도형 생성
            else:
                self.oneLineDown()  # 한 줄 아래로 떨어뜨리기
        else:
            super(Board, self).timerEvent(event)  # 다른 타이머 이벤트는 기본 이벤트 처리

    def clearBoard(self):
        """보드를 클리어"""
        for i in range(Board.BoardHeight * Board.BoardWidth):
            self.board.append(Tetrominoe.NoShape)  # 모든 위치를 NoShape로 설정

    def dropDown(self):
        """현재 도형을 가장 낮은 위치까지 떨어뜨림"""
        newY = self.curY
        while newY > 0:
            if not self.tryMove(self.curPiece, self.curX, newY - 1):  # 더 이상 이동할 수 없다면
                break
            newY -= 1
        self.pieceDropped()  # 도형을 떨어뜨린 후 처리

    def oneLineDown(self):
        """도형을 한 줄 아래로 이동"""
        if not self.tryMove(self.curPiece, self.curX, self.curY - 1):  # 이동이 불가능하면
            self.pieceDropped()  # 도형을 떨어뜨린 후 처리

    def pieceDropped(self):
        """도형이 떨어진 후 라인 제거 및 새로운 도형 생성"""
        for i in range(4):
            x = self.curX + self.curPiece.x(i)
            y = self.curY - self.curPiece.y(i)
            self.setShapeAt(x, y, self.curPiece.shape())  # 도형을 보드에 추가

        self.removeFullLines()  # 전체 라인 제거

        if not self.isWaitingAfterLine:  # 라인 제거 후 대기 상태가 아니라면 새로운 도형 생성
            self.newPiece()

    def removeFullLines(self):
        """완전한 라인을 제거"""
        numFullLines = 0
        rowsToRemove = []  # 제거할 라인 저장

        for i in range(Board.BoardHeight):  # 각 라인을 검사
            n = 0
            for j in range(Board.BoardWidth):
                if not self.shapeAt(j, i) == Tetrominoe.NoShape:
                    n = n + 1

            if n == 10:  # 라인이 모두 채워졌다면
                rowsToRemove.append(i)

        rowsToRemove.reverse()  # 제거할 라인 순서를 뒤집음

        for m in rowsToRemove:  # 라인 제거 후 아래쪽 라인들 한 칸씩 올림
            for k in range(m, Board.BoardHeight):
                for l in range(Board.BoardWidth):
                    self.setShapeAt(l, k, self.shapeAt(l, k + 1))

        numFullLines = numFullLines + len(rowsToRemove)

        if numFullLines > 0:  # 제거된 라인이 있다면 상태바에 업데이트
            self.numLinesRemoved = self.numLinesRemoved + numFullLines
            self.msg2Statusbar.emit(str(self.numLinesRemoved))

            self.isWaitingAfterLine = True  # 라인 제거 후 대기 상태로 변경
            self.curPiece.setShape(Tetrominoe.NoShape)  # 현재 도형 초기화
            self.update()

    def newPiece(self):
        """새로운 도형을 생성"""
        self.curPiece = Shape()  # 새로운 도형 객체 생성
        self.curPiece.setRandomShape()  # 랜덤 도형 설정
        self.curX = Board.BoardWidth // 2 + 1  # X 좌표 중앙 설정
        self.curY = Board.BoardHeight - 1 + self.curPiece.minY()  # Y 좌표 설정

        if not self.tryMove(self.curPiece, self.curX, self.curY):  # 이동이 불가능하면 게임 오버
            self.curPiece.setShape(Tetrominoe.NoShape)  # 도형 초기화
            self.timer.stop()  # 타이머 정지
            self.isStarted = False  # 게임 시작 상태 변경
            self.msg2Statusbar.emit("Game over")  # 게임 오버 메시지 표시

    def tryMove(self, newPiece, newX, newY):
        """새로운 도형을 이동하려 시도"""
        for i in range(4):
            x = newX + newPiece.x(i)
            y = newY - newPiece.y(i)

            if x < 0 or x >= Board.BoardWidth or y < 0 or y >= Board.BoardHeight:
                return False  # 보드를 벗어나면 이동 불가

            if self.shapeAt(x, y) != Tetrominoe.NoShape:
                return False  # 이미 도형이 있다면 이동 불가

        self.curPiece = newPiece  # 도형 업데이트
        self.curX = newX  # X 좌표 업데이트
        self.curY = newY  # Y 좌표 업데이트
        self.update()  # 화면 갱신

        return True  # 이동 성공

    def drawSquare(self, painter, x, y, shape):
        """도형의 사각형을 그리는 메서드"""
        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]  # 색상 테이블

        color = QColor(colorTable[shape])  # 색상 설정
        painter.fillRect(x + 1, y + 1, self.squareWidth() - 2,
                         self.squareHeight() - 2, color)  # 사각형 채우기

        painter.setPen(color.lighter())  # 연한 색으로 테두리 그리기
        painter.drawLine(x, y + self.squareHeight() - 1, x, y)
        painter.drawLine(x, y, x + self.squareWidth() - 1, y)

        painter.setPen(color.darker())  # 진한 색으로 하단 테두리 그리기
        painter.drawLine(x + 1, y + self.squareHeight() - 1,
                         x + self.squareWidth() - 1, y + self.squareHeight() - 1)
        painter.drawLine(x + self.squareWidth() - 1,
                         y + self.squareHeight() - 1, x + self.squareWidth() - 1, y + 1)


class Tetrominoe:
    """테트리스 도형 종류를 정의하는 클래스"""
    NoShape = 0  # 빈 도형
    ZShape = 1  # Z 모양
    SShape = 2  # S 모양
    LineShape = 3  # 직선 모양
    TShape = 4  # T 모양
    SquareShape = 5  # 네모 모양
    LShape = 6  # L 모양
    MirroredLShape = 7  # 거울 반전된 L 모양


class Shape:
    """테트리스 도형 클래스"""
    coordsTable = (
        ((0, 0), (0, 0), (0, 0), (0, 0)),  # 빈 도형
        ((0, -1), (0, 0), (-1, 0), (-1, 1)),  # Z 모양
        ((0, -1), (0, 0), (1, 0), (1, 1)),   # S 모양
        ((0, -1), (0, 0), (0, 1), (0, 2)),    # 직선 모양
        ((-1, 0), (0, 0), (1, 0), (0, 1)),    # T 모양
        ((0, 0), (1, 0), (0, 1), (1, 1)),     # 네모 모양
        ((-1, -1), (0, -1), (0, 0), (0, 1)),  # L 모양
        ((1, -1), (0, -1), (0, 0), (0, 1))    # 거울 반전된 L 모양
    )

    def __init__(self):
        """Shape 클래스 초기화"""
        self.coords = [[0, 0] for i in range(4)]  # 좌표 리스트 초기화
        self.pieceShape = Tetrominoe.NoShape  # 도형 모양 초기화
        self.setShape(Tetrominoe.NoShape)  # 초기 도형 설정

    def shape(self):
        """현재 도형을 반환"""
        return self.pieceShape

    def setShape(self, shape):
        """도형 모양 설정"""
        table = Shape.coordsTable[shape]  # 도형에 맞는 좌표 테이블 가져오기
        for i in range(4):
            for j in range(2):
                self.coords[i][j] = table[i][j]  # 좌표 설정
        self.pieceShape = shape  # 도형 모양 설정

    def setRandomShape(self):
        """랜덤 도형 설정"""
        self.setShape(random.randint(1, 7))  # 1부터 7 사이의 랜덤 숫자

    def x(self, index):
        """x 좌표 반환"""
        return self.coords[index][0]

    def y(self, index):
        """y 좌표 반환"""
        return self.coords[index][1]

    def setX(self, index, x):
        """x 좌표 설정"""
        self.coords[index][0] = x

    def setY(self, index, y):
        """y 좌표 설정"""
        self.coords[index][1] = y

    def minX(self):
        """최소 x 값 반환"""
        m = self.coords[0][0]
        for i in range(4):
            m = min(m, self.coords[i][0])  # 최소값 찾기
        return m

    def maxX(self):
        """최대 x 값 반환"""
        m = self.coords[0][0]
        for i in range(4):
            m = max(m, self.coords[i][0])  # 최대값 찾기
        return m

    def minY(self):
        """최소 y 값 반환"""
        m = self.coords[0][1]
        for i in range(4):
            m = min(m, self.coords[i][1])  # 최소값 찾기
        return m

    def maxY(self):
        """최대 y 값 반환"""
        m = self.coords[0][1]
        for i in range(4):
            m = max(m, self.coords[i][1])  # 최대값 찾기
        return m

    def rotateLeft(self):
        """왼쪽으로 회전"""
        if self.pieceShape == Tetrominoe.SquareShape:
            return self  # 네모 모양은 회전하지 않음

        result = Shape()
        result.pieceShape = self.pieceShape
        for i in range(4):
            result.setX(i, self.y(i))  # x, y 좌표 교환하여 회전
            result.setY(i, -self.x(i))
        return result

    def rotateRight(self):
        """오른쪽으로 회전"""
        if self.pieceShape == Tetrominoe.SquareShape:
            return self  # 네모 모양은 회전하지 않음

        result = Shape()
        result.pieceShape = self.pieceShape
        for i in range(4):
            result.setX(i, -self.y(i))  # y, x 좌표 교환하여 회전
            result.setY(i, self.x(i))
        return result


def main():
    """게임 실행"""
    app = QApplication([])  # QApplication 객체 생성
    tetris = Tetris()  # Tetris 객체 생성
    sys.exit(app.exec())  # 애플리케이션 실행


if __name__ == '__main__':
    main()  # 프로그램 실행
