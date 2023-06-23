import pygame

pygame.init()

def upload_animation(filename: str, frames: int, edit: float=1, opacity: int=300):
    all_frames = []
    
    for i in range(1, frames + 1): 
        image = pygame.image.load(f"Deltacell/images/objects/{filename}{i}.png").convert_alpha()
        image = pygame.transform.scale(image, (image.get_size()[0] * edit, image.get_size()[1] * edit))
        image.set_alpha(opacity)
        
        all_frames.append(image)

    return all_frames