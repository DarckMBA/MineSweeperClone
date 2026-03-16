import pygame
from settings import *

class SettingsMenu:
    def __init__(self):
        self.settingsMenu_surface = pygame.Surface((SETTINGSMENUWIDTH, SETTINGSMENUHEIGHT))

    def display_settingsMenu(self, screen):
        screen.blit(self.settingsMenu_surface, (0, 0))

class ControlsExplanation:
    def __init__(self):
        self.rect = pygame.Rect(50, 50, 300, 300)
        self.font = pygame.font.SysFont("Arial", 30, bold = True)

    def display_controllsExplanation(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)

        lines = [
            "Left click = A Key",
            "Right click = S Key",
            "Q Key = Reset",
            "W Key = Back",
            "E Key = Quit",
            "R Key = Settings",
        ]
        line_spacing = 10
        y = self.rect.top + 20

        for line in lines:
            text = self.font.render(line, True, WHITE)
            text_rect = text.get_rect(midtop = (self.rect.centerx, y))
            screen.blit(text, text_rect)
            y += text.get_height() + line_spacing

class BackButton:
    def __init__(self):
        self.rect = pygame.Rect(150, 370, 100, 40)
        self.font = pygame.font.SysFont("Arial", 30, bold = True)

    def display_backButton(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)
        text = self.font.render(f"Back", True, WHITE)
        text_rect = text.get_rect(center = self.rect.center)
        screen.blit(text, text_rect)

    def is_inside_backButton(self, x, y):
        return self.rect.collidepoint(x, y)
    
class QuitButton:
    def __init__(self):
        self.rect = pygame.Rect(150, 430, 100, 40)
        self.font = pygame.font.SysFont("Arial", 30, bold = True)

    def display_quitButton(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)
        text = self.font.render(f"Quit", True, WHITE)
        text_rect = text.get_rect(center = self.rect.center)
        screen.blit(text, text_rect)

    def is_inside_quitButton(self, x, y):
        return self.rect.collidepoint(x, y)