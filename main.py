import os
os.environ["SDL_VIDEO_CENTERED"] = "1"
import pygame
from settings import *
from gameUI import *
from gameViews import mainMenuView
from gameViews import settingsMenuView

class App:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        self.modes = {
            "easy": {
                "rows": 9,
                "cols": 9,
                "mines": 10,
                "ui": {
                    "minecount": (20, 5),
                    "timer": (150, 5),
                    "reset": (15, 50),
                    "back": (115, 50),
                    "quit": (205, 50),
                },
            },
            "medium": {
                "rows": 16,
                "cols": 16,
                "mines": 40,
                "ui": {
                    "minecount": (5, 30),
                    "timer": (115, 30),
                    "reset": (245, 30),
                    "back": (345, 30),
                    "quit": (435, 30),
                },
            },
            "hard": {
                "rows": 16,
                "cols": 30,
                "mines": 99,
                "ui": {
                    "minecount": (40, 30),
                    "timer": (180, 30),
                    "reset": (340, 30),
                    "back": (470, 30),
                    "quit": (590, 30),
                },
            },
        }

        self.current_mode = "easy"
        self.rows = self.modes[self.current_mode]["rows"]
        self.cols = self.modes[self.current_mode]["cols"]
        self.amountMines = self.modes[self.current_mode]["mines"]
        self.screen = pygame.display.set_mode((MAINMENUWIDTH, MAINMENUHEIGHT))
        pygame.display.set_caption(TITLE)


    def new_main_menu(self):
        self.screen = pygame.display.set_mode((MAINMENUWIDTH, MAINMENUHEIGHT))
        self.mainMenu = mainMenuView.MainMenu()
        self.easyButton = mainMenuView.EasyButton()
        self.mediumButton = mainMenuView.MediumButton()
        self.hardButton = mainMenuView.HardButton()
        self.settingsButton = mainMenuView.SettingsButton()
        self.quitButton = mainMenuView.QuitButton()

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
        self.settingsButton.display_settingsButton(self.screen)
        self.quitButton.display_quitButton(self.screen)
        pygame.display.flip()

    def main_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            action = self.get_input_action(event)
            if action is None:
                continue

            if action in ("reset", "back"):
                continue

            if action == "settings":
                self.new_settings_menu()
                self.run_settings_menu()

            if action == "quit":
                pygame.quit()
                raise SystemExit

            mx, my = pygame.mouse.get_pos()

            if action in ("left", "right") and self.easyButton.is_inside_easyButton(mx, my):
                self.new_game("easy")
                self.run_game()
                return

            if action in ("left", "right") and self.mediumButton.is_inside_mediumButton(mx, my):
                self.new_game("medium")
                self.run_game()
                return

            if action in ("left", "right") and self.hardButton.is_inside_hardButton(mx, my):
                self.new_game("hard")
                self.run_game()
                return
            
            if action in ("left", "right") and self.settingsButton.is_inside_settingsButton(mx, my):
                self.new_settings_menu()
                self.run_settings_menu()

            if action in ("left", "right") and self.quitButton.is_inside_quitButton(mx, my):
                pygame.quit()
                raise SystemExit


    def new_game(self, mode_name):
        self.current_mode = mode_name
        mode_settings = self.modes[mode_name]
        self.rows = mode_settings["rows"]
        self.cols = mode_settings["cols"]
        self.amountMines = mode_settings["mines"]
        game_width = self.cols * TILESIZE
        game_height = self.rows * TILESIZE
        self.screen = pygame.display.set_mode((game_width, game_height + TOPSECTION))

        self.board = Board(self.rows, self.cols, self.amountMines)
        ui = mode_settings["ui"]
        self.mineCount = MineCount(*ui["minecount"])
        self.timer = Timer(*ui["timer"])
        self.first_click_done = False
        self.resetButton = ResetButton(*ui["reset"])
        self.backButton = BackButton(*ui["back"])
        self.quitButton = QuitButton(*ui["quit"])

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
            self.new_game(self.current_mode)

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
                raise SystemExit

            action = self.get_input_action(event)
            if action is None:
                continue

            if action == "reset":
                self.new_game(self.current_mode)
                return

            if action == "back":
                self.back_to_menu = True
                self.playing = False
                return

            if action == "quit":
                pygame.quit()
                raise SystemExit

            mx, my = pygame.mouse.get_pos()

            if action in ("left", "right") and self.resetButton.is_inside_resetButton(mx, my):
                self.new_game(self.current_mode)
                return

            if action in ("left", "right") and self.backButton.is_inside_backButton(mx, my):
                self.back_to_menu = True
                self.playing = False
                return

            if action in ("left", "right") and self.quitButton.is_inside_quitButton(mx, my):
                pygame.quit()
                raise SystemExit

            if my < TOPSECTION:
                continue
                
            my -= TOPSECTION
            mx //= TILESIZE
            my //= TILESIZE

            if not self.board.is_inside_board(mx, my):
                continue

            tile = self.board.board_list[mx][my]

            if action == "left":
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
                        
            elif action == "right":
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


    def new_settings_menu(self):
        self.screen = pygame.display.set_mode((SETTINGSMENUWIDTH, SETTINGSMENUHEIGHT))
        self.settingsMenu = settingsMenuView.SettingsMenu()
        self.controlsExplanation = settingsMenuView.ControlsExplanation()
        self.backButton = settingsMenuView.BackButton()
        self.quitButton = settingsMenuView.QuitButton()
    
    def run_settings_menu(self):
        while True:
            self.isInSettingsMenu = True
            self.back_to_menu = False
            while self.isInSettingsMenu:
                self.clock.tick(FPS)
                self.settings_menu_events()
                self.draw_settings_menu()
            if self.back_to_menu:
                self.new_main_menu()
                break

            self.close_app()
            self.new_settings_menu()

    def draw_settings_menu(self):
        self.screen.fill(BGCOLOUR)
        self.controlsExplanation.display_controllsExplanation(self.screen)
        self.backButton.display_backButton(self.screen)
        self.quitButton.display_quitButton(self.screen)
        pygame.display.flip()

    def settings_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            action = self.get_input_action(event)
            if action is None:
                continue

            if action == "reset":
                continue

            if action == "back":
                self.back_to_menu = True
                self.isInSettingsMenu = False
                return

            if action == "quit":
                pygame.quit()
                raise SystemExit

            mx, my = pygame.mouse.get_pos()

            if action in ("left", "right") and self.backButton.is_inside_backButton(mx, my):
                self.back_to_menu = True
                self.isInSettingsMenu = False
                return

            if action in ("left", "right") and self.quitButton.is_inside_quitButton(mx, my):
                pygame.quit()
                raise SystemExit


    def close_app(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

                action = self.get_input_action(event)
                if action is None:
                    continue

                if action in ("left", "right", "reset"):
                    return

                if action == "back":
                    self.back_to_menu = True
                    return

                if action == "quit":
                    pygame.quit()
                    raise SystemExit
                
    def get_input_action(self, event):
        if event.type == (pygame.MOUSEBUTTONDOWN and pygame.MOUSEBUTTONUP) and event.button == 1:
            return "left"
        if event.type == (pygame.MOUSEBUTTONDOWN and pygame.MOUSEBUTTONUP) and event.button == 3:
            return "right"
        if event.type == (pygame.KEYDOWN and pygame.KEYUP) and event.key == pygame.K_a:
            return "left"
        if event.type == (pygame.KEYDOWN and pygame.KEYUP) and event.key == pygame.K_s:
            return "right"
        if event.type == (pygame.KEYDOWN and pygame.KEYUP) and event.key == pygame.K_q:
            return "reset"
        if event.type == (pygame.KEYDOWN and pygame.KEYUP) and event.key == pygame.K_w:
            return "back"
        if event.type == (pygame.KEYDOWN and pygame.KEYUP) and event.key == pygame.K_e:
            return "quit"
        if event.type == (pygame.KEYDOWN and pygame.KEYUP) and event.key == pygame.K_r:
            return "settings"
        return None


app = App()
while True:
    app.new_main_menu()
    app.run_app()