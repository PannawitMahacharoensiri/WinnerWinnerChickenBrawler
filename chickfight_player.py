import random

import pygame
from Sprite_handle import *

class Player(pygame.sprite.Sprite):
    max_velocity = 4
    acceleration = 0.2
    deceleration_ratio = 0.4
    player = SpriteHandler(pygame.image.load('sprites\demo_sheet.png'))
    # temporary probably all change when really got the sprite sheet

    # image = pygame.image.load('jim.png')
    def __init__(self, position, name='BOY'):
        super().__init__()
        self.last_update = pygame.time.get_ticks()
        self.frame_counter = 0
        self.current_frame = 0
        self.animation_step = [(0,2),(2,4) ] # idle up-down , idle swap head
        self.choose = random.choice(self.animation_step)


        self.size = 5
        self.image = Player.player.read_sprite_sheet(self.frame_counter,16,16,self.size)
        self.rect = self.image.get_rect()
        self.name = name
        self.rect.center = (position[0] // 2,position[1] // 2)#(0, position[1] // 2)
        self.velocity = [0,0]
        # self.max_velocity = 1
        # self.acceleration = 0.2
        # self.face_state = 'left'


    def update(self, event=None):

        move_pos = [0,0]
        if event.is_keypress(pygame.K_SPACE):
            self.roll()
            return

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
            self.image = pygame.transform.scale(self.image, (200,200))

        if move_pos == [0,0]:
            animation_delay = 450
            current_time = pygame.time.get_ticks()


            if current_time - self.last_update > animation_delay:
                self.last_update = current_time
                self.frame_counter += 1
                print(self.choose)
                if self.frame_counter >= self.choose[1]:
                    self.frame_counter = 0
                    self.image = Player.player.read_sprite_sheet(self.frame_counter, 16, 16, self.size)
                    self.choose = random.choice(self.animation_step)
                    self.frame_counter = self.choose[0]
                else:
                    self.image = Player.player.read_sprite_sheet(self.frame_counter, 16, 16, self.size)


        self.move(move_pos)

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


    def draw_player(self, _window):
        _window.blit(self.image, (self.pos_x, self.pos_y))

    def roll(self):
        self.rect.x += 150