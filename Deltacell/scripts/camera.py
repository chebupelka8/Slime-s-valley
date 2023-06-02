import pygame
from scripts.shake_surface import shake_screen

class Camera:
    def __init__(self, size=250):
        self.display = shake_screen

        self.barrier = pygame.Rect(0, 0, size, size)
        self.barrier.center = self.display.get_rect().center

    def collide(self, body):
        if body.rect.topleft[0] <= 175: 
            body.xvel += 1.5
            return "left"
        if body.rect.topright[0] >= 425: 
            body.xvel -= 1.5
            return "right"
    
    def collide_center(self, body):
        if body.xvel > 0: 
            return "right"
        if body.xvel < 0: 
            return "left"

    def update(self):
        pygame.draw.rect(self.display, "white", (self.barrier), 3)