import pygame
from pygame.locals import *
from scripts.text import SetText

pygame.init()

class MenuButton:
    def __init__(self, pos=(), size=(), color=(0, 0, 0), text='', text_size=12, text_color='white'):
        self.display = pygame.display.get_surface()
        
        self.position = pygame.Vector2(pos)
        self.size = [size[0], size[1]]
        self.color = color
        self.text = text
        self.text_size = text_size
        self.text_color = text_color

        self.rect = pygame.Rect(self.position.x, self.position.y, self.size[0], self.size[1])
    
    def set_color(self, new_color): # replace color
        self.color = new_color
    
    def get_collide(self): # if mouse collide with button
        self.mousepos = pygame.mouse.get_pos()

        if self.rect.collidepoint(self.mousepos): return True
    
    def get_pressed(self): # if mouse pressed on button
        self.mousepress = pygame.mouse.get_pressed()
        
        if self.mousepress[0] and self.get_collide(): return True 
    
    def update_press(self, color_collide, color_press, color_standart): # if prees and collide replace color

        if self.get_collide():
            self.set_color(new_color=color_collide)
            if self.get_pressed(): self.set_color(new_color=color_press)

        else: self.set_color(new_color=color_standart) 
    
    def update(self):
        self.rect.center = self.position
        pygame.draw.rect(self.display, self.color, (self.rect))
        SetText(text=self.text, pos=(self.rect.center), size=self.text_size, font='comic sans ms', color=self.text_color)
