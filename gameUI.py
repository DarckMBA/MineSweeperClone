import random
import pygame
from settings import *

# Tyle types
# "u" = unknown
# "m" = mine
# "c" = clue
# "e" = empty

class Tile:
    def __init__(self, x, y, image, type, revealed = False, flagged = False):
        self.x, self.y = x * TILESIZE, y * TILESIZE
        self.image = image
        self.type = type
        self.revealed = revealed
        self.flagged = flagged

    def draw(self, board_surface):
        if not self.flagged and self.revealed:
            board_surface.blit(self.image, (self.x, self.y))
        elif self.flagged and not self.revealed:
            board_surface.blit(tile_flag, (self.x, self.y))
        elif not self.revealed:
            board_surface.blit(tile_unknown, (self.x, self.y))
    
    def __repr__(self):
        return self.type

class Board:
    def __init__(self, rows, cols, amount_mines):
        self.rows = rows
        self.cols = cols
        self.amount_mines = amount_mines
        self.width = TILESIZE * self.cols
        self.height = TILESIZE * self.rows

        self.board_surface = pygame.Surface((self.width, self.height))
        self.board_list = [
            [Tile(col, row, tile_empty, "u") for row in range(self.rows)]
            for col in range(self.cols)
        ]
        self.dug = []
        self.mines_placed = False

    def is_inside_board(self, x, y):
        return 0 <= x < self.cols and 0 <= y < self.rows

    def place_mines(self, safe_x, safe_y):
        safe_cells = {(safe_x, safe_y)}
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                nx, ny = safe_x + dx, safe_y + dy
                if self.is_inside_board(nx, ny):
                    safe_cells.add((nx, ny))

        placed = 0
        while placed < self.amount_mines:
            x = random.randint(0, self.cols - 1)
            y = random.randint(0, self.rows - 1)
            if (x, y) in safe_cells:
                continue
            if self.board_list[x][y].type == "u":
                self.board_list[x][y].image = tile_mine
                self.board_list[x][y].type = "m"
                placed += 1

    def place_clues(self):
        for x in range(self.cols):
            for y in range(self.rows):
                if self.board_list[x][y].type != "m":
                    total_mines = self.check_neighbours(x, y)
                    if total_mines > 0:
                        self.board_list[x][y].image = tile_numbers[total_mines - 1]
                        self.board_list[x][y].type = "c"

    def check_neighbours(self, x, y):
        total_mines = 0
        for x_offset in range(-1, 2):
            for y_offset in range(-1, 2):
                neighbour_x = x + x_offset
                neighbour_y = y + y_offset
                if self.is_inside_board(neighbour_x, neighbour_y) and self.board_list[neighbour_x][neighbour_y].type == "m":
                    total_mines += 1
        return total_mines

    def dig(self, x, y):
        self.dug.append((x, y))
        if self.board_list[x][y].type == "m":
            self.board_list[x][y].revealed = True
            self.board_list[x][y].image = tile_exploded
            return False
        elif self.board_list[x][y].type == "c":
            self.board_list[x][y].revealed = True
            return True

        self.board_list[x][y].revealed = True
        for row in range(max(0, x - 1), min(self.cols - 1, x + 1) + 1):
            for col in range(max(0, y - 1), min(self.rows - 1, y + 1) + 1):
                if (row, col) not in self.dug:
                    self.dig(row, col)
        return True
    
    def generate_after_first_click(self, first_x, first_y):
        if self.mines_placed:
            return
        self.place_mines(first_x, first_y)
        self.place_clues()
        self.mines_placed = True

    def draw(self, screen):
        for row in self.board_list:
            for tile in row:
                tile.draw(self.board_surface)
        screen.blit(self.board_surface, (0, TOPSECTION))

class MineCount:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 100, 40)
        self.shade = pygame.Rect(x + 5, y + 5, 100, 40)
        self.font = pygame.font.SysFont("Arial", 30, bold = True)

    def display_mineCount(self, screen, count):
        pygame.draw.rect(screen, BLACK, self.shade, 0, 10)
        pygame.draw.rect(screen, LIGHTGREY, self.rect, 0, 10)
        mine_icon_pos = (self.rect.x + 5, self.rect.y + (self.rect.height - TILESIZE) // 2)
        screen.blit(tile_mine, mine_icon_pos)
        text = self.font.render(f"= {count}", True, WHITE)
        screen.blit(text, (self.rect.x + 40, self.rect.y + 2))

class Timer:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 120, 40)
        self.shade = pygame.Rect(x + 5, y + 5, 120, 40)
        self.font = pygame.font.SysFont("Arial", 30, bold = True)
        self.start_ticks = 0
        self.frozen_ms = None
        self.started = False

    def start(self):
        self.start_ticks = pygame.time.get_ticks()
        self.frozen_ms = None
        self.started = True
    
    def stop(self):
        if self.frozen_ms is None:
            self.frozen_ms = pygame.time.get_ticks() - self.start_ticks

    def get_elapsed_ms(self):
        if not self.started:
            return 0
        if self.frozen_ms is not None:
            return self.frozen_ms
        return pygame.time.get_ticks() - self.start_ticks

    def display_timer(self, screen):
        elapsed_ms = self.get_elapsed_ms()
        milliseconds = (elapsed_ms % 1000) // 10
        seconds = (elapsed_ms // 1000) % 60
        minutes = elapsed_ms // 60000

        timer_text = f"{minutes:02}:{seconds:02}:{milliseconds:02}"

        pygame.draw.rect(screen, BLACK, self.shade, 0, 10)
        pygame.draw.rect(screen, LIGHTGREY, self.rect, 0, 10)
        text = self.font.render(timer_text, True, WHITE)
        text_rect = text.get_rect(center = self.rect.center)
        screen.blit(text, text_rect)

class ResetButton:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 90, 40)
        self.shade = pygame.Rect(x + 5, y + 5, 90, 40)
        self.font = pygame.font.SysFont("Arial", 30, bold = True)

    def display_resetButton(self, screen):
        pygame.draw.rect(screen, BLACK, self.shade, 0, 10)
        pygame.draw.rect(screen, LIGHTGREY, self.rect, 0, 10)
        text = self.font.render(f"RESET", True, WHITE)
        text_rect = text.get_rect(center = self.rect.center)
        screen.blit(text, text_rect)

    def is_inside_resetButton(self, x, y):
        return self.rect.collidepoint(x, y)
    
class BackButton:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 80, 40)
        self.shade = pygame.Rect(x + 5, y + 5, 80, 40)
        self.font = pygame.font.SysFont("Arial", 30, bold = True)

    def display_backButton(self, screen):
        pygame.draw.rect(screen, BLACK, self.shade, 0, 10)
        pygame.draw.rect(screen, LIGHTGREY, self.rect, 0, 10)
        text = self.font.render(f"BACK", True, WHITE)
        text_rect = text.get_rect(center = self.rect.center)
        screen.blit(text, text_rect)

    def is_inside_backButton(self, x, y):
        return self.rect.collidepoint(x, y)
    
class QuitButton:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 70, 40)
        self.shade = pygame.Rect(x + 5, y + 5, 70, 40)
        self.font = pygame.font.SysFont("Arial", 30, bold = True)

    def display_quitButton(self, screen):
        pygame.draw.rect(screen, BLACK, self.shade, 0, 10)
        pygame.draw.rect(screen, LIGHTGREY, self.rect, 0, 10)
        text = self.font.render(f"QUIT", True, WHITE)
        text_rect = text.get_rect(center = self.rect.center)
        screen.blit(text, text_rect)

    def is_inside_quitButton(self, x, y):
        return self.rect.collidepoint(x, y)