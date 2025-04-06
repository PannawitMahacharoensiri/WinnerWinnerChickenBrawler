import pygame

class Attack(pygame.sprite.Sprite):

    def __init__(self, a_type, maker, damage, hit_box, mouse_position):
        super().__init__()
        self.a_type = a_type
        self.maker = maker
        self.damage = damage
        self.image = pygame.Surface(hit_box) #Attack hit box tuple - How wide
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = mouse_position[0]  # self.maker.rect.x +
        self.rect.y = mouse_position[1]  # self.maker.rect.y +
        self.frame_counter = 0

    def update(self, frame, atk_group):
        self.frame_counter += frame

        if self.a_type == 'remote':
            self.rect.x += 5

        self.delete_atk(atk_group)

    def delete_atk(self, group):
        if self.frame_counter == 2:
            group.remove(self)