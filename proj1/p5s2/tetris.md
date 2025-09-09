이 코드는 **PyQt6**를 사용하여 **테트리스(Tetris)** 게임을 구현한 것입니다. 게임의 흐름을 이해하려면, 프로그램이 실행되는 순서대로 주요 클래스를 살펴봐야 합니다. 아래에서 게임이 실행되는 과정과 함께 각 코드의 역할을 설명할게요.

### 1. **프로그램 시작 (`main` 함수)**

```python
def main():
    app = QApplication([])  # QApplication 객체 생성
    tetris = Tetris()  # Tetris 객체 생성
    sys.exit(app.exec())  # 애플리케이션 실행
```

* **`QApplication([])`**: PyQt6 애플리케이션을 실행할 때 필수적으로 필요한 객체입니다. 이 객체는 GUI 애플리케이션의 이벤트 루프를 처리합니다.
* **`Tetris()`**: `Tetris` 클래스의 객체를 생성하여 게임의 메인 윈도우를 띄웁니다.
* **`app.exec()`**: 이벤트 루프를 시작합니다. 이 함수가 호출된 후, 애플리케이션이 종료될 때까지 계속 실행됩니다.

### 2. **`Tetris` 클래스 (게임 윈도우)**

`Tetris` 클래스는 `QMainWindow`를 상속하여 게임의 메인 윈도우를 구성합니다. 게임의 초기화와 화면 구성, 윈도우 중앙 정렬 등을 담당합니다.

#### `Tetris.__init__()`와 `initUI()`

```python
class Tetris(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
```

* **`initUI()`**: 게임 화면을 초기화합니다. `Board` 클래스를 중앙 위젯으로 설정하고, 상태바를 준비한 후, 게임을 시작합니다.

#### `initUI()` 함수의 주요 역할:

1. **`self.tboard = Board(self)`**: 게임 보드를 담당하는 `Board` 객체를 생성합니다.
2. **`self.setCentralWidget(self.tboard)`**: `Tetris` 윈도우의 중앙 위젯으로 `Board`를 설정합니다. 즉, 게임 보드가 윈도우의 주요 영역을 차지하게 됩니다.
3. **`self.statusbar = self.statusBar()`**: 상태바를 설정하여 점수와 게임 상태(예: "paused", "Game over")를 표시합니다.
4. **`self.tboard.start()`**: 게임을 시작합니다.
5. **`self.resize(360, 760)`**: 윈도우 크기를 설정합니다.
6. **`self.center()`**: 게임 윈도우를 화면의 중앙에 위치시킵니다.

#### `center()` 함수

윈도우를 화면의 중앙에 배치하는 함수입니다.

```python
def center(self):
    qr = self.frameGeometry()
    cp = self.screen().availableGeometry().center()
    qr.moveCenter(cp)
    self.move(qr.topLeft())
```

### 3. **`Board` 클래스 (게임 보드)**

`Board` 클래스는 실제 게임 보드와 관련된 모든 로직을 처리합니다. 도형의 움직임, 라인 제거, 도형 생성 등을 담당합니다.

#### `Board.__init__()`와 `initBoard()`

```python
class Board(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()

    def initBoard(self):
        self.timer = QBasicTimer()  # 타이머 설정
        self.isWaitingAfterLine = False  # 라인 제거 후 대기 상태
        self.curX = 0  # 현재 도형의 X 좌표
        self.curY = 0  # 현재 도형의 Y 좌표
        self.numLinesRemoved = 0  # 제거된 라인 수
        self.board = []  # 보드 상태
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)  # 키보드 입력을 받을 수 있도록 설정
        self.isStarted = False  # 게임 시작 여부
        self.isPaused = False  # 게임 일시 정지 여부
        self.clearBoard()  # 보드 초기화
```

* **`self.timer = QBasicTimer()`**: 게임의 타이머를 설정합니다. 타이머는 도형을 일정한 시간 간격으로 이동시키는 데 사용됩니다.
* **`self.clearBoard()`**: 보드의 상태를 초기화합니다. 게임이 시작되면 모든 칸은 `NoShape`로 설정되어 빈 상태로 시작됩니다.

#### `start()` 함수

```python
def start(self):
    if self.isPaused:
        return
    self.isStarted = True
    self.isWaitingAfterLine = False
    self.numLinesRemoved = 0
    self.clearBoard()  # 보드 초기화
    self.msg2Statusbar.emit(str(self.numLinesRemoved))  # 상태바에 점수 표시
    self.newPiece()  # 새로운 도형 생성
    self.timer.start(Board.Speed, self)  # 타이머 시작
```

* \*\*`self.isPaused`\*\*가 `True`인 경우에는 게임을 시작하지 않고 종료합니다.
* 게임이 시작되면 \*\*`clearBoard()`\*\*를 호출하여 보드를 초기화하고, \*\*`newPiece()`\*\*를 호출하여 새로운 도형을 생성합니다.
* \*\*`self.timer.start(Board.Speed, self)`\*\*는 타이머를 시작하여 일정 시간 간격으로 \*\*`timerEvent()`\*\*를 호출합니다.

#### `timerEvent()` 함수

```python
def timerEvent(self, event):
    if event.timerId() == self.timer.timerId():
        if self.isWaitingAfterLine:
            self.isWaitingAfterLine = False
            self.newPiece()  # 새로운 도형 생성
        else:
            self.oneLineDown()  # 도형을 한 줄 아래로 내려줌
    else:
        super(Board, self).timerEvent(event)
```

* \*\*`timerEvent()`\*\*는 타이머가 동작할 때마다 호출됩니다. 이 함수는 게임의 주요 동작을 처리합니다.

  * \*\*`self.isWaitingAfterLine`\*\*이 `True`일 경우, 즉 라인 제거 후 대기 상태일 경우, 새로운 도형을 생성합니다.
  * 그 외의 경우, \*\*`oneLineDown()`\*\*을 호출하여 현재 도형을 한 줄 아래로 이동시킵니다.

### 4. **`Shape` 클래스 (도형)**

`Shape` 클래스는 테트리스 도형의 모양과 좌표를 관리합니다. 도형은 4개의 작은 블록으로 이루어져 있으며, 이 블록들이 보드 위에 놓입니다.

#### `Shape.setRandomShape()`

```python
def setRandomShape(self):
    self.setShape(random.randint(1, 7))  # 랜덤 도형 설정
```

* \*\*`setRandomShape()`\*\*는 1부터 7까지의 숫자 중 하나를 랜덤으로 선택하고, 해당 번호에 맞는 도형을 생성합니다.

#### 도형 회전

```python
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
```

* **`rotateLeft()`**: 도형을 왼쪽으로 회전시킵니다. `SquareShape`는 회전하지 않습니다.
* **`rotateRight()`**: 도형을 오른쪽으로 회전시킵니다. `SquareShape`는 회전하지 않습니다.

### 5. **`Tetrominoe` 클래스 (도형 종류)**

`Tetrominoe` 클래스는 테트리스에서 사용되는 도형들의 종류를 정의합니다. 각 도형은 고유한 번호로 식별됩니다.

```python
class Tetrominoe:
    NoShape = 0
    ZShape = 1
    SShape = 2
    LineShape = 3
    TShape = 4
    SquareShape = 5
    LShape = 6
    MirroredLShape = 7
```

### 게임 흐름 요약

1. **게임 시작**: `main()`에서 `Tetris` 클래스가 초기화되고, `initUI()` 함수가 호출되어 게임을 시작합니다.
2. **보드 초기화**: `Board` 클래스가 초기화되고, `start()` 함수에서 게임을 시작합니다. `clearBoard()`로 보드를 초기화하고, 새로운 도형을 생성합니다.
3. **도형 움직이기**: 타이머가 작동하여 도형이 일정 시간 간격으로 아래로 내려가고, 키보드 입력에 따라 도형을 이동하거나 회전시킬 수 있습니다.
4. **라인 제거**: 도형이 바닥에 도달하면 해당 도형을 보드에 배치하고, `removeFullLines()`를 호출하여 가득 찬 라인을 제거합니다.
5. **게임 종료**: 새로운 도형을 생성할 수 없으면 "Game over" 메시지가 표시되고 게임이 종료됩니다.

이런 방식으로 게임이 진행됩니다.
