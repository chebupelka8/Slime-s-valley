import pygame
from scripts.sprite import Sprite

class Object(Sprite):
    def __init__(self, pos=(), kind="", filename="", edit=1, anim=False, frames=1):
        super().__init__(pos=pos)

        self.display = pygame.display.get_surface()

        self.edit = edit
        self.anim = anim
        self.filename = filename
        self.kind = kind
        self.frames = frames

        self.image = pygame.image.load(f"Deltacell/images/objects/{self.kind}/{self.filename}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0] * self.edit, self.image.get_size()[1] * self.edit))
        self.rect = self.image.get_rect(topleft=self.position)

        # animation
        self.frame = 1
    
    def set_pos(self, pos=()):
        self.position = pos
    
    def get_pos(self):
        return self.position
    
    def get_collide(self, body):
        return self.rect.colliderect(body)
    
    def animation(self):
        self.frame += 0.028
        
        if self.frame >= self.frames: self.frame = 1 # updating frames

        self.image = pygame.image.load(f"Deltacell\images\objects\{self.kind}\{self.filename[:-1]}{int(self.frame)}.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0] * self.edit, self.image.get_size()[1] * self.edit))
    
    def update(self):
        self.rect.topleft = self.position # update in topleft
        #pygame.draw.rect(self.display, "red", (self.rect), 1)
        
        if self.anim: self.animation()

        self.display.blit(self.image, self.rect)