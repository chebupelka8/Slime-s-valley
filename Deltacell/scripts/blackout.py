import pygame
from scripts.shake_surface import shake_screen

blackout_screen = pygame.Surface((600, 600))

alpha = 300
d = 8

def blackout():
    global alpha, d
    alpha += d

    if alpha >= 300: d = -1.5
    if alpha <= 0: d = 6
    
    return [alpha, d]