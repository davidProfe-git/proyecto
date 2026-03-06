from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
import random
import sys
import json
import os

# Configuration
WIDTH, HEIGHT = 10, 20
BLOCK_SIZE = 30
HIGHSCORE_FILE = 'highscores.json'
MAX_HIGHS = 3

# Colors
COLORS = [
    QColor(0, 255, 255),  # I
    QColor(255, 255, 0),  # O
    QColor(128, 0, 128),  # T
    QColor(0, 255, 0),    # S
    QColor(255, 0, 0),    # Z
    QColor(0, 0, 255),    # J
    QColor(255, 165, 0),  # L
]

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
]


def rotate(shape):
    return [list(row) for row in zip(*shape[::-1])]


def load_highscores():
    if not os.path.exists(HIGHSCORE_FILE):
        return []
    with open(HIGHSCORE_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_highscores(scores):
    with open(HIGHSCORE_FILE, 'w') as f:
        json.dump(scores[:MAX_HIGHS], f)


def add_score(score):
    scores = load_highscores()
    scores.insert(0, score)
    scores.sort(reverse=True)
    save_highscores(scores)


class Tetris(QMainWindow):
    def __init__(self):
        super().__init__()

        self.board = Board(self)
        self.setCentralWidget(self.board)

        self.statusbar = self.statusBar()
        self.board.msg2statusbar[str].connect(self.statusbar.showMessage)

        self.board.start()

        self.setWindowTitle('Tetris')
        self.setFixedSize(WIDTH * BLOCK_SIZE, HEIGHT * BLOCK_SIZE)  # Disable fullscreen by fixing the window size
        self.show()


class Board(QFrame):
    msg2statusbar = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)

        self.timer = QBasicTimer()
        self.is_paused = False
        self.is_started = False
        self.board = [[0] * WIDTH for _ in range(HEIGHT)]
        self.current_shape = None
        self.current_pos = None
        self.score = 0

        self.setFocusPolicy(Qt.StrongFocus)

    def start(self):
        self.is_started = True
        self.is_paused = False
        self.clear_board()
        self.new_shape()
        self.timer.start(300, self)
        self.msg2statusbar.emit(str(self.score))

    def pause(self):
        if not self.is_started:
            return

        self.is_paused = not self.is_paused

        if self.is_paused:
            self.timer.stop()
            self.msg2statusbar.emit('Paused')
        else:
            self.timer.start(300, self)

        self.update()

    def clear_board(self):
        self.board = [[0] * WIDTH for _ in range(HEIGHT)]

    def new_shape(self):
        self.current_shape = random.choice(SHAPES)
        color = random.randint(1, len(COLORS))
        self.current_shape = [[cell * color for cell in row] for row in self.current_shape]
        self.current_pos = (-len(self.current_shape), WIDTH // 2 - len(self.current_shape[0]) // 2)

        if self.check_collision(self.current_pos):
            self.timer.stop()
            self.is_started = False
            self.msg2statusbar.emit('Game Over')

    def check_collision(self, pos):
        y0, x0 = pos
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    ny, nx = y0 + y, x0 + x
                    # Ensure the tetromino stays within the defined arc (board boundaries)
                    if nx < 0 or nx >= WIDTH or ny >= HEIGHT:
                        return True
                    if ny >= 0 and self.board[ny][nx]:
                        return True
        return False

    def merge_shape(self):
        y0, x0 = self.current_pos
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell:
                    self.board[y0 + y][x0 + x] = cell

    def clear_lines(self):
        new_board = [row for row in self.board if not all(row)]
        cleared = HEIGHT - len(new_board)
        for _ in range(cleared):
            new_board.insert(0, [0] * WIDTH)
        self.board = new_board
        self.score += cleared * 100
        self.msg2statusbar.emit(str(self.score))

        # End the game if the score reaches 500
        if self.score >= 500:
            self.timer.stop()
            self.is_started = False
            self.msg2statusbar.emit('Game Over - You reached 500 points!')

    def paintEvent(self, event):
        painter = QPainter(self)
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell:
                    color = COLORS[cell - 1]
                    painter.fillRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE, color)
                    painter.drawRect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)

        if self.current_shape:
            y0, x0 = self.current_pos
            for y, row in enumerate(self.current_shape):
                for x, cell in enumerate(row):
                    if cell:
                        color = COLORS[cell - 1]
                        painter.fillRect((x0 + x) * BLOCK_SIZE, (y0 + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE, color)
                        painter.drawRect((x0 + x) * BLOCK_SIZE, (y0 + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)

    def keyPressEvent(self, event):
        if not self.is_started or not self.current_shape:
            return

        key = event.key()

        if key == Qt.Key_Left:
            new_pos = (self.current_pos[0], self.current_pos[1] - 1)
            if not self.check_collision(new_pos):
                self.current_pos = new_pos
        elif key == Qt.Key_Right:
            new_pos = (self.current_pos[0], self.current_pos[1] + 1)
            if not self.check_collision(new_pos):
                self.current_pos = new_pos
        elif key == Qt.Key_Down:
            self.drop()
        elif key == Qt.Key_Space:
            new_shape = rotate(self.current_shape)
            if not self.check_collision(self.current_pos):
                self.current_shape = new_shape

        self.update()

    def drop(self):
        new_pos = (self.current_pos[0] + 1, self.current_pos[1])
        if not self.check_collision(new_pos):
            self.current_pos = new_pos
        else:
            self.merge_shape()
            self.clear_lines()
            self.new_shape()

        self.update()

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.drop()
        else:
            super(Board, self).timerEvent(event)


def rotate_shape(self):
    new_shape = rotate(self.current_shape)
    y0, x0 = self.current_pos

    # Check if the rotated shape goes out of bounds on the right
    max_x = x0 + len(new_shape[0])
    if max_x > WIDTH:
        x0 -= max_x - WIDTH  # Shift left to fit within bounds

    # Ensure the rotated shape does not collide after adjustment
    if not self.check_collision((y0, x0)):
        self.current_shape = new_shape
        self.current_pos = (y0, x0)


def main():
    app = QApplication(sys.argv)
    tetris = Tetris()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
