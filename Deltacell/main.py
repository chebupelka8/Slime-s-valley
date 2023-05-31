import pygame
import json
from random import randint
from pygame.locals import *
from scripts.settings import *
from scripts.particles import Particles
from scripts.object import Object
from scripts.player import Player
from scripts.enemy import Enemy
from scripts.bullets import Bullets
from scripts.cursor import Cursor # aim
from scripts.shake_surface import shaking # shake screen
from scripts.text import write_json

with open("Deltacell\scripts\data.json") as file:
    data = json.load(file)

if data["data"]["id"] == "None": data["data"]["id"] = str(randint(1000, 1999))

with open("Deltacell\scripts\data.json", "w") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

pygame.init()

class MainApp:
    def __init__(self):
        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_icon(pygame.image.load("Deltacell/images/ics/free-icon-rainbow-4475005.png")) 

        self.all_objects = []
        self.all_pics = []
        self.all_enemies = []
        self.all_obstacles = []
        self.all_benefits = []
        self.grid = []

        self.offsetx, self.offsety = 0, 0 
    
    def update(self):
        pygame.display.update()
        self.clock.tick(FPS)
        self.display.fill("lightblue")
        pygame.display.set_caption(f"Slime's Valley       |       FPS:{int(self.clock.get_fps())}")
    
    def events(self):
        for self.event in pygame.event.get():
            if self.event.type == QUIT:
                self.run = False
    
    def create_map(self):
        side = self.display.get_size()[0] // len(MAP)

        for row in range(len(MAP)):       
            for col in range(len(MAP)):
                x, y = col * side, row * side

                self.tile_rect = pygame.Rect(x, y, side, side) # grid
                self.grid.append(self.tile_rect)



                if MAP[row][col] == "1":
                    self.block = Object(pos=(x, y), kind="platforms", filename="Idle", edit=2)
                    
                    self.all_objects.append(self.block)
                
                if MAP[row][col] == "2":
                    self.platform = Object(pos=(x, y), kind="platforms", filename="Brown Off", edit=2)

                    self.all_objects.append(self.platform)
                
                if MAP[row][col] == "3":
                    self.iron_block = Object(pos=(x, y), kind="platforms", filename="iron_box", edit=1.6)

                    self.all_objects.append(self.iron_block)
                
                if MAP[row][col] == "4":
                    self.apple = Object(pos=(x + 6, y), kind="benefits", filename="Apple", edit=2)

                    self.all_benefits.append(self.apple)
                
                if MAP[row][col] == "5":
                    self.enemy = Enemy(pos=(x, y + 15))

                    self.all_enemies.append(self.enemy)
                
                if MAP[row][col] == "6":
                    self.spikes = Object(pos=(x + 1, y + 16), kind="obstacles", filename="Idle", edit=2)

                    self.all_obstacles.append(self.spikes)
                
                if MAP[row][col] == "7":
                    self.palm = Object(pos=(x - 20, y - 10), edit=2, kind="palm", filename="Front Palm Tree Top 01", anim=True, frames=4)
                    self.leg = Object(pos=(x + 10, y + 50), edit=2, kind="palm", filename="Front Palm leg")

                    self.all_pics.append(self.leg)
                    self.all_objects.append(self.palm)
                
                if MAP[row][col] == "8":
                    self.cloud = Object(pos=(x, y), edit=2, kind="clouds", filename=f"Small Cloud {randint(1, 2)}")

                    self.all_pics.append(self.cloud)

    def new_classes(self):
        self.player = Player(pos=(50, 500))
        self.bullet = Bullets(pos=(0, 0))

        self.particles = Particles()
        self.cursor = Cursor(filename="cursor.png", edit=0.9) 

    def main(self):
        self.new_classes() # >>
        self.create_map() # map spawn

        
        self.run = True
        while self.run:

            #self.offsetx, self.offsety = shaking(speed=5) # shaking
            self.particles.spawn()
            
            for obj in self.all_pics, self.all_objects, self.all_obstacles: # collide with objects and obstacles 
                for i in obj:
                    i.update()
                    i.set_hitbox()
            
            # bullets
            self.bullet.update()
            self.bullet.rotate(self.player.position) # rotate to mouse
            self.bullet.flugbahn() # line follow to mouse
            self.bullet.update_pos(self.player.position)
            self.bullet.collide(bodies=self.all_objects) # collide with objects in self.all_objects

            # player
            self.player.animation()
            self.player.jump()
            self.player.move()
            self.player.update()
            self.player.barrier() # deid if posy > 590
            self.player.name(name="You")  # nickname
            self.player.set_hitbox()
            self.player.collide(bodies=self.all_objects, obstacles=self.all_obstacles, benefits=self.all_benefits, enemies=self.all_enemies)

            for bnf in self.all_benefits: # benefit and bonuses
                bnf.update()
                bnf.set_hitbox()

                if self.player.get_collide(bnf): self.all_benefits.remove(bnf) # do not draw
            
            # enemy
            for enm in self.all_enemies:
                enm.update()
                enm.set_hitbox()
                enm.name(name="Monster") # nickname
                enm.animations()
                enm.move(size=50) #    50 - center(start_pos) + 50
                
                if len(self.bullet.bullets) > 0:
                    if self.bullet.get_collide(enm): 
                        for i in range(20): self.particles.add(pos=enm.position, color="green&red") # kill particles
                        
                        write_json(filename="Deltacell\scripts\data.json", name1="statistics", name2="kill")

                        self.all_enemies.remove(enm) # do not draw
            
            #for j in self.grid: pygame.draw.rect(self.display, "white", (j), 1) # show grid

            # effects
            self.particles.update(pos=pygame.mouse.get_pos())
            self.cursor.update()

            self.update()
            self.events()
        
        pygame.quit()

if __name__ == '__main__':
    game = MainApp().main()