import pygame
from settings import *
from sprites import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

    def new(self):
        self.board = Board()
        self.board.dislplay_board()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.draw()
        else:
            self.end_screen()

    def draw(self):
        self.screen.fill(BGCOLOUR)
        self.board.draw(self.screen)
        pygame.display.flip()

    def check_win(self):
        for row in self.board.board_list:
            for tile in row:
                if tile.type != "m" and not tile.revealed:
                    return False
        return True
    
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                mx //= TILESIZE
                my //= TILESIZE

                if event.button == 1:
                    if not self.board.board_list[mx][my].flagged:
                        if not self.board.dig(mx, my):
                            for row in self.board.board_list:
                                for tile in row:
                                    if tile.flagged and tile.type != "m":
                                        tile.flagged = False
                                        tile.revealed = True
                                        tile.image = tile_not_mine
                                    elif tile.type == "m":
                                        tile.revealed = True
                            self.playing = False
                if event.button == 3:
                    if not self.board.board_list[mx][my].revealed:
                        self.board.board_list[mx][my].flagged = not self.board.board_list[mx][my].flagged
            
            if self.check_win():
                self.win = True
                self.playing = False
                for row in self.board.board_list:
                    for tile in row:
                        if not tile.revealed:
                            tile.flagged = True
    
    def end_screen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    return
                
game = Game()
while True:
    game.new()
    game.run()