import pygame
from settings import *

pygame.font.init()


class Tile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, text):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.x, self.y = x, y
        self.text = text
        self.rect = self.image.get_rect()
        if self.text != "empty":
            self.font = pygame.font.SysFont("Verdana", 50)
            font_surface = self.font.render(self.text, True, BLACK)
            self.image.fill(WHITE)
            self.font_size = self.font.size(self.text)
            draw_x = (TILESIZE / 2) - self.font_size[0] / 2
            draw_y = (TILESIZE / 2) - self.font_size[1] / 2
            self.image.blit(font_surface, (draw_x, draw_y))
        else:
            self.image.fill(BLACK)

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    def click(self, mouse_x, mouse_y):
        return self.rect.left <= mouse_x <= self.rect.right and self.rect.top <= mouse_y <= self.rect.bottom

    def right(self):
        return self.rect.x + TILESIZE < GAME_SIZE * TILESIZE

    def left(self):
        return self.rect.x - TILESIZE >= 0

    def up(self):
        return self.rect.y - TILESIZE >= 0

    def down(self):
        return self.rect.y + TILESIZE < GAME_SIZE * TILESIZE


class UIElement:
    def __init__(self, x, y, text):
        self.x, self.y = x, y
        self.text = text

    def draw(self, screen):
        font = pygame.font.SysFont("Verdana", 30)
        text = font.render(self.text, True, WHITE)
        screen.blit(text, (self.x, self.y))


class RoundedButton:
    def __init__(self, x, y, width, height, text, color, text_color, border_radius=10):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.border_radius = border_radius
        self.font = pygame.font.SysFont("Verdana", 30)
        self.text_surface = self.font.render(self.text, True, self.text_color)

    def draw(self, screen):
        pygame.draw.rect(screen, pygame.Color('gray'), self.rect, border_radius=self.border_radius)
        pygame.draw.rect(screen, self.color, self.rect.inflate(-4, -4), border_radius=self.border_radius)

        text_rect = self.text_surface.get_rect(center=self.rect.center)
        screen.blit(self.text_surface, text_rect)

    def collidepoint(self, pos):
        return self.rect.collidepoint(pos)

    def click(self, mouse_x, mouse_y):
        return self.rect.x <= mouse_x <= self.rect.x + self.rect.width and self.rect.y <= mouse_y <= self.rect.y + self.rect.height