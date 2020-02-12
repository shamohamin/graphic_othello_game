from tkinter import *
from .gamelogic import Logic, Point
import sys
import time


class OthelloFrame(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.board = [[0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 1, 2, 0, 0, 0],
                      [0, 0, 0, 2, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0]]
        self.temp = [[0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 1, 2, 0, 0, 0],
                      [0, 0, 0, 2, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0]]
        self.canvas = Canvas(self)
        self.canvas.bind("<Button-1>", self.event_handling)
        self.turn = 1
        self.make_field()
        self.run()

    def make_field(self):
        # canvas = Canvas(self)
        x1, y1, offset = 0, 0, 15

        for x in self.board:
            for y in x:
                if y == 0:
                    self.canvas.create_rectangle(x1, y1, x1+offset, y1+offset, fill="black", outline="white")
                elif y == 1:
                    self.canvas.create_rectangle(x1, y1, x1+offset, y1+offset, fill="red", outline="white")
                elif y == 2:
                    self.canvas.create_rectangle(x1, y1, x1+offset, y1+offset, fill="blue", outline="white")
                x1 += 15
            x1 = 0
            y1 = y1 + 15

        self.canvas.pack()
        self.pack()

    def run(self):
        logic = Logic(1)
        if not logic.game_over(self.board):
            if self.turn == 1:
                self.cop()
                point = logic.minimax_decision(self.temp, 1)
                print(point)
                logic.print(self.board)
                logic.make_move(self.board, point)
                self.cop()
                logic.print(self.temp)
                self.pack_forget()
                self.make_field()
                self.turn = 2
                # time.sleep(2)

        # sys.exit(1)

    def cop(self):
        for (index_x, x) in enumerate(self.board):
            for (index_y, y) in enumerate(x):
                self.temp[index_x][index_y] = y

    def event_handling(self, event):
        position = "(x={}, y={})".format(event.x, event.y)
        x = int(event.x / 15)
        y = int(event.y / 15)
        self.board[y][x] = 2
        print("{}:{}".format(x, y))
        print(event.type, "event", position)
        self.make_field()
        self.turn = 1
        self.run()
