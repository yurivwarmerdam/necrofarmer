import random
import pygame as pg

UP = 1
RIGHT = 2
DOWN = 4
LEFT = 8


# following symbolizes a fully open maze:
#  1
# 8 2
#  4
# this sums to 15

# Game should also implement in init:
# maze_tiles = sheet_to_sprites(load_image("art/dumb_maze.png"), Vector2(16, 16))
# self.maze_tiles_bitmasked = {
#     0: maze_tiles[(3, 2)],
#     maze.UP: maze_tiles[(0, 4)],
#     maze.RIGHT: maze_tiles[(1, 4)],
#     maze.DOWN: maze_tiles[(2, 4)],
#     maze.LEFT: maze_tiles[(3, 4)],
#     maze.DOWN + maze.RIGHT: maze_tiles[(0, 0)],
#     maze.LEFT + maze.RIGHT: maze_tiles[(1, 0)],
#     maze.DOWN + maze.LEFT: maze_tiles[(2, 0)],
#     maze.UP + maze.DOWN: maze_tiles[(0, 1)],
#     maze.UP + maze.DOWN + maze.LEFT + maze.RIGHT: maze_tiles[(1, 1)],
#     maze.UP + maze.RIGHT: maze_tiles[(0, 2)],
#     maze.LEFT + maze.UP: maze_tiles[(2, 2)],
#     maze.RIGHT + maze.DOWN + maze.LEFT: maze_tiles[(0, 3)],
#     maze.DOWN + maze.LEFT + maze.UP: maze_tiles[(1, 3)],
#     maze.UP + maze.RIGHT + maze.LEFT: maze_tiles[(2, 3)],
#     maze.RIGHT + maze.DOWN + maze.UP: maze_tiles[(3, 3)],
# }


class Maze:
    def __init__(self, game, maze_size):
        self.game = game

        visited = {}
        unvisited = []
        stack = []

        for x in range(maze_size[0]):
            for y in range(maze_size[1]):
                unvisited.append((x, y))

        initial = (0, 0)
        unvisited.remove(initial)
        stack.append(initial)
        visited[initial] = 0

        while len(stack) > 0:
            current = stack.pop()
            unv_neigh = self.get_unvisited_neigbors(current, unvisited)
            if unv_neigh:
                stack.append(current)

                chosen = random.choice(unv_neigh)
                unvisited.remove(chosen)
                if current[0] < chosen[0]:
                    visited[current] += RIGHT
                    visited[chosen] = LEFT
                elif current[0] > chosen[0]:
                    visited[current] += LEFT
                    visited[chosen] = RIGHT
                elif current[1] > chosen[1]:
                    visited[current] += UP
                    visited[chosen] = DOWN
                elif current[1] < chosen[1]:
                    visited[current] += DOWN
                    visited[chosen] = UP
                stack.append(chosen)
        self.maze = visited

    def get_unvisited_neigbors(self, cell, unvisited):
        neigbors = [
            (cell[0] - 1, cell[1]),
            (cell[0] + 1, cell[1]),
            (cell[0], cell[1] - 1),
            (cell[0], cell[1] + 1),
        ]
        result = []
        for cell in neigbors:
            if cell in unvisited:
                result.append(cell)
        return result

    def render(self, display):
        for tile in self.maze:
            display.blit(
                self.game.maze_tiles_bitmasked[self.maze[tile]],
                (tile[0] * 16, tile[1] * 16),
            )
