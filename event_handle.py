import pygame
from config import Config

class EventHandle:
    def __init__(self):
        self.key_press = set()
        self.mouse_position = (0,0)
        self.mouse_button = set()
        self.quit = False

    def update_event(self, game=None):
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.VIDEORESIZE:
                # print(event.dict['size'])
                game.window = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)
                print(event.dict['size'])
                # config.screen_info = event.dict['size']
                ## SEND VALUE TO CONFIGURE TO GET THE SCREEN THAT STILL 16:9 RATIO
                game.screen_info = event.dict['size']
            if event.type == pygame.QUIT:
                self.quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit = True
                self.key_press.add(event.key)
            # if event.type == pygame.KEYUP:
            #     self.key_press.remove(event.key)
            if event.type == pygame.MOUSEMOTION:
                self.mouse_position = event.pos
            # if event.type == pygame.MOUSEBUTTONUP:
            #     self.mouse_button.remove(event.button)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_button.add(event.button)


    def reset_event(self):
        self.key_press = set()
        self.mouse_position = (0,0)
        self.mouse_button = set()

    def is_keypress(self, key):
        if key in self.key_press:
            self.key_press.remove(key)
            return True
        return False

    def mouse_click(self, button):
        if button in self.mouse_button:
            self.mouse_button.remove(button)
            return True
        return False

    def quit_press(self):
        return self.quit


event_object = EventHandle()