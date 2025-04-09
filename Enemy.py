from Sprite_handle import *
from config import *
import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, heath=100):
        super().__init__()
        self.health = heath
        self.size = 5
        self.action = "idle"
        self.direction = 0
        self.frame_counter = 0
        self.animation = set()

    def load_sprite(self, sprites_key):
        Enemy_sprite_sheet = SpriteHandler(pygame.image.load(self.sprite_dir))
        self.animation = Enemy_sprite_sheet.pack_sprite(sprites_key, self.size)


class Boss1(Enemy):
    sprites_key = {"idle": [[4, 0, 0, 16, 16], [4, 0, 0, 16, 16], [4, 0, 0, 16, 16], [4, 0, 0, 16, 16]],
                   "walk": [[4, 0, 1, 16, 16], [4, 0, 1, 16, 16], [4, 0, 1, 16, 16], [4, 0, 1, 16, 16]]}#,
                   # "attack1": [[4, 0, 1, 16, 16], [4, 4, 1, 16, 16], [4, 8, 1, 16, 16], [4, 12, 1, 16, 16]],
                   # "attack2": [[4, 0, 1, 16, 16], [4, 4, 1, 16, 16], [4, 8, 1, 16, 16], [4, 12, 1, 16, 16]]}

    def __init__(self,name, x,y):
        super().__init__()
        self.name = name
        self.sprite_dir = 'sprites\\Boss1_substitute.png'
        self.load_sprite(Boss1.sprites_key)
        self.image = self.animation[self.action][self.direction][self.frame_counter]
        self.rect = self.image.get_rect()
        self.rect.x = x#Config.screen_info[0]//2 - self.rect.width
        self.rect.y = y #Config.screen_info[1] //2


    def update(self, frame, atk_group, event=None):
        self.frame_counter += frame
        if self.frame_counter > len(self.animation[self.action][self.direction])-1:
            self.frame_counter = 0
        self.image = self.animation[self.action][self.direction][self.frame_counter]
