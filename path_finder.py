import pygame
import math
import queue
from queue import PriorityQueue
import colors
import algorithms
import spot

SIZE = 800
WINDOW = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption("Path Finding Algorithms")
COLORS = {"reset": colors.WHITE, "closed": colors.LIGHTRED, "open": colors.LIGHTGREEN, "barrier": colors.DARKGRAY, "start": colors.LIGHTORANGE, "end": colors.TURQUOISE, "path": colors.LIGHTPURPLE}








def make_grid(rows, width):  # data structure
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = spot.Spot(i, j, gap, rows)
            grid[i].append(node)

    return grid


def draw_grid(window, rows, width):  # grid lines
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(window, colors.LIGHTGRAY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(window, colors.LIGHTGRAY, (j * gap, 0), (j * gap, width))


def draw(window, grid, rows, width):  # draw game grid
    window.fill(colors.WHITE)

    for row in grid:
        for node in row:
            node.draw(window)

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
                node = grid[row][col]
                if not start and node != end:  # make start
                    start = node
                    start.make_start()

                elif not end and node != start:  # make end
                    end = node
                    end.make_end()

                elif node != start and node != end:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # right click
                pos = pygame.mouse.get_pos()
                row, col = get_click_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    algorithms.astar(lambda: draw(window, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_d and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    algorithms.djikstra(lambda: draw(window, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_b and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    algorithms.bfs(lambda: draw(window, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_n:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()


main(WINDOW, SIZE)

