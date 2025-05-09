import pygame

class SpriteHandler:
    def __init__(self, sheet_image):
        self.__sheet = sheet_image

    def read_sprite_sheet(self, row, level, w_area, h_area, scale_size = None, flip = False ):
        image = pygame.Surface((w_area, h_area))
        image.blit(self.__sheet, (0, 0), ((row * w_area), (level * h_area), w_area, h_area))
        image.set_colorkey((255, 255, 255))

        if scale_size is not None:
            image = pygame.transform.scale(image, (w_area * scale_size, h_area * scale_size))
        if flip:
            image = pygame.transform.flip(image, True, False)

        return image

    def pack_sprite(self, sprites_key, scale_size):
        sprites_animation = dict()
        for name,action in sprites_key.items():
            temp_big_list = []
            for d in action:
                temp_small_list = []
                for i in range(d[0]):
                    image = self.read_sprite_sheet(d[1]+i, d[2], d[3], d[4], scale_size)
                    temp_small_list.append(image)
                temp_big_list.append(temp_small_list)
            sprites_animation[name] = temp_big_list
        return sprites_animation

