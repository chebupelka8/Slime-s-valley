import pygame
from scripts.shake_surface import shake_screen

class Effect:
    def __init__(self, pos: list, filename: str, opacity=300, edit=1, frames=1):
        self.display = shake_screen

        self.position = pygame.Vector2(pos)
        
        self.filename = filename
        self.edit = edit
        self.opacity = opacity
        self.frame = 1
        self.frames = frames
        self.all_frames = list()

        self.is_collide = False

        for i in range(1, self.frames + 1):
            self.image = pygame.image.load(f"Deltacell/images/effects/{self.filename}{int(i)}.png")
            self.image = pygame.transform.scale(self.image, (self.image.get_size()[0] * self.edit, self.image.get_size()[1] * self.edit))
            self.image.set_alpha(self.opacity)
            self.rect = self.image.get_rect()
            self.all_frames.append([self.image, self.rect])
    
    def set_pos(self, pos: list):
        self.position = pygame.Vector2(pos)
    
    def animation(self, speed_frames: float):
        self.frame += speed_frames # update frames
        self.all_frames[int(self.frame)][1] = self.position
    
    def update(self):
        self.display.blit(self.all_frames[int(self.frame)][0], self.all_frames[int(self.frame)][1]) # draw
        pygame.draw.rect(self.display, "red", (self.rect), 1)

        


