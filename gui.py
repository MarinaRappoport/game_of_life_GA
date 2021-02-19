import tkinter

import numpy as np

from board import Board

CELL_WIDTH = 5
CELL_HEIGHT = 5


class Gui:
    """ Class to visualise the board"""
    def __init__(self, board, max_lifespan, margin):
        self.width = board.width + margin*2
        self.height = board.height + margin*2
        self.board = board
        self.max_lifespan = max_lifespan
        matrix = board.matrix
        self.window = tkinter.Tk()
        self.window.title("Methuselah by Marina Rappoport")
        self.label = tkinter.Label(text="Initial pattern")
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
    """ Class to update the gui according to timer"""
    def __init__(self, gui):
        self.gui = gui
        self.update()

    def update(self):
        if self.gui.board.lifespan == self.gui.max_lifespan:
            self.gui.label.config(text="Step {}".format(self.gui.board.lifespan))
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


def show_evolution_chromosome(to_show, steps):
    """ For debugging and visualisation"""
    pattern = np.fromstring('1 1 0 1 0 1 0 1 0 1', dtype=int, sep=' ')
    board = Board(pattern, 2)
    if to_show:
        gui = Gui(board,steps, 50)
        tkinter.Button(text="Start", command=lambda: TimerUpdate(gui)).pack()
        gui.window.mainloop()
    else:
        board.print_pattern()
        board.evolve(steps)
        board.print_data()

# show_evolution_chromosome(True, 50)
