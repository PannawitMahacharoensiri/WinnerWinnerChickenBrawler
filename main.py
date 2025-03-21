from chickfight_player import Player
from event_handle import event_object
from Sprite_handle import *
import pygame

# class Player(pygame.sprite.Sprite):
#
#     # temporary probably all change when really got the sprite sheet
#
#     # image = pygame.image.load('jim.png')
#     def __init__(self, position, name='BOY'):
#         super().__init__()
#         self.size = 45
#
#         # pygame.transform after build other is just work of self.image container -> value not change
#         self.image = pygame.transform.scale(pygame.image.load('jim.png'), (self.size,self.size))
#         self.rect = self.image.get_rect()
#
#         self.name = name
#         self.pos_x = position[0] // 2
#         self.pos_y = position[1] // 2
#         self.speed = 1
#         self.face_state = 'left'
#         self.rect.center = (self.pos_x, self.pos_y)
#
#         # self.move_up = False
#         # self.move_down = False
#         # self.move_left = False
#         # self.move_right = False
#
#     # def move(self, key):
#     #     if key == 'up':
#     #         self.pos_y -= self.speed
#     #     elif key == 'down':
#     #         self.pos_y += self.speed
#     #     elif key == 'left':
#     #         self.pos_x -= self.speed
#     #     elif key == 'right':
#     #         self.pos_x += self.speed
#     def update(self, event_list=None):
#         if event_object.is_keypress(pygame.K_SPACE):
#             self.roll()
#             return
#
#         keys = pygame.key.get_pressed()
#         if keys[pygame.K_a]:
#             self.rect.x -= self.speed
#         if keys[pygame.K_d]:
#             self.rect.x += self.speed
#         if keys[pygame.K_w]:
#             self.rect.y -= self.speed
#         if keys[pygame.K_s]:
#             self.rect.y += self.speed
#         if keys[pygame.K_LSHIFT]:
#             self.image = pygame.transform.scale(self.image, (200,200))
#
#
#
#     def draw_player(self, _window):
#         _window.blit(self.image, (self.pos_x, self.pos_y))
#
#     def roll(self):
#         self.rect.x += 200

color = {'black':(0, 0, 0), 'white':(255, 255, 255)}
screen_info = (1024,576)

clock = pygame.time.Clock()

# main game setting
play_state = True
window = pygame.display.set_mode(screen_info)#, pygame.FULLSCREEN)
pygame.display.set_caption('ChickenFight')
player = Player(screen_info,"jim")


#Background
background = pygame.transform.scale(pygame.image.load("sprites\grass.jpg"),screen_info)

all_objects = pygame.sprite.Group()
all_objects.add(player)


while play_state:

    event_object.update_event()

    # window.fill(color['white'])
    dt = clock.tick(60) #FPS cap in millisecond

    # print(dt)
    # print(f"FPS: {clock.get_fps():.2f}")

    all_objects.update(event_object)

    window.blit(background,(0,0))

    # window.blit(frame0, (100,100) )


    all_objects.draw(window)

    pygame.display.update()

    event_object.reset_event()
    if event_object.quit_press():
        play_state = False
# if out of while loop p will rogramquit
pygame.quit()

