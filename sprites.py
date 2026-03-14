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
    def __init__(self):
        self.board_surface = pygame.Surface((WIDTH, HEIGHT))
        self.board_list = [[Tile(col, row, tile_empty, "u") for row in range(ROWS)] for col in range(COLS)]
        self.dug = []
        self.mines_placed = False

    def place_mines(self, safe_x, safe_y):
        safe_cells = {(safe_x, safe_y)}
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                nx, ny = safe_x + dx, safe_y + dy
                if self.is_inside(nx, ny):
                    safe_cells.add((nx, ny))

        placed = 0
        while placed < AMOUNT_MINES:
            x = random.randint(0, COLS - 1)
            y = random.randint(0, ROWS - 1)
            if (x, y) in safe_cells:
                continue
            if self.board_list[x][y].type == "u":
                self.board_list[x][y].image = tile_mine
                self.board_list[x][y].type = "m"
                placed += 1
    
    def place_clues(self):
        for x in range(COLS):
            for y in range(ROWS):
                if self.board_list[x][y].type != "m":
                    total_mines = self.check_neighbours(x, y)
                    if total_mines > 0:
                        self.board_list[x][y].image = tile_numbers[total_mines - 1]
                        self.board_list[x][y].type = "c"

    @staticmethod
    def is_inside(x,y):
        return 0 <= x < COLS and 0 <= y < ROWS
    
    def check_neighbours(self, x, y):
        total_mines = 0
        for x_offset in range(-1, 2):
            for y_offset in range(-1, 2):
                neighbour_x = x + x_offset
                neighbour_y = y + y_offset
                if self.is_inside(neighbour_x, neighbour_y) and self.board_list[neighbour_x][neighbour_y].type == "m":
                    total_mines += 1

        return total_mines
    
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

        for row in range(max(0, x - 1), min(COLS - 1, x + 1) + 1):
              for col in range(max(0, y - 1), min(ROWS - 1, y + 1) + 1):
                  if (row, col) not in self.dug:
                      self.dig(row, col)
        return True
    
    def dislplay_board(self):
        for row in self.board_list:
            print(row)

class MineCount:
    def __init__(self):
        self.mineCount_surface = pygame.Surface((100, 40))
        self.font = pygame.font.SysFont("Arial", 30, bold = True)

    def display_mineCount(self, screen, count):
        screen.blit(self.mineCount_surface, (40, 20))
        screen.blit(tile_mine, (45, 24))
        text = self.font.render(f"= {count}", True, WHITE)
        screen.blit(text, (85, 22))