import pygame
from settings import *
from sprites import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT + TOPSECTION))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

    def new(self):
        self.board = Board()
        self.mineCount = MineCount()
        self.first_click_done = False

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
        flags_paced = sum(title.flagged for col in self.board.board_list for title in col)
        self.mineCount.display_mineCount(self.screen, AMOUNT_MINES - flags_paced)
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

            if event.type != pygame.MOUSEBUTTONDOWN:
                continue

            mx, my = pygame.mouse.get_pos()
            if my < TOPSECTION:
                continue
            my -= TOPSECTION
            mx //= TILESIZE
            my //= TILESIZE

            if not self.board.is_inside(mx, my):
                continue

            tile = self.board.board_list[mx][my]

            if event.button == 1:
                if tile.flagged or tile.revealed:
                    continue

                if not self.first_click_done:
                    self.board.generate_after_first_click(mx, my)
                    self.first_click_done = True

                if not self.board.dig(mx, my):
                    for row in self.board.board_list:
                        for t in row:
                            if t.flagged and tile.type != "m":
                                t.flagged = False
                                t.revealed = True
                                t.image = tile_not_mine
                            elif t.type == "m":
                                t.revealed = True
                    self.playing = False
                        
            elif event.button == 3:
                if not tile.revealed:
                    tile.flagged = not tile.flagged
            
            if self.check_win():
                self.win = True
                self.playing = False
                for row in self.board.board_list:
                    for t in row:
                        if not t.revealed:
                            t.flagged = True
    
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