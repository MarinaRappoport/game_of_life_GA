import tkinter

import numpy as np

from board import Board

CELL_WIDTH = 5
CELL_HEIGHT = 5


class Gui:
    def __init__(self, board, max_lifespan, margin):
        self.width = board.width + margin*2
        self.height = board.height + margin*2
        self.board = board
        self.max_lifespan = max_lifespan
        matrix = board.matrix
        self.window = tkinter.Tk()
        self.window.title("Methuselah by Marina Rappoport")
        self.label = tkinter.Label(text="Gen 1")
        self.label.pack()
        self.item_ids = [[0] * self.width for _ in range(self.height)]
        self.canvas = tkinter.Canvas(self.window, height=self.height * CELL_HEIGHT, width=self.width * CELL_WIDTH)
        self.canvas.pack()
        for x in range(self.width):
            for y in range(self.height):
                color = 'white'
                if margin <= x < (self.width - margin) and margin <= y < (self.height - margin):
                    color = 'black' if matrix[y-margin][x-margin] == 1 else 'white'
                cell_id = self.canvas.create_rectangle(x * CELL_WIDTH, y * CELL_HEIGHT, (x + 1) * CELL_WIDTH,
                                                       (y + 1) * CELL_HEIGHT,
                                                       fill=color)
                self.item_ids[y][x] = cell_id


class TimerUpdate:
    def __init__(self, gui):
        self.gui = gui
        self.day = 1
        self.update()

    def update(self):
        if self.gui.board.lifespan == self.gui.max_lifespan:
            self.gui.label.config(text="COMPLETE! Step {}".format(self.gui.board.lifespan))
        else:
            self.gui.board.update_board()
            board = self.gui.board
            matrix = board.matrix
            margin = int((self.gui.width - board.width) / 2)
            self.gui.window.after(100, self.update)
            self.gui.label.config(text="Step {}".format(self.gui.board.lifespan))
            for x in range(self.gui.width):
                for y in range(self.gui.height):
                    if margin <= x < (self.gui.width - margin) and margin <= y < (self.gui.height - margin):
                        color = 'black' if matrix[y - margin][x - margin] == 1 else 'white'
                        self.gui.canvas.itemconfig(self.gui.item_ids[y][x], fill=color)


# res = []
# for i in range(10):
#     res.append(np.arange(10*i, 10*(i+1)))
#
# res = np.array(res)
# slice = res[0:res.shape[0],0:res.shape[1]]

pattern = np.fromstring('1 1 1 1 0 1 0 0 1', dtype=int, sep=' ')
board = Board(pattern, 3, 3)
gui = Gui(board,300, 50)
tkinter.Button(text="Start", command=lambda: TimerUpdate(gui)).pack()
gui.window.mainloop()