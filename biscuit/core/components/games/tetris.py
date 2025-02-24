import tkinter as tk
from tkinter import messagebox
import random
from collections import Counter

from .game import BaseGame

SIDE = 25
WIDTH = 10 * SIDE
HEIGHT = 15 * SIDE


class Tetris(BaseGame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, None, None, *args, **kwargs)
        self.master = master
        self.base = master.base

        self.config(bg='#F4EEE0')
        
        self.path = "games/tetris"
        self.diff = False
        self.exists = False
        self.filename = "Tetris"
        self.content = None
        self.loop = None

        self.status_var = tk.StringVar()
        self.status_label = tk.Label(self, textvariable=self.status_var, font='Fixedsys 18', bg='#F4EEE0', fg='#B99B6B')
        self.status_label.pack(side='top', pady=5)

        self.board = tk.Canvas(self, width=WIDTH, height=HEIGHT, bg='#F1DFB4')
        self.board.pack(side='left', padx=(40, 20), expand=True)
        
        self.preview = tk.Canvas(self, width=5*SIDE, height=5*SIDE, bg='#F1DFB4')
        self.preview.pack(padx=(0, 40), expand=True, side=tk.TOP)

        self.controls = tk.Text(self, relief=tk.FLAT, 
            bg='#F4EEE0', insertbackground='#F4EEE0', fg='#F4EEE0')
        self.controls.pack(fill=tk.BOTH, side=tk.BOTTOM)

        self.controls.bind("<Key>", self.handle_events)
        self.bind('<Motion>', lambda _: self.controls.focus())
        self.start()

    def start(self):
        self.board.delete('all')
        self.score = 0
        self.level = 1
        self.speed = 500
        self.pieces = {}
        self.lines_cleared = [0]
        self.total_lines = 0
        self.update_status()
        self.falling_piece = Piece(self.preview)
        self.preview.delete('all')
        self.falling_piece.canvas = self.board
        self.falling_piece.place_on_board()
        self.next_piece = Piece(self.preview)
        self.run()

    def run(self):
        if not self.falling_piece.move(0, 1):
            self.clear_lines()
            self.update_status()
            self.falling_piece = self.next_piece
            self.falling_piece.canvas = self.board
            self.falling_piece.place_on_board()
            self.preview.delete('all')
            self.next_piece = Piece(self.preview)
            if not self.falling_piece.is_move_allowed(0,1):
                self.game_over()
                return

        self.loop = self.after(self.speed, self.run)

    def game_over(self):
        res = messagebox.askyesno(title="GAME OVER", message = f"Level: {self.level}  Score: {self.score}\nRetry?")
        if res:
            self.start()
        else:
            return
        
    def destroy(self):
        self.after_cancel(self.loop)
        return super().destroy()

    def clear_lines(self):
        lines = 0

        all_squares = self.board.find_all()
        all_squares_h = {k : v for k,v in zip(all_squares, [self.board.coords(sq)[3] for sq in all_squares])}
        count = Counter()
        for sq in all_squares_h.values(): count[sq] += 1
        full_lines = [k for k,v in count.items() if v == WIDTH/SIDE]
        
        if full_lines:
            lines = len(full_lines)
            remaining_squares_h = {}
            for k,v in all_squares_h.items():
                if v in full_lines:
                    self.board.delete(k)
                else:
                    remaining_squares_h[k] = v
            all_squares_h = remaining_squares_h

            for sq, h in all_squares_h.items():
                for line in full_lines:
                    if h < line:
                        self.board.move(sq, 0, SIDE)

        self.lines_cleared.append(lines)
        self.total_lines += lines

    def handle_events(self, event):
        if event.keysym in ("Left", "a"):
            self.falling_piece.move(-1, 0)
        if event.keysym in ("Right", "d"):
            self.falling_piece.move(1, 0)
        if event.keysym in ("Down", "s"):
            self.falling_piece.move(0, 1)
        if event.keysym in ("Up", "w"):
            self.falling_piece.rotate()
        
        return "break"

    def update_status(self):

        points = [0, 40, 100, 300, 1200]
        self.score += self.level * points[self.lines_cleared[-1]]
        self.level = 1 + divmod(self.total_lines, 10)[0]
        self.status_var.set(f"Level: {self.level} Score: {self.score}")
        self.speed = 500 - 20*self.level


class Piece:
    START_PT = 10*SIDE // 2 // SIDE * SIDE - SIDE

    def __init__(self, canvas):
        self.PIECES = [
            ["#A9907E", (0, 0), (1, 0), (0, 1), (1, 1)],     # square
            ["#698269", (0, 0), (1, 0), (2, 0), (3, 0)],  # line
            ["#ABC4AA", (2, 0), (0, 1), (1, 1), (2, 1)],     # right el
            ["#675D50", (0, 0), (0, 1), (1, 1), (2, 1)],       # left el
            ["#609966", (0, 1), (1, 1), (1, 0), (2, 0)],      # right wedge
            ["#B99B6B", (0, 0), (1, 0), (1, 1), (2, 1)],        # left wedge
            ["#AA5656", (1, 0), (0, 1), (1, 1), (2, 1)],     # symmetrical wedge
        ]
        random.shuffle(self.PIECES)

        self.squares = []
        self.piece = random.choice(self.PIECES)
        self.color = self.piece.pop(0)
        self.canvas = canvas

        for point in self.piece:
            square = canvas.create_rectangle(
                point[0] * SIDE + 10,
                point[1] * SIDE + 10,
                point[0] * SIDE + SIDE + 10,
                point[1] * SIDE + SIDE + 10,
                fill=self.color, outline=self.color)
            self.squares.append(square)

    def place_on_board(self):
        self.squares = []
        for point in self.piece:
            square = self.canvas.create_rectangle(
                point[0] * SIDE + Piece.START_PT,
                point[1] * SIDE,
                point[0] * SIDE + SIDE + Piece.START_PT,
                point[1] * SIDE + SIDE,
                fill=self.color, outline=self.color)
            self.squares.append(square)

    def move(self, x, y):
        if not self.is_move_allowed(x, y):
            return False
        else:
            for square in self.squares:
                self.canvas.move(square, x * SIDE, y * SIDE)
            return True

    def rotate(self):
        squares = self.squares[:]
        pivot = squares.pop(2)

        def get_move_coords(square, pivot):
            sq_coords = self.canvas.coords(square)
            pivot_coords = self.canvas.coords(pivot)
            x_diff = sq_coords[0] - pivot_coords[0]
            y_diff = sq_coords[1] - pivot_coords[1]
            x_move = (- x_diff - y_diff) / SIDE
            y_move = (x_diff - y_diff) / SIDE
            return x_move, y_move

        for sq in squares:
            xmove, ymove = get_move_coords(sq, pivot)
            if not self.is_sq_allowed(sq, xmove, ymove):
                return False

        for sq in squares:
            xmove, ymove = get_move_coords(sq, pivot)
            self.canvas.move(sq, xmove*SIDE, ymove*SIDE)

    def is_sq_allowed(self, sq, x, y):

        x = x * SIDE
        y = y * SIDE
        coords = self.canvas.coords(sq)

        if coords[3] + y > HEIGHT:
            return False
        if coords[2] + x <= 0:
            return False
        if coords[2] + x > WIDTH:
            return False

        overlap = set(self.canvas.find_overlapping(
            (coords[0] + coords[2]) / 2 + x,
            (coords[1] + coords[3]) / 2 + y,
            (coords[0] + coords[2]) / 2 + x,
            (coords[1] + coords[3]) / 2 + y)) - set(self.squares)

        other = set(self.canvas.find_all()) - set(self.squares)

        if overlap and other:
            return False

        return True

    def is_move_allowed(self, x, y):

        for sq in self.squares:
            if not self.is_sq_allowed(sq, x, y):
                return False
        return True
