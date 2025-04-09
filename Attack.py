import pygame
from config import Config

class Attack(pygame.sprite.Sprite):
    atk_direction = {"NORTH":(0,-100), "SOUTH":(0,100), "EAST":(-100,0), "WEST":(100,0)}

    def __init__(self, a_type, maker, damage, hit_box, mouse_position):
        super().__init__()
        self.a_type = a_type
        self.maker = maker
        self.damage = damage
        self.image = pygame.Surface(hit_box) #Attack hit box tuple - How wide
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()

        self.atk_dir = None

        self.set_position(mouse_position)
        self.frame_counter = 0

    def update(self, frame, atk_group):
        self.frame_counter += frame

        if self.a_type == 'remote':
            self.rect.x += 5

        self.delete_atk(atk_group)

    def set_position(self, mouse_position):
        atk_degree = Config.get_degree(self.maker.rect.center, mouse_position)
        direction = Config.check_direction(atk_degree)
        if direction == "NORTH":
            self.atk_dir = 0
        else :
            self.atk_dir = 1
        # self.rect.x = mouse_position[0]
        # self.rect.y = mouse_position[1]
        self.rect.x = self.maker.rect.x + Attack.atk_direction[direction][0]
        self.rect.y = self.maker.rect.y + Attack.atk_direction[direction][1]

    def delete_atk(self, group):
        if self.frame_counter == 2:
            group.remove(self)