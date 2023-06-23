from random import randint 
import pygame
from scripts.settings import WIDTH, HEIGHT

pygame.init()

try:
    e_screen = pygame.Surface((WIDTH * 4, HEIGHT * 4)).convert_alpha()
    print('k')
except:
    shake_screen = pygame.Surface((WIDTH * 4, HEIGHT * 4))

def shaking(speed): return [randint(-speed, speed), randint(-speed, speed)]

