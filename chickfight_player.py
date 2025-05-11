import math
import random

import pygame
from Sprite_handle import *
from Attack import Attack
from config import Config

class Player(pygame.sprite.Sprite):
    """
    Sprites key index:
    1 is how long the frame
    2 is row 
    3 is column 
    4,5 is w,h_area of sprite
    """
    sprites_key = {"idle": [[4, 0, 0, 16, 16], [4, 0, 0, 16, 16], [4, 5, 0, 16, 16], [4, 5, 0, 16, 16]],
                   "walk": [[4, 0, 1, 16, 16], [4, 0, 1, 16, 16], [4, 5, 1, 16, 16], [4, 5, 1, 16, 16]],
                   "attack1": [[3, 0, 2, 16, 16], [3, 0, 2, 16, 16], [3, 5, 2, 16, 16], [3, 5, 2, 16, 16]],
                   "attack2": [[3, 0, 2, 16, 16], [3, 0, 2, 16, 16], [3, 5, 2, 16, 16], [3, 5, 2, 16, 16]],
                   "hurt": [[1, 4, 0, 16, 16], [1, 4, 0, 16, 16], [1, 9, 0, 16, 16], [1, 9, 0, 16, 16]],
                   "death": [[2, 2, 2, 16, 16], [2, 2, 2, 16, 16], [2, 2, 5, 16, 16], [2, 2, 5, 16, 16]],
                   "enter_arena":[[4, 5, 1, 16, 16], [4, 5, 1, 16, 16], [4, 5, 1, 16, 16], [4, 5, 1, 16, 16]]}
    player_behavior = {"hurt":{"cooldown":1500}, "attack1":{"cooldown":300, "damage":5},
                       "attack2":{"cooldown":500, "damage":10}, "roll":{"charge_time":200, "cooldown":250}}

    def __init__(self, position, game, name='Player',health=100.0):
        super().__init__()
        # Animation related
        self.game = game
        self.name = name
        self.max_health = health
        self.health = self.max_health
        self.sprite_dir = "sprites\\player.png"
        self.size = self.game.screen_scale
        self.status = None
        self.image = None
        self.rect = None

        self.max_velocity = 70 #pixel per second (1second loop around 60 time that mean 1 loop walk 0.72)
        self.acceleration = int(self.max_velocity/7)
        self.deceleration = int(self.max_velocity/5)

        self.frame_animation = 0
        self.action = 'idle'
        self.loop_action = False
        self.facing = 0
        self.death = False
        """ Direction 
            0 : NORTH
            1 : WEST(left)
            2 : SOUTH
            3 : EAST(right)
        """
        self.animation = {}
        self.load_sprite(Player.sprites_key)
        self.old_position = (0,0)
        self.atk_pos = (0, 0)
        self.rect.center = (position[0], position[1])
        self.velocity = [0,0]
        self.cooldown = {"hurt": 0, "bounce":0, "attack1":0, "attack2":0, "roll":0}
        self.charge = {"bounce":0, "enter_arena":0, "roll":0}


    def update(self, frame, ms_per_loop, atk_group, event=None):
        self.update_per_loop(frame, ms_per_loop)
        self.status_update(frame, ms_per_loop)

        self.player_on_entities()
        self.life_check()

        move_pos = self.player_key_handle(event)
        if self.action not in ["attack1", "attack2", "hurt", "death", "enter_arena"]:
            if move_pos != [0, 0] or self.velocity != [0, 0]:
                self.action = "walk"
                self.loop_action = True
                self.movement(move_pos, ms_per_loop)
        self.attack(atk_group)
        self.animated()


    def animated(self):
        if self.death is False:
            if self.frame_animation > len(self.animation[self.action][self.facing])-1:
                self.frame_animation = 0
                if self.loop_action is False:
                    self.action = "idle"
        self.image = self.animation[self.action][self.facing][self.frame_animation]


    def health_reduce(self, bullet_damage):
        if self.health > 0 and self.cooldown["hurt"] == 0:
            self.health -= bullet_damage
            self.action = "hurt"
            self.cooldown["hurt"] = self.player_behavior["hurt"]["cooldown"]
            self.frame_animation = 0
            self.status = "bounce"
            if self.facing in [1, 3]:
                if self.facing == 1:
                    velocity_x = 10
                    velocity_y = -10
                else:
                    velocity_x = -10
                    velocity_y = -10
            else:
                velocity_x = 0
                if self.facing == 0:
                    velocity_y = 20
                else:
                    velocity_y = -10
            self.velocity = [velocity_x, velocity_y]



    def update_per_loop(self, frame, ms_per_loop):
        ## 1 frame = 250ms == ms_per_1frame of game file
        if self.death is True:
            return
        #frame_base
        if frame == 1:
            self.frame_animation += frame
            self.loop_action = False
        # time based
        for keys,values in self.cooldown.items():
            if values > 0:
                self.cooldown[keys] -= ms_per_loop
            else :
                self.cooldown[keys] = 0

    def status_update(self, frame, ms_per_loop):
        self.old_position = [self.rect.x, self.rect.y]
        if self.death is True:
            return

        if self.status == "bounce":
            self.action = "hurt"
            self.loop_action = True
            self.charge["bounce"] += ms_per_loop
            if self.charge["bounce"] >= 300:
                self.charge["bounce"] = 0
                self.status = None
                self.velocity = [0, 0]
                return
            if self.facing in [1,3]:
                if self.charge["bounce"] > 100:
                    self.velocity[1] += 300 * (ms_per_loop / 1000)
                else :
                    self.velocity[1] += 150 * (ms_per_loop / 1000)
            else:
                if self.charge["bounce"] > 70:
                    if self.facing == 0:
                        self.velocity[1] -= 250 * (ms_per_loop / 1000)
                    else:
                        self.velocity[1] += 250 * (ms_per_loop / 1000)
            self.rect.x += self.velocity[0] * self.game.screen_scale * (ms_per_loop / 1000)
            self.rect.y += self.velocity[1] * self.game.screen_scale * (ms_per_loop / 1000)

            check1_x, check1_y, hit_wall, wall_dir = Config.check_boundary(self, self.game.arena_area)
            self.rect.x = check1_x
            self.rect.y = check1_y

        elif self.status == "enter_arena":
            self.action = "enter_arena"
            self.loop_action = True
            accelerate = 500
            gravity = 2500
            bounce_strength = 1500
            damping = 5

            if self.rect.x < self.game.arena_area["start_x"]:
                self.velocity[0] += accelerate * (ms_per_loop / 1000)
                self.velocity[1] -= bounce_strength * (ms_per_loop / 1000)
            elif self.rect.right > self.game.arena_area["end_x"]:
                self.velocity[0] -= accelerate * (ms_per_loop / 1000)
                self.velocity[1] -= bounce_strength * (ms_per_loop / 1000)

            if self.rect.y < self.game.arena_area["start_y"]:
                self.velocity[1] += gravity * (ms_per_loop / 1000)
            elif self.rect.bottom > self.game.arena_area["end_y"]:
                self.velocity[1] -= gravity * (ms_per_loop / 1000)

            for i in range(2):
                self.velocity[i] -= self.velocity[i] * damping * (ms_per_loop / 1000)
                if abs(self.velocity[i]) < 2:
                    self.velocity[i] = 0

            self.rect.x += self.velocity[0] * self.game.screen_scale * (ms_per_loop / 1000)
            self.rect.y += self.velocity[1] * self.game.screen_scale * (ms_per_loop / 1000)

            inside_x = self.game.arena_area["start_x"] < self.rect.x < self.game.arena_area["end_x"] - self.rect.width
            inside_y = self.game.arena_area["start_y"] < self.rect.y < self.game.arena_area["end_y"] - self.rect.height
            if inside_x and inside_y and self.velocity == [0, 0]:
                self.status = None

        elif self.status == "roll":
            # self.action =
            self.loop_action = True
            self.charge["roll"] += ms_per_loop
            if self.facing == 0:
                self.rect.y -= 100 * self.game.screen_scale * (ms_per_loop / 1000)
            elif self.facing == 2:
                self.rect.y += 100 * self.game.screen_scale * (ms_per_loop / 1000)
            elif self.facing == 1:
                self.rect.x -= 100 * self.game.screen_scale * (ms_per_loop / 1000)
            else :
                self.rect.x += 100 * self.game.screen_scale * (ms_per_loop / 1000)
            if self.charge["roll"] >= self.player_behavior["roll"]["charge_time"]:
                self.charge["roll"] = 0
                self.status = None
            check1_x, check1_y, hit_wall, wall_dir = Config.check_boundary(self, self.game.arena_area)
            if hit_wall is True and wall_dir == self.facing:
                self.status = "bounce"
                if self.facing in [1, 3]:
                    if self.facing == 1:
                        velocity_x = 200
                        velocity_y = -150
                    else:
                        velocity_x = -200
                        velocity_y = -150
                else:
                    velocity_x = 0
                    if self.facing == 0:
                        velocity_y = 350
                    else:
                        velocity_y = -350
                self.velocity = [velocity_x, velocity_y]
                self.cooldown["bounce"] = 128

    def life_check(self):
        if self.health <= 0:
            self.action = "death"
        if self.action == "death" and self.frame_animation == self.sprites_key["death"][self.facing][0] - 1:
            self.death = True

    def player_on_entities(self):
        for each_one in self.game.entities_group:
            if each_one != self:
                overlay = Config.check_overlay(each_one, self)
                if overlay is True and self.cooldown["bounce"]==0:
                    self.status = "bounce"
                    if self.facing in [1, 3]:
                        if self.facing == 1:
                            velocity_x = 50
                            velocity_y = -30
                        else:
                            velocity_x = -50
                            velocity_y = -30
                    else:
                        velocity_x = 0
                        if self.facing == 0:
                            velocity_y = 70
                        else:
                            velocity_y = -70
                    self.velocity = [velocity_x, velocity_y]

    def player_key_handle(self, event):
        move_pos = [0,0]

        # JUMP OUT FIRST
        if self.action in ["hurt","enter_arena"] or self.death is  True:
            return [0,0]
        if event.is_keypress(pygame.K_SPACE):
            self.roll()
            return [0,0]

        if self.action not in ["attack1",'attack2']:
            if event.is_keypress(pygame.K_w):
                self.facing = 0
            elif event.is_keypress(pygame.K_a):
                self.facing = 1
            elif event.is_keypress(pygame.K_s):
                self.facing = 2
            elif event.is_keypress(pygame.K_d):
                self.facing = 3

        keys = pygame.key.get_pressed()
        if self.facing == 3:
            if keys[pygame.K_a]:
                move_pos[0] = -1
            if keys[pygame.K_d]:
                move_pos[0] = 1
        elif self.facing == 1:
            if keys[pygame.K_d]:
                move_pos[0] = 1
            if keys[pygame.K_a]:
                move_pos[0] = -1
        else :
            if keys[pygame.K_a]:
                move_pos[0] -= 1
            if keys[pygame.K_d]:
                move_pos[0] += 1

        if self.facing == 2:
            if keys[pygame.K_w]:
                move_pos[1] = -1
            if keys[pygame.K_s]:
                move_pos[1] = 1
        elif self.facing == 0:
            if keys[pygame.K_s]:
                move_pos[1] = 1
            if keys[pygame.K_w]:
                move_pos[1] = -1
        else :
            if keys[pygame.K_w]:
                move_pos[1] -= 1
            if keys[pygame.K_s]:
                move_pos[1] += 1

        if move_pos == [1,0]:
            self.facing = 3
        elif move_pos == [-1,0]:
            self.facing = 1
        elif move_pos == [0,1]:
            self.facing = 2
        elif move_pos == [0,-1]:
            self.facing = 0

        if keys[pygame.K_LSHIFT]:
            self.frame_animation = 1
            self.image = self.animation['idle'][self.facing][self.frame_animation]

        if self.action not in ["attack1","attack2"]:
            if event.mouse_click(1) and self.cooldown["attack1"] <= 0:
                self.frame_animation = 0
                self.action = "attack1"
                self.atk_pos = event.mouse_position
            elif event.mouse_click(3) and self.cooldown["attack2"] <= 0:
                self.frame_animation = 0
                self.action = "attack2"
                self.atk_pos = event.mouse_position

        return move_pos

    def attack(self, atk_group):
        if self.action == 'attack1':
            if self.frame_animation == len(self.animation[self.action][self.facing]) :
                atk = Attack("melee", self, self.player_behavior["attack1"]["damage"] ,
                             (50, 50), self.atk_pos, direction_type=2)
                atk_group.add(atk)

                # self.direction = atk.atk_dir
                self.cooldown["attack1"] = self.player_behavior["attack1"]["cooldown"]
                self.action = 'idle'
                self.atk_pos = (0, 0)
        elif self.action == 'attack2':
            if self.frame_animation == len(self.animation[self.action][self.facing])-2 :
                atk = Attack("melee", self, self.player_behavior["attack2"]["damage"] ,
                             (30, 30), self.atk_pos)
                atk_group.add(atk)
                # self.direction = atk.atk_dir
                # RESET VALUE
                self.cooldown["attack2"] = self.player_behavior["attack2"]["cooldown"]
                self.action = 'idle'
                self.atk_pos = (0,0)
                if self.facing == 0:
                    self.rect.y -= 2 * self.game.screen_scale
                elif self.facing == 2:
                    self.rect.y += 2 * self.game.screen_scale
                elif self.facing == 1:
                    self.rect.x -= 2 * self.game.screen_scale
                else :
                    self.rect.x += 2 * self.game.screen_scale

    def movement(self, move_pos, ms_per_loop):
        self.old_position = (self.rect.x, self.rect.y)

        self.velocity[0] += self.acceleration * move_pos[0]
        self.velocity[1] += self.acceleration * move_pos[1]
        total_speed = math.hypot(self.velocity[0], self.velocity[1])
        if total_speed > self.max_velocity:
            scale_down = self.max_velocity/ total_speed
            self.velocity[0] *= scale_down
            self.velocity[1] *= scale_down

        for i in range(2):
            if move_pos[i] == 0:
                if self.velocity[i] > 0:
                    self.velocity[i] -= self.deceleration
                    if self.velocity[i] < 0:
                        self.velocity[i] = 0
                elif self.velocity[i] < 0:
                    self.velocity[i] += self.deceleration
                    if self.velocity[i] > 0:
                        self.velocity[i] = 0

        self.rect.x += self.velocity[0] * self.game.screen_scale * (ms_per_loop/1000)
        self.rect.y += self.velocity[1] * self.game.screen_scale * (ms_per_loop/1000)

        # Reset value when it exceeds boundaries
        check1_x, check1_y, hit_wall, wall_dir = Config.check_boundary(self, self.game.arena_area)
        self.rect.x, self.rect.y = Config.entities_overlay(self, (check1_x, check1_y),
                                                                 self.old_position)

    def roll(self):
        if self.cooldown["roll"] <= 0:
            self.status = "roll"


    def load_sprite(self, sprites_key):
        player_sprite_sheet = SpriteHandler(pygame.image.load(self.sprite_dir))
        self.animation = player_sprite_sheet.pack_sprite(sprites_key, self.game.screen_scale)
        self.size = self.game.screen_scale * sprites_key["idle"][0][3]
        self.animated()
        self.rect = self.image.get_rect()