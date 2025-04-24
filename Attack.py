import pygame
from config import Config

class Attack(pygame.sprite.Sprite):

    def __init__(self, a_type, maker, damage, hit_box, mouse_position, bullet_speed = 0):
        super().__init__()
        self.a_type = a_type
        self.maker = maker
        self.damage = damage
        self.classic_hitbox = hit_box
        print(f"This is hitbox {self.classic_hitbox}")
        self.image = pygame.Surface((hit_box[0]*self.maker.game.screen_scale,hit_box[1]*self.maker.game.screen_scale)) #Attack hit box tuple - How wide
        self.show_hitbox()

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

    def show_hitbox(self):
        if self.maker.game.debug_mode is True:
            self.image.fill((0, 255, 0))
        else :
            self.image.set_colorkey((0, 0, 0))

    def set_position(self, mouse_position):
        if self.a_type == "global":
            self.rect.center = mouse_position
        else :
            atk_degree = Config.get_degree(self.maker.rect.center, mouse_position)
            direction = Config.check_8direction(atk_degree)
            real_position = Config.direction_position(direction, self.rect.height, self.maker.size)
            self.rect.center = (self.maker.rect.center[0] + real_position[0],
                                self.maker.rect.center[1] + real_position[1])

    def delete_atk(self, group):
        if self.frame_counter == 30:
            group.remove(self)

    def change_scale(self, game_scale):
        print(f"attack hitbox {self.classic_hitbox[0]*game_scale, self.classic_hitbox[1]*game_scale}")
        self.image = pygame.Surface((self.classic_hitbox[0]*game_scale, self.classic_hitbox[1]*game_scale))
        self.rect = self.image.get_rect()
        self.show_hitbox()

    # def load_sprite(self, sprites_key):
    #     Enemy_sprite_sheet = SpriteHandler(pygame.image.load(self.sprite_dir))
    #     self.animation = Enemy_sprite_sheet.pack_sprite(sprites_key, self.game.screen_scale)
    #     self.size = self.game.screen_scale * sprites_key["idle"][0][4]
    #     self.image = self.animation[self.action][self.direction][self.frame_animation]
    #     self.rect = self.image.get_rect()