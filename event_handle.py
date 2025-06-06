import pygame

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
                game.change_window_size(event.dict['size'])
            if event.type == pygame.QUIT:
                self.quit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit = True
                self.key_press.add(event.key)
            if event.type == pygame.KEYUP:
                if event.key in self.key_press:
                    self.key_press.remove(event.key)
            if event.type == pygame.MOUSEMOTION:
                self.mouse_position = event.pos
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button in self.mouse_button:
                    self.mouse_button.remove(event.button)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_button.add(event.button)

    @staticmethod
    def key_to_char(key):
        if pygame.K_a <= key <= pygame.K_z:
            return chr(key)
        if pygame.K_0 <= key <= pygame.K_9:
            return chr(key)
        if key == pygame.K_SPACE:
            return ' '
        return ''

    def reset_event(self, exclude):
        if exclude != "key_press" or "key_press" not in exclude:
            self.key_press = set()
        if exclude != "mouse_pos" or "mouse_pos" not in exclude:
            self.mouse_position = (0,0)
        if exclude != "mouse_button" or "mouse_button" not in exclude:
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



