import pygame
from settings import *

class MainMenu:
    def __init__(self):
        self.mainMenu_surface = pygame.Surface((MAINMENUWIDTH, MAINMENUHEIGHT))

    def display_mainMenu(self, screen):
        screen.blit(self.mainMenu_surface, (0, 0))

class EasyButton:
    def __init__(self):
        self.rect = pygame.Rect(100, 40, 100, 40)
        self.font = pygame.font.SysFont("Arial", 30, bold = True)

    def display_easyButton(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)
        text = self.font.render(f"Easy", True, WHITE)
        text_rect = text.get_rect(center = self.rect.center)
        screen.blit(text, text_rect)

    def is_inside_easyButton(self, x, y):
        return self.rect.collidepoint(x, y)
    
class MediumButton:
    def __init__(self):
        self.rect = pygame.Rect(100, 100, 100, 40)
        self.font = pygame.font.SysFont("Arial", 30, bold = True)

    def display_mediumButton(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)
        text = self.font.render(f"Medium", True, WHITE)
        text_rect = text.get_rect(center = self.rect.center)
        screen.blit(text, text_rect)

    def is_inside_mediumButton(self, x, y):
        return self.rect.collidepoint(x, y)
    
class HardButton:
    def __init__(self):
        self.rect = pygame.Rect(100, 160, 100, 40)
        self.font = pygame.font.SysFont("Arial", 30, bold = True)

    def display_hardButton(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)
        text = self.font.render(f"Hard", True, WHITE)
        text_rect = text.get_rect(center = self.rect.center)
        screen.blit(text, text_rect)

    def is_inside_hardButton(self, x, y):
        return self.rect.collidepoint(x, y)
    
class QuitButton:
    def __init__(self):
        self.rect = pygame.Rect(100, 220, 100, 40)
        self.font = pygame.font.SysFont("Arial", 30, bold = True)

    def display_quitButton(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)
        text = self.font.render(f"Quit", True, WHITE)
        text_rect = text.get_rect(center = self.rect.center)
        screen.blit(text, text_rect)

    def is_inside_quitButton(self, x, y):
        return self.rect.collidepoint(x, y)