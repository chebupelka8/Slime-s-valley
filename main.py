import pygame
import json
import sys
from random import randint
from pygame.locals import *
from scripts.settings import *
from scripts.particles import Particles
from scripts.object import Object, AnimatedObject
from scripts.player import Player
from scripts.enemy import Enemy
from scripts.bullets import Bullets
from scripts.cursor import Cursor # aim
from scripts.shake_surface import shake_screen, shaking # shake screen
from scripts.text import write_json, SetText
from scripts.camera import Camera
from scripts.blackout import blackout_screen
from scripts.menu_button import PictureButton, MenuButton
from scripts.effect import Effect
from scripts.animation import upload_animation

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
        pygame.display.set_icon(pygame.image.load("Deltacell/images/ics/FacesetWhite.png")) 

        self.all_objects = []
        self.all_animated = []
        self.all_pics = []
        self.all_enemies = []
        self.all_obstacles = []
        self.all_benefits = []
        self.all_destructible = []
        self.portals = []

        self.MAP = None

        self.offset = pygame.Vector2((230, 0)) # offset objects (camera)

        self.shake_offset = pygame.Vector2((0, 0)) # shaking offset

        self.is_blackout = False
        self.alpha_blackout = 0
        self.alpha_speed = 6

        self.SCENE = 0 #! scene

        """
        0: menu
        1: level_menu
        2: game
        """
    
    def update(self):
        pygame.display.update()
        self.clock.tick(FPS) #! 144
        pygame.display.set_caption(f"Slime's Valley       |       FPS:{int(self.clock.get_fps())}")
        self.display.blit(blackout_screen, (0, 0))
    
    def events(self):
        for self.event in pygame.event.get():
            if self.event.type == QUIT:
                self.run = False
            if self.event.type == KEYDOWN: #* open pause menu
                if self.event.key  == K_ESCAPE and self.SCENE == 2:
                    self.is_blackout = False
                    self.alpha_blackout = 0
                    self.SCENE = 5
    
    def create_map(self):
        sidex = shake_screen.get_size()[0] // len(self.MAP)
        sidey = shake_screen.get_size()[1] // len(self.MAP) 

        for row in range(len(self.MAP)):       
            for col in range(len(self.MAP)):
                x, y = col * sidex, row * sidey

                if self.MAP[row][col] == "#":
                    self.barrier = Object(pos=(x, y), filename="platforms/barrier", edit=2)

                    self.all_objects.append(self.barrier)

                if self.MAP[row][col] == "1":
                    self.block = Object(pos=(x, y), filename="platforms/terrain", edit=2)
                    
                    self.all_objects.append(self.block)
                
                if self.MAP[row][col] == "2":
                    self.platform = Object(pos=(x, y), filename="platforms/platform", edit=2)

                    self.all_objects.append(self.platform)
                
                if self.MAP[row][col] == "3":
                    self.iron_block = Object(pos=(x, y), filename="platforms/iron_box", edit=2)

                    self.all_objects.append(self.iron_block)
                
                if self.MAP[row][col] == "4":
                    self.apple = Object(pos=(x + 6, y), filename="benefits/Apple", edit=2)

                    self.all_benefits.append(self.apple)
                
                if self.MAP[row][col] == "5":
                    self.enemy = Enemy(pos=(x + 15, y + 15))

                    self.all_enemies.append(self.enemy)
                
                if self.MAP[row][col] == "6":
                    self.spikes = Object(pos=(x + 1, y + 16), filename="obstacles/Idle", edit=2)

                    self.all_obstacles.append(self.spikes)
                
                if self.MAP[row][col] == "7":
                    self.palm = AnimatedObject(pos=(x - 20, y - 10), frames=upload_animation(frames=4, filename="palm/Front Palm Tree Top 0", edit=2), speed_animation=0.03)
                    self.leg = Object(pos=(x + 10, y + 50), edit=2, filename="palm/Front Palm leg")

                    self.all_pics.append(self.leg)
                    self.all_animated.append(self.palm)
                    self.all_objects.append(self.palm)
                
                if self.MAP[row][col] == "8":
                    self.cloud = Object(pos=(x, y), edit=2, filename=f"clouds/Small Cloud {randint(1, 2)}", opacity=180)

                    self.all_pics.append(self.cloud)
                
                if self.MAP[row][col] == "9":
                    self.box = Object(pos=(x, y), filename="platforms/box1", edit=2)

                    self.all_destructible.append(self.box)
                
                if self.MAP[row][col] == "s":
                    self.tree = Object(pos=(x, y), filename="decorations/stone_head")

                    self.all_objects.append(self.tree)
                
                if self.MAP[row][col] == "f":
                    self.spiked_ball = AnimatedObject(pos=(x, y), frames=upload_animation(filename="rotate_spike/Suriken", frames=6, edit=2), speed_animation=0.08)

                    self.all_obstacles.append(self.spiked_ball)
                    self.all_animated.append(self.spiked_ball)
                
                if self.MAP[row][col] == "a":
                    self.flower = Object(pos=(x + 4, y + 2), filename="decorations/flower", edit=2)

                    self.all_pics.append(self.flower)

                if self.MAP[row][col] == "b":
                    self.tablet = Object(pos=(x, y), filename="decorations/tablet", edit=2)

                    self.all_pics.append(self.tablet)
                
                if self.MAP[row][col] == "P":
                    self.portal = Object(pos=(x, y - 5), filename="portal/0", edit=2)
                    self.gravity_effect = AnimatedObject(pos=(x - 32, y - 14), frames=upload_animation(filename="gravity/Gravity", frames=20), speed_animation=0.1)

                    self.all_pics.append(self.portal)
                    self.all_animated.append(self.gravity_effect)
                    self.all_pics.append(self.gravity_effect)
                    self.portals.append(self.portal)

    def clear_map(self):
        self.all_benefits.clear()
        self.all_animated.clear()
        self.all_destructible.clear()
        self.all_enemies.clear()
        self.all_objects.clear()
        self.all_obstacles.clear()
        self.all_pics.clear()
        self.portals.clear()

    def menu(self): #! SCENE: 0
        self.display.fill("lightblue")
        pygame.mouse.set_visible(True)

        self.start_label_shadow.update()
        self.start_label.update()

        self.start.update_press()
        self.start.update()
        if self.start.get_pressed(): 
            self.is_blackout = True
            self.alpha_blackout = 0

        self.quit.update_press()
        self.quit.update()
        if self.quit.get_pressed(): sys.exit()

        #& blackout
        if self.is_blackout: 
            self.alpha_blackout += self.alpha_speed 
        
            if self.alpha_blackout >= 300: self.alpha_speed = -2
            if self.alpha_blackout <= 0: self.alpha_speed = 4
            blackout_screen.set_alpha(self.alpha_blackout)
            self.display.blit(blackout_screen, (0, 0))
            
            if self.alpha_blackout >= 300: # ceneter blackout
                self.SCENE = 1 #* to level menu
            
            if self.alpha_blackout <= 0: # end blackuot
                self.is_blackout = False    
                self.alpha_blackout = 0

    def level_menu(self): #! SCENE: 1
        self.display.fill("lightblue")
        pygame.mouse.set_visible(True)

        #& update ui
        self.easy_level.update()
        self.easy_level.update_press_size()
        self.medium_level.update()
        self.medium_level.update_press_size()
        self.hard_level.update()
        self.hard_level.update_press_size()

        SetText(text="Easy", pos=(self.easy_level.rect.centerx, self.easy_level.rect.centery - 40), color="green", size=22, font="Deltacell/fonts/Minecraftia-Regular.ttf")
        SetText(text="Medium", pos=(self.medium_level.rect.centerx, self.medium_level.rect.centery - 40), color="yellow", size=22, font="Deltacell/fonts/Minecraftia-Regular.ttf")
        SetText(text="Hard", pos=(self.hard_level.rect.centerx, self.hard_level.rect.centery - 40), color="red", size=22, font="Deltacell/fonts/Minecraftia-Regular.ttf")
        
        #& update press
        if self.easy_level.get_pressed(): 
            self.MAP = LEVEL_1
            self.is_blackout = True

        if self.medium_level.get_pressed():
            self.MAP = LEVEL_2
            self.is_blackout = True

        if self.hard_level.get_pressed():
            self.MAP = LEVEL_3
            self.is_blackout = True
        
        #& blackout
        if self.is_blackout: 
            self.alpha_blackout += self.alpha_speed 
        
            if self.alpha_blackout >= 300: self.alpha_speed = -2
            if self.alpha_blackout <= 0: self.alpha_speed = 4
            blackout_screen.set_alpha(self.alpha_blackout)
            self.display.blit(blackout_screen, (0, 0))
            
            if self.alpha_blackout >= 300: # ceneter blackout
                if self.MAP != None:
                    # return in start pos
                    self.player.position.x, self.player.position.y = 300, 540
                    self.offset.x = 230
                    self.player.hit = True
                    # clear map
                    self.clear_map()
                    self.create_map()
                    self.SCENE = 2

            if self.alpha_blackout <= 0: # end blackuot
                self.is_blackout = False    
                self.alpha_blackout = 0

    def game(self): #! SCENE: 2
        
        # display settings
        self.display.fill("lightblue")
        self.display.blit(shake_screen, self.shake_offset) # blit shake surf on main display
        shake_screen.fill("lightblue")

        #self.particles.spawn() #& particles spawn update
        
        
        for animated in self.all_animated: #* animated objects
            animated.animation()
            #animated.update()
            animated.set_pos(pos=(animated.get_pos()[0] + self.offset.x, animated.get_pos()[1]))
            animated.set_hitbox()
        
        
        
        for objects in self.all_pics, self.all_objects, self.all_obstacles: #* objects, obstacles and pictures
            for i in objects:
                i.update()
                i.set_pos(pos=(i.get_pos()[0] + self.offset.x, i.get_pos()[1])) # update on offset.x
                i.set_hitbox()
        
        
        
        for destructible in self.all_destructible: #* object which may break
            destructible.update()
            destructible.set_pos(pos=(destructible.get_pos()[0] + self.offset.x, destructible.get_pos()[1]))
            destructible.set_hitbox()
            
            
            if self.bullet.get_collide(destructible): # collide bullet with destructible object

                write_json(filename="Deltacell\scripts\data.json", name1="statistics", name2="break")
                
                self.all_destructible.remove(destructible) # delete object
                self.bullet.shaking = True # shake screen

        
        for bonus in self.all_benefits: #* benefit and bonuses
            bonus.update()
            bonus.set_pos(pos=(bonus.get_pos()[0] + self.offset.x, bonus.get_pos()[1])) # update on offset.x
            bonus.set_hitbox()

            if self.player.get_collide(bonus): # collide apple with player
                write_json(filename="Deltacell\scripts\data.json", name1="statistics", name2="collect")
                self.all_benefits.remove(bonus) # do not draw
        

        for enemy in self.all_enemies: #* enemy with bullet
            enemy.update()
            enemy.set_pos(pos=(enemy.get_pos()[0] + self.offset.x, enemy.get_pos()[1]))
            enemy.set_hitbox()
            enemy.animations()

            

            if self.bullet.get_collide(enemy): #* kill enemy | collide bullets with enemy

                self.bullet.shaking = True # update shaking
                write_json(filename="Deltacell\scripts\data.json", name1="statistics", name2="kill")

                self.all_enemies.remove(enemy) # do not draw
        
        
        for portal in self.portals: #* collide player with portal
            if self.player.get_collide(portal): 
                self.clear_map() # clear map
                self.SCENE = 1 # level menu
        
        
        #& bullets
        if not self.player.hit: # if player not invisble 
            self.bullet.update()
            self.bullet.rotate(self.player.position) # rotate to mouse
            self.bullet.flugbahn() # line follow to mouse
            self.bullet.update_pos(self.player.position)
            self.bullet.collide(bodies=[self.all_objects, self.all_obstacles]) # collide with objects in self.all_objects
        else: self.bullet.bullets.clear() # if player invisible he cant shoot

        #& player
        self.player.animation()
        self.player.jump()
        self.player.move()
        self.player.update()
        self.player.barrier() # deid if posy > 590
        self.player.set_hitbox()
        self.player.collide(bodies=[self.all_objects, self.all_destructible], obstacles=self.all_obstacles, enemies=self.all_enemies)

        
        #& effects
        # camera update and change offset.x
        if self.camera.collide_center(body=self.player) == "left": self.offset.x += 1.5
        if self.camera.collide_center(body=self.player) == "right": self.offset.x -= 1.5
        
        if self.player.die_time == 0:  # if player dead
            self.is_blackout = True
            self.alpha_blackout = 0
            self.bullet.shaking = True

        
        #& blackout
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
                

        #& shaking screen
        if self.bullet.shaking: self.shake_offset = shaking(10)
        else: self.shake_offset = [0, 0]

        self.cursor.update() # update aim

    def pause_menu(self): #! SCENE: 5
        pygame.mouse.set_visible(True)

        self.pause_label_shadow.update()
        self.pause_label.update()

        self.resume.update_press()
        self.resume.update()
        if self.resume.get_pressed(): self.SCENE = 2

        self.restart.update_press()
        self.restart.update()
        if self.restart.get_pressed(): 
            self.player.dead()
            self.SCENE = 2
            self.is_blackout = True
            self.alpha_blackout = 300

        self.main_menu.update_press()
        self.main_menu.update()
        if self.main_menu.get_pressed(): 
            self.is_blackout = True
            # clear map
            self.clear_map()
            
        self.exit.update_press()
        self.exit.update()
        if self.exit.get_pressed(): sys.exit()

        if self.is_blackout:
            self.display.set_colorkey((0, 0, 0)) 
            self.alpha_blackout += self.alpha_speed 
        
            if self.alpha_blackout >= 300: self.alpha_speed = -2
            if self.alpha_blackout <= 0: self.alpha_speed = 4
            blackout_screen.set_alpha(self.alpha_blackout)
            self.display.blit(blackout_screen, (0, 0))
            
            if self.alpha_blackout >= 300: # ceneter blackout
                self.SCENE = 0 #* to menu
            
            if self.alpha_blackout <= 0: # end blackuot
                self.is_blackout = False    
                self.alpha_blackout = 0
                 

    def new_classes(self):
        #* game
        self.player = Player(pos=(300, 540))
        self.bullet = Bullets(pos=(0, 0))

        self.camera = Camera()
        self.cursor = Cursor(filename="cursor.png", edit=0.9) 
        self.particles = Particles()

        #* menu
        self.start_label = PictureButton(pos=(100, 100), filename="Menu", edit=3)
        self.start_label_shadow = PictureButton(pos=(105, 105), filename="Menu_shadow", edit=3)

        self.start = PictureButton(pos=(100, 200), filename=["start/start1", "start/start2"], edit=2)
        self.quit = PictureButton(pos=(100, 270), filename=["quit/quit1", "quit/quit2"], edit=2)

        #* level menu
        self.easy_level = PictureButton(pos=(100, 300), filename="level_screenshots/Faceset2", edit=3, color_edge="green")
        self.medium_level = PictureButton(pos=(300, 300), filename="level_screenshots/Faceset", edit=3, color_edge="yellow")
        self.hard_level = PictureButton(pos=(500, 300), filename="level_screenshots/Faceset1", edit=3, color_edge="red")

        #* pause menu
        self.resume = PictureButton(pos=(300, 280), filename=["continue/continue1", "continue/continue2"], edit=2)
        self.restart = PictureButton(pos=(300, 350), filename=["restart/restart1", "restart/restart2"], edit=2)
        self.main_menu = PictureButton(pos=(300, 420), filename=["menu/menu1", "menu/menu2"], edit=2)
        self.exit = PictureButton(pos=(300, 490), filename=["quit/quit1", "quit/quit2"], edit=2)
        self.pause_label = PictureButton(pos=(300, 120), filename="Pause", edit=3)
        self.pause_label_shadow = PictureButton(pos=(305, 125), filename="Pause_shadow", edit=3)

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