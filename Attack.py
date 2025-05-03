import pygame
import math
from config import Config

"""
direction_type = 0: 4-direction , 1: 8-direction, 2: all-direction
"""

class Attack(pygame.sprite.Sprite):

    def __init__(self, attack_type, maker, damage, hit_box, attack_pos, direction_type = 0, bullet_speed = 2,
                 dash_attack=False):
        super().__init__()
        self.attack_type = attack_type
        self.maker = maker
        self.damage = damage
        self.classic_hitbox = hit_box
        self.image = pygame.Surface((hit_box[0]*self.maker.game.screen_scale,hit_box[1]*self.maker.game.screen_scale)) #Attack hit box tuple - How wide
        self.show_hitbox()

        self.rect = self.image.get_rect()
        self.size = self.rect.width

        self.old_position = (0,0)

        self.bullet_direction = [0,0]
        self.bullet_speed = bullet_speed
        self.already_hit = []
        self.set_position(attack_pos, direction_type, dash_attack)
        self.frame_counter = 0

    def update(self, frame, atk_group):
        self.frame_counter += frame

        # simple bullet
        if self.attack_type == 'bullet':
            self.old_position = (self.rect.x, self.rect.y)
            self.rect.center = (self.rect.center[0] + (self.bullet_direction[0]*self.bullet_speed),
                                self.rect.center[1] + (self.bullet_direction[1]*self.bullet_speed))
            self.rect.x, self.rect.y , hit_wall = Config.check_boundary(self, self.maker.game.screen_info,
                                                                        self.maker.game.screen_start)
            if hit_wall is True:
                self.bullet_speed = 0
        self.delete_atk(atk_group)

    def show_hitbox(self):
        if self.maker.game.debug_mode is True:
            self.image.fill((0, 255, 0))
        else :
            self.image.set_colorkey((0, 0, 0))

    def set_position(self, attack_pos, direction_type, dash_attack=False):
        if self.attack_type == "global":
            self.rect.center = attack_pos
        else :
            atk_degree = Config.get_degree(self.maker.rect.center, attack_pos)

            if direction_type == 0:
                direction = Config.check_4direction(atk_degree)
                shift_pos = Config.shift_position(direction, self.rect.width, self.rect.height, self.maker.size)
            elif direction_type == 1:
            ## NOW CHECK THE DIRECTION TYPE, to get real position (call direction for 4,8 | just put as mouse position)
                direction = Config.check_8direction(atk_degree)
                shift_pos = Config.shift_position(direction, self.rect.width, self.rect.height, self.maker.size)
            else :
                dx = attack_pos[0] - self.maker.rect.center[0]
                dy = attack_pos[1] - self.maker.rect.center[1]
                lenght = math.sqrt(dx ** 2 + dy ** 2)
                if lenght != 0:
                    self.bullet_direction = [dx/lenght, dy/lenght]
                else :
                    self.bullet_direction = [0,0]
                shift_pos = [self.bullet_direction[0] * self.maker.size , self.bullet_direction[1] * self.maker.size]
                if dash_attack is True:
                    shift_pos = self.bullet_direction

            self.rect.center = (self.maker.rect.center[0] + shift_pos[0],
                                self.maker.rect.center[1] + shift_pos[1])

    def delete_atk(self, group):
        if self.attack_type == "bullet":
            if self.bullet_speed == 0:
                group.remove(self)
        elif self.attack_type == "global":
            if self.frame_counter == 2:
                group.remove(self)
        else :
            if self.frame_counter == 5:
                group.remove(self)


    def change_scale(self, game_scale):
        self.image = pygame.Surface((self.classic_hitbox[0]*game_scale, self.classic_hitbox[1]*game_scale))
        self.rect = self.image.get_rect()
        self.size = self.rect.width
        self.show_hitbox()
