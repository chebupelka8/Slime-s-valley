import pygame
from scripts.sprite import Sprite
from random import random, choice

class Enemy(Sprite):
    def __init__(self, pos=()):
        super().__init__(pos)

        
        self.image = pygame.image.load("Deltacell/images/enemy/0.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0] * 0.5, self.image.get_size()[1] * 0.5))
        self.rect = self.image.get_rect(center=self.position)

        self.start_pos = pos

        self.speed = 0.5
        self.frame = 0

        self.is_collide = None

        self.bullets = []
    
    def get_collide(self, body):
        return self.rect.colliderect(body.rect)
    
    def get_pos(self):
        return self.start_pos

    def set_pos(self, pos):
        self.position.x = pos[0]
    
    def add(self):
        self.bullets.append([[self.position.x, self.position.y], [random() * (1 + 1) - 1, random() * (1 + 1) - 1]])
    
    def animations(self):
        self.frame += 0.02
        if self.frame >= 4: self.frame = 0

        self.image = pygame.image.load(f"Deltacell\images\enemy\{int(self.frame)}.png") # image open
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0] * 0.5, self.image.get_size()[1] * 0.5)) 

    def update(self):
        self.rect.center = self.position # update on center

        self.display.blit(self.image, self.rect)