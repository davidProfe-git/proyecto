from blessed import Terminal
import random
import time
import json
import os

# Configuration
term = Terminal()
WIDTH = 10
HEIGHT = 20
TICK_RATE = 0.5  # seconds per drop
HIGHSCORE_FILE = 'highscores.json'
MAX_HIGHS = 3

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


def draw_board(board, score):
    with term.location():
        print(term.clear)
        for y, row in enumerate(board):
            for x, cell in enumerate(row):
                ch = '#' if cell else '.'
                print(term.move_xy(x, y) + ch, end='')
        print(term.move_xy(WIDTH + 2, 0) + f"Score: {score}")


def merge_shape(board, shape, pos):
    y0, x0 = pos
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                board[y0 + y][x0 + x] = 1


def collision(board, shape, pos):
    y0, x0 = pos
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                ny, nx = y0 + y, x0 + x
                if nx < 0 or nx >= WIDTH or ny >= HEIGHT:
                    return True
                if ny >= 0 and board[ny][nx]:
                    return True
    return False


def clear_lines(board):
    new_board = [row for row in board if not all(row)]
    cleared = HEIGHT - len(new_board)
    for _ in range(cleared):
        new_board.insert(0, [0] * WIDTH)
    return new_board, cleared


def game():
    board = [[0] * WIDTH for _ in range(HEIGHT)]
    score = 0

    shape = random.choice(SHAPES)
    pos = (-len(shape), WIDTH // 2 - len(shape[0]) // 2)
    drop_time = time.time()

    with term.cbreak(), term.hidden_cursor():
        while True:
            now = time.time()
            if now - drop_time > TICK_RATE:
                new_pos = (pos[0] + 1, pos[1])
                if not collision(board, shape, new_pos):
                    pos = new_pos
                else:
                    if pos[0] < 0:
                        # game over
                        add_score(score)
                        return score
                    merge_shape(board, shape, pos)
                    board, cleared = clear_lines(board)
                    score += cleared * 100
                    shape = random.choice(SHAPES)
                    pos = (-len(shape), WIDTH // 2 - len(shape[0]) // 2)
                drop_time = now

            draw_board(board, score)

            key = term.inkey(timeout=0.01)
            if key.name == "KEY_LEFT":
                new_pos = (pos[0], pos[1] - 1)
                if not collision(board, shape, new_pos):
                    pos = new_pos
            elif key.name == "KEY_RIGHT":
                new_pos = (pos[0], pos[1] + 1)
                if not collision(board, shape, new_pos):
                    pos = new_pos
            elif key.name == "KEY_DOWN":
                new_pos = (pos[0] + 1, pos[1])
                if not collision(board, shape, new_pos):
                    pos = new_pos
            elif key == ' ':  # Space to rotate
                new_shape = rotate(shape)
                if not collision(board, new_shape, pos):
                    shape = new_shape


def main():
    score = game()

    print("Game Over")
    print(f"Your score: {score}")
    print("Recent High Scores:")
    for i, s in enumerate(load_highscores()[:MAX_HIGHS], start=1):
        print(f"{i}. {s}")


if __name__ == '__main__':
    main()
