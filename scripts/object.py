import pygame
from scripts.sprite import Sprite

class Object(Sprite):
    def __init__(self, pos=(), kind="", filename="", edit=1, anim=False, frames=1, speed_frame=0.028, opacity=300):
        super().__init__(pos=pos)

        self.edit = edit
        self.anim = anim
        self.filename = filename
        self.kind = kind
        self.frames = frames
        self.speed_frame = speed_frame
        self.opacity = opacity
        self.start_pos = pos

        self.image = pygame.image.load(f"Deltacell/images/objects/{self.kind}/{self.filename}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0] * self.edit, self.image.get_size()[1] * self.edit))
        self.image.set_alpha(self.opacity)
        self.rect = self.image.get_rect(topleft=self.position)

        # animation
        self.frame = 1
    
    def set_pos(self, pos=()):
        self.position = pos
    
    def get_pos(self):
        return self.start_pos
    
    def get_collide(self, body):
        return self.rect.colliderect(body)
    
    def animation(self):
        self.frame += self.speed_frame
        
        if self.frame >= self.frames: self.frame = 1 # updating frames

        self.image = pygame.image.load(f"Deltacell\images\objects\{self.kind}\{self.filename[:-1]}{int(self.frame)}.png")
        self.image.set_alpha(self.opacity)
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0] * self.edit, self.image.get_size()[1] * self.edit))
    
    def update(self):
        self.rect.topleft = self.position # update in topleft
        if self.anim: self.animation()

        self.display.blit(self.image, self.rect)
        #pygame.draw.rect(self.display, "red", (self.rect), 1)


