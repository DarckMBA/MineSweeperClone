import pygame
import os

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
GREY = (100, 100, 100)
LIGHTGREY = (140, 140, 140)
GREEN = (0, 255, 0)
DARKGREEN = (0, 200, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BGCOLOUR = GREY

# General game settings
MAINMENUHEIGHT = 300
MAINMENUWIDTH = 300

SETTINGSMENUHEIGHT = 520
SETTINGSMENUWIDTH = 400

TILESIZE = 32

TOPSECTION = 100
BOTTOMSECTION = TOPSECTION

MINECOUNTX = 0
MINECOUNTY = 0

TIMERX = 0
TIMERY = 0

RESETBUTTONX = 0
RESETBUTTONY = 0

BACKBUTTONX = 0
BACKBUTTONY = 0

QUITBUTTONX = 0
QUITBUTTONY = 0

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