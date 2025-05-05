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
                game.screen_start_before = game.screen_start
                game.before_scale = game.screen_scale
                result_change_ratio = Config.screen_ratio(event.dict['size'], game.screen_scale)

                if result_change_ratio[0] is True:
                    game.change_size["screen"] = result_change_ratio[0]
                    game.screen_info = result_change_ratio[1]
                    game.screen_scale = result_change_ratio[2]
                valid_window = Config.window_to_screen(event.dict['size'], game.screen_info)
                game.window = pygame.display.set_mode(valid_window, pygame.RESIZABLE)
                game.screen_start = ((round(valid_window[0]-game.screen_info[0])/ 2),
                                     (round(valid_window[1]-game.screen_info[1])/ 2))
                if game.screen_start != game.screen_start_before :
                    game.change_size["window"] = True
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


class Widget:

    def __init__(self, name, game, border_position, border_ratio, level, text
                 , widget_type = "text", font_name = None,
                 text_color= (0,0,0), color = (255,255,255) ,hover_color = (100,100,100)):
        self.name = name
        self.game = game
        self.initial_position = border_position
        self.initial_ratio = border_ratio #(width, height)
        self.level = level
        self.type = widget_type
        self.border = None
        self.rect = None

        self.font_name = font_name
        self.font = None
        self.text_color = text_color
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.text_surface = None
        self.text_rect = None
        self.widget_setting()

        self.hovered = False
        self.action = False

    def widget_setting(self):
        self.border = pygame.Surface((self.initial_ratio[0] * self.game.screen_scale, self.initial_ratio[1] * self.game.screen_scale))  ##DRAW BORDER
        self.border.fill(self.color)
        self.rect = self.border.get_rect()
        self.rect.x = (self.initial_position[0]*self.game.screen_scale) + self.game.screen_start[0]
        self.rect.y = (self.initial_position[1]*self.game.screen_scale) + self.game.screen_start[1]
        self.font = pygame.font.SysFont(self.font_name, int(self.initial_ratio[1] * self.game.screen_scale ))
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)


    def check_hover(self, event):
        self.hovered = False
        if (self.rect.x <= event.mouse_position[0] <= self.rect.x + self.initial_ratio[0] * self.game.screen_scale and
            self.rect.y <= event.mouse_position[1] <= self.rect.y + self.initial_ratio[1] * self.game.screen_scale):
            self.hovered = True

    def update(self, event, game_level):
        self.action = False
        if game_level != self.level:
            return

        if self.type == "button":
            self.check_hover(event)
        if self.hovered is True and event.mouse_click(1):
            self.action = True

    def draw(self, screen, game_level):
        if game_level != self.level:
            return
        if self.hovered is True:
            self.border.fill(self.hover_color)
        else :
            self.border.fill(self.color)
        screen.blit(self.border, ((self.initial_position[0]*self.game.screen_scale) + self.game.screen_start[0],
                                 (self.initial_position[1]*self.game.screen_scale) + self.game.screen_start[1]))
        screen.blit(self.text_surface, self.text_rect)



