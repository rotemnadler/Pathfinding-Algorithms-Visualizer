import pygame
import math
import queue
from queue import PriorityQueue

SIZE = 800
WINDOW = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption("Path Finding Algorithms")

LIGHTRED = (255, 102, 102)  # in closed set
LIGHTGREEN = (204, 255, 153)  # in open set
BLUE = (71, 58, 191)
YELLOW = (235, 224, 144)
WHITE = (255, 255, 255)  # not visited
DARKGRAY = (41, 41, 61)  # barrier
LIGHTORANGE = (255, 170, 128)  # start node
TURQUOISE = (179, 255, 236)  # end node
LIGHTGRAY = (230, 230, 230)
LIGHTPURPLE = (153, 153, 255)  # chosen path
COLORS = {"reset": WHITE, "closed": LIGHTRED, "open": LIGHTGREEN, "barrier": DARKGRAY, "start": LIGHTORANGE, "end": TURQUOISE, "path": LIGHTPURPLE}


class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.colors = {"reset": True, "closed": False, "open": False, "barrier": False, "start": False, "end": False, "path": False}
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
        self.colors = {"reset": True, "closed": False, "open": False, "barrier": False, "start": False, "end": False, "path": False}

    def make_closed(self):
        self.colors = {"reset": False, "closed": True, "open": False, "barrier": False, "start": False, "end": False, "path": False}

    def make_open(self):
        self.colors = {"reset": False, "closed": False, "open": True, "barrier": False, "start": False, "end": False, "path": False}

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
        self.colors = {"reset": False, "closed": False, "open": False, "barrier": False, "start": False, "end": False, "path": True}

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


def h(p1, p2):  # huristic function using manhatten distance
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconst_path(came_from, cur, draw):
    while cur in came_from:
        cur = came_from[cur]
        cur.make_path()
        draw()
    cur.make_start()
    draw()


def astar(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_position(), end.get_position())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        cur = open_set.get()[2]
        open_set_hash.remove(cur)

        if cur == end:
            reconst_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in cur.neighbors:
            temp_g_score = g_score[cur] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = cur
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_position(), end.get_position())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if cur != start:
            cur.make_closed()

    return False


def djikstra(draw, grid, start, end):
    count = 0
    open_set = queue.PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    dist = {spot: float("inf") for row in grid for spot in row}
    dist[start] = 0

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        cur = open_set.get()[2]
        open_set_hash.remove(cur)

        if cur == end:
            reconst_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in cur.neighbors:
            temp_dist = dist[cur] + 1

            if temp_dist < dist[neighbor]:
                came_from[neighbor] = cur
                dist[neighbor] = temp_dist
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((dist[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if cur != start:
            cur.make_closed()

    return False


def bfs(draw, grid, start, end):
    open_set = queue.Queue()
    open_set.put(start)
    came_from = {}
    dist = {spot: 0 for row in grid for spot in row}
    dist[start] = 0

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        cur = open_set.get()

        if cur == end:
            reconst_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in cur.neighbors:
            if neighbor not in open_set_hash:
                came_from[neighbor] = cur
                dist[neighbor] = dist[cur] + 1
                open_set_hash.add(neighbor)
                open_set.put(neighbor)
                neighbor.make_open()
        draw()

        if cur != start:
            cur.make_closed()

    return False


def make_grid(rows, width):  # data structure
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid


def draw_grid(window, rows, width):  # grid lines
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(window, LIGHTGRAY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(window, LIGHTGRAY, (j * gap, 0), (j * gap, width))


def draw(window, grid, rows, width):  # draw game grid
    window.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(window)

    draw_grid(window, rows, width)
    pygame.display.update()


def reset(start, end, ROWS, width):
    start.reset()
    end.reset()
    make_grid(ROWS, width)



def get_click_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col


def main(window, width):  # game play
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    while run:
        draw(window, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # player closed window
                run = False

            if pygame.mouse.get_pressed()[0]:  # left click
                pos = pygame.mouse.get_pos()
                row, col = get_click_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:  # make start
                    start = spot
                    start.make_start()

                elif not end and spot != start:  # make end
                    end = spot
                    end.make_end()

                elif spot != start and spot != end:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # right click
                pos = pygame.mouse.get_pos()
                row, col = get_click_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    astar(lambda: draw(window, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_d and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    djikstra(lambda: draw(window, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_b and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    bfs(lambda: draw(window, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_n:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()


main(WINDOW, SIZE)

