from chickfight_player import Player
import pygame

color = {'black':(0, 0, 0), 'white':(255, 255, 255)}
screen_info = (700,500)

clock = pygame.time.Clock()

# main game setting
playing = True
window = pygame.display.set_mode(screen_info)#, pygame.FULLSCREEN)
pygame.display.set_caption('ChickenFight')
player = Player(screen_info,"jim")


#Background
background = pygame.transform.scale(pygame.image.load("grass.jpg"),screen_info)

all_sprite = pygame.sprite.Group()
all_sprite.add(player)


while playing:
    # check all input(include game running state)
    # window.fill(color['white'])
    dt = clock.tick(60) #FPS cap in millisecond


    # print(dt)
    # print(f"FPS: {clock.get_fps():.2f}")

    event_list = pygame.event.get()

    for event in event_list:
        if event.type == pygame.QUIT:
            playing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                playing = False
                print("Quit")
            if event.key == pygame.K_SPACE:
                player.image = pygame.transform.flip(player.image, False, True)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                # what happen if we not update size -> everytime you Keyup it fixed to this size but if you press
                # again it will continue update size from last time
                player.size = 45
                player.image = pygame.transform.scale(pygame.image.load('jim.png'), (player.size,player.size))

    all_sprite.update(event_list)

    window.blit(background,(0,0))
    all_sprite.draw(window)
        #     if event.key == pygame.K_w:
        #         player.move_up = True
        #     if event.key == pygame.K_s:
        #         player.move_down = True
        #     if event.key == pygame.K_a:
        #         player.move_left = True
        #     if event.key == pygame.K_d:
        #         player.move_right = True
        # if event.type == pygame.KEYUP:
        #     if event.key == pygame.K_w:
        #         player.move_up = False
        #     if event.key == pygame.K_s:
        #         player.move_down = False
        #     if event.key == pygame.K_a:
        #         player.move_left = False
        #     if event.key == pygame.K_d:
        #         player.move_right = False

        # if player.move_up:
        #     player.move('up')
        # if player.move_down:
        #     player.move('down')
        # if player.move_left:
        #     player.move('left')
        # if player.move_right:
        #     player.move('right')
    pygame.display.update()

# if out of while playing will quit
pygame.quit()

