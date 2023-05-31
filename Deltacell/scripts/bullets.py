import pygame
from math import cos, sin, atan2
from scripts.particles import Particles
from scripts.text import write_json

class Bullet:
    def __init__(self, pos=(0, 0)):
        self.position = pygame.Vector2(pos)


class Bullets(Bullet):
    def __init__(self, pos=(0, 0)):
        self.display = pygame.display.get_surface()

        self.bullets = []
        self.time = 0

        self.particles = Particles()

        super().__init__(pos=pos)
    
    def rotate(self, pos): # rotate towards the body
        self.mx, self.my = pygame.mouse.get_pos()
        self.x, self.y = pos

        self.rel_angle = atan2(self.y - self.my, self.x - self.mx)
        self.velx = cos(self.rel_angle) * 6
        self.vely = sin(self.rel_angle) * 6

    def flugbahn(self): # flugbahn towards the body (if rotate: True)

        self.angle = atan2(self.x - self.mx, self.y - self.my)
        pygame.draw.line(self.display, "white", (self.x, self.y), ((self.x + sin(self.angle) * -40), (self.y + cos(self.angle) * -40)), 2)
    
    def update_pos(self, pos): # new position
        self.position = pygame.Vector2(pos)

    def add(self):
        self.bullets.append([[self.position.x, self.position.y], [self.velx, self.vely]])

        write_json(filename="Deltacell\scripts\data.json", name1="statistics", name2="shoot")
    
    def spawn(self):
        for self.bullet in self.bullets:
            self.bullet[0][0] -= self.bullet[1][0]
            self.bullet[0][1] -= self.bullet[1][1]

            self.circle = pygame.draw.circle(self.display, "white", (self.bullet[0][0], self.bullet[0][1]), 5)

            if self.bullet[0][1] < 0: self.delete()
    
    def get_collide(self, body):
        if len(self.bullets) > 0: return self.circle.colliderect(body.rect)
    
    def collide(self, bodies):
        self.particles.spawn()

        for body in bodies:
            
            if self.get_collide(body) and len(self.bullets) > 0: 
                self.bullets.remove(self.bullet) # do not draw
                
                for i in range(10): self.particles.add(pos=(self.bullet[0][0], self.bullet[0][1]))

    def update(self):
        self.time += 0.1

        self.mousepos = pygame.mouse.get_pos()
        self.mousepress = pygame.mouse.get_pressed()

        if self.mousepress[0] and self.time >= 10:
            self.add()
            self.time = 0
        
        self.spawn()
    
    def delete(self): 
        if len(self.bullets) > 0: self.bullets.remove(self.bullet) # delete bullet
