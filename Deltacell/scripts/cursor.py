import pygame

class Cursor:
    def __init__(self, filename, edit=1):
        self.display = pygame.display.get_surface()

        self.image = pygame.image.load(f"Deltacell\images\cursor\{filename}").convert_alpha() # load image
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0] * edit, self.image.get_size()[1] * edit))
    
    def update(self):
        self.mousepress = pygame.mouse.get_pressed()
        self.mousepos = pygame.mouse.get_pos()

        if self.mousepress[2]: pygame.mouse.set_visible(True)
        else: pygame.mouse.set_visible(False)

        self.rect = self.image.get_rect(center=self.mousepos)
        self.display.blit(self.image, self.rect)