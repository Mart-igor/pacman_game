import pygame
from maze import Maze
import random
from collections import deque
import heapq


CELL_SIZE = 30

class PacmanGame:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.running = True

        self.game_over = False
        self.game_won = False

        self.cell_size = 30
        self.maze_map = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
            [3, 3, 3, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 3, 3],
            [1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1],
            [3, 3, 3, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 3, 3],
            [3, 3, 3, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 3, 3],
            [3, 3, 3, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 3, 3],
            [3, 3, 3, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 3, 3],
            [1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
            [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1],
            [1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1],
            [1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1],
            [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]

        self.maze = Maze(self.maze_map)
        self.screen_width = self.maze.width * self.cell_size
        self.screen_height = self.maze.height * self.cell_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pacman")
        self.pacman = Pacman(1, 1)
        self.score = 0
        self.font = pygame.font.SysFont(None, 36)  
        self.big_font = pygame.font.SysFont(None, 72)
        self.ghosts = [
            Ghost(11, 15, 'astar', 'sprites/en1.png'),
            Ghost(2, 22, 'bfs_chase', 'sprites/en2.png'),
            Ghost(32, 2, 'dfs_chase', 'sprites/en3.png'),
            Ghost(32, 22, 'dijkstra_chase', 'sprites/en4.png')
        ]

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.maze.draw(self.screen)
        self.pacman.draw(self.screen)
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

        for ghost in self.ghosts:
            ghost.draw(self.screen)

        if self.game_over or self.game_won:
            self._draw_end_game_screen()

        pygame.display.flip()

    def _draw_end_game_screen(self):
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  
        self.screen.blit(overlay, (0, 0))
        
        if self.game_over:
            text = self.big_font.render("GAME OVER", True, (255, 0, 0))
        else:
            text = self.big_font.render("YOU WIN!", True, (0, 255, 0))
        
        text_rect = text.get_rect(center=(self.screen_width//2, self.screen_height//2))
        self.screen.blit(text, text_rect)
        
        score_text = self.font.render(f"Final Score: {self.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.screen_width//2, self.screen_height//2 + 50))
        self.screen.blit(score_text, score_rect)
        
        restart_text = self.font.render("Press R to restart or ESC to quit", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(self.screen_width//2, self.screen_height//2 + 100))
        self.screen.blit(restart_text, restart_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if (self.game_over or self.game_won) and event.key == pygame.K_r:
                    self._reset_game()  
                elif (self.game_over or self.game_won) and event.key == pygame.K_ESCAPE:
                    self.running = False
        
        if not (self.game_over or self.game_won):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.pacman.next_direction = 'left'
            elif keys[pygame.K_RIGHT]:
                self.pacman.next_direction = 'right'
            elif keys[pygame.K_UP]:
                self.pacman.next_direction = 'up'
            elif keys[pygame.K_DOWN]:
                self.pacman.next_direction = 'down'

    def update(self):
        if self.game_over or self.game_won:
            return
        self.pacman.update(self.maze)
        if hasattr(self.pacman, 'dot_eaten') and self.pacman.dot_eaten:
            self.score += 10
            self.pacman.dot_eaten = False

            if self.maze.all_dots_eaten():
                self.game_won = True
        for ghost in self.ghosts:
            ghost.update(self.maze, self.pacman)
            
            if self._check_collision(ghost):
                self._handle_collision(ghost)

    def _check_collision(self, ghost):
        return (abs(ghost.x - self.pacman.x) < CELL_SIZE and 
                abs(ghost.y - self.pacman.y) < CELL_SIZE)
    
    def _handle_collision(self, ghost):
        # if ghost.behavior == 'frightened':
        #     self.score += 200
        #     ghost.reset_position()
        # else:   
        self.game_over = True

    def _reset_game(self):
        self.__init__()
            
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()


class Pacman:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.direction = 'right'
        self.next_direction = 'right'
        self.speed = 0.2
        self.x = col * CELL_SIZE
        self.y = row * CELL_SIZE
        self.animation_frame = 0
        self.animation_speed = 0.2
        self.last_update = pygame.time.get_ticks()
        
        self.sprites = {
            'right': [],
            'left': [],
            'up': [],
            'down': []
        }
        self._load_sprites()
        
        self.current_sprite = self.sprites['right'][0]

    def _load_sprites(self):
        for direction in ['right', 'left', 'up', 'down']:
            for i in range(1, 4): 
                sprite = pygame.image.load(f'sprites/{direction}{i}.png')
                sprite = pygame.transform.scale(sprite, (CELL_SIZE, CELL_SIZE))
                self.sprites[direction].append(sprite)


    def update(self, maze):
        self._update_animation()
        
        target_x = self.col * CELL_SIZE
        target_y = self.row * CELL_SIZE
        
        if abs(self.x - target_x) > 1 or abs(self.y - target_y) > 1:
            if self.direction == 'left':
                self.x -= self.speed * CELL_SIZE
            elif self.direction == 'right':
                self.x += self.speed * CELL_SIZE
            elif self.direction == 'up':
                self.y -= self.speed * CELL_SIZE
            elif self.direction == 'down':
                self.y += self.speed * CELL_SIZE
        else:
            self.x, self.y = target_x, target_y
            
            self.dot_eaten = maze.eat_dot(self.row, self.col)

            self._move(maze)

    def _update_animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 100:  
            self.last_update = now
            self.animation_frame += self.animation_speed
            if self.animation_frame >= len(self.sprites[self.direction]):
                self.animation_frame = 0
            
            frame_index = int(self.animation_frame)
            self.current_sprite = self.sprites[self.direction][frame_index]

    def _move(self, maze):
        if self.next_direction != self.direction:
            new_row, new_col = self._get_next_cell(self.next_direction)
            if not maze.is_wall(new_row, new_col):
                self.direction = self.next_direction
                self.animation_frame = 0 

        new_row, new_col = self._get_next_cell(self.direction)
        if not maze.is_wall(new_row, new_col):
            self.row, self.col = new_row, new_col

    def _get_next_cell(self, direction):
        if direction == 'left':
            return self.row, self.col - 1
        elif direction == 'right':
            return self.row, self.col + 1
        elif direction == 'up':
            return self.row - 1, self.col
        elif direction == 'down':
            return self.row + 1, self.col
        return self.row, self.col

    def draw(self, screen):
        screen.blit(self.current_sprite, (self.x, self.y))


class Ghost:
    def __init__(self, row, col, behavior, sprite_path):
        self.row = row
        self.col = col
        self.start_row = row  
        self.start_col = col
        self.behavior = behavior 
        self.direction = random.choice(['left', 'right', 'up', 'down'])
        self.x = col * CELL_SIZE
        self.y = row * CELL_SIZE
        self.speed = 0.1 
        self.decision_interval = 10  
        self.decision_counter = 0
        self.target_x = self.x
        self.target_y = self.y
        self.other_ghosts = []

        # self.frightened = False  
        # self.frightened_timer = 0

        self.sprites = self._load_sprites(sprite_path)
        self.current_sprite = self.sprites[self.direction]

        # self.frightened_sprite = pygame.Surface((CELL_SIZE, CELL_SIZE))
        # self.frightened_sprite.fill((0, 0, 255))  

    def reset_position(self):
        self.row, self.col = self.start_row, self.start_col
        self.x = self.col * CELL_SIZE
        self.y = self.row * CELL_SIZE
        self.direction = random.choice(['left', 'right', 'up', 'down'])
        # self.frightened = False
        # self.frightened_timer = 0

    def _load_sprites(self, sprite_path):
        original_sprite = pygame.image.load(sprite_path)
        original_sprite = pygame.transform.scale(original_sprite, ((CELL_SIZE - 3), (CELL_SIZE - 3)))
        return {
            'left': original_sprite,
            'right': pygame.transform.flip(original_sprite, True, False),
            'up': pygame.transform.rotate(original_sprite, 90),
            'down': pygame.transform.rotate(original_sprite, -90)
        }

    def draw(self, screen):
        # if self.frightened:
        #     screen.blit(self.frightened_sprite, (self.x, self.y))
        # else:
        screen.blit(self.current_sprite, (self.x, self.y))

    def update(self, maze, pacman):
        # if self.frightened:
        #     self.frightened_timer -= 1
        #     if self.frightened_timer <= 0:
        #         self.frightened = False

        self.decision_counter += 1

        new_row, new_col = self._get_next_cell()
        if maze.is_wall(new_row, new_col):
            self.x = self.col * CELL_SIZE
            self.y = self.row * CELL_SIZE
            self._random_behavior(maze)
            return

        if self.direction == 'left':
            self.x -= self.speed * CELL_SIZE
        elif self.direction == 'right':
            self.x += self.speed * CELL_SIZE
        elif self.direction == 'up':
            self.y -= self.speed * CELL_SIZE
        elif self.direction == 'down':
            self.y += self.speed * CELL_SIZE

        new_cell_x = int(self.x // CELL_SIZE)
        new_cell_y = int(self.y // CELL_SIZE)

        if new_cell_x != self.col or new_cell_y != self.row:
            self.row, self.col = new_cell_y, new_cell_x
            self.target_x = self.col * CELL_SIZE
            self.target_y = self.row * CELL_SIZE

        if self.decision_counter >= self.decision_interval:
            self.decision_counter = 0
            # if not self.frightened:
            self._update_direction(maze, pacman)

        self.current_sprite = self.sprites[self.direction]

    def _update_direction(self, maze, pacman):
        if self.behavior == 'random':
            self._random_behavior(maze)
        elif self.behavior == 'bfs_chase':
            self._bfs_chase_behavior(maze, pacman)
        elif self.behavior == 'dfs_chase':
            self._dfs_chase_behavior(maze, pacman)
        elif self.behavior == 'dijkstra_chase':
            self._dijkstra_chase_behavior(maze, pacman)
        elif self.behavior == 'astar':  
            self._astar_chase_behavior(maze, pacman)

    def _random_behavior(self, maze):
        possible_dirs = []
        for direction in ['left', 'right', 'up', 'down']:
            new_row, new_col = self._get_next_cell(direction)
            if not maze.is_wall(new_row, new_col):
                possible_dirs.append(direction)

        if possible_dirs:
            self.direction = random.choice(possible_dirs)
            
    def _bfs_chase_behavior(self, maze, pacman):
        next_step = self._find_next_step_bfs(maze, pacman.row, pacman.col)
        self.direction = next_step

    def _find_next_step_bfs(self, maze, target_row, target_col):
        queue = deque()
        queue.append((self.row, self.col, []))  
        visited = set()
        visited.add((self.row, self.col))

        while queue:
            row, col, path = queue.popleft()

            if row == target_row and col == target_col:
                return path[0] if path else None

            for direction in ['up', 'down', 'left', 'right']:
                if direction == 'up':
                    new_row, new_col = row - 1, col
                elif direction == 'down':
                    new_row, new_col = row + 1, col
                elif direction == 'left':
                    new_row, new_col = row, col - 1
                else:  
                    new_row, new_col = row, col + 1

                if (0 <= new_row < maze.height and 
                    0 <= new_col < maze.width and 
                    not maze.is_wall(new_row, new_col) and 
                    (new_row, new_col) not in visited):
                    
                    visited.add((new_row, new_col))
                    queue.append((new_row, new_col, path + [direction]))

        return self._random_behavior(maze) 
    
    def _dfs_chase_behavior(self, maze, pacman):
        distance = abs(self.row - pacman.row) + abs(self.col - pacman.col)
        
        if distance <= 5:
            next_step = self._find_next_step_dfs(maze, pacman.row, pacman.col)
            if next_step in ['up', 'down', 'left', 'right']:
                self.direction = next_step
                return
        
        self._greedy_chase(maze, pacman)

    def _find_next_step_dfs(self, maze, target_row, target_col, max_depth=50):
        if (self.row, self.col) == (target_row, target_col):
            return self._random_behavior(maze)

        dir_priority = self._get_direction_priority(target_row, target_col)
        stack = [(self.row, self.col, [], dir_priority)]
        visited = set()

        while stack:
            row, col, path, directions = stack.pop()
            
            if (row, col) in visited:
                continue
            visited.add((row, col))

            if (row, col) == (target_row, target_col):
                return path[0] if path else None

            if len(path) >= max_depth:
                continue

            for direction in directions:
                dr, dc = 0, 0
                if direction == 'up': dr = -1
                elif direction == 'down': dr = 1
                elif direction == 'left': dc = -1
                else: dc = 1  

                new_row, new_col = row + dr, col + dc
                
                if (0 <= new_row < maze.height and 
                    0 <= new_col < maze.width and 
                    not maze.is_wall(new_row, new_col)):
                    
                    new_priority = self._get_direction_priority(
                        target_row - new_row, 
                        target_col - new_col
                    )
                    stack.append((new_row, new_col, path + [direction], new_priority))

        return self._random_behavior(maze)

    def _greedy_chase(self, maze, pacman):
        best_dir = None
        min_dist = float('inf')
        
        for direction in ['up', 'down', 'left', 'right']:
            new_row, new_col = self._get_next_cell(direction)
            
            if (0 <= new_row < maze.height and 
                0 <= new_col < maze.width and 
                not maze.is_wall(new_row, new_col)):
                
                dist = abs(new_row - pacman.row) + abs(new_col - pacman.col)
                
                if direction == self.direction:
                    dist -= 0.5  
                
                if dist < min_dist:
                    min_dist = dist
                    best_dir = direction
        
        if best_dir:
            self.direction = best_dir
        else:
            self._random_behavior(maze)

    def _get_direction_priority(self, row_diff, col_diff):
        priority = []
        
        if abs(row_diff) > abs(col_diff):
            if row_diff < 0: priority.append('up')
            else: priority.append('down')
            if col_diff < 0: priority.append('left')
            else: priority.append('right')
        else:
            if col_diff < 0: priority.append('left')
            else: priority.append('right')
            if row_diff < 0: priority.append('up')
            else: priority.append('down')
        
        return priority
    
    def _dijkstra_chase_behavior(self, maze, pacman):
        next_step = self._find_next_step_dijkstra(maze, pacman.row, pacman.col)
        if next_step:
            self.direction = next_step
        else:
            self._random_behavior(maze)

    def _find_next_step_dijkstra(self, maze, target_row, target_col):
        if (self.row == target_row and self.col == target_col):
            return self._random_behavior(maze)  

        heap = []
        heapq.heappush(heap, (0, self.row, self.col, None))  
        visited = set()
        came_from = {} 

        COSTS = {
            'normal': 1,
            'tunnel': 2,
            'danger': 2,
            'wall': float('inf')
        }

        while heap:
            current_cost, row, col, first_dir = heapq.heappop(heap)
            
            if (row, col) in visited:
                continue
            visited.add((row, col))
            
            if row == target_row and col == target_col:
                return first_dir 
            
            for direction in ['up', 'down', 'left', 'right']:
                new_row = row + (-1 if direction == 'up' else 1 if direction == 'down' else 0)
                new_col = col + (-1 if direction == 'left' else 1 if direction == 'right' else 0)
                
                if not (0 <= new_row < maze.height and 0 <= new_col < maze.width):
                    continue
                if maze.is_wall(new_row, new_col):
                    continue
                
                cell_type = self._get_cell_type(maze, new_row, new_col)
                new_cost = current_cost + COSTS[cell_type]
                
                if (new_row, new_col) not in visited:
                    next_first_dir = first_dir if first_dir is not None else direction
                    heapq.heappush(heap, (new_cost, new_row, new_col, next_first_dir))
        
        return self._random_behavior(maze)  

    def _get_cell_type(self, maze, row, col):
        if self._is_tunnel(maze, row, col):
            return 'tunnel'
            
        if self._is_danger_zone(row, col):
            return 'danger'
            
        return 'normal'

    def _is_tunnel(self, maze, row, col):
        horizontal = not maze.is_wall(row, col-1) or not maze.is_wall(row, col+1)
        vertical = not maze.is_wall(row-1, col) or not maze.is_wall(row+1, col)
        return horizontal and vertical

    def _is_danger_zone(self, row, col):
        for ghost in self.other_ghosts: 
            if abs(ghost.row - row) + abs(ghost.col - col) <= 2:
                return True
        return False
    
    def _astar_chase_behavior(self, maze, pacman):
        next_step = self._find_path_astar(maze, pacman.row, pacman.col)
        if next_step in ['up', 'down', 'left', 'right']:
            self.direction = next_step
        else:
            self._greedy_chase(maze, pacman)  

    def _find_path_astar(self, maze, target_row, target_col):
        if (self.row, self.col) == (target_row, target_col):
            return self._random_behavior(maze)

        open_set = []
        heapq.heappush(open_set, (0, 0, self.row, self.col, []))
        
        closed_set = set()
        g_scores = {(self.row, self.col): 0}

        while open_set:
            _, g_score, row, col, path = heapq.heappop(open_set)
            
            if (row, col) == (target_row, target_col):
                return path[0] if path else None

            if (row, col) in closed_set:
                continue
            closed_set.add((row, col))

            for direction, (dr, dc) in [('up', (-1,0)), ('down', (1,0)),
                                    ('left', (0,-1)), ('right', (0,1))]:
                new_row, new_col = row + dr, col + dc
                
                if not (0 <= new_row < maze.height and 0 <= new_col < maze.width):
                    continue
                if maze.is_wall(new_row, new_col):
                    continue

                cost = self._get_cell_cost(maze, new_row, new_col)
                tentative_g = g_score + cost

                if (new_row, new_col) not in g_scores or tentative_g < g_scores[(new_row, new_col)]:
                    g_scores[(new_row, new_col)] = tentative_g
                    f_score = tentative_g + self._heuristic(new_row, new_col, target_row, target_col)
                    heapq.heappush(open_set, (f_score, tentative_g, new_row, new_col, path + [direction]))

        return self._random_behavior(maze) 

    def _heuristic(self, row1, col1, row2, col2):
        return abs(row1 - row2) + abs(col1 - col2)

    def _get_cell_cost(self, maze, row, col):
        base_cost = 1
        
        if self._is_tunnel(maze, row, col):
            base_cost += 2
            
        for ghost in self.other_ghosts:
            if abs(ghost.row - row) + abs(ghost.col - col) <= 2:
                base_cost += 1
                
        return base_cost

    def _get_next_cell(self, direction=None):
        direction = direction or self.direction
        if direction == 'left':
            return self.row, self.col - 1
        elif direction == 'right':
            return self.row, self.col + 1
        elif direction == 'up':
            return self.row - 1, self.col
        elif direction == 'down':
            return self.row + 1, self.col
        return self.row, self.col
    

if __name__ == "__main__":
    game = PacmanGame()
    game.run()