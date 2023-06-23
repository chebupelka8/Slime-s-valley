import pygame
from scripts.sprite import Sprite

class Object(Sprite):
    def __init__(self, pos=(),  filename="", edit=1, opacity=300):
        super().__init__(pos=pos)

        self.edit = edit
        self.filename = filename
        self.opacity = opacity
        self.start_pos = pos

        self.is_collide = True
        
        self.image = pygame.image.load(f"Deltacell/images/objects/{self.filename}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0] * self.edit, self.image.get_size()[1] * self.edit))
        self.image.set_alpha(self.opacity)
        self.rect = self.image.get_rect(topleft=self.position)
    
    def set_pos(self, pos=()):
        self.position = pygame.Vector2(pos)
    
    def get_pos(self):
        return self.start_pos
    
    def get_collide(self, body):
        return self.rect.colliderect(body)
    
    def update(self):
        self.rect.topleft = self.position

        self.display.blit(self.image, self.rect)
        #pygame.draw.rect(self.display, "red", (self.rect), 1)


class AnimatedObject(Sprite):
    def __init__(self, pos: tuple, frames: list, speed_animation: float):
        super().__init__(pos)

        self.start_pos = pos
        self.frames = frames
        self.speed_animation = speed_animation
        self.frame = 1
    
    def set_pos(self, pos: tuple):
        self.position = pygame.Vector2(pos)

    def get_pos(self):
        return self.start_pos 

    def animation(self):
        self.frame += self.speed_animation

        if self.frame >= len(self.frames): self.frame = 1

        self.rect = self.frames[int(self.frame)].get_rect(topleft=self.position)

    def update(self):
        self.display.blit(self.frames[int(self.frame)], self.rect)




