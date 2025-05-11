import random

from Sprite_handle import *
from config import Config
from Attack import Attack
import pygame
import math

class Enemy(pygame.sprite.Sprite):
    sprites_key = None
    enemy_behavior = None

    def __init__(self, heath=100):
        super().__init__()
        self.max_health = heath
        self.health = self.max_health
        self.before_health = self.health
        self.image = None
        self.rect = None

        self.size = 1
        self.action = "idle"
        self.loop_action = False
        self.death = False

        self.facing = 0
        self.frame_animation = 0
        self.speed = None

        self.animation = set()
        self.atk_pos = (0,0)
        self.old_position = (0,0)
        self.status = None
        self.velocity = [0,0]
        self.length = 0
        self.cooldown = {"hurt": 0}

    def update(self, frame, ms_per_loop, atk_group, event=None):

        self.update_per_loop(frame, ms_per_loop)
        self.status_update(frame, ms_per_loop)

        self.life_check()

        if self.action not in [*self.cooldown.keys(),*self.charge.keys(), "death"] and self.status is None:
            #and self.status != "confuse"#[*Boss1.attack_move.keys() ,"hurt"]:
            self.behaviour(frame, ms_per_loop)

        self.do_action(atk_group, frame, ms_per_loop)
        self.animated()

    def animated(self):
        if self.death is False:
            if self.frame_animation > len(self.animation[self.action][self.facing])-1:
                self.frame_animation = 0
                if self.loop_action is False:
                    self.action = "idle"
        self.image = self.animation[self.action][self.facing][self.frame_animation]

    def update_per_loop(self, frame, ms_per_loop):
        ## 1 frame = 250ms == ms_per_1frame of game file
        if self.death is True:
            return
        if self.enemy_behavior is None or self.sprites_key is None:
            return
        #frame_base
        self.frame_animation += frame
        self.loop_action = False
        # time based
        for keys,values in self.cooldown.items():
            if values > 0:
                self.cooldown[keys] -= ms_per_loop
            else :
                self.cooldown[keys] = 0

    def status_update(self, frame, ms_per_loop):
        pass


    def health_reduce(self, bullet_damage):
        if self.health > 0 and self.cooldown["hurt"] == 0:
            self.health -= bullet_damage
            self.action = "hurt"
            self.cooldown["hurt"] = self.enemy_behavior["hurt"]["cooldown"]
            self.frame_animation = 0

    def life_check(self):
        if self.health <= 0:
            self.action = "death"
        if self.action == "death" and self.frame_animation == self.sprites_key["death"][self.facing][0] - 1 :
            self.death = True

    def load_sprite(self, sprites_key):
        Enemy_sprite_sheet = SpriteHandler(pygame.image.load(self.sprite_dir))
        self.animation = Enemy_sprite_sheet.pack_sprite(sprites_key, self.game.screen_scale)
        self.size = self.game.screen_scale * sprites_key["idle"][0][3]
        self.animated()
        self.rect = self.image.get_rect()




class Dummy(Enemy):
    sprites_key = {"idle": [[1, 0, 0, 16, 16], [1, 0, 0, 16, 16], [1, 0, 0, 16, 16], [1, 0, 0, 16, 16]],
                   "hurt" : [[1, 1, 1, 16, 16],[2, 1, 1, 16, 16],[2, 1, 1, 16, 16],[2, 1, 1, 16, 16]],
                   "death": [[1, 1, 1, 16, 16],[2, 1, 1, 16, 16],[2, 1, 1, 16, 16],[2, 1, 1, 16, 16]]}
    enemy_behavior = {"hurt":{"cooldown":200}}


    def __init__(self, position, game):
        super().__init__()
        self.sprite_dir = 'sprites\\Dummy_demo.png'
        self.game = game
        self.name = "__DUMMY08"
        self.max_health = 10000
        self.health = self.max_health
        self.cooldown = {"hurt": 0}
        self.load_sprite(Dummy.sprites_key)
        self.rect.x = position[0]
        self.rect.y = position[1]

    def update(self, frame, ms_per_loop, atk_group, event=None):
        self.update_per_loop(frame, ms_per_loop)
        self.animated()


########################################################################################################################
########################################################################################################################

class Boss1(Enemy):
    sprites_key = {"idle": [[4, 0, 0, 16, 16], [4, 0, 0, 16, 16], [4, 0, 0, 16, 16], [4, 0, 0, 16, 16]],
                   "walk": [[4, 0, 1, 16, 16], [4, 0, 1, 16, 16], [4, 0, 1, 16, 16], [4, 0, 1, 16, 16]],
                   "attack1": [[4, 0, 0, 16, 16], [4, 0, 0, 16, 16], [4, 0, 0, 16, 16], [4, 0, 0, 16, 16]],
                   "attack2": [[4, 0, 0, 16, 16], [4, 0, 0, 16, 16], [4, 0, 0, 16, 16], [4, 0, 0, 16, 16]],
                   "dash_attack": [[4, 0, 0, 16, 16], [4, 0, 0, 16, 16], [4, 0, 0, 16, 16], [4, 0, 0, 16, 16]],
                   "charge_dash_attack": [[5, 0, 2, 16, 16], [5, 0, 2, 16, 16], [5, 0, 2, 16, 16], [5, 0, 2, 16, 16]],
                   "hurt" : [[1, 0, 1, 16, 16],[1, 1, 1, 16, 16],[1, 2, 1, 16, 16],[1, 3, 1, 16, 16]],
                   "death": [[6,0,3,16,16],[6,0,3,16,16],[6,0,3,16,16],[6,0,3,16,16]],
                   "enter_arena" : [[1, 0, 1, 16, 16],[1, 1, 1, 16, 16],[1, 2, 1, 16, 16],[1, 3, 1, 16, 16]]}

    ## ONLY FOR READ AND NOT CHANGE THE VALUE SO I NOT PUT IT IN ATTRIBUTE
    enemy_behavior = {"attack1":{"damage":5, "hitbox":(3,3), "cooldown":3},
                   "attack2":{"damage":20, "hitbox":(20,20), "cooldown":100},
                   "dash_attack":{"damage":20, "hitbox":(20,20), "cooldown":35, "charge_time":1000, "multiply_speed":5},
                      "hurt":{"cooldown":300}, "stunt":{"charge_time":1500}}

    def __init__(self, position, game, name):
        super().__init__()
        self.game = game
        self.name = name
        self.status = "enter_arena"
        self.sprite_dir = 'sprites\\Boss1_substitute.png'
        self.size = self.game.screen_scale
        self.load_sprite(Boss1.sprites_key)
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.cooldown = {"hurt":0, "attack1":0, "attack2":0, "dash_attack":0}
        self.charge = {"charge_dash_attack":0, "bounce":0, "stunt":0, "attack_bounce":0}

        self.normal_speed = 45 #pixel per second
        self.speed = self.normal_speed

    def behaviour(self, frame, ms_per_loop):
        length, dx, dy = Config.get_length(self.rect.center, self.game.player.rect.center)
        if length == 0:
            length = 0.001
        self.velocity = [ dx/length, dy/length]

        if frame != 1:
            self.movement(length, ms_per_loop)
            return
        # check behaviour for attack 1
        if length >= 350 and self.cooldown["dash_attack"]==0:
            self.frame_animation = 0
            self.action = "charge_dash_attack"
            self.cooldown["dash_attack"] = Boss1.enemy_behavior["dash_attack"]["cooldown"]
        ## ONE TIME THE ATTACK NOT FIRE DIAGONAL TURN OUT IT JUST ONLY TO FAR FROM IT LENGTH
        elif length <= self.size + Boss1.enemy_behavior["attack1"]["hitbox"][0] and self.cooldown["attack1"]==0:
            self.frame_animation = 0
            self.atk_pos = self.game.player.rect.center
            self.action = "attack1"
            self.cooldown["attack1"] = Boss1.enemy_behavior["attack1"]["cooldown"]
        else :
            self.movement(length, ms_per_loop)

    def status_update(self, frame, ms_per_loop):
        self.old_position = [self.rect.x, self.rect.y]
        if self.death is True:
            return

        if self.status == "attack_bounce":
            self.action = "hurt"
            self.loop_action = True
            self.charge["attack_bounce"] += ms_per_loop
            if self.charge["attack_bounce"] >= 300:
                self.charge["attack_bounce"] = 0
                self.status = None
                self.velocity = [0, 0]
                return
            if self.facing in [1,3]:
                if self.charge["attack_bounce"] > 100:
                    self.velocity[1] += 300 * (ms_per_loop / 1000)
                else :
                    self.velocity[1] += 150 * (ms_per_loop / 1000)
            else:
                if self.charge["attack_bounce"] > 70:
                    if self.facing == 0:
                        self.velocity[1] -= 250 * (ms_per_loop / 1000)
                    else:
                        self.velocity[1] += 250 * (ms_per_loop / 1000)
            self.rect.x += self.velocity[0] * self.game.screen_scale * (ms_per_loop / 1000)
            self.rect.y += self.velocity[1] * self.game.screen_scale * (ms_per_loop / 1000)

            check1_x, check1_y, hit_wall, wall_dir = Config.check_boundary(self, self.game.arena_area)
            self.rect.x = check1_x
            self.rect.y = check1_y

        elif self.status == "bounce":
            self.action = "hurt"
            self.loop_action = True
            self.charge["bounce"] += ms_per_loop

            if self.charge["bounce"] >= 300:
                self.charge["bounce"] = 0
                self.status = "stunt"
                self.velocity = [0, 0]
                self.speed = self.normal_speed
                return
            elif self.charge["bounce"] <= 100:
                self.rect.y -= 4
            self.rect.x += self.velocity[0] * self.speed * self.game.screen_scale * (ms_per_loop / 1000)
            self.rect.y += self.velocity[1] * self.speed * self.game.screen_scale * (ms_per_loop / 1000)

            check1_x, check1_y, hit_wall, wall_dir = Config.check_boundary(self, self.game.arena_area)
            self.rect.x = check1_x
            self.rect.y = check1_y


        elif self.status == "stunt":
            self.action = "hurt"
            self.loop_action = True
            self.charge[self.status] += ms_per_loop
            if self.charge[self.status] >= self.enemy_behavior["stunt"]["charge_time"]:
                self.charge[self.status] = 0
                self.status = None

        elif self.status == "enter_arena":
            self.action = "enter_arena"
            self.loop_action = True
            accelerate = 500
            gravity = 2500
            bounce_strength = 1800
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

    def health_reduce(self, bullet_damage):
        if self.health > 0 and self.cooldown["hurt"] == 0:
            self.health -= bullet_damage
            self.action = "hurt"
            self.cooldown["hurt"] = self.enemy_behavior["hurt"]["cooldown"]
            self.frame_animation = 0
            self.status = "attack_bounce"
            if self.facing in [1, 3]:
                if self.facing == 1:
                    velocity_x = 20
                    velocity_y = -20
                else:
                    velocity_x = -20
                    velocity_y = -20
            else:
                velocity_x = 0
                if self.facing == 0:
                    velocity_y = 20
                else:
                    velocity_y = -20
            self.velocity = [velocity_x, velocity_y]

    def movement(self, length, ms_per_loop):
        if length > (self.game.player.size + self.size)/2:
            self.loop_action = True
            if self.action != "walk":
                self.frame_animation = 0
            self.action = "walk"

            self.old_position = (self.rect.x, self.rect.y)
            self.rect.center = (self.rect.center[0] + (self.velocity[0] * self.speed
                                    * self.game.screen_scale * (ms_per_loop/1000)),
                                self.rect.center[1] + (self.velocity[1] * self.speed
                                    * self.game.screen_scale * (ms_per_loop/1000)) )

            check1_x, check1_y, hit_wall, wall_dir = Config.check_boundary(self, self.game.arena_area)
            self.rect.x, self.rect.y = Config.entities_overlay(self, (check1_x, check1_y),
                                                                     self.old_position)


    # WHY YOU NOT CALL IN THE BEHAVIOUR CAUSE THERE ARE SOME DELAY BETWEEN COMMAND TO ATTACK AND REAL BUILD ATK HITBOX
    def do_action(self, atk_group, frame, ms_per_loop):
        if self.death is True:
            return


        if self.action == "attack1" and self.frame_animation == 1 :
            atk = Attack("melee", self, Boss1.enemy_behavior["attack1"]["damage"], Boss1.enemy_behavior["attack1"]["hitbox"], self.atk_pos)
            atk_group.add(atk)
            self.action = "idle"
            self.atk_pos = (0,0)
            self.frame_animation = 0

        elif self.action == "charge_dash_attack":
            self.loop_action = True
            self.charge["charge_dash_attack"] += ms_per_loop
            if self.charge["charge_dash_attack"] >= Boss1.enemy_behavior["dash_attack"]["charge_time"]:
                self.charge["charge_dash_attack"] = 0
                self.action = "dash_attack"
                self.frame_animation = 0
                self.atk_pos = (self.game.player.rect.center[0] + (self.game.player.velocity[0] * 50 * self.game.screen_scale * (ms_per_loop / 1000) ) , #self.charge time * speed * screen scale * ???-> 5 * 2
                                self.game.player.rect.center[1] + (self.game.player.velocity[1] * 50 * self.game.screen_scale * (ms_per_loop / 1000)))
                length, dx, dy = Config.get_length(self.rect.center, self.atk_pos)
                self.velocity = [dx/length, dy/length]

        elif self.action == "dash_attack":
            self.speed = self.normal_speed * Boss1.enemy_behavior["dash_attack"]["multiply_speed"]
            self.loop_action = True
            self.rect.center = (self.rect.center[0] + ((self.velocity[0]) * self.speed * self.game.screen_scale * (ms_per_loop / 1000) ),
                                self.rect.center[1] + ((self.velocity[1]) * self.speed * self.game.screen_scale * (ms_per_loop / 1000) ))
            check1_x, check1_y, hit_wall, wall_dir = Config.check_boundary(self, self.game.arena_area)
            self.rect.x = check1_x
            self.rect.y = check1_y

            self.atk_pos = self.rect.center
            atk = Attack("melee", self, Boss1.enemy_behavior["dash_attack"]["damage"],
                         [2,2], self.atk_pos,decay_time=1, direction_type=2)
            atk_group.add(atk)
            if hit_wall is True or self.action == "hurt":
                self.status = "bounce"
                self.velocity = [-self.velocity[0]/2, -self.velocity[1]/2]


class Boss2(Enemy):
    sprites_key = {"idle": [[5, 0, 0, 16, 25], [5, 0, 0, 16, 25], [5, 0, 0, 16, 25], [5, 0, 0, 16, 25]],
                   "try_to_run":[[3, 0, 1, 16, 25], [3, 0, 1, 16, 25], [3, 0, 1, 16, 25], [3, 0, 1, 16, 25]],
                   "attack":[[1, 0, 0, 16, 25], [1, 0, 0, 16, 25], [1, 0, 0, 16, 25], [1, 0, 0, 16, 25]],
                   "hurt":[[1,1,2,16,25],[1,1,2,16,25],[1,1,2,16,25],[1,1,2,16,25]],
                   "death":[[2,4,2,16,25],[2,4,2,16,25],[2,4,2,16,25],[2,4,2,16,25]],
                   "run":[[1,1,2,16,25],[1,1,2,16,25],[1,1,2,16,25],[1,1,2,16,25]],
                   "spike":[[6,1,2,16,25],[6,1,2,16,25],[6,1,2,16,25],[6,1,2,16,25]],
                   "enter_arena":[[6,1,2,16,25],[6,1,2,16,25],[6,1,2,16,25],[6,1,2,16,25]],
                   "appear":[[6,1,2,16,25],[6,1,2,16,25],[6,1,2,16,25],[6,1,2,16,25]],
                   "stuck":[[6,1,2,16,25],[6,1,2,16,25],[6,1,2,16,25],[6,1,2,16,25]]}

    enemy_behavior = {"run":{"damage":0, "hitbox":(0, 0), "cooldown":10000, "charge_time":1500},
                  "attack":{"damage":10, "hitbox":(3,3), "cooldown":750},
                  "spike":{"damage":5, "hitbox":(32,32), "cooldown":2500, "sprite_dir":'sprites\\spike_attack.png',
                           "sprite_key":{"normal":[[1,0,0,32,32]]}},
                      "stunt":{"charge_time":3500}}

    def __init__(self, position, game, name):
        super().__init__()
        self.game = game
        self.name = name
        self.sprite_dir = 'sprites\\Boss2.png'
        self.status = "enter_arena"
        self.size = self.game.screen_scale
        self.load_sprite(Boss2.sprites_key)
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.cooldown = {"hurt":0, "attack":0, "attack2":0, "try_to_run":0, "spike":0}
        self.charge = {"try_to_run":0, "bounce":0, "stunt":0, "random_run":0}

        self.normal_speed = 100
        self.speed = self.normal_speed

    def behaviour(self, frame, ms_per_loop):
        ## Length is in pixel GOOD
        length, dx, dy = Config.get_length(self.rect.center, self.game.player.rect.center)
        self.velocity = [ - dx / length, - dy / length]

        if frame != 1:
            if self.action == "run":
                self.movement(length, ms_per_loop)
            return

        ## CHANGE TO BE SCALE(1) * self.game.screen_scale
        if length <= 100 * self.game.screen_scale and self.cooldown["try_to_run"] == 0:
            self.action = "try_to_run"

        elif self.action == "run" and length <= 90 * self.game.screen_scale and self.cooldown["spike"] == 0:
            self.action = "spike"

        elif length > 270 * self.game.screen_scale and self.action == "run":
            ## THIS COULD BE STOP RUNNING
            # self.action = "set_up"
            print("enough")
            self.action = "idle"

        elif length > 350 * self.game.screen_scale :
            self.action = "idle"

        elif self.action not in ["run","try_to_run"] and self.cooldown["attack"] <= 0:
            self.action = "attack"

        elif self.action == "run" :
            self.movement(length, ms_per_loop)

    def status_update(self, frame, ms_per_loop):
        self.old_position = [self.rect.x, self.rect.y]
        if self.death is True:
            return

        elif self.status == "bounce":
            self.action = "hurt"
            self.loop_action = True
            self.charge["bounce"] += ms_per_loop

            if self.charge["bounce"] >= 300:
                self.charge["bounce"] = 0
                self.status = "stunt"
                self.velocity = [0, 0]
                self.speed = self.normal_speed
                return
            elif self.charge["bounce"] <= 100:
                self.rect.y -= 4
            self.rect.x += self.velocity[0] * self.speed * self.game.screen_scale * (ms_per_loop / 1000)
            self.rect.y += self.velocity[1] * self.speed * self.game.screen_scale * (ms_per_loop / 1000)

            check1_x, check1_y, hit_wall, wall_dir = Config.check_boundary(self, self.game.arena_area)
            self.rect.x = check1_x
            self.rect.y = check1_y

        elif self.status == "random_run":
            self.charge[self.status] += ms_per_loop
            if self.facing == 0:
                self.rect.y -= self.speed * self.game.screen_scale * (ms_per_loop / 1000)
            elif self.facing == 2:
                self.rect.y += self.speed * self.game.screen_scale * (ms_per_loop / 1000)
            elif self.facing == 1:
                self.rect.x -= self.speed * self.game.screen_scale * (ms_per_loop / 1000)
            else :
                self.rect.x += self.speed * self.game.screen_scale * (ms_per_loop / 1000)
            check1_x, check1_y, hit_wall, wall_dir = Config.check_boundary(self, self.game.arena_area)
            if hit_wall is True and wall_dir == self.facing or [self.rect.x, self.rect.y] == self.old_position:
                self.charge[self.status] = 0
                self.status = None


        elif self.status == "stunt":
            self.action = "stuck"
            self.loop_action = True
            self.charge[self.status] += ms_per_loop
            if self.charge[self.status] == self.enemy_behavior["stunt"]["charge_time"]:
                self.charge[self.status] = 0
                self.status = None

        elif self.status == "enter_arena":
            self.action = "enter_arena"
            self.loop_action = True
            accelerate = 500
            gravity = 2500
            bounce_strength = 1800
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
            if (inside_x and inside_y and self.velocity == [0, 0]
                    and self.frame_animation == self.sprites_key["enter_arena"][0][0]-1):
                self.status = None
                self.action = "appear"

    def do_action(self, atk_group, frame, ms_per_loop):
        if self.death is True:
            return

        if self.action == "attack":
            self.cooldown["attack"] = self.enemy_behavior["attack"]["cooldown"]
            self.atk_pos = self.game.player.rect.center
            atk = Attack("bullet", self, Boss2.enemy_behavior["attack"]["damage"],
                         Boss2.enemy_behavior["attack"]["hitbox"], self.atk_pos, direction_type=2)
            atk_group.add(atk)
            self.action = "idle"
            self.atk_pos = (0,0)
            self.frame_animation = 0

        elif self.action == "try_to_run":
            self.loop_action = True
            self.charge["try_to_run"] += ms_per_loop
            if self.charge["try_to_run"] >= self.enemy_behavior["run"]["charge_time"]:
                self.charge["try_to_run"] = 0
                self.cooldown["try_to_run"] = self.enemy_behavior["run"]["cooldown"]
                self.action = "run"
                self.frame_animation = 0

        elif self.action == "spike" and self.frame_animation == 5:
            self.atk_pos = self.game.player.rect.center
            atk = Attack("ground", self, Boss2.enemy_behavior["spike"]["damage"],
                         Boss2.enemy_behavior["spike"]["hitbox"], self.atk_pos, decay_time=100, direction_type=1,
                         sprite_dir=Boss2.enemy_behavior["spike"]["sprite_dir"], sprite_key=Boss2.enemy_behavior["spike"]["sprite_key"])
            atk_group.add(atk)
            self.cooldown["spike"] = self.enemy_behavior["spike"]["cooldown"]
            self.action = "run"
            self.frame_animation = 0


    def health_reduce(self, bullet_damage):
        if self.health > 0:
            ## ADD MORE ANIMATION
            if self.action == "run":
                self.status = "stunt"

            self.health -= bullet_damage
            self.action = "hurt"
            self.cooldown["hurt"] = 5
            self.frame_animation = 0
            if self.cooldown["try_to_run"] > 0:
                self.cooldown["try_to_run"] -= 100
            if self.cooldown["try_to_run"] < 0:
                self.cooldown["try_to_run"] = 0

    def movement(self, length, ms_per_loop):
        self.loop_action = True
        self.action = "run"

        self.old_position = (self.rect.x, self.rect.y)
        self.rect.center = (
            self.rect.center[0] + ( self.velocity[0] * self.speed * self.game.screen_scale * (ms_per_loop/1000)),
            self.rect.center[1] + (self.velocity[1] * self.speed * self.game.screen_scale * (ms_per_loop/1000)))
        check1_x, check1_y, hit_wall, wall_dir = Config.check_boundary(self, self.game.arena_area)
        self.rect.x, self.rect.y = Config.entities_overlay(self, (check1_x, check1_y),
                                                           self.old_position)
        if hit_wall is True:
            self.status = "random_run"
            if wall_dir in [0,2]:
                self.facing = random.choice((1,3))
            else :
                self.facing = random.choice((0,2))
