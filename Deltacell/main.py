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
from scripts.shake_surface import shake_screen, shaking # shake screen
from scripts.text import write_json
from scripts.camera import Camera
from scripts.blackout import *

with open("Deltacell\scripts\data.json") as file:
    data = json.load(file)

if data["data"]["id"] == "None": data["data"]["id"] = str(randint(1000, 1999))

with open("Deltacell\scripts\data.json", "w") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

write_json(filename="Deltacell\scripts\data.json", name1="statistics", name2="start")

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
        self.all_destructible = []
        self.portals = []

        self.MAP = LEVEL_1

        self.offset = pygame.Vector2((230, 0)) # offset objects (camera)

        self.shake_offset = pygame.Vector2((0, 0)) # shaking offset

        self.is_blackout = True
        self.alpha_blackout = 0
    
    def update(self):
        pygame.display.update()
        self.clock.tick(FPS)
        self.display.fill("lightblue")
        pygame.display.set_caption(f"Slime's Valley       |       FPS:{int(self.clock.get_fps())}")
        self.display.blit(shake_screen, self.shake_offset)
        shake_screen.fill("lightblue")
    
    def events(self):
        for self.event in pygame.event.get():
            if self.event.type == QUIT:
                self.run = False
    
    def create_map(self):
        sidex = shake_screen.get_size()[0] // len(self.MAP)
        sidey = shake_screen.get_size()[1] // len(self.MAP) 

        for row in range(len(self.MAP)):       
            for col in range(len(self.MAP)):
                x, y = col * sidex, row * sidey

                self.tile_rect = pygame.Rect(x, y, sidex, sidey) # grid
                self.grid.append(self.tile_rect)

                if self.MAP[row][col] == "#":
                    self.barrier = Object(pos=(x, y), kind="platforms", filename="barrier", edit=2)

                    self.all_objects.append(self.barrier)

                if self.MAP[row][col] == "1":
                    self.block = Object(pos=(x, y), kind="platforms", filename="terrain", edit=2)
                    
                    self.all_objects.append(self.block)
                
                if self.MAP[row][col] == "2":
                    self.platform = Object(pos=(x, y), kind="platforms", filename="platform", edit=2)

                    self.all_objects.append(self.platform)
                
                if self.MAP[row][col] == "3":
                    self.iron_block = Object(pos=(x, y), kind="platforms", filename="iron_box", edit=2)

                    self.all_objects.append(self.iron_block)
                
                if self.MAP[row][col] == "4":
                    self.apple = Object(pos=(x + 6, y), kind="benefits", filename="Apple", edit=2)

                    self.all_benefits.append(self.apple)
                
                if self.MAP[row][col] == "5":
                    self.enemy = Enemy(pos=(x + 15, y + 15))

                    self.all_enemies.append(self.enemy)
                
                if self.MAP[row][col] == "6":
                    self.spikes = Object(pos=(x + 1, y + 16), kind="obstacles", filename="Idle", edit=2)

                    self.all_obstacles.append(self.spikes)
                
                if self.MAP[row][col] == "7":
                    self.palm = Object(pos=(x - 20, y - 10), edit=2, kind="palm", filename="Front Palm Tree Top 01", anim=True, frames=5)
                    self.leg = Object(pos=(x + 10, y + 50), edit=2, kind="palm", filename="Front Palm leg")

                    self.all_pics.append(self.leg)
                    self.all_objects.append(self.palm)
                
                if self.MAP[row][col] == "8":
                    self.cloud = Object(pos=(x, y), edit=2, kind="clouds", filename=f"Small Cloud {randint(1, 2)}")

                    self.all_pics.append(self.cloud)
                
                if self.MAP[row][col] == "9":
                    self.box = Object(pos=(x, y), kind="platforms", filename="box1", edit=2)

                    self.all_destructible.append(self.box)
                
                if self.MAP[row][col] == "s":
                    self.tree = Object(pos=(x, y), kind="decorations", filename="stone_head")

                    self.all_objects.append(self.tree)
                
                if self.MAP[row][col] == "f":
                    self.spiked_ball = Object(pos=(x, y), kind="obstacles", filename="spiked_ball", edit=1.4)

                    self.all_obstacles.append(self.spiked_ball)
                    self.all_objects.append(self.spiked_ball)
                
                if self.MAP[row][col] == "a":
                    self.flower = Object(pos=(x + 4, y + 2), kind="decorations", filename="flower", edit=2)

                    self.all_pics.append(self.flower)

                if self.MAP[row][col] == "b":
                    self.tablet = Object(pos=(x, y), kind="decorations", filename="tablet", edit=2)

                    self.all_pics.append(self.tablet)
                
                if self.MAP[row][col] == "P":
                    self.portal = Object(pos=(x, y - 5), kind="portal", filename="0", edit=2)

                    self.all_pics.append(self.portal)
                    self.portals.append(self.portal)



    def new_classes(self):
        self.player = Player(pos=(300, 540))
        self.bullet = Bullets(pos=(0, 0))

        self.camera = Camera()
        self.particles = Particles()
        self.cursor = Cursor(filename="cursor.png", edit=0.9) 

    def main(self):
        self.new_classes() # >>
        self.create_map() # map spawn

        
        self.run = True
        while self.run:

            self.particles.spawn() # spawning particels

            
            for objects in self.all_pics, self.all_objects, self.all_obstacles: # collide with objects and obstacles 
                for i in objects:
                    i.update()
                    i.set_pos(pos=(i.get_pos()[0] + self.offset.x, i.get_pos()[1])) # update on offset.x
                    i.set_hitbox()
            
            
            for destructible in self.all_destructible: # object which may break
                destructible.update()
                destructible.set_pos(pos=(destructible.get_pos()[0] + self.offset.x, destructible.get_pos()[1]))
                destructible.set_hitbox()

                if self.bullet.get_collide(destructible): # collide bullet with destructible object
                    for i in range(20): self.particles.add(pos=destructible.position, color="brown", size=(8, 24)) # add particles

                    write_json(filename="Deltacell\scripts\data.json", name1="statistics", name2="break")
                    
                    self.all_destructible.remove(destructible) # delete object
                    self.bullet.shaking = True # shake screen
            
            
            for bonus in self.all_benefits: # benefit and bonuses
                bonus.update()
                bonus.set_pos(pos=(bonus.get_pos()[0] + self.offset.x, bonus.get_pos()[1])) # update on offset.x
                bonus.set_hitbox()

                if self.player.get_collide(bonus): # collide apple with player
                    for i in range(10): self.particles.add(pos=bonus.position, color="green&red")
                    self.all_benefits.remove(bonus) # do not draw
            

            for enemy in self.all_enemies: # enemy with bullet
                enemy.update()
                enemy.set_pos(pos=(enemy.get_pos()[0] + self.offset.x, enemy.get_pos()[1]))
                enemy.set_hitbox()
                enemy.animations()

                
                if self.bullet.get_collide(enemy): 
                    for i in range(20): self.particles.add(pos=enemy.position, color="green&red") # kill particles
                    
                    self.bullet.shaking = True # update shaking
                    write_json(filename="Deltacell\scripts\data.json", name1="statistics", name2="kill")

                    self.all_enemies.remove(enemy) # do not draw
            
            for portal in self.portals: # collide player with portal
                if self.player.get_collide(portal): 
                    self.MAP = LEVEL_2 # next level
                    self.is_blackout = True
            
            
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
            self.player.set_hitbox()
            self.player.collide(bodies=[self.all_objects, self.all_destructible], obstacles=self.all_obstacles, benefits=self.all_benefits, enemies=self.all_enemies)

            
            # effects
            
            # camera update and change offset.x
            if self.camera.collide_center(body=self.player) == "left": self.offset.x += 1.5
            if self.camera.collide_center(body=self.player) == "right": self.offset.x -= 1.5
            if self.player.die_time == 0:  # if player dead
                self.is_blackout = True
                self.bullet.shaking = True


            
            # blackout
            if self.is_blackout:  # if player dead
                self.alpha_blackout = blackout()[0]
                blackout_screen.set_alpha(self.alpha_blackout)
                shake_screen.blit(blackout_screen, (0, 0))

                if self.alpha_blackout >= 300: # return to the start pos
                    self.player.position.x, self.player.position.y = 300, 540
                    self.offset.x = 230
                    if self.player.die_time < 10:  # if player dead
                        self.player.hit = True
                        # update map
                    self.all_benefits.clear()
                    self.all_destructible.clear()
                    self.all_enemies.clear()
                    self.all_objects.clear()
                    self.all_obstacles.clear()
                    self.all_pics.clear()
                    self.portals.clear()
                    self.grid.clear()
                    self.create_map() # update map
                
                if self.alpha_blackout <= 0: # end blackuot
                    self.is_blackout = False    
                    self.alpha_blackout = 0
                    self.player.hit = False
                    

            # shaking screen
            if self.bullet.shaking: self.shake_offset = shaking(10)
            else: self.shake_offset = [0, 0]

            self.cursor.update() # update aim

            self.update()
            self.events()
        
        pygame.quit()

if __name__ == '__main__':
    game = MainApp().main()