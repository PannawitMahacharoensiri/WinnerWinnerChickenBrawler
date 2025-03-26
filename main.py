from chickfight_player import Player
from event_handle import event_object
from Sprite_handle import *
import pygame

pygame.init()
color = {'black':(0, 0, 0), 'white':(255, 255, 255)}
screen_info = (1024,576)
tracker1 = pygame.time.get_ticks()
clock = pygame.time.Clock()
frame_delay = 300

# main game setting
play_state = True
player = Player(screen_info,name = "jim")

# window setting
window = pygame.display.set_mode(screen_info)#, pygame.FULLSCREEN)
pygame.display.set_caption('ChickenFight')


#Background
background = pygame.transform.scale(pygame.image.load("sprites\grass.jpg"),screen_info)

all_objects = pygame.sprite.Group()
all_objects.add(player)

while play_state:
    frame = 0
    tracker2 = pygame.time.get_ticks()
    # print(tracker1, "||||||||||||||" ,tracker2)

    # frame update calculate
    if tracker2 - tracker1 >= frame_delay:
        frame = 1
        tracker1 = tracker2

    event_object.update_event()
    clock.tick(60)

    # print(f"FPS: {clock.get_fps():.2f}")
    all_objects.update(frame, event_object)
    window.blit(background,(0,0))
    all_objects.draw(window)

    pygame.display.update()
    # event_object.reset_event()
    if event_object.quit_press():
        play_state = False
pygame.quit()

