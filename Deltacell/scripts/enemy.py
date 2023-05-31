import pygame
from PIL import Image
from scripts.sprite import Sprite
from scripts.text import SetText
from scripts.particles import Particles

class Enemy(Sprite):
    def __init__(self, pos=()):
        super().__init__(pos)

        self.display = pygame.display.get_surface()

        self.image = pygame.image.load("Deltacell\images\enemy\Snake1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0] * 2.5, self.image.get_size()[1] * 2.5))
        self.rect = self.image.get_rect(center=self.position)

        self.start_pos = pos

        self.speed = 0.5
        self.frame = 1
        self.action = 0
    
    def get_collide(self, body):
        return self.rect.colliderect(body.rect)
    
    def animations(self):
        self.frame += 0.04
        if self.frame >= 4: self.frame = 1

        self.image = Image.open(f"Deltacell\images\enemy\Snake{int(self.frame)}.png") # image open
        self.image = self.image.convert("RGB") # convert to RGB

        self.image = pygame.image.fromstring(self.image.tobytes(), self.image.size, "RGB") # to pygame
        self.image.set_colorkey((0, 0, 0))
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0] * 2.5, self.image.get_size()[1] * 2.5)) 
    
    def follow(self, body): # follow the body

        if self.position.x < body.position.x: self.position.x += self.speed
        if self.position.x > body.position.x: self.position.x -= self.speed
        if self.position.y < body.position.y: self.position.y += self.speed
        if self.position.y > body.position.y: self.position.y -= self.speed

        self.rect.center = self.position # update in center
    
    def move(self, size):
        self.position.x += self.speed

        if self.position.x >= self.start_pos[0] + size: 
            self.speed *= -1 # <
            self.action = 1
        if self.position.x <= self.start_pos[0] - size: 
            self.speed = abs(self.speed) # >
            self.action = 0
        
        if self.action == 1: self.image = pygame.transform.flip(self.image, True, False) # flip <>
        
        self.rect.center = self.position # update on center

    
    def name(self, name): # nickname
        SetText(text=name, pos=(self.position.x, self.position.y - 30), font="comic sans ms", color="red", size=10)
    
    def update(self):
        self.display.blit(self.image, self.rect)