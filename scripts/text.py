import pygame
import math
import time
import json

def write_json(filename, name1, name2):
    with open(filename) as file:
        data = json.load(file)
    
    data[name1][name2] += 1

    with open(filename, "w") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def SetText(text="", pos=(0, 0), size=12, font="arial", color="white", jump=False):
    display = pygame.display.get_surface() # main display
    
    font = pygame.font.Font(font, size).render(text, True, color) # render text

    if not jump: rect = font.get_rect(center=pos)
    if jump: rect = font.get_rect(center=(pos[0], pos[1] + (math.sin(time.time() * 8) * 10))) # always jumping
    
    display.blit(font, rect)