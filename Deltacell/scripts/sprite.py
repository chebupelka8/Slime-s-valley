import pygame
from scripts.shake_surface import shake_screen

class Sprite:
    def __init__(self, pos=()):
        self.display = shake_screen

        self.position = pygame.Vector2(pos) # set position
    
    def set_hitbox(self):
        # top
        self.top_rect = pygame.Rect(0, 0, self.rect[2] - 5, 5)
        self.top_rect.topleft = (self.rect.topleft[0] + 5, self.rect.topleft[1]) # don't intersect rect
        #pygame.draw.rect(self.display, "red", (self.top_rect), 1)

        # bottom
        self.bottom_rect = pygame.Rect(0, 0, self.rect[2] - 5, 5)
        self.bottom_rect.bottomleft = (self.rect.bottomleft[0] + 5, self.rect.bottomleft[1])
        #pygame.draw.rect(self.display, "green", (self.bottom_rect), 1)        
        
        # right
        self.right_rect = pygame.Rect(0, 0, 5, self.rect[3] - 4)
        self.right_rect.topleft = (self.rect.topright[0], self.rect.topright[1] + 2)
        #pygame.draw.rect(self.display, "blue", (self.right_rect), 1)
        
        # left
        self.left_rect = pygame.Rect(0, 0, 5, self.rect[3] - 4)
        self.left_rect.topleft = (self.rect.topleft[0], self.rect.topleft[1] + 2)
        #pygame.draw.rect(self.display, "purple", (self.left_rect), 1)
