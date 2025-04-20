import pygame
from config import config

class Attack(pygame.sprite.Sprite):
    atk_direction = {"N":(0,-10), "S":(0,100), "E":(-100,0), "W":(100,0)}

    def __init__(self, a_type, maker, damage, hit_box, mouse_position, bullet_speed = 0):
        super().__init__()
        self.a_type = a_type
        self.maker = maker
        self.damage = damage
        self.image = pygame.Surface(hit_box) #Attack hit box tuple - How wide

        if config.debug_mode is True:
            self.image.fill((0, 255, 0))
        else :
            self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()
        self.bullet_speed = bullet_speed
        self.already_hit = []

        self.atk_dir = None

        self.set_position(mouse_position)
        self.frame_counter = 0

    def update(self, frame, atk_group):
        self.frame_counter += frame

        # simple bullet
        if self.a_type == 'remote':
            self.rect.x += self.bullet_speed

        self.delete_atk(atk_group)

    def set_position(self, mouse_position):
        if self.a_type == "global":
            self.rect.center = mouse_position
        else :
            atk_degree = config.get_degree(self.maker.rect.center, mouse_position)
            direction = config.check_8direction(atk_degree)
            real_position = config.direction_position(direction, self.rect.height, self.maker.size)
            self.rect.center = (self.maker.rect.center[0] + real_position[0],
                                self.maker.rect.center[1] + real_position[1])

    def delete_atk(self, group):
        if self.frame_counter == 10:
            group.remove(self)