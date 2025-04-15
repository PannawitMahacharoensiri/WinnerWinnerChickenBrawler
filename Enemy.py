from Sprite_handle import *
from config import *
from Attack import Attack
import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, heath=100):
        super().__init__()
        self.health = heath
        self.size = 5
        self.action = "idle"
        self.direction = 0
        self.frame_animation = 0
        self.frame_behaviour = 0
        self.animation = set()
        self.atk_pos = (0,0)

    def load_sprite(self, sprites_key):
        Enemy_sprite_sheet = SpriteHandler(pygame.image.load(self.sprite_dir))
        self.animation = Enemy_sprite_sheet.pack_sprite(sprites_key, self.size)
        self.size *= self.sprites_key["idle"][0][4]


class Boss1(Enemy):
    sprites_key = {"idle": [[4, 0, 0, 16, 16], [4, 0, 0, 16, 16], [4, 0, 0, 16, 16], [4, 0, 0, 16, 16]],
                   "walk": [[4, 0, 1, 16, 16], [4, 0, 1, 16, 16], [4, 0, 1, 16, 16], [4, 0, 1, 16, 16]],
                   "attack": [[4, 0, 0, 16, 16], [4, 0, 0, 16, 16], [4, 0, 0, 16, 16], [4, 0, 0, 16, 16]]}#,
                   # "attack1": [[4, 0, 1, 16, 16], [4, 4, 1, 16, 16], [4, 8, 1, 16, 16], [4, 12, 1, 16, 16]],
                   # "attack2": [[4, 0, 1, 16, 16], [4, 4, 1, 16, 16], [4, 8, 1, 16, 16], [4, 12, 1, 16, 16]]}

    def __init__(self,name, x,y, game):
        super().__init__()
        self.name = name
        self.sprite_dir = 'sprites\\Boss1_substitute.png'
        self.load_sprite(Boss1.sprites_key)
        self.image = self.animation[self.action][self.direction][self.frame_animation]
        self.rect = self.image.get_rect()
        self.rect.x = x #Config.screen_info[0]//2 - self.rect.width
        self.rect.y = y #Config.screen_info[1] //2
        self.game = game
        self.cooldown = 0


    def update(self, frame, atk_group, event=None):
        # separate frame loop and it behaviour
        if self.cooldown > 0:
            self.cooldown -= frame

        self.frame_animation += frame
        self.frame_behaviour += frame

        self.behaviour()

        # Simple animation mechanic
        if self.frame_animation > len(self.animation[self.action][self.direction])-1:
            self.frame_animation = 0
        self.attack(atk_group)
        self.image = self.animation[self.action][self.direction][self.frame_animation]
        # print(self.action, self.frame_animation)

    def attack(self, atk_group):
        if self.action == "attack" and self.cooldown == 0:
            # if self.frame_animation == len(self.animation[self.action][self.direction])-2 :
            atk = Attack("melee", self, 5, (100/2,100/2), self.atk_pos)
            atk_group.add(atk)
            self.action = "idle"
            self.atk_pos = (0,0)
            self.frame_animation = 0
            self.cooldown = 10



    def behaviour(self):
        # print(self.game.player.rect.center)
        # print(self.rect.center[0] - self.size/2 - 50, self.rect.center[0] + self.size/2 + 50)
        # print((self.rect.center[0] - self.size/2 - 50 < self.game.player.rect.center[0] < self.rect.center[0] + self.size/2 + 50))

        if ( (self.rect.center[0] - self.size/2 - 100 < self.game.player.rect.center[0] < self.rect.center[0] + self.size/2 + 100) and
            (self.rect.center[1] - self.size/2 - 100 < self.game.player.rect.center[1] < self.rect.center[1] + self.size/2 + 100) ):
            self.atk_pos = self.game.player.rect.center
            self.action = "attack"
        # if self.rect.x > 0:
        #     self.rect.x -= 1
