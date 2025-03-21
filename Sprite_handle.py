import pygame

# duck_demo_sheet = pygame.image.load('sprites\demo_sheet.png')

class SpriteHandler:
    def __init__(self, sheet_image):
        self.sheet = sheet_image

    def read_sprite_sheet(self, frame, w_area, h_area, scale_size):
        image = pygame.Surface((w_area, h_area))
        image.blit(self.sheet, (0, 0), ((frame * w_area), 0, w_area, h_area))
        image = pygame.transform.scale(image, (w_area * scale_size, h_area * scale_size))
        image.set_colorkey((255, 255, 255))
        return image


# frame0 = SpriteHandler.read_sprite_sheet(pygame.image.load('sprites\demo_sheet.png'), 0,16,16,5)