from Sprite_handle import *
from config import Config
from Attack import Attack
import pygame
import math

class Enemy(pygame.sprite.Sprite):
    def __init__(self, heath=100):
        super().__init__()
        self.health = heath
        self.before_health = self.health
        self.image = None
        self.rect = None

        self.size = 1
        self.action = "idle"
        self.direction = 0
        self.frame_animation = 0
        self.animation = set()
        self.atk_pos = (0,0)
        self.status = None

    def load_sprite(self, sprites_key):
        Enemy_sprite_sheet = SpriteHandler(pygame.image.load(self.sprite_dir))
        self.animation = Enemy_sprite_sheet.pack_sprite(sprites_key, self.game.screen_scale)
        self.size = self.game.screen_scale * sprites_key["idle"][0][3]
        if self.frame_animation > len(self.animation[self.action][self.direction])-1:
            self.frame_animation = 0
        self.image = self.animation[self.action][self.direction][self.frame_animation]
        self.rect = self.image.get_rect()

    def health_reduce(self, bullet_damage):
        self.health -= bullet_damage
        self.action = "hurt"
        self.frame_animation = 0

    def animated(self):
        if self.frame_animation > len(self.animation[self.action][self.direction])-1:
            self.frame_animation = 0
            self.action = "idle"
        self.image = self.animation[self.action][self.direction][self.frame_animation]

class Dummy(Enemy):
    sprites_key = {"idle": [[1, 0, 0, 16, 16], [1, 0, 0, 16, 16], [1, 0, 0, 16, 16], [1, 0, 0, 16, 16]],
                   "hurt" : [[1, 1, 1, 16, 16],[2, 1, 1, 16, 16],[2, 1, 1, 16, 16],[2, 1, 1, 16, 16]]}

    def __init__(self, position, game):
        super().__init__()
        self.sprite_dir = 'sprites\\Dummy_demo.png'
        self.game = game
        self.health = 0
        self.name = "__DUMMY08"
        self.cooldown = {"hurt": 0}
        self.load_sprite(Dummy.sprites_key)
        self.rect.x = position[0]
        self.rect.y = position[1]

    def update(self, frame, atk_group, event=None):
        self.animated()
        if self.cooldown["hurt"] > 0:
            self.cooldown["hurt"] -= frame
        self.frame_animation += frame

class Boss1(Enemy):
    sprites_key = {"idle": [[4, 0, 0, 16, 16], [4, 0, 0, 16, 16], [4, 0, 0, 16, 16], [4, 0, 0, 16, 16]],
                   "walk": [[4, 0, 1, 16, 16], [4, 0, 1, 16, 16], [4, 0, 1, 16, 16], [4, 0, 1, 16, 16]],
                   "attack1": [[4, 0, 0, 16, 16], [4, 0, 0, 16, 16], [4, 0, 0, 16, 16], [4, 0, 0, 16, 16]],
                   "attack2": [[4, 0, 0, 16, 16], [4, 0, 0, 16, 16], [4, 0, 0, 16, 16], [4, 0, 0, 16, 16]],
                   "hurt" : [[1, 0, 1, 16, 16],[1, 1, 1, 16, 16],[1, 2, 1, 16, 16],[1, 3, 1, 16, 16]]}

                   # "attack1": [[4, 0, 1, 16, 16], [4, 4, 1, 16, 16], [4, 8, 1, 16, 16], [4, 12, 1, 16, 16]],
                   # "attack2": [[4, 0, 1, 16, 16], [4, 4, 1, 16, 16], [4, 8, 1, 16, 16], [4, 12, 1, 16, 16]]}

    ## ONLY FOR READ AND NOT CHANGE THE VALUE SO I NOT PUT IT IN ATTRIBUTE
    attack_move = {"attack1":{"damage":5, "hitbox":(3,3)}, "attack2":{"damage":20, "hitbox":(20,20)}}

    def __init__(self, position, game, name):
        super().__init__()
        self.game = game
        self.name = name
        self.sprite_dir = 'sprites\\Boss1_substitute.png'
        self.size = self.game.screen_scale
        self.load_sprite(Boss1.sprites_key)
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.cooldown = {"hurt":0, "attack1":0, "attack2":0}
        self.speed = 2

    def update_by_frame(self, frame):
        for keys,values in self.cooldown.items():
            if values > 0:
                self.cooldown[keys] -= frame
        self.frame_animation += frame

    def update(self, frame, atk_group, event=None):
        # separate frame loop and it behaviour
        self.update_by_frame(frame)
        self.animated()

        # if self already action return out ? -> make enemy stop when attack
        if self.action not in [Boss1.attack_move.keys(),"hurt"]:
            # update action choose ...
            self.behaviour(frame)
        self.attack(atk_group)



    # WHY YOU NOT CALL IN THE BEHAVIOUR CAUSE THEIR ARE SOME DELAY BETWEEN COMMAND TO ATTACK AND REAL BUILD ATK HITBOX
    def attack(self, atk_group):
            # FOR SIMPLE ATTACK
        if self.action == "attack1" and self.frame_animation == 1 :
            atk = Attack("melee", self, Boss1.attack_move["attack1"]["damage"], Boss1.attack_move["attack1"]["hitbox"], self.atk_pos)
            atk_group.add(atk)
            self.action = "idle"
            self.atk_pos = (0,0)
            self.frame_animation = 0
            self.cooldown["attack1"] = 5
        elif self.action == "attack2":
            ## RELOAD SET SPEED "A" FRAME
            self.atk_pos = self.rect.center
            atk = Attack("melee", self, Boss1.attack_move["attack2"]["damage"], Boss1.attack_move["attack2"]["hitbox"], self.atk_pos)
            atk_group.add(atk)
            self.atk_pos = (0,0)
            if self.cooldown["attack2"] == 0:
                self.frame_animation = 0
                self.cooldown["attack2"] = 30
            if self.frame_animation == len(self.animation[self.action][self.direction]) - 1:
                self.speed = 2
    def movement(self):
        player_x,player_y = self.game.player.rect.center

        dx = player_x - self.rect.center[0]
        dy = player_y - self.rect.center[1]
        lenght = math.sqrt(dx**2 + dy**2)

        if lenght > 0:
            before_move = (self.rect.x, self.rect.y)
            self.rect.center = (self.rect.center[0] + (dx/lenght) * self.speed ,
                                self.rect.center[1] + (dy/lenght) * self.speed)
            self.rect.x, self.rect.y, hit_wall = Config.check_boundary(self, self.game.screen_info, self.game.screen_start, before_move)
        return lenght


    def behaviour(self, frame):

        # Move enemy and also get distance from player to enemy use for choose attack move later
        lenght = self.movement()
        # Track the health value because I check health round by round
        self.before_health = self.health

        # Not calculate the behaviour unless it already change 1 frame (1frame = 1frame_delay = 300ms)
        if frame != 1:
            return
        # check behaviour for attack 1
        if lenght >= 350 and self.cooldown["attack2"]==0:
            self.action = "attack2"
            self.speed = 7
        elif lenght <= self.size/2 + Boss1.attack_move["attack1"]["hitbox"][0] and self.cooldown["attack1"]==0:
            self.atk_pos = self.game.player.rect.center
            self.action = "attack1"




