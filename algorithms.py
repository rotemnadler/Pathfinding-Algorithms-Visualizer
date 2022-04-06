import pygame
import math
import queue
from queue import PriorityQueue
import colors


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


def draw(window, grid, rows, width):  # draw game grid
    window.fill(colors.WHITE)

    for row in grid:
        for node in row:
            node.draw(window)

    draw_grid(window, rows, width)
    pygame.display.update()


def astar(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
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
    dist = {node: float("inf") for row in grid for node in row}
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
    dist = {node: 0 for row in grid for node in row}
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
