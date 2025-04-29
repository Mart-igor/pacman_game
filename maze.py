import pygame
import os

CELL_SIDE = 30

class Wall:
    def __init__(self, x, y, maze_map):
        self.x = x
        self.y = y
        self.type = self._get_wall_type(y, x, maze_map)
        self.texture = self._load_texture()

    def _get_wall_type(self, row, col, maze_map):
        if maze_map[row][col] != 1:
            return None

        height = len(maze_map)
        width = len(maze_map[0]) if height > 0 else 0

        is_top = row == 0
        is_bottom = row == height - 1
        is_left = col == 0
        is_right = col == width - 1

        left = not is_left and maze_map[row][col - 1] == 1
        right = not is_right and maze_map[row][col + 1] == 1
        top = not is_top and maze_map[row - 1][col] == 1
        bottom = not is_bottom and maze_map[row + 1][col] == 1

        left_pass = not is_left and maze_map[row][col - 1] == 0
        right_pass = not is_right and maze_map[row][col + 1] == 0
        top_pass = not is_top and maze_map[row - 1][col] == 0
        bottom_pass = not is_bottom and maze_map[row + 1][col] == 0

        top_left = not is_top and not is_left and maze_map[row - 1][col - 1] == 0
        top_right = not is_top and not is_right and maze_map[row - 1][col + 1] == 0
        bottom_left = not is_bottom and not is_left and maze_map[row + 1][col - 1] == 0
        bottom_right = not is_bottom and not is_right and maze_map[row + 1][col + 1] == 0

        if (top_pass and left_pass) or (is_top and is_left) or (top_pass and left_pass and top_left) or (bottom_right and right and bottom ):
            return "top_left_corner"
        elif (top_pass and right_pass) or (is_top and is_right) or (top_pass and right_pass and top_right) or (bottom_left and left and bottom):
            return "top_right_corner"
        elif (bottom_pass and left_pass) or (is_bottom and is_left) or (bottom_pass and left_pass and bottom_left) or (top_right and top and right):
            return "bottom_left_corner"
        elif (bottom_pass and right_pass) or (is_bottom and is_right) or (bottom_pass and right_pass and bottom_right) or (top_left and top and left):
            return "bottom_right_corner"

        elif (top_pass and left and right) or (bottom_pass and left and right):
            return "horizontal"

        elif (left_pass and top and bottom) or (right_pass and top and bottom):
            return "vertical"

        elif is_top or is_bottom:
            return "horizontal"
        elif (is_left and right):
            return "horizontal"
        elif (is_right and left):
            return "horizontal"
        elif is_left or is_right:
            return "vertical"

        else:
            return "floor"

    def _load_texture(self):
        texture_path = os.path.join("sprites", f"{self.type}.png")
        texture = pygame.image.load(texture_path)
        return pygame.transform.scale(texture, (CELL_SIDE, CELL_SIDE))

    def draw(self, screen):
        screen.blit(self.texture, (self.x * CELL_SIDE, self.y * CELL_SIDE))

DOT_VALUE = 2
class Maze:
    def __init__(self, maze_map):
        self.maze_map = maze_map
        self.walls = []
        self.load_maze(maze_map)
        self.width = len(maze_map[0])
        self.height = len(maze_map)
        self.dots = self._init_dots()
        self.dot_sprite = pygame.image.load('sprites/dot.png')
        self.dot_sprite = pygame.transform.scale(self.dot_sprite, (CELL_SIDE//2, CELL_SIDE//2))

    def _init_dots(self):
        dots_map = []
        for row in range(self.height):
            dots_row = []
            for col in range(self.width):
                if self.maze_map[row][col] == 0:  # Если это проход
                    dots_row.append(DOT_VALUE)     # Добавляем точку
                else:
                    dots_row.append(0)             # Стена - без точки
            dots_map.append(dots_row)
        return dots_map

    def load_maze(self, maze_map):
        for y in range(len(maze_map)):
            for x in range(len(maze_map[0])):
                if maze_map[y][x] == 1:
                    self.walls.append(Wall(x, y, maze_map))

    def draw(self, screen):
        for wall in self.walls:
            wall.draw(screen)
        for row in range(self.height):
            for col in range(self.width):
                if self.dots[row][col] == 2:
                    dot_pos = (
                        col * CELL_SIDE + CELL_SIDE//2 - self.dot_sprite.get_width()//2,
                        row * CELL_SIDE + CELL_SIDE//2 - self.dot_sprite.get_height()//2
                    )
                    screen.blit(self.dot_sprite, dot_pos)

    def is_wall(self, row, col):
        if 0 <= row < self.height and 0 <= col < self.width:
            return self.maze_map[row][col] == 1
        return True
    
    def all_dots_eaten(self):
        for row in self.dots:
            if DOT_VALUE  in row:  # 0 представляет клетку с точкой
                return False
        return True
    
    def eat_dot(self, row, col):
        if 0 <= row < self.height and 0 <= col < self.width:
            if self.dots[row][col] == DOT_VALUE:
                self.dots[row][col] = 0
                return True
        return False

