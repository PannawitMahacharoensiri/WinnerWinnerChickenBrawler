import math
import random

import pygame
from Sprite_handle import *
from Attack import Attack
from config import Config

class Player(pygame.sprite.Sprite):
    # speed relate
    # max_velocity = 4
    # acceleration = 0.2
    # deceleration_ratio = 0.4
    """
    Sprites key index:
    1 is how long the frame
    2 is row 
    3 is column 
    4,5 is w,h_area of sprite
    """
    sprites_key = {"idle": [[2, 0, 0, 16, 16], [2, 2, 0, 16, 16], [2, 4, 0, 16, 16], [2, 6, 0, 16, 16]],
                   "walk": [[4, 0, 1, 16, 16], [4, 4, 1, 16, 16], [4, 8, 1, 16, 16], [4, 12, 1, 16, 16]],
                   "attack1": [[4, 0, 1, 16, 16], [4, 4, 1, 16, 16], [4, 8, 1, 16, 16], [4, 12, 1, 16, 16]],
                   "attack2": [[4, 0, 1, 16, 16], [4, 4, 1, 16, 16], [4, 8, 1, 16, 16], [4, 12, 1, 16, 16]],
                   "hurt": [[2, 0, 2, 16, 16], [2, 0, 2, 16, 16], [2, 0, 2, 16, 16], [2, 0, 2, 16, 16]],
                   "death": [[6, 0, 3, 16, 16], [6, 0, 3, 16, 16], [6, 0, 3, 16, 16], [6, 0, 3, 16, 16]]}

    def __init__(self, position, game, name='Player',health=100.0):
        super().__init__()
        # Animation related
        self.game = game
        self.name = name
        self.health = 1
        self.sprite_dir = "sprites\\Walk_substitute2.png"
        self.size = self.game.screen_scale
        self.status = None
        self.image = None
        self.rect = None

        self.max_velocity = 60 #when screen scale = 1 run 60 pixel per second
        self.acceleration = 3
        self.deceleration_ratio = 6

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

        ### MANUAL UPDATE SIZE
        # self.rect.width = 50
        # self.rect.height = 50
        self.old_position = (0,0)
        self.atk_pos = (0, 0)
        self.rect.center = (self.size/2, position[1] // 2)
        # self.rect.y = position[1]//2

        self.velocity = [0,0]
        self.cooldown = {"hurt": 0}
        self.charge = {"bounce":0}

    def load_sprite(self, sprites_key):
        player_sprite_sheet = SpriteHandler(pygame.image.load(self.sprite_dir))
        self.animation = player_sprite_sheet.pack_sprite(sprites_key, self.game.screen_scale)
        self.size = self.game.screen_scale * sprites_key["idle"][0][3]
        self.animated()
        self.rect = self.image.get_rect()

    def health_reduce(self, bullet_damage):
        # only decrese health when not dead
        if self.health > 0:
            self.health -= bullet_damage
            self.action = "hurt"
            self.cooldown["hurt"] = 5
            self.frame_animation = 0

    def update(self, frame, atk_group, event=None):

        self.frame_update(frame)
        self.player_on_entities()
        self.life_check()
        move_pos = self.player_key_handle(event)
        self.status_update(frame)
        if self.action not in ["attack1","attack2","hurt", "death"]:
            if move_pos != [0,0] or self.velocity != [0,0]:
                self.action = "walk"
                self.loop_action = True
                self.movement(move_pos)
        self.attack(atk_group)
        self.animated()

    def frame_update(self, frame):
        if self.death is False:
            for keys,values in self.cooldown.items():
                if values > 0:
                    self.cooldown[keys] -= frame
            self.frame_animation += frame
            self.loop_action = False

    def status_update(self, frame):
        if self.death is True:
            return

        if self.status == "bounce":
            self.charge[self.status] += frame
            self.action = "hurt"
            self.loop_action = True
            new_velocity  = Config.bounce(self.charge[self.status], velocity= self.velocity, facing= self.facing, size= self.size)
            self.rect.x += new_velocity[0] * Config.dt_per_second * self.game.screen_scale
            self.rect.y += new_velocity[1] * Config.dt_per_second * self.game.screen_scale
            valid_x, valid_y, hit_wall, wall_dir = Config.check_boundary(self, self.game.screen_info, self.game.screen_start)
            if new_velocity[0] == 4:
                print(frame)
            self.rect.x = valid_x
            self.rect.y = valid_y
            if self.charge[self.status] == 2:
                self.charge[self.status] = 0
                self.status = None

    def life_check(self):
        if self.health <= 0:
            self.action = "death"

        if self.action == "death" and self.frame_animation == self.sprites_key["death"][self.facing][0] - 1:
            self.death = True

    def player_on_entities(self):
        for each_one in self.game.entities_group:
            if each_one != self:
                overlay = Config.check_overlay(each_one, self)
                if overlay is True and self.status != "bounce":
                    self.velocity = [0,0]
                    self.status = "bounce"

    def player_key_handle(self, event):
        move_pos = [0,0]

        # JUMP OUT FIRST
        if self.status == "bounce" or self.death is  True:
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
            if event.mouse_click(1):
                self.frame_animation = 0
                self.action = "attack1"
                self.atk_pos = event.mouse_position
            elif event.mouse_click(3):
                self.frame_animation = 0
                self.action = "attack2"
                self.atk_pos = event.mouse_position

        return move_pos

    def attack(self, atk_group):
        if self.action == 'attack1':
            if self.frame_animation == len(self.animation[self.action][self.facing]) :
                atk = Attack("bullet", self, 200 ,(10, 10), self.atk_pos, direction_type=2)
                atk_group.add(atk)
                # self.direction = atk.atk_dir
                # RESET VALUE
                self.action = 'idle'
                self.atk_pos = (0, 0)
        elif self.action == 'attack2':
            if self.frame_animation == len(self.animation[self.action][self.facing])-2 :
                atk = Attack("global", self, 7 ,(2, 2), self.atk_pos)
                atk_group.add(atk)
                # self.direction = atk.atk_dir
                # RESET VALUE
                self.action = 'idle'
                self.atk_pos = (0,0)

    def movement(self, move_pos):
        self.old_position = (self.rect.x, self.rect.y)
        if move_pos != [0,0]:
            if (abs(self.velocity[0])+self.acceleration >= self.max_velocity or
            abs(self.velocity[1])+self.acceleration >= self.max_velocity):
                limit_velo = self.max_velocity - self.acceleration
                velo_x = self.velocity[0]
                velo_y = self.velocity[1]

                if self.velocity[0] > limit_velo:
                    velo_x = limit_velo
                elif self.velocity[0] < - limit_velo:
                    velo_x = - limit_velo
                if self.velocity[1] > limit_velo:
                    velo_y = limit_velo
                elif self.velocity[1] < - limit_velo:
                    velo_y = - limit_velo
                self.velocity = [velo_x, velo_y]
            self.velocity[0] += self.acceleration * move_pos[0]
            self.velocity[1] += self.acceleration * move_pos[1]

        if 0 in move_pos :
            if move_pos[0] == 0:
                if self.velocity[0] > 0:
                    self.velocity[0] -= self.velocity[0] * self.deceleration_ratio * Config.dt_per_second * self.game.screen_scale
                else :
                    self.velocity[0] += self.velocity[0] * self.deceleration_ratio * -1 * Config.dt_per_second * self.game.screen_scale
                if abs(self.velocity[0]) <= 0.01:
                    self.velocity[0] = 0
            if move_pos[1] == 0:
                if self.velocity[1] > 0:
                    self.velocity[1] -= self.velocity[1] * self.deceleration_ratio * Config.dt_per_second * self.game.screen_scale
                else :
                    self.velocity[1] += self.velocity[1] * self.deceleration_ratio * -1 * Config.dt_per_second * self.game.screen_scale
                if abs(self.velocity[1]) <= 0.01:
                    self.velocity[1] = 0
        self.rect.x += self.velocity[0] * self.game.screen_scale * Config.dt_per_second
        self.rect.y += self.velocity[1] * self.game.screen_scale * Config.dt_per_second

        # Reset value when it exceeds boundaries
        check1_x, check1_y, hit_wall, wall_dir = Config.check_boundary(self, self.game.screen_info, self.game.screen_start)
        self.rect.x, self.rect.y = Config.entities_overlay(self, (check1_x, check1_y),
                                                                 self.old_position)

    def roll(self):
        if self.facing == 0:
            self.rect.y -= 100
        elif self.facing  == 1:
            self.rect.x -= 100
        elif self.facing == 2:
            self.rect.y += 100
        elif self.facing == 3:
            self.rect.x += 100
        check1_x, check1_y, hit_wall, wall_dir = Config.check_boundary(self, self.game.screen_info, self.game.screen_start)
        if hit_wall is True and wall_dir == self.facing:
            self.status = "bounce"
            self.velocity[0] *= -1
            self.velocity[1] *= -1

    def animated(self):
        if self.death is False:
            if self.frame_animation > len(self.animation[self.action][self.facing])-1:
                self.frame_animation = 0
                if self.loop_action is False:
                    self.action = "idle"
        self.image = self.animation[self.action][self.facing][self.frame_animation]