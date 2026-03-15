import os
os.environ["SDL_VIDEO_CENTERED"] = "1"
import pygame
from settings import *
from sprites import *

class App:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        self.modes = {
            "easy": (9, 9, 10),
            "medium": (16, 16, 40),
            "hard": (16, 30, 99),
        }

        self.rows, self.cols, self.amountMines = self.modes["easy"]
        self.screen = pygame.display.set_mode((MAINMENUWIDTH, MAINMENUHEIGHT))
        pygame.display.set_caption(TITLE)


    def new_main_menu(self):
        self.screen = pygame.display.set_mode((MAINMENUWIDTH, MAINMENUHEIGHT))
        self.mainMenu = MainMenu()
        self.easyButton = EasyButton()
        self.mediumButton = MediumButton()
        self.hardButton = HardButton()

    def run_app(self):
        self.open = True
        while self.open:
            self.clock.tick(FPS)
            self.main_menu_events()
            self.draw_main_menu()
        else:
            self.close_app()

    def draw_main_menu(self):
        self.screen.fill(BGCOLOUR)
        self.easyButton.display_easyButton(self.screen)
        self.mediumButton.display_mediumButton(self.screen)
        self.hardButton.display_hardButton(self.screen)
        pygame.display.flip()

    def main_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type != pygame.MOUSEBUTTONDOWN:
                continue

            mx, my = pygame.mouse.get_pos()

            if event.button == 1 and self.easyButton.is_inside_easyButton(mx, my):
                self.new_game(*self.modes["easy"])
                self.run_game()
                return
            
            if event.button == 1 and self.mediumButton.is_inside_mediumButton(mx, my):
                self.new_game(*self.modes["medium"])
                self.run_game()
                return
            
            if event.button == 1 and self.hardButton.is_inside_hardButton(mx, my):
                self.new_game(*self.modes["hard"])
                self.run_game()
                return


    def new_game(self, rows, cols, amount_mines):
        self.rows, self.cols, self.amountMines = rows, cols, amount_mines
        game_width = self.cols * TILESIZE
        game_height = self.rows * TILESIZE
        self.screen = pygame.display.set_mode((game_width, game_height + TOPSECTION))

        self.board = Board(self.rows, self.cols, self.amountMines)
        self.mineCount = MineCount()
        self.timer = Timer()
        self.first_click_done = False
        self.resetButton = ResetButton()
        self.backButton = BackButton()
        self.quitButton = QuitButton()

    def run_game(self):
        while True:
            self.playing = True
            self.back_to_menu = False
            while self.playing:
                self.clock.tick(FPS)
                self.game_events()
                self.draw_game()
            if self.back_to_menu:
                self.new_main_menu()
                break

            self.close_app()
            self.new_game(self.rows, self.cols, self.amountMines)

    def draw_game(self):
        self.screen.fill(BGCOLOUR)
        flags_paced = sum(title.flagged for col in self.board.board_list for title in col)
        self.mineCount.display_mineCount(self.screen, self.amountMines - flags_paced)
        self.timer.display_timer(self.screen)
        self.resetButton.display_resetButton(self.screen)
        self.backButton.display_backButton(self.screen)
        self.quitButton.display_quitButton(self.screen)
        self.board.draw(self.screen)
        pygame.display.flip()

    def check_win(self):
        for row in self.board.board_list:
            for tile in row:
                if tile.type != "m" and not tile.revealed:
                    return False
        return True
    
    def game_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type != pygame.MOUSEBUTTONDOWN:
                continue

            mx, my = pygame.mouse.get_pos()

            if (event.button == 1 or event.button == 3) and self.resetButton.is_inside_resetButton(mx, my):
                self.new_game(self.rows, self.cols, self.amountMines)
                return
            
            if (event.button == 1 or event.button == 3) and self.backButton.is_inside_backButton(mx, my):
                self.back_to_menu = True
                self.playing = False
                return
            
            if (event.button == 1 or event.button == 3) and self.quitButton.is_inside_quitButton(mx, my):
                pygame.quit()
                return

            if my < TOPSECTION:
                continue
                
            my -= TOPSECTION
            mx //= TILESIZE
            my //= TILESIZE

            if not self.board.is_inside_board(mx, my):
                continue

            tile = self.board.board_list[mx][my]

            if event.button == 1:
                if tile.flagged or tile.revealed:
                    continue

                if not self.first_click_done:
                    self.board.generate_after_first_click(mx, my)
                    self.timer.start()
                    self.first_click_done = True

                if not self.board.dig(mx, my):
                    for row in self.board.board_list:
                        for t in row:
                            if t.flagged and t.type != "m":
                                t.flagged = False
                                t.revealed = True
                                t.image = tile_not_mine
                            elif t.type == "m":
                                t.revealed = True
                    self.playing = False
                    self.timer.stop()
                        
            elif event.button == 3:
                if not self.first_click_done:
                    self.board.generate_after_first_click(mx, my)
                    self.timer.start()
                    self.first_click_done = True
                    
                if not tile.revealed:
                    tile.flagged = not tile.flagged
            
            if self.check_win():
                self.win = True
                self.playing = False
                self.timer.stop()
                for row in self.board.board_list:
                    for t in row:
                        if not t.revealed:
                            t.flagged = True
    

    def close_app(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    return


app = App()
while True:
    app.new_main_menu()
    app.run_app()