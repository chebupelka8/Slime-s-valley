import pygame
import json
import sys
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
from scripts.text import write_json, SetText
from scripts.camera import Camera
from scripts.blackout import blackout_screen
from scripts.menu_button import PictureButton, MenuButton

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

        self.is_blackout = False
        self.alpha_blackout = 0
        self.alpha_speed = 6

        self.SCENE = 1 # scene

        """
        0: menu
        1: level_menu
        2: game
        """
    
    def update(self):
        pygame.display.update()
        self.clock.tick(FPS)
        pygame.display.set_caption(f"Slime's Valley       |       FPS:{int(self.clock.get_fps())}")
        self.display.blit(blackout_screen, (0, 0))
    
    def events(self):
        for self.event in pygame.event.get():
            if self.event.type == QUIT:
                self.run = False
            if self.event.type == KEYDOWN:
                if self.event.key  == K_ESCAPE and self.SCENE == 2:
                    self.SCENE = 5
    
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
                    self.cloud = Object(pos=(x, y), edit=2, kind="clouds", filename=f"Small Cloud {randint(1, 2)}", opacity=180)

                    self.all_pics.append(self.cloud)
                
                if self.MAP[row][col] == "9":
                    self.box = Object(pos=(x, y), kind="platforms", filename="box1", edit=2)

                    self.all_destructible.append(self.box)
                
                if self.MAP[row][col] == "s":
                    self.tree = Object(pos=(x, y), kind="decorations", filename="stone_head")

                    self.all_objects.append(self.tree)
                
                if self.MAP[row][col] == "f":
                    self.spiked_ball = Object(pos=(x, y), kind="rotate_spike", filename="Suriken1", edit=2, frames=6, anim=True)

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
                    self.gravity_effect = Object(pos=(x - 32, y - 14), kind="gravity", filename="Gravity1", anim=True, frames=20, speed_frame=0.1, opacity=150)

                    self.all_pics.append(self.portal)
                    self.all_pics.append(self.gravity_effect)
                    self.portals.append(self.portal)

    def clear_map(self):
        self.all_benefits.clear()
        self.all_destructible.clear()
        self.all_enemies.clear()
        self.all_objects.clear()
        self.all_obstacles.clear()
        self.all_pics.clear()
        self.portals.clear()
        self.grid.clear()

    def menu(self): # SCENE: 0
        pass

    def level_menu(self): # SCENE: 1
        self.display.fill("lightblue")
        pygame.mouse.set_visible(True)

        self.easy_level.update()
        self.easy_level.update_press()
        self.medium_level.update()
        self.medium_level.update_press()
        self.hard_level.update()
        self.hard_level.update_press()

        SetText(text="Easy", pos=(self.easy_level.rect.centerx, self.easy_level.rect.centery - 40), color="green", size=22, font="Deltacell/fonts/Minecraftia-Regular.ttf")
        SetText(text="Medium", pos=(self.medium_level.rect.centerx, self.medium_level.rect.centery - 40), color="yellow", size=22, font="Deltacell/fonts/Minecraftia-Regular.ttf")
        SetText(text="Hard", pos=(self.hard_level.rect.centerx, self.hard_level.rect.centery - 40), color="red", size=22, font="Deltacell/fonts/Minecraftia-Regular.ttf")
        
        
        if self.easy_level.get_pressed(): 
            self.MAP = LEVEL_1
            self.is_blackout = True

        if self.medium_level.get_pressed():
            self.MAP = LEVEL_2
            self.is_blackout = True

        if self.hard_level.get_pressed():
            self.MAP = LEVEL_3
            self.is_blackout = True
        
        if self.is_blackout: 
            self.alpha_blackout += self.alpha_speed 
        
            if self.alpha_blackout >= 300: self.alpha_speed = -2
            if self.alpha_blackout <= 0: self.alpha_speed = 4
            blackout_screen.set_alpha(self.alpha_blackout)
            self.display.blit(blackout_screen, (0, 0))
            
            if self.alpha_blackout >= 300: # ceneter blackout
                # return in start pos
                self.player.position.x, self.player.position.y = 300, 540
                self.offset.x = 230
                self.player.hit = True
                # clear map
                self.clear_map()
                self.create_map()
                self.SCENE = 2


    def game(self): # SCENE: 2
        self.particles.spawn() # spawning particels
        
        # display settings
        self.display.fill("lightblue")
        self.display.blit(shake_screen, self.shake_offset)
        shake_screen.fill("lightblue")

            
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

            
            if self.bullet.get_collide(enemy): # kill enemy | collide bullets with enemy
                for i in range(20): self.particles.add(pos=enemy.position, color="green&red") # kill particles
                
                self.bullet.shaking = True # update shaking
                write_json(filename="Deltacell\scripts\data.json", name1="statistics", name2="kill")

                self.all_enemies.remove(enemy) # do not draw
        
        for portal in self.portals: # collide player with portal
            if self.player.get_collide(portal): 
                self.clear_map() # clear map
                self.SCENE = 1 # level menu
        
        
        # bullets
        if not self.player.hit: # if player not invisble 
            self.bullet.update()
            self.bullet.rotate(self.player.position) # rotate to mouse
            self.bullet.flugbahn() # line follow to mouse
            self.bullet.update_pos(self.player.position)
            self.bullet.collide(bodies=self.all_objects) # collide with objects in self.all_objects
        else: self.bullet.bullets.clear() # if player invisible he cant shoot

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
            self.alpha_blackout = 0
            self.bullet.shaking = True

        
        # blackout
        shake_screen.blit(blackout_screen, (0, 0))
        blackout_screen.set_alpha(self.alpha_blackout)
        if self.is_blackout:  # if player dead
            self.alpha_blackout += self.alpha_speed
            if self.alpha_blackout >= 300: self.alpha_speed = -2
            if self.alpha_blackout <= 0: self.alpha_speed = 4

            if self.alpha_blackout >= 300: # return to the start pos
                self.player.position.x, self.player.position.y = 300, 540
                self.offset.x = 230
                self.player.die = False
                self.player.hit = True
                
                # update map
                self.clear_map() # clear map: player dead | next level
                self.create_map() # create map
            
            if self.alpha_blackout <= 0: # end blackuot
                self.is_blackout = False    
                self.alpha_blackout = 0
                self.player.hit = False
                

        # shaking screen
        if self.bullet.shaking: self.shake_offset = shaking(10)
        else: self.shake_offset = [0, 0]

        self.cursor.update() # update aim

    def pause_menu(self): # SCENE: 5
        pygame.mouse.set_visible(True)
        self.surf = pygame.Surface((600, 600))
        self.surf.set_alpha(100)
        #self.display.blit(self.surf, (0, 0))
        #self.display.set_colorkey("lightblue")
        self.display.set_alpha(300)

        SetText(pos=(300, 100), text="PAUSE", jump=False, size=50, font="Deltacell/fonts/Minecraftia-Regular.ttf")

        self.resume.update()
        self.resume.update_press(color_standart=(0, 180, 0), color_collide=(0, 100, 0), color_press=(0, 70, 0))
        if self.resume.get_pressed(): self.SCENE = 2

        self.exit.update()
        self.exit.update_press(color_standart=(180, 0, 0), color_collide=(100, 0, 0), color_press="black")
        if self.exit.get_pressed(): sys.exit()

        self.main_menu.update()
        self.main_menu.update_press(color_standart=(0, 0, 180), color_collide=(0, 0, 100), color_press=(0, 70, 0))
        if self.main_menu.get_pressed(): 
            self.SCENE = 1
            self.is_blackout = False
            # clear map
            self.clear_map()
                 

    def new_classes(self):
        # game
        self.player = Player(pos=(300, 540))
        self.bullet = Bullets(pos=(0, 0))

        self.camera = Camera()
        self.particles = Particles()
        self.cursor = Cursor(filename="cursor.png", edit=0.9) 

        # level menu
        self.easy_level = PictureButton(pos=(100, 300), kind="level_screenshots", filename="Faceset", edit=3, color_edge="green")
        self.medium_level = PictureButton(pos=(300, 300), kind="level_screenshots", filename="Faceset2", edit=3, color_edge="yellow")
        self.hard_level = PictureButton(pos=(500, 300), kind="level_screenshots", filename="Faceset1", edit=3, color_edge="red")

        # pause menu
        self.resume = MenuButton(pos=(300, 280), size=(200, 40), text="Resume", text_size=20)
        self.exit = MenuButton(pos=(300, 350), size=(200, 40), text="Exit", text_size=20)
        self.main_menu = MenuButton(pos=(300, 420), size=(200, 40), text="Main Menu", text_size=20)

    def main(self):
        self.new_classes() # >>
        
        self.run = True
        while self.run:

            if self.SCENE == 0: self.menu()
            if self.SCENE == 1: self.level_menu()
            if self.SCENE == 2: self.game()
            if self.SCENE == 5: self.pause_menu()

            self.update()
            self.events()
        
        pygame.quit()

if __name__ == '__main__':
    game = MainApp().main()