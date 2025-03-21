import pygame

class EventHandle:
    def __init__(self):
        self.key_press = set()
        self.mouse_position = (0,0)
        self.quit = False

    def update_event(self):
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                self.quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit = True
                self.key_press.add(event.key)
            # if event.type == pygame.KEYUP:
            #     self.key_press.remove(event.key)
            if  event.type == pygame.MOUSEMOTION:
                self.mouse_position = event.pos

    def reset_event(self):
        self.key_press = set()
        self.mouse_position = (0,0)

    def is_keypress(self, key):
        if key in self.key_press:
            return True
        return False

    def quit_press(self):
        return self.quit


event_object = EventHandle()