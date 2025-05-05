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
        self.loop_action = False

        self.facing = 0
        self.frame_animation = 0
        self.animation = set()
        self.atk_pos = (0,0)
        self.old_position = (0,0)
        self.status = None
        self.velocity = [0,0]
        self.length = 0

    def load_sprite(self, sprites_key):
        Enemy_sprite_sheet = SpriteHandler(pygame.image.load(self.sprite_dir))
        self.animation = Enemy_sprite_sheet.pack_sprite(sprites_key, self.game.screen_scale)
        self.size = self.game.screen_scale * sprites_key["idle"][0][3]
        self.animated()
        self.rect = self.image.get_rect()

    #reset charge time
    def health_reduce(self, bullet_damage):
        if self.action == "dash_attack":
            self.status = "bounce"
            self.velocity = [0,0]
        self.health -= bullet_damage
        self.action = "hurt"
        self.cooldown["hurt"] = 5
        self.frame_animation = 0

    def animated(self):
        if self.frame_animation > len(self.animation[self.action][self.facing])-1:
            self.frame_animation = 0
            if self.loop_action is False:
                self.action = "idle"
        self.image = self.animation[self.action][self.facing][self.frame_animation]

class Dummy(Enemy):
    sprites_key = {"idle": [[1, 0, 0, 16, 16], [1, 0, 0, 16, 16], [1, 0, 0, 16, 16], [1, 0, 0, 16, 16]],
                   "hurt" : [[1, 1, 1, 16, 16],[2, 1, 1, 16, 16],[2, 1, 1, 16, 16],[2, 1, 1, 16, 16]]}

    def __init__(self, position, game):
        super().__init__()
        self.sprite_dir = 'sprites\\Dummy_demo.png'
        self.game = game
        self.health = 1000
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

########################################################################################################################
########################################################################################################################

class Boss1(Enemy):
    sprites_key = {"idle": [[4, 0, 0, 16, 16], [4, 0, 0, 16, 16], [4, 0, 0, 16, 16], [4, 0, 0, 16, 16]],
                   "walk": [[4, 0, 1, 16, 16], [4, 0, 1, 16, 16], [4, 0, 1, 16, 16], [4, 0, 1, 16, 16]],
                   "attack1": [[4, 0, 0, 16, 16], [4, 0, 0, 16, 16], [4, 0, 0, 16, 16], [4, 0, 0, 16, 16]],
                   "attack2": [[4, 0, 0, 16, 16], [4, 0, 0, 16, 16], [4, 0, 0, 16, 16], [4, 0, 0, 16, 16]],
                   "dash_attack": [[4, 0, 0, 16, 16], [4, 0, 0, 16, 16], [4, 0, 0, 16, 16], [4, 0, 0, 16, 16]],
                   "charge_dash_attack": [[5, 0, 2, 16, 16], [5, 0, 2, 16, 16], [5, 0, 2, 16, 16], [5, 0, 2, 16, 16]],
                   "hurt" : [[1, 0, 1, 16, 16],[1, 1, 1, 16, 16],[1, 2, 1, 16, 16],[1, 3, 1, 16, 16]]}

    ## ONLY FOR READ AND NOT CHANGE THE VALUE SO I NOT PUT IT IN ATTRIBUTE
    attack_move = {"attack1":{"damage":5, "hitbox":(3,3), "cooldown":3},
                   "attack2":{"damage":20, "hitbox":(20,20), "cooldown":10},
                   "dash_attack":{"damage":20, "hitbox":(20,20), "cooldown":35, "charge_time":10, "speed":7}}

    def __init__(self, position, game, name):
        super().__init__()
        self.game = game
        self.name = name
        self.sprite_dir = 'sprites\\Boss1_substitute.png'
        self.size = self.game.screen_scale
        self.load_sprite(Boss1.sprites_key)
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.cooldown = {"hurt":0, "attack1":0, "attack2":0, "dash_attack":0}
        self.charge = {"charge_dash_attack":0, "bounce":0}

        self.normal_speed = 30 # 2 * 15
        self.speed = self.normal_speed


    def update(self, frame, atk_group, event=None):
        self.frame_update(frame)
        self.status_update(frame)
        if self.action not in [*self.cooldown.keys(),*self.charge.keys()]: #and self.status != "confuse"#[*Boss1.attack_move.keys() ,"hurt"]:
            self.behaviour(frame)

        self.attack(atk_group, frame)
        self.animated()

    def status_update(self, frame):
        if self.status == "bounce":
            self.charge[self.status] += frame
            self.action = "hurt"
            self.loop_action = True
            new_velocity = Config.bounce(self.charge[self.status], velocity=self.velocity, facing=self.facing, size=self.size)
            self.rect.x += new_velocity[0] * Config.dt_per_second * self.game.screen_scale
            self.rect.y += new_velocity[1] * Config.dt_per_second * self.game.screen_scale
            valid_x, valid_y, hit_wall, wall_dir = Config.check_boundary(self, self.game.screen_info, self.game.screen_start)
            self.rect.x = valid_x
            self.rect.y = valid_y
            if self.charge[self.status] == 2:
                self.charge[self.status] = 0
                self.status = None
                self.speed = self.normal_speed

    def frame_update(self, frame):
        for keys,values in self.cooldown.items():
            if values > 0:
                self.cooldown[keys] -= frame
        self.frame_animation += frame
        self.before_health = self.health
        self.loop_action = False
        ## ADD STATUS MECHANIC HEAR


    def behaviour(self, frame):
        length, dx, dy = Config.get_length(self.rect.center, self.game.player.rect.center)
        self.velocity = [dx/length, dy/length]

        if frame != 1:
            self.movement(length)
            return
        # check behaviour for attack 1
        if length >= 350 and self.cooldown["dash_attack"]==0:
            self.frame_animation = 0
            self.action = "charge_dash_attack"
            self.cooldown["dash_attack"] = Boss1.attack_move["dash_attack"]["cooldown"]
        ## ONE TIME THE ATTACK NOT FIRE DIAGONAL TURN OUT IT JUST ONLY TO FAR FROM IT LENGTH
        elif length <= self.size + Boss1.attack_move["attack1"]["hitbox"][0] and self.cooldown["attack1"]==0:
            self.frame_animation = 0
            self.atk_pos = self.game.player.rect.center
            self.action = "attack1"
            self.cooldown["attack1"] = Boss1.attack_move["attack1"]["cooldown"]
        else :
            self.movement(length)

    def movement(self, length):
        if length > (self.game.player.size + self.size)/2:
            self.loop_action = True
            if self.action != "walk":
                self.frame_animation = 0
            self.action = "walk"

            self.old_position = (self.rect.x, self.rect.y)
            self.rect.center = (self.rect.center[0] + ((self.velocity[0]) * self.speed * Config.dt_per_second * self.game.screen_scale),
                                self.rect.center[1] + ((self.velocity[1]) * self.speed * Config.dt_per_second * self.game.screen_scale))
            check1_x, check1_y, hit_wall, wall_dir = Config.check_boundary(self, self.game.screen_info, self.game.screen_start)
            self.rect.x, self.rect.y = Config.entities_overlay(self, (check1_x, check1_y),
                                                                     self.old_position)


    # WHY YOU NOT CALL IN THE BEHAVIOUR CAUSE THERE ARE SOME DELAY BETWEEN COMMAND TO ATTACK AND REAL BUILD ATK HITBOX
    def attack(self, atk_group, frame):

        if self.action == "attack1" and self.frame_animation == 1 :
            atk = Attack("melee", self, Boss1.attack_move["attack1"]["damage"], Boss1.attack_move["attack1"]["hitbox"], self.atk_pos)
            atk_group.add(atk)
            self.action = "idle"
            self.atk_pos = (0,0)
            self.frame_animation = 0

        elif self.action == "charge_dash_attack":
            self.loop_action = True
            if frame == 1:
                self.charge["charge_dash_attack"] += 1
            if self.charge["charge_dash_attack"] == Boss1.attack_move["dash_attack"]["charge_time"] - 1:
                self.charge["charge_dash_attack"] = 0
                self.action = "dash_attack"
                self.frame_animation = 0
                self.atk_pos = (self.game.player.rect.center[0] + (self.game.player.velocity[0] * 20 * Config.dt_per_second * self.game.screen_scale ) , #self.charge time * speed * screen scale * ???-> 5 * 2
                                self.game.player.rect.center[1] + (self.game.player.velocity[1] * 20 * Config.dt_per_second * self.game.screen_scale))
                length, dx, dy = Config.get_length(self.rect.center, self.atk_pos)
                self.velocity = [dx/length, dy/length]

        elif self.action == "dash_attack":
            self.speed = self.normal_speed * Boss1.attack_move["dash_attack"]["speed"]
            self.loop_action = True
            self.rect.center = (self.rect.center[0] + ((self.velocity[0]) * self.speed * Config.dt_per_second * self.game.screen_scale),
                                self.rect.center[1] + ((self.velocity[1]) * self.speed * Config.dt_per_second * self.game.screen_scale))
            check1_x, check1_y, hit_wall, wall_dir = Config.check_boundary(self, self.game.screen_info, self.game.screen_start)
            self.rect.x = check1_x
            self.rect.y = check1_y

            self.atk_pos = self.rect.center
            atk = Attack("melee", self, Boss1.attack_move["dash_attack"]["damage"],
                         [2,2], self.atk_pos,decay_time=1, direction_type=2)
            atk_group.add(atk)
            if hit_wall is True or self.action == "hurt":
                self.action = "hurt"
                self.frame_animation = 0
                self.status = "bounce"
                self.velocity[0] *= -1 * self.speed
                self.velocity[1] *= -1 * self.speed








