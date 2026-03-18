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
        self.shade = pygame.Rect(55, 55, 300, 300)
        self.font = pygame.font.SysFont("Arial", 30, bold = True)

    def display_controllsExplanation(self, screen):
        pygame.draw.rect(screen, BLACK, self.shade, 0, 10)
        pygame.draw.rect(screen, LIGHTGREY, self.rect, 0, 10)

        lines = [
            "LEFT CLICK = A KEY",
            "RIGHT CLICK = S KEY",
            "Q KEY = RESET",
            "W KEY = BACK",
            "E KEY = QUIT",
            "R KEY = SETTINGS",
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
        self.shade = pygame.Rect(155, 375, 100, 40)
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
    def __init__(self):
        self.rect = pygame.Rect(150, 430, 100, 40)
        self.shade = pygame.Rect(155, 435, 100, 40)
        self.font = pygame.font.SysFont("Arial", 30, bold = True)

    def display_quitButton(self, screen):
        pygame.draw.rect(screen, BLACK, self.shade, 0, 10)
        pygame.draw.rect(screen, LIGHTGREY, self.rect, 0, 10)
        text = self.font.render(f"QUIT", True, WHITE)
        text_rect = text.get_rect(center = self.rect.center)
        screen.blit(text, text_rect)

    def is_inside_quitButton(self, x, y):
        return self.rect.collidepoint(x, y)