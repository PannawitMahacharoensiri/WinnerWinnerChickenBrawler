import pygame

class Player(pygame.sprite.Sprite):

    # temporary probably all change when really got the sprite sheet

    # image = pygame.image.load('jim.png')
    def __init__(self, position, name='BOY'):
        super().__init__()
        self.size = 45

        # pygame.transform after build other is just work of self.image container -> value not change
        self.image = pygame.transform.scale(pygame.image.load('jim.png'), (self.size,self.size))
        self.rect = self.image.get_rect()

        self.name = name
        self.pos_x = position[0] // 2
        self.pos_y = position[1] // 2
        self.speed = 5
        self.face_state = 'left'
        self.rect.center = (self.pos_x, self.pos_y)

        # self.move_up = False
        # self.move_down = False
        # self.move_left = False
        # self.move_right = False

    # def move(self, key):
    #     if key == 'up':
    #         self.pos_y -= self.speed
    #     elif key == 'down':
    #         self.pos_y += self.speed
    #     elif key == 'left':
    #         self.pos_x -= self.speed
    #     elif key == 'right':
    #         self.pos_x += self.speed
    def update(self, event_list=None):

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_LSHIFT]:
            self.image = pygame.transform.scale(self.image, (200,200))

        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_3:
                    print("Hooray")

    def draw_player(self, _window):
        _window.blit(self.image, (self.pos_x, self.pos_y))