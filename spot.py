import colors
import pygame


COLORS = {"reset": colors.WHITE, "closed": colors.LIGHTRED, "open": colors.LIGHTGREEN, "barrier": colors.DARKGRAY, "start": colors.LIGHTORANGE, "end": colors.TURQUOISE, "path": colors.LIGHTPURPLE}


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.colors = {"reset": True, "closed": False, "open": False, "barrier": False, "start": False, "end": False,
                       "path": False}
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_position(self):
        return self.row, self.col

    def is_closed(self):
        return self.colors["closed"]

    def is_open(self):
        return self.colors["open"]

    def is_barrier(self):
        return self.colors["barrier"]

    def is_start(self):
        return self.colors["start"]

    def is_end(self):
        return self.colors["end"]

    def reset(self):
        self.colors = {"reset": True, "closed": False, "open": False, "barrier": False, "start": False, "end": False,
                       "path": False}

    def make_closed(self):
        self.colors = {"reset": False, "closed": True, "open": False, "barrier": False, "start": False, "end": False,
                       "path": False}

    def make_open(self):
        self.colors = {"reset": False, "closed": False, "open": True, "barrier": False, "start": False, "end": False,
                       "path": False}

    def make_barrier(self):
        self.colors["reset"] = False
        self.colors["barrier"] = True

    def make_start(self):
        self.colors["reset"] = False
        self.colors["start"] = True

    def make_end(self):
        self.colors["reset"] = False
        self.colors["end"] = True

    def make_path(self):
        self.colors = {"reset": False, "closed": False, "open": False, "barrier": False, "start": False, "end": False,
                       "path": True}

    def draw(self, window):
        for state in self.colors:
            if self.colors[state]:
                color = COLORS[state]

        pygame.draw.rect(window, color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False
