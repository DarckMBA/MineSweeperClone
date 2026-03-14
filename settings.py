import pygame
import os

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
DARKGREEN = (0, 200, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BGCOLOUR = LIGHTGREY

# Easy settings
#ROWS = 9
#COLS = 9
#AMOUNT_MINES = 10

# Medium settings
#ROWS = 16
#COLS = 16
#AMOUNT_MINES = 40

# Hard settings
ROWS = 16
COLS = 30
AMOUNT_MINES = 99

# General game settings
TILESIZE = 32
WIDTH = TILESIZE * COLS
HEIGHT = TILESIZE * ROWS
FPS = 60
TITLE = "Minesweeper Clone"

tile_numbers = []
for i in range(1, 9):
    tile_numbers.append(pygame.transform.scale(pygame.image.load(os.path.join("assets", "original", f"Tile{i}.png")), (TILESIZE, TILESIZE)))

tile_empty = pygame.transform.scale(pygame.image.load(os.path.join("assets", "original", "TileEmpty.png")), (TILESIZE, TILESIZE))
tile_exploded = pygame.transform.scale(pygame.image.load(os.path.join("assets", "original", "TileExploded.png")), (TILESIZE, TILESIZE))
tile_flag = pygame.transform.scale(pygame.image.load(os.path.join("assets", "original", "TileFlag.png")), (TILESIZE, TILESIZE))
tile_mine = pygame.transform.scale(pygame.image.load(os.path.join("assets", "original", "TileMine.png")), (TILESIZE, TILESIZE))
tile_unknown = pygame.transform.scale(pygame.image.load(os.path.join("assets", "original", "TileUnknown.png")), (TILESIZE, TILESIZE))
tile_not_mine = pygame.transform.scale(pygame.image.load(os.path.join("assets", "original", "TileNotMine.png")), (TILESIZE, TILESIZE))