import tkinter as tk
import random
import json
import os

# Configuration
WIDTH, HEIGHT = 10, 20
BLOCK_SIZE = 30
HIGHSCORE_FILE = 'highscores.json'
MAX_HIGHS = 3

# Colors
COLORS = [
    "cyan",  # I
    "yellow",  # O
    "purple",  # T
    "green",  # S
    "red",  # Z
    "blue",  # J
    "orange",  # L
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


def draw_board(canvas, board):
    canvas.delete("all")
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                color = COLORS[cell - 1]
                canvas.create_rectangle(
                    x * BLOCK_SIZE, y * BLOCK_SIZE,
                    (x + 1) * BLOCK_SIZE, (y + 1) * BLOCK_SIZE,
                    fill=color, outline="black"
                )


def merge_shape(board, shape, pos):
    y0, x0 = pos
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                board[y0 + y][x0 + x] = cell


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
    root = tk.Tk()
    root.title("Tetris")

    canvas = tk.Canvas(root, width=WIDTH * BLOCK_SIZE, height=HEIGHT * BLOCK_SIZE, bg="white")
    canvas.pack()

    board = [[0] * WIDTH for _ in range(HEIGHT)]
    score = 0

    shape = random.choice(SHAPES)
    color = random.randint(1, len(COLORS))
    shape = [[cell * color for cell in row] for row in shape]
    pos = (-len(shape), WIDTH // 2 - len(shape[0]) // 2)

    def drop():
        nonlocal shape, pos, board, score
        new_pos = (pos[0] + 1, pos[1])
        if not collision(board, shape, new_pos):
            pos = new_pos
        else:
            if pos[0] < 0:
                add_score(score)
                root.destroy()
                return
            merge_shape(board, shape, pos)
            board, cleared = clear_lines(board)
            score += cleared * 100
            shape = random.choice(SHAPES)
            color = random.randint(1, len(COLORS))
            shape = [[cell * color for cell in row] for row in shape]
            pos = (-len(shape), WIDTH // 2 - len(shape[0]) // 2)
        draw_board(canvas, board)
        draw_board(canvas, [[0] * WIDTH for _ in range(HEIGHT)])
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    canvas.create_rectangle(
                        (pos[1] + x) * BLOCK_SIZE, (pos[0] + y) * BLOCK_SIZE,
                        (pos[1] + x + 1) * BLOCK_SIZE, (pos[0] + y + 1) * BLOCK_SIZE,
                        fill=COLORS[cell - 1], outline="black"
                    )
        root.after(500, drop)

    def move_left(event):
        nonlocal pos
        new_pos = (pos[0], pos[1] - 1)
        if not collision(board, shape, new_pos):
            pos = new_pos

    def move_right(event):
        nonlocal pos
        new_pos = (pos[0], pos[1] + 1)
        if not collision(board, shape, new_pos):
            pos = new_pos

    def move_down(event):
        nonlocal pos
        new_pos = (pos[0] + 1, pos[1])
        if not collision(board, shape, new_pos):
            pos = new_pos

    def rotate_shape(event):
        nonlocal shape
        new_shape = rotate(shape)
        if not collision(board, new_shape, pos):
            shape = new_shape

    root.bind("<Left>", move_left)
    root.bind("<Right>", move_right)
    root.bind("<Down>", move_down)
    root.bind("<space>", rotate_shape)

    drop()
    root.mainloop()


def main():
    game()
    print("Game Over")
    print("Recent High Scores:")
    for i, s in enumerate(load_highscores()[:MAX_HIGHS], start=1):
        print(f"{i}. {s}")


if __name__ == '__main__':
    main()
