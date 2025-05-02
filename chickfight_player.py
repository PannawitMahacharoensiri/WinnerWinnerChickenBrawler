import random

import pygame
from Sprite_handle import *
from Attack import Attack
from config import Config

class Player(pygame.sprite.Sprite):
    # speed relate
    max_velocity = 4
    acceleration = 0.2
    deceleration_ratio = 0.4
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
                   "hurt": [[1, 0, 2, 16, 16], [1, 0, 2, 16, 16], [1, 0, 2, 16, 16], [1, 0, 2, 16, 16]]}

    def __init__(self, position, game, name='Player',health=100.0):
        super().__init__()
        # Animation related
        self.game = game
        self.name = name
        self.health = health
        self.sprite_dir = "sprites\\Walk_substitute2.png"
        self.size = self.game.screen_scale
        self.status = None
        self.image = None
        self.rect = None

        self.frame_animation = 0
        self.action = 'idle'
        self.loop_action = False
        self.direction = 0
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
        self.rect.center = (20, position[1] // 2)
        # self.rect.y = position[1]//2

        self.velocity = [0,0]
        self.atk_pos = (0,0)
        self.cooldown = {"hurt": 0}

    def load_sprite(self, sprites_key):
        player_sprite_sheet = SpriteHandler(pygame.image.load(self.sprite_dir))
        self.animation = player_sprite_sheet.pack_sprite(sprites_key, self.game.screen_scale)
        self.size = self.game.screen_scale * sprites_key["idle"][0][3]
        self.animated()
        self.rect = self.image.get_rect()

    def health_reduce(self, bullet_damage):
        self.health -= bullet_damage
        self.action = "hurt"
        self.frame_animation = 0

    def update(self, frame, atk_group, event=None):
        self.frame_update(frame)
        move_pos = self.player_key_handle(event)
        if self.action not in ["attack1","attack2"]:
            if move_pos != [0,0] or self.velocity != [0,0]:
                self.action = "walk"
                self.loop_action = True
                self.movement(move_pos)
        self.attack(atk_group)
        self.animated()

    def frame_update(self, frame):
        for keys,values in self.cooldown.items():
            if values > 0:
                self.cooldown[keys] -= frame
        self.frame_animation += frame
        self.loop_action = False

    def player_key_handle(self, event):
        move_pos = [0,0]

        # JUMP OUT FIRST
        if event.is_keypress(pygame.K_SPACE):
            self.roll()
            return [0,0]

        if self.action not in ["attack1",'attack2']:
            if event.is_keypress(pygame.K_w):
                self.direction = 0
            elif event.is_keypress(pygame.K_a):
                self.direction = 1
            elif event.is_keypress(pygame.K_s):
                self.direction = 2
            elif event.is_keypress(pygame.K_d):
                self.direction = 3

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            move_pos[0] = -1
        if keys[pygame.K_d]:
            move_pos[0] = 1
        if keys[pygame.K_w]:
            move_pos[1] = -1
        if keys[pygame.K_s]:
            move_pos[1] = 1

        if keys[pygame.K_LSHIFT]:
            self.frame_animation = 1
            self.image = self.animation['idle'][self.direction][self.frame_animation]

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
            if self.frame_animation == len(self.animation[self.action][self.direction]) :
                atk = Attack("bullet", self, 7 ,(10, 10), self.atk_pos, direction_type=2)
                atk_group.add(atk)
                # self.direction = atk.atk_dir
                # RESET VALUE
                self.action = 'idle'
                self.atk_pos = (0, 0)
        elif self.action == 'attack2':
            if self.frame_animation == len(self.animation[self.action][self.direction])-2 :
                atk = Attack("global", self, 7 ,(2, 2), self.atk_pos)
                atk_group.add(atk)
                # self.direction = atk.atk_dir
                # RESET VALUE
                self.action = 'idle'
                self.atk_pos = (0,0)

    def movement(self, move_pos):
        before_move = (self.rect.x, self.rect.y)
        if move_pos != [0,0]:
            if (abs(self.velocity[0])+self.acceleration >= Player.max_velocity or
            abs(self.velocity[1])+self.acceleration >= Player.max_velocity):
                max_velo = Player.max_velocity - Player.acceleration
                self.velocity[0] = max(-max_velo, min(self.velocity[0], max_velo))
                self.velocity[1] = max(-max_velo, min(self.velocity[1], max_velo))
            self.velocity[0] += self.acceleration * move_pos[0]
            self.velocity[1] += self.acceleration * move_pos[1]
        if 0 in move_pos :
            if move_pos[0] == 0:
                if self.velocity[0] > 0:
                    self.velocity[0] -= self.velocity[0] * Player.deceleration_ratio
                else :
                    self.velocity[0] += self.velocity[0] * Player.deceleration_ratio * -1
            if move_pos[1] == 0:
                if self.velocity[1] > 0:
                    self.velocity[1] -= self.velocity[1] * Player.deceleration_ratio
                else :
                    self.velocity[1] += self.velocity[1] * Player.deceleration_ratio * -1

        if abs(self.velocity[0])< 0.01:
            self.velocity[0] = 0
        if abs(self.velocity[1])< 0.01:
            self.velocity[1] = 0

        # USE VELOCITY TO MOVE CHARACTER
        # print(self.velocity)
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        # Reset value when it exceeds boundaries
        check1_x, check1_y, hit_wall = Config.check_boundary(self, self.game.screen_info, self.game.screen_start,
                                                             before_move)
        self.rect.x, self.rect.y = Config.check_entities_overlay(self, (check1_x, check1_y), before_move)

    def roll(self):
        if self.direction == 0:
            self.rect.y -= 100
        elif self.direction  == 1:
            self.rect.x -= 100
        elif self.direction == 2:
            self.rect.y += 100
        elif self.direction == 3:
            self.rect.x += 100

    def animated(self):
        if self.frame_animation > len(self.animation[self.action][self.direction])-1:
            self.frame_animation = 0
            if self.loop_action is False:
                self.action = "idle"
        self.image = self.animation[self.action][self.direction][self.frame_animation]