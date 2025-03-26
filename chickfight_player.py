import random

import pygame
from Sprite_handle import *

class Player(pygame.sprite.Sprite):
    # speed relate
    max_velocity = 4
    acceleration = 0.2
    deceleration_ratio = 0.4

    def __init__(self, position, name='Player'):
        super().__init__()
        # Animation related

        self.sprite_dir = 'sprites\\test_extract.jpg'
        self.size = 5

        self.frame_counter = 0
        self.action = 'idle'
        # self.next_action = None
        self.direction = 0

        self.animation = {}
        self.load_sprite()

        self.image = self.animation['idle'][self.direction][self.frame_counter]
        self.rect = self.image.get_rect()
        self.name = name
        self.rect.center = (position[0] // 2,position[1] // 2) # get rect from pygame.sprite.Sprite
        self.velocity = [0,0]

    def load_sprite(self):
        player_sprite_sheet = SpriteHandler(pygame.image.load(self.sprite_dir))

        sprites_key = {"idle":[[2,0,0,16,16],[2,2,0,16,16]],
                          "walk":[[2,0,1,16,16],[2,2,1,16,16]]}

        self.animation = player_sprite_sheet.pack_sprite(sprites_key, self.size)


    def update(self, frame, event=None):
        self.frame_counter += frame

        move_pos = [0,0]
        # pygame.KEYDOWN
        if event.is_keypress(pygame.K_SPACE):
            self.roll()
            return
        if event.is_keypress(pygame.K_0):
            self.action = "idle"
            return

        if event.is_keypress(pygame.K_w):
            self.direction = 0
        elif event.is_keypress(pygame.K_a):
            self.direction = 1
        # elif event.is_keypress(pygame.K_s):
        #     self.direction = 2
        # elif event.is_keypress(pygame.K_d):
        #     self.direction = 3

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
            self.frame_counter = 1
            # self.size = 200
            self.image = self.animation['idle'][self.direction][self.frame_counter]
            # self.image = pygame.transform.scale(self.image, (self.size,self.size))

        if self.action == "walk":
            self.move(move_pos)
        # if self.velocity == [0,0]:
        #     self.action = 'idle'
        self.animated()


    def animated(self):
        # update self.image
        print(self.action )
        if self.check_end_animated():
            self.action =  'idle'
        else :
            self.image = self.animation[self.action][self.direction][self.frame_counter]



    def check_end_animated(self):
        if self.frame_counter >= len(self.animation[self.action][self.direction]):
            self.frame_counter = 0
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

    def roll(self):
        self.rect.x += 100