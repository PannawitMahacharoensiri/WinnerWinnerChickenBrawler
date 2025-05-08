import pygame
import math
from config import Config
from Sprite_handle import *

"""
direction_type = 0: 4-direction , 1: 8-direction, 2: all-direction
"""

class Attack(pygame.sprite.Sprite):

    def __init__(self, attack_type, maker, damage, hit_box, attack_pos, decay_time = 2,
                 direction_type = 0, bullet_speed = 30, sprite_dir = None ,sprite_key = None):
        super().__init__()
        self.attack_type = attack_type
        self.maker = maker
        self.damage = damage
        self.classic_hitbox = hit_box
        self.animation = None
        self.image = None

        self.sprite_key = sprite_key
        self.sprite_dir = sprite_dir
        self.load_sprite(self.classic_hitbox)


        # self.show_hitbox()

        self.rect = self.image.get_rect()
        self.size = self.rect.width

        self.old_position = (0,0)

        self.bullet_direction = [0,0]
        self.bullet_speed = bullet_speed
        self.already_hit = []
        self.set_position(attack_pos, direction_type)
        self.frame_counter = 0
        self.decay_time = decay_time

    def load_sprite(self, hit_box):
        if self.sprite_dir is None or self.sprite_key is None:
            self.image = pygame.Surface((hit_box[0] * self.maker.game.screen_scale,
                                         hit_box[1] * self.maker.game.screen_scale))  # Attack hit box tuple - How wide
            if self.attack_type in ["bullet","global"]:
                self.image.fill((80, 80, 80))
            else :
                self.image.set_colorkey((0, 0, 0))
        else :
            Attack_sprite = SpriteHandler(pygame.image.load(self.sprite_dir))
            self.animation = Attack_sprite.pack_sprite(self.sprite_key, self.maker.game.screen_scale)
            self.image = self.animation["normal"][0][0]
            self.rect = self.image.get_rect()
            self.size = self.maker.game.screen_scale * self.rect.width

    def update(self, frame, atk_group):
        self.frame_counter += frame
        self.decay_time -= frame

        # simple bullet
        if self.attack_type == 'bullet':
            ## BUG WITH SCREEN SCALE
            self.old_position = (self.rect.x, self.rect.y)
            move_speed_x = (self.bullet_direction[0]*self.bullet_speed * Config.dt_per_second * self.maker.game.screen_scale)
            move_speed_y = (self.bullet_direction[1]*self.bullet_speed * Config.dt_per_second * self.maker.game.screen_scale)

            self.rect.center = (self.rect.center[0] + move_speed_x,
                                self.rect.center[1] + move_speed_y)
            self.rect.x, self.rect.y , hit_wall, wall_dir = Config.check_boundary(self, self.maker.game.screen_info,
                                                                        self.maker.game.screen_start)
            if hit_wall is True:
                self.bullet_speed = 0
        elif self.attack_type == "ground":
            if self.frame_counter == 5:
                self.already_hit = []
                self.frame_counter = 0


        self.delete_atk(atk_group)

    def show_hitbox(self):
        if self.maker.game.debug_mode is True:
            self.image.fill((0, 255, 0))
        else :
            self.image.set_colorkey((0, 0, 0))

    def set_position(self, attack_pos, direction_type):
        if self.attack_type == "global":
            self.rect.center = attack_pos
        else :
            atk_degree = Config.get_degree(self.maker.rect.center, attack_pos)

            if direction_type == 0:
                direction = Config.check_4direction(atk_degree)
                shift_pos = Config.shift_position(direction, self.rect.width, self.rect.height, self.maker.size)

                dx = shift_pos[0]
                dy = shift_pos[1]
                lenght = math.sqrt(dx ** 2 + dy ** 2)
                if lenght != 0:
                    self.bullet_direction = [dx / lenght, dy / lenght]
                else :
                    self.bullet_direction = [0,0]
            elif direction_type == 1:
                direction = Config.check_8direction(atk_degree)
                shift_pos = Config.shift_position(direction, self.rect.width, self.rect.height, self.maker.size)

                dx = shift_pos[0]
                dy = shift_pos[1]
                lenght = math.sqrt(dx ** 2 + dy ** 2)
                if lenght != 0:
                    self.bullet_direction = [dx / lenght, dy / lenght]
                else:
                    self.bullet_direction = [0, 0]
            else :
                dx = attack_pos[0] - self.maker.rect.center[0]
                dy = attack_pos[1] - self.maker.rect.center[1]
                lenght = math.sqrt(dx ** 2 + dy ** 2)
                if lenght != 0:
                    self.bullet_direction = [dx/lenght, dy/lenght]
                else :
                    self.bullet_direction = [0,0]
                shift_pos = [self.bullet_direction[0] * self.maker.size , self.bullet_direction[1] * self.maker.size]

            self.rect.center = (self.maker.rect.center[0] + shift_pos[0],self.maker.rect.center[1] + shift_pos[1])

    def delete_atk(self, group):
        if self.attack_type == "bullet":
            if self.bullet_speed == 0:
                group.remove(self)
        else :
            if self.decay_time <= 0:
                group.remove(self)

    def change_scale(self, game_scale):
        self.load_sprite(self.classic_hitbox)
        self.rect = self.image.get_rect()
        self.size = self.rect.width
        # self.show_hitbox()
