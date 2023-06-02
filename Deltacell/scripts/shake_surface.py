from random import randint 
import pygame
from scripts.settings import WIDTH, HEIGHT

shake_screen = pygame.Surface((WIDTH * 4, HEIGHT * 4))

def shaking(speed): return [randint(-speed, speed), randint(-speed, speed)]

