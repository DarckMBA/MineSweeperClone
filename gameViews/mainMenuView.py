import pygame
from settings import *

class MainMenu:
    def __init__(self):
        self.mainMenu_surface = pygame.Surface((MAINMENUWIDTH, MAINMENUHEIGHT))

    def display_mainMenu(self, screen):
        screen.blit(self.mainMenu_surface, (0, 0))

class EasyButton:
    def __init__(self):
        self.rect = pygame.Rect(40, 60, 80, 40)
        self.shade = pygame.Rect(45, 65, 80, 40)
        self.font = pygame.font.SysFont("Arial", 30, bold = True)

    def display_easyButton(self, screen):
        pygame.draw.rect(screen, BLACK, self.shade, 0, 10)
        pygame.draw.rect(screen, LIGHTGREY, self.rect, 0, 10)
        text = self.font.render(f"EASY", True, WHITE)
        text_rect = text.get_rect(center = self.rect.center)
        screen.blit(text, text_rect)

    def is_inside_easyButton(self, x, y):
        return self.rect.collidepoint(x, y)
    
class MediumButton:
    def __init__(self):
        self.rect = pygame.Rect(150, 60, 120, 40)
        self.shade = pygame.Rect(155, 65, 120, 40)
        self.font = pygame.font.SysFont("Arial", 30, bold = True)

    def display_mediumButton(self, screen):
        pygame.draw.rect(screen, BLACK, self.shade, 0, 10)
        pygame.draw.rect(screen, LIGHTGREY, self.rect, 0, 10)
        text = self.font.render(f"MEDIUM", True, WHITE)
        text_rect = text.get_rect(center = self.rect.center)
        screen.blit(text, text_rect)

    def is_inside_mediumButton(self, x, y):
        return self.rect.collidepoint(x, y)
    
class HardButton:
    def __init__(self):
        self.rect = pygame.Rect(110, 120, 90, 40)
        self.shade = pygame.Rect(115, 125, 90, 40)
        self.font = pygame.font.SysFont("Arial", 30, bold = True)

    def display_hardButton(self, screen):
        pygame.draw.rect(screen, BLACK, self.shade, 0, 10)
        pygame.draw.rect(screen, LIGHTGREY, self.rect, 0, 10)
        text = self.font.render(f"HARD", True, WHITE)
        text_rect = text.get_rect(center = self.rect.center)
        screen.blit(text, text_rect)

    def is_inside_hardButton(self, x, y):
        return self.rect.collidepoint(x, y)
    
class SettingsButton:
    def __init__(self):
        self.rect = pygame.Rect(40, 180, 130, 40)
        self.shade = pygame.Rect(45, 185, 130, 40)
        self.font = pygame.font.SysFont("Arial", 30, bold = True)

    def display_settingsButton(self, screen):
        pygame.draw.rect(screen, BLACK, self.shade, 0, 10)
        pygame.draw.rect(screen, LIGHTGREY, self.rect, 0, 10)
        text = self.font.render(f"SETTINGS", True, WHITE)
        text_rect = text.get_rect(center = self.rect.center)
        screen.blit(text, text_rect)

    def is_inside_settingsButton(self, x, y):
        return self.rect.collidepoint(x, y)
    
class QuitButton:
    def __init__(self):
        self.rect = pygame.Rect(200, 180, 70, 40)
        self.shade = pygame.Rect(205, 185, 70, 40)
        self.font = pygame.font.SysFont("Arial", 30, bold = True)

    def display_quitButton(self, screen):
        pygame.draw.rect(screen, BLACK, self.shade, 0, 10)
        pygame.draw.rect(screen, LIGHTGREY, self.rect, 0, 10)
        text = self.font.render(f"QUIT", True, WHITE)
        text_rect = text.get_rect(center = self.rect.center)
        screen.blit(text, text_rect)

    def is_inside_quitButton(self, x, y):
        return self.rect.collidepoint(x, y)