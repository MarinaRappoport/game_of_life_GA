import numpy as np

BOARD_RESIZE_STEP = 2
MAX_BOARD_WIDTH = 100
MAX_BOARD_HEIGHT = 100


def apply_game_of_life_rules(matrix, x, y, ):
    """ Game of life rules for 1 cell"""
    is_alive = matrix[x][y] == 1
    count = neighbors_count(matrix, x, y)
    if count == 3:
        return 1
    if is_alive and count == 2:
        return 1
    else:
        return 0


def neighbors_count(matrix, x, y):
    """ Count neighbors of the cell"""
    width = len(matrix[0])
    height = len(matrix)
    neighbours_count = 0
    if x > 0:
        neighbours_count += matrix[x - 1][y]
        if y > 0:
            neighbours_count += matrix[x - 1][y - 1]
        if y < width - 1:
            neighbours_count += matrix[x - 1][y + 1]
    if x < height - 1:
        neighbours_count += matrix[x + 1][y]
        if y > 0:
            neighbours_count += matrix[x + 1][y - 1]
        if y < width - 1:
            neighbours_count += matrix[x + 1][y + 1]
    if y > 0:
        neighbours_count += matrix[x][y - 1]
    if y < width - 1:
        neighbours_count += matrix[x][y + 1]
    return neighbours_count


class Board:
    """ Class that contains all info about the board"""
    def __init__(self, chromosome, num_columns):
        self.init_config = np.reshape(chromosome, (-1, num_columns))
        self.init_config_size = np.sum(self.init_config)
        self.max_config_size = self.init_config_size
        self.current_config_size = self.init_config_size
        self.lifespan = 0
        # resize board
        self.matrix = self.init_config
        self.resize_board()
        self.width = len(self.matrix[0])
        self.height = len(self.matrix)
        # save last 3 states to find cycles
        self.board_history = []
        self.is_cycle = False

    def resize_board(self):
        """ Dynamically add to current board extra margin"""
        init_width = len(self.matrix[0])
        init_height = len(self.matrix)
        if init_width >= MAX_BOARD_WIDTH or init_height >= MAX_BOARD_HEIGHT:
            return
        self.width = init_width + BOARD_RESIZE_STEP*2
        self.height = init_height + BOARD_RESIZE_STEP*2
        new_matrix = np.zeros((self.height, self.width), dtype=int)
        x = BOARD_RESIZE_STEP
        new_matrix[x:x + self.matrix.shape[0],
        x:x + self.matrix.shape[1]] = self.matrix
        self.matrix = new_matrix

    def update_board(self):
        """ One step in cellular automata - update all the cells"""
        new_matrix = np.zeros((self.height, self.width), dtype=int)
        need_resize = False
        for x in range(self.height):
            for y in range(self.width):
                new_matrix[x][y] = apply_game_of_life_rules(self.matrix, x, y)
                if new_matrix[x][y] and (x == 0 or x == self.height - 1 or y == 0 or y == self.width - 1):
                    need_resize = True
        self.lifespan += 1
        self.current_config_size = np.sum(self.matrix)
        if self.current_config_size > self.max_config_size:
            self.max_config_size = self.current_config_size
        self.matrix = new_matrix
        board_hash = hash(new_matrix.data.tobytes())
        self.is_cycle = board_hash in self.board_history
        if not self.is_cycle:
            self.board_history.append(board_hash)
            if len(self.board_history) > 3:
                self.board_history = self.board_history[-3:]
        if need_resize:
            self.resize_board()

    def evolve(self, max_steps):
        """ Evolve the cellular automata up to max steps or until all cells die"""
        while self.current_config_size > 0 and self.lifespan < max_steps and not self.is_cycle:
            self.update_board()

    def print_board(self):
        """For debugging purpose - print current board"""
        for x in range(self.height):
            for y in range(self.width):
                if self.matrix[x][y] == 1:
                    print("#", end="")
                else:
                    print(".", end="")
                if y == self.width - 1:
                    print("")

    def print_pattern(self):
        """Print initial configuration (pattern)"""
        width = len(self.init_config[0])
        height = len(self.init_config)
        for x in range(height):
            for y in range(width):
                if self.init_config[x][y] == 1:
                    print("#", end="")
                else:
                    print(".", end="")
                if y == width - 1:
                    print("")

    def print_data(self):
        """Print all data about the pattern life"""
        print("Init config size: {}".format(self.init_config_size))
        print("Final config size: {}".format(self.current_config_size))
        print("Max config size: {}".format(self.max_config_size))
        print("Lifespan: {}".format(self.lifespan))
