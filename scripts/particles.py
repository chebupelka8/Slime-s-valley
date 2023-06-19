import pygame
from scripts.shake_surface import shake_screen
from random import random, randint, choice

class Particles:
    def __init__(self):
        self.display = shake_screen
        
        self.particles = []
    
    def add(self, pos=(), color="gray", size=(3, 18)):
        colors = {
            "rainbow": ["red", "orange", "yellow", "green", "light blue", "blue", "purple"],
            "green&red": [(0, 180, 0), (0, 140, 0), (0, 100, 0), (0, 255, 0), (180, 0, 0), (140, 0, 0), (100, 0, 0), (255, 0, 0) ],
            "red": [(180, 0, 0), (140, 0, 0), (100, 0, 0), (255, 0, 0)],
            "brown": ["#79553D", "#755C48", "#734222", "#673923", "#45322E"],
            "gray": [(50, 50, 50), (60, 60, 60), (70, 70, 70), (90, 90, 90), (110, 110, 110), (130, 130, 130), (150, 150, 150)]
        }

        self.particles.append([[pos[0], pos[1]], [random() * (1 + 1) - 1, random() * (1 + 1) - 1], [randint(size[0], size[1])], [choice(colors[color])]])
    
    def spawn(self):
        for self.particle in self.particles:
            self.particle[0][0] -= self.particle[1][0]
            self.particle[0][1] -= self.particle[1][1]
            self.particle[2][0] -= 0.2
            
            pygame.draw.rect(self.display, self.particle[3][0], (self.particle[0][0], self.particle[0][1], self.particle[2][0], self.particle[2][0]))

            if self.particle[2][0] <= 0: self.delete()
    
    def delete(self):
        self.particles.remove(self.particle) # delete particle 
    
    def update(self, pos): # if pressed mouse button
        if pygame.mouse.get_pressed()[1]: self.add(pos)
        self.spawn()

