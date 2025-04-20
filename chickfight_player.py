import random

import pygame
from Sprite_handle import *
from Attack import Attack

class Player(pygame.sprite.Sprite):
    # speed relate
    max_velocity = 4
    acceleration = 0.2
    deceleration_ratio = 0.4

    def __init__(self, position, name='Player',health=100.0):
        super().__init__()
        # Animation related
        self.health = health
        self.sprite_dir = 'sprites\\Walk_substitute2.png'
        self.size = 5
        self.status = None

        self.frame_animation = 0
        self.action = 'idle'
        self.direction = 0

        self.animation = {}
        self.load_sprite()

        self.image = self.animation['idle'][self.direction][self.frame_animation] ## Pygame Surface
        self.rect = self.image.get_rect() # function of pygame.Surface # get hit box base on picture -> may still do the same
        # self.rect = pygame.Rect(0,0,20,20)
        # print(self.rect)

        ### MANUAL UPDATE SIZE
        # self.rect.width = 50
        # self.rect.height = 50

        self.name = name
        self.rect.center = (0, position[1] // 2) # get rect from pygame.sprite.Sprite
        self.rect.x = 0

        # self.rect.y = position[1]//2

        self.velocity = [0,0]
        self.atk_pos = (0,0)

    def load_sprite(self):
        player_sprite_sheet = SpriteHandler(pygame.image.load(self.sprite_dir))

        """
        1 is how long the frame
        2 is row 
        3 is column 
        4,5 is w,h_area of picture
        """
        sprites_key = {"idle":[[2,0,0,16,16],[2,2,0,16,16],[2,4,0,16,16],[2,6,0,16,16]],
                        "walk":[[4,0,1,16,16],[4,4,1,16,16],[4,8,1,16,16],[4,12,1,16,16]],
                        "attack1":[[4,0,1,16,16],[4,4,1,16,16],[4,8,1,16,16],[4,12,1,16,16]],
                        "attack2":[[4,0,1,16,16],[4,4,1,16,16],[4,8,1,16,16],[4,12,1,16,16]],
                        "hurt":[[4,0,1,16,16],[4,4,1,16,16],[4,8,1,16,16],[4,12,1,16,16]]}

        self.animation = player_sprite_sheet.pack_sprite(sprites_key, self.size)

        ## REUSE CONTAINTER FOR LATER FUNCTION
        self.size *= sprites_key["idle"][0][4]

    """
    Direction :
        0 : NORTH
        1 : WEST, LEFT
        2 : SOUTH
        3 : EAST, RIGHT
    """

    def update(self, frame, atk_group, event=None):

        self.frame_animation += frame

        move_pos = [0,0]
        # pygame.KEYDOWN
        if event.is_keypress(pygame.K_SPACE):
            self.roll()
            return
        if event.is_keypress(pygame.K_0):
            self.action = "idle"
            return

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
            if self.action == "idle" :
                self.action = "walk"
            # self.next_action = "walk"
        if keys[pygame.K_d]:
            move_pos[0] = 1
            if self.action == "idle" :
                self.action = "walk"
        if keys[pygame.K_w]:
            move_pos[1] = -1
            if self.action == "idle" :
                self.action = "walk"
        if keys[pygame.K_s]:
            move_pos[1] = 1
            if self.action == "idle" :
                self.action = "walk"
        if keys[pygame.K_LSHIFT]:
            self.frame_animation = 1
            # self.size = 200
            self.image = self.animation['idle'][self.direction][self.frame_animation]
            # self.image = pygame.transform.scale(self.image, (self.size,self.size))

        if self.action == "walk":
            self.move(move_pos)

        if event.mouse_click(1):
            if self.action != "attack1":
                self.frame_animation = 0
            """set frame when click"""
            self.action = "attack1"
            self.atk_pos = event.mouse_position
        elif event.mouse_click(3):
            if self.action != "attack2":
                self.frame_animation = 0
            self.action = "attack2"
            self.atk_pos = event.mouse_position

        # if self.velocity == [0,0]:
        #     self.action = 'idle'
        self.attack(atk_group)
        self.animated()
    # def keyboard_input(self):
    #     move_pos = [0,0]
    #     # pygame.KEYDOWN
    #     if event.is_keypress(pygame.K_SPACE):
    #         self.roll()
    #         return
    #     if event.is_keypress(pygame.K_0):
    #         self.action = "idle"
    #         return
    #
    #     if event.is_keypress(pygame.K_w):
    #         self.direction = 0
    #     elif event.is_keypress(pygame.K_a):
    #         self.direction = 1
    #     elif event.is_keypress(pygame.K_s):
    #         self.direction = 2
    #     elif event.is_keypress(pygame.K_d):
    #         self.direction = 3
    #
    #     keys = pygame.key.get_pressed()
    #     if keys[pygame.K_a]:
    #         move_pos[0] = -1
    #         if self.action == "idle" :
    #             self.action = "walk"
    #         # self.next_action = "walk"
    #     if keys[pygame.K_d]:
    #         move_pos[0] = 1
    #         if self.action == "idle" :
    #             self.action = "walk"
    #     if keys[pygame.K_w]:
    #         move_pos[1] = -1
    #         if self.action == "idle" :
    #             self.action = "walk"
    #     if keys[pygame.K_s]:
    #         move_pos[1] = 1
    #         if self.action == "idle" :
    #             self.action = "walk"
    #     if keys[pygame.K_LSHIFT]:
    #         self.frame_counter = 1
    #         # self.size = 200
    #         self.image = self.animation['idle'][self.direction][self.frame_counter]
    #         # self.image = pygame.transform.scale(self.image, (self.size,self.size))
    #
    #     if self.action == "walk":
    #         self.move(move_pos)

    def animated(self):
        # update self.image
        # print(self.action )
        if self.check_end_animated():
            self.action =  'idle'
        else :
            self.image = self.animation[self.action][self.direction][self.frame_animation]

    def health_reduce(self, bullet_damage):
        self.health -= bullet_damage
        self.action = "hurt"



    def check_end_animated(self):
        if self.frame_animation >= len(self.animation[self.action][self.direction]):
            self.frame_animation = 0
            return True
        return False

    def move(self, move_pos):
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

    def attack(self, atk_group):
        if self.action == 'attack1':
            if self.frame_animation == len(self.animation[self.action][self.direction]) :
                atk = Attack("melee", self, 7 ,(self.rect.width, self.rect.height), self.atk_pos)
                atk_group.add(atk)
                # self.direction = atk.atk_dir
                # RESET VALUE
                self.action = 'idle'
                self.atk_pos = (0, 0)
        elif self.action == 'attack2':
            if self.frame_animation == len(self.animation[self.action][self.direction])-2 :
                atk = Attack("global", self, 7 ,(self.rect.width/3, self.rect.height/3), self.atk_pos)
                atk_group.add(atk)
                # self.direction = atk.atk_dir
                # RESET VALUE
                self.action = 'idle'
                self.atk_pos = (0,0)

    def roll(self):
        if self.direction == 0:
            self.rect.y -= 100
        elif self.direction  == 1:
            self.rect.x -= 100
        elif self.direction == 2:
            self.rect.y += 100
        elif self.direction == 3:
            self.rect.x += 100