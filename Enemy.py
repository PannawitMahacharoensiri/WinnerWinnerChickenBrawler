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
        self.death = False

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
        if self.health > 0:
            if self.action == "dash_attack":
                self.status = "bounce"
                self.velocity = [0,0]
            self.health -= bullet_damage
            self.action = "hurt"
            self.cooldown["hurt"] = 5
            self.frame_animation = 0

    def life_check(self):
        if self.health <= 0:
            self.action = "death"

        if self.action == "death" and self.frame_animation == self.sprites_key["death"][self.facing][0] - 1 :
            self.death = True

    def animated(self):
        if self.death is False:
            if self.frame_animation > len(self.animation[self.action][self.facing])-1:
                self.frame_animation = 0
                if self.loop_action is False:
                    self.action = "idle"
        self.image = self.animation[self.action][self.facing][self.frame_animation]

class Dummy(Enemy):
    sprites_key = {"idle": [[1, 0, 0, 16, 16], [1, 0, 0, 16, 16], [1, 0, 0, 16, 16], [1, 0, 0, 16, 16]],
                   "hurt" : [[1, 1, 1, 16, 16],[2, 1, 1, 16, 16],[2, 1, 1, 16, 16],[2, 1, 1, 16, 16]],
                   "death": [[1, 1, 1, 16, 16],[2, 1, 1, 16, 16],[2, 1, 1, 16, 16],[2, 1, 1, 16, 16]]}

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
                   "hurt" : [[1, 0, 1, 16, 16],[1, 1, 1, 16, 16],[1, 2, 1, 16, 16],[1, 3, 1, 16, 16]],
                   "death": [[6,0,3,16,16],[6,0,3,16,16],[6,0,3,16,16],[6,0,3,16,16]]}

    ## ONLY FOR READ AND NOT CHANGE THE VALUE SO I NOT PUT IT IN ATTRIBUTE
    attack_move = {"attack1":{"damage":5, "hitbox":(3,3), "cooldown":3},
                   "attack2":{"damage":20, "hitbox":(20,20), "cooldown":10},
                   "dash_attack":{"damage":20, "hitbox":(20,20), "cooldown":35, "charge_time":10, "speed":7}}

    def __init__(self, position, game, name):
        super().__init__()
        self.game = game
        self.name = name
        self.health = 1
        self.sprite_dir = 'sprites\\Boss1_substitute.png'
        self.size = self.game.screen_scale
        self.load_sprite(Boss1.sprites_key)
        self.rect.x = position[0]
        self.rect.y = position[1]
        self.cooldown = {"hurt":0, "attack1":0, "attack2":0, "dash_attack":0}
        self.charge = {"charge_dash_attack":0, "bounce":0, "confuse":0}

        self.normal_speed = 30 # 2 * 15
        self.speed = self.normal_speed


    def update(self, frame, atk_group, event=None):
        self.frame_update(frame)
        self.status_update(frame)
        self.life_check()

        if self.action not in [*self.cooldown.keys(),*self.charge.keys(), "death"] and self.status != "confuse":
            #and self.status != "confuse"#[*Boss1.attack_move.keys() ,"hurt"]:
            self.behaviour(frame)

        self.attack(atk_group, frame)
        self.animated()

    def status_update(self, frame):
        if self.death is True:
            return

        if self.status == "bounce":
            self.charge[self.status] += frame
            self.action = "hurt"
            self.loop_action = True
            new_velocity = Config.bounce(self.charge[self.status], velocity=self.velocity, facing=self.facing, size=self.size)
            self.rect.x += new_velocity[0] * Config.dt_per_second * self.game.screen_scale
            self.rect.y += new_velocity[1] * Config.dt_per_second * self.game.screen_scale
            valid_x, valid_y, hit_wall, wall_dir = Config.check_boundary(self, self.game.arena_area)
            self.rect.x = valid_x
            self.rect.y = valid_y
            if self.charge[self.status] == 2:
                self.charge[self.status] = 0
                self.status = None
                self.speed = self.normal_speed
                self.status = "confuse"

        elif self.status == "confuse":
            self.action = "hurt"
            self.loop_action = True
            self.charge[self.status] += frame
            if self.charge[self.status] == 5:
                self.charge[self.status] = 0
                self.status = None

    def frame_update(self, frame):
        if self.death is False:
            for keys,values in self.cooldown.items():
                if values > 0:
                    self.cooldown[keys] -= frame
            self.frame_animation += frame
            self.before_health = self.health
            self.loop_action = False


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
            check1_x, check1_y, hit_wall, wall_dir = Config.check_boundary(self, self.game.arena_area)
            self.rect.x, self.rect.y = Config.entities_overlay(self, (check1_x, check1_y),
                                                                     self.old_position)


    # WHY YOU NOT CALL IN THE BEHAVIOUR CAUSE THERE ARE SOME DELAY BETWEEN COMMAND TO ATTACK AND REAL BUILD ATK HITBOX
    def attack(self, atk_group, frame):
        if self.death is True:
            return


        if self.action == "attack1" and self.frame_animation == 1 :
            atk = Attack("melee", self, Boss1.attack_move["attack1"]["damage"], Boss1.attack_move["attack1"]["hitbox"], self.atk_pos)
            atk_group.add(atk)
            self.action = "idle"
            self.atk_pos = (0,0)
            self.frame_animation = 0

        elif self.action == "charge_dash_attack":
            self.loop_action = True
            self.charge["charge_dash_attack"] += frame
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
            check1_x, check1_y, hit_wall, wall_dir = Config.check_boundary(self, self.game.arena_area)
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


class Boss2(Enemy):
    sprites_key = {"idle": [[5, 0, 0, 16, 25], [5, 0, 0, 16, 25], [5, 0, 0, 16, 25], [5, 0, 0, 16, 25]],
                   "try_to_run":[[3, 0, 1, 16, 25], [3, 0, 1, 16, 25], [3, 0, 1, 16, 25], [3, 0, 1, 16, 25]],
                   "attack":[[1, 0, 0, 16, 25], [1, 0, 0, 16, 25], [1, 0, 0, 16, 25], [1, 0, 0, 16, 25]],
                   "hurt":[[1,1,2,16,25],[1,1,2,16,25],[1,1,2,16,25],[1,1,2,16,25]],
                   "death":[[1,4,2,16,25],[1,4,2,16,25],[1,4,2,16,25],[1,4,2,16,25]],
                   "run":[[1,1,2,16,25],[1,1,2,16,25],[1,1,2,16,25],[1,1,2,16,25]],
                   "spike":[[6,1,2,16,25],[6,1,2,16,25],[6,1,2,16,25],[6,1,2,16,25]]
                   }
    enemy_move = {"run":{"damage":0, "hitbox":(0,0), "cooldown":100, "charge_time":6},
                  "attack":{"damage":5, "hitbox":(3,3), "cooldown":3},
                  "spike":{"damage":20, "hitbox":(32,32), "cooldown":45, "sprite_dir":'sprites\\spike_attack.png',
                           "sprite_key":{"normal":[[1,0,0,32,32]]}}}

    def __init__(self, position, game, name):
        super().__init__()
        self.game = game
        self.name = name
        self.health = 100
        self.sprite_dir = 'sprites\\Boss2.png'
        self.size = self.game.screen_scale
        self.load_sprite(Boss2.sprites_key)
        self.rect.x = position[0] * self.game.screen_scale
        self.rect.y = position[1] * self.game.screen_scale
        self.cooldown = {"hurt":0, "attack":0, "attack2":0, "try_to_run":0, "spike":0}
        self.charge = {"try_to_run":0, "bounce":0, "stuck":0}

        self.normal_speed = 20 # 2 * 15
        self.speed = self.normal_speed

    def update(self, frame, atk_group, event=None):
        self.frame_update(frame)
        self.status_update(frame)
        self.life_check()

        ## WHEN CHARACTER NOT MOVE ONE TIME BECAUSE I LET RUN BE THE PART OF COOLDOWN WHEN ACTION == RUN THE MOVEMENT THAT IN BEHAVIOUR ALSO NOT GET RUN
        ## When character already decide to attack, or in between charge or it in PAIN sprite don't let it think
        if self.action not in [*self.cooldown.keys(),*self.charge.keys(), "death"] and self.status != "stuck":
            self.behaviour(frame)

        self.attack(atk_group, frame)
        self.animated()

    def frame_update(self, frame):
        if self.death is False:
            for keys,values in self.cooldown.items():
                if values > 0:
                    self.cooldown[keys] -= frame
            self.frame_animation += frame
            self.before_health = self.health
            self.loop_action = False


    def behaviour(self, frame):

        ## Length is in pixel GOOD
        length, dx, dy = Config.get_length(self.rect.center, self.game.player.rect.center)
        self.velocity = [ - dx / length, - dy / length]

        if frame != 1:
            if self.action == "run":
                self.movement(length)
            return

        ## CHANGE TO BE SCALE(1) * self.game.screen_scale
        if length <= 350 and self.cooldown["try_to_run"] == 0:
            self.action = "try_to_run"

        elif self.action == "run" and length <= 350 and self.cooldown["spike"] == 0:
            self.action = "spike"

        elif length > 400 and self.action == "run":
            ## THIS COULD BE STOP RUNNING
            # self.action = "set_up"
            self.action = "idle"

        elif length > 800 :
            self.action = "idle"

        elif self.action not in ["run","try_to_run"] and self.cooldown["attack"] == 0:
            self.action = "attack"

        elif self.action == "run" :
            self.movement(length)

    def attack(self, atk_group, frame):
        if self.death is True:
            return

        if self.action == "attack":
            self.atk_pos = self.game.player.rect.center
            atk = Attack("bullet", self, Boss2.enemy_move["attack"]["damage"],
                         Boss2.enemy_move["attack"]["hitbox"], self.atk_pos, direction_type=2)
            atk_group.add(atk)
            self.action = "idle"
            self.atk_pos = (0,0)
            self.frame_animation = 0

        elif self.action == "try_to_run":
            self.loop_action = True
            self.charge["try_to_run"] += frame
            if self.charge["try_to_run"] == self.enemy_move["run"]["charge_time"] -1:
                self.charge["try_to_run"] = 0
                self.cooldown["try_to_run"] = self.enemy_move["run"]["cooldown"]
                self.action = "run"
                self.frame_animation = 0

        elif self.action == "spike" and self.frame_animation == 5:
            self.atk_pos = self.game.player.rect.center
            atk = Attack("ground", self, Boss2.enemy_move["spike"]["damage"],
                         Boss2.enemy_move["spike"]["hitbox"], self.atk_pos, decay_time=100, direction_type=1,
                         sprite_dir=Boss2.enemy_move["spike"]["sprite_dir"], sprite_key=Boss2.enemy_move["spike"]["sprite_key"])
            atk_group.add(atk)
            self.cooldown["spike"] = self.enemy_move["spike"]["cooldown"]
            self.action = "run"
            self.frame_animation = 0


    def health_reduce(self, bullet_damage):
        if self.health > 0:
            ## ADD MORE ANIMATION
            if self.action == "run":
                self.status = "stuck"

            self.health -= bullet_damage
            self.action = "hurt"
            self.cooldown["hurt"] = 5
            self.frame_animation = 0
            if self.cooldown["try_to_run"] > 0:
                self.cooldown["try_to_run"] -= 4

            #ERROR HANDLE
            if self.cooldown["try_to_run"] < 0:
                self.cooldown["try_to_run"] = 0


    def status_update(self, frame):
        if self.death is True:
            return

        if self.status == "bounce":
            self.charge[self.status] += frame
            self.action = "hurt"
            self.loop_action = True
            new_velocity = Config.bounce(self.charge[self.status], velocity=self.velocity, facing=self.facing, size=self.size)
            self.rect.x += new_velocity[0] * Config.dt_per_second * self.game.screen_scale
            self.rect.y += new_velocity[1] * Config.dt_per_second * self.game.screen_scale
            valid_x, valid_y, hit_wall, wall_dir = Config.check_boundary(self, self.game.arena_area)
            self.rect.x = valid_x
            self.rect.y = valid_y
            if self.charge[self.status] == 2:
                self.charge[self.status] = 0
                self.status = None
                self.speed = self.normal_speed
        elif self.status == "stuck":
            self.charge[self.status] += frame
            self.action = "hurt"
            self.loop_action = True

            if self.charge[self.status] == 10:
                self.charge[self.status] = 0
                self.status = None


    def movement(self, length):
        self.loop_action = True
        self.action = "run"

        self.old_position = (self.rect.x, self.rect.y)
        print((self.velocity[0]) * self.speed * Config.dt_per_second * self.game.screen_scale)
        self.rect.center = (
            self.rect.center[0] + ((self.velocity[0]) * self.speed * Config.dt_per_second * self.game.screen_scale),
            self.rect.center[1] + ((self.velocity[1]) * self.speed * Config.dt_per_second * self.game.screen_scale))
        check1_x, check1_y, hit_wall, wall_dir = Config.check_boundary(self, self.game.arena_area)
        self.rect.x, self.rect.y = Config.entities_overlay(self, (check1_x, check1_y),
                                                           self.old_position)
        # if hit_wall is True:
        #     self.action = "idle"
