from scripts.sprite import Sprite
from scripts.text import SetText
from scripts.particles import Particles
import pygame
from pygame.locals import *
from scripts.text import write_json

class Player(Sprite):
    def __init__(self, pos=()):
        super().__init__(pos)
        
        # vel position 
        self.xvel, self.yvel = 0, 0
        
        # animation
        self.action = 0
        self.frame = 1
        self.hit = False
        self.die = False

        # fall
        self.gravity = 0.035
        self.isfall = True
        self.die_time = 10

        self.image = pygame.image.load("Deltacell\images\player\Idle\Slime_Medium_Red1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0] * 3, self.image.get_size()[1] * 3))
        self.rect = self.image.get_rect(center=self.position)

        self.particles = Particles()
    
    def set_pos(self, pos):
        self.position = pygame.Vector2(pos) 

    def get_pos(self):
        return self.position
    
    def animation(self):
        self.actions = ["Idle", "Left", "Right", "Hit", "Dead"]
        
        self.frame += 0.05
        if self.frame >= 5: self.frame = 1

        self.image = pygame.image.load(f"Deltacell\images\player\{self.actions[self.action]}\Slime_Medium_Red{int(self.frame)}.png")
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0] * 3, self.image.get_size()[1] * 3))
    
    def name(self, name):
        SetText(text=name, pos=(self.position.x, self.position.y - 30), color="white", size=10, font="comic sans ms")
    
    def collide(self, bodies, obstacles, benefits, enemies): # collide with objects and interactions
        self.yvel += self.gravity

        for i in bodies:
            for body in i:
                if self.get_collide(body): # with all_objects (var)
                    
                    # horizontal
                    if self.left_rect.colliderect(body.right_rect): 
                        self.xvel += 1.5
                    if self.right_rect.colliderect(body.left_rect): 
                        self.xvel -= 1.5

                    # vertical 
                    if self.bottom_rect.colliderect(body.top_rect):
                        self.isfall = False
                        if self.yvel > 4: self.position.y -= self.yvel
                        self.yvel = 0
                    if self.top_rect.colliderect(body.bottom_rect):
                        self.isfall = True
                        self.yvel = 0.5
        
        self.particles.spawn() # particles update

        for obstacle in obstacles: # kill, if you collide with this object
            if self.get_collide(obstacle): 
                self.die = True
                
                if self.die_time > 10: self.dead() # go to start position
        
        for enemy in enemies: # kill, if you collide with this object
            if self.get_collide(enemy):
                self.die = True

                if self.die_time > 10: self.dead()
        
        for benefit in benefits: # get benefits
            if self.get_collide(benefit):
                write_json(filename="Deltacell\scripts\data.json", name1="statistics", name2="collect")

                for i in range(10): self.particles.add(pos=benefit.rect.center, color="green&red")

    def jump(self):
        keypress = pygame.key.get_pressed()
        
        if keypress[K_SPACE] and not self.isfall and self.yvel == 0 and not self.hit and not self.die: 
            self.isfall = True
            self.yvel = -2.5

    def move(self): # moving left, right and up, down
        keypress = pygame.key.get_pressed()

        # update position
        self.position.y += self.yvel

        if not self.hit and not self.die:
            if keypress[K_LEFT] or keypress[K_a]: 
                self.xvel = -1.5
                self.action = 1
            if keypress[K_RIGHT] or keypress[K_d]: 
                self.xvel = 1.5
                self.action = 2
        
        if self.hit: self.action = 3
        if self.die: 
            self.xvel = 0
            self.action = 4
        
        if not keypress[K_LEFT] and not keypress[K_RIGHT] and not keypress[K_a] and not keypress[K_d] and not self.die: # if no key is pressed
            self.xvel = 0
            if not self.hit:
                self.action = 0 
        
        self.rect.center = self.position # update by center
    
    def barrier(self):
        if self.position.y >= 680 and self.die_time > 10:
            self.dead() # go to start position
    
    def dead(self):
        self.yvel = 0
        self.die_time = 0
        
        write_json(filename="Deltacell\scripts\data.json", name1="statistics", name2="dead")

    
    def get_collide(self, body): # collide with the body
        if self.rect.colliderect(body.rect): return True
        else: return False
    
    def update(self):
        
        self.die_time += 0.1
        
        self.display.blit(self.image, self.rect)