import pygame

pygame.init()

try:
    blackout_screen = pygame.Surface((600, 600)).convert_alpha()
    print('i')
except:
    blackout_screen = pygame.Surface((600, 600))
