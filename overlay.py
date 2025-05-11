import math

import pygame
from config import Config

class Overlay:
    def __init__(self):
        self.blocker = False
        self.timer_ms = 0

    def update_overlay(self, ms_per_loop):
        pass  # Only used for blocking overlays

    def draw_overlay(self, screen):
        pass

    def setting(self):
        pass

    def reset(self):
        pass

class HealthBarOverlay(Overlay):
    def __init__(self, game,entity, position=(10, 10), border_ratio=(80, 8), color=(0, 255, 0), border_color=(0, 0, 0)):
        super().__init__()
        self.game = game
        self.entity = entity
        self.initial_position = position
        self.position = None
        self.initial_ratio = border_ratio
        self.size = None
        self.color = color
        self.border_color = border_color
        self.setting()

    def setting(self):
        self.size = (self.initial_ratio[0] * self.game.screen_scale,self.initial_ratio[1] * self.game.screen_scale)  ##DRAW BORDER
        self.position = ((self.initial_position[0] *self.game.screen_scale) + self.game.screen_start[0],
                         ((self.initial_position[1]) *self.game.screen_scale) + self.game.screen_start[1])

    def update_overlay(self, ms_per_loop):
        pass  # You can animate here later if needed

    def draw_overlay(self, screen):
        # Bar dimensions
        bar_x, bar_y = self.position
        bar_width = int((self.entity.health / self.entity.max_health) * self.size[0])
        bar_height = self.size[1]

        # Draw background (optional: gray)
        pygame.draw.rect(screen, (100, 100, 100), (bar_x, bar_y, self.size[0], bar_height))

        # Draw filled health
        pygame.draw.rect(screen, self.color, (bar_x, bar_y, bar_width, bar_height))

        # Draw border
        pygame.draw.rect(screen, self.border_color, (bar_x, bar_y, self.size[0], bar_height), 2)


class TimerOverlay(Overlay):
    def __init__(self, game, border_position, border_ratio,
                 font_name = None, text_color= (255,255,255)):
        super().__init__()
        self.game = game
        self.blocker = False
        self.font_name = font_name
        self.font = None
        self.initial_position = border_position
        self.elapsed_time = 0      # in ms
        self.finished = False
        self.start_timer = False
        self.initial_ratio = border_ratio #(width, height)
        self.border = None
        self.rect = None
        self.text_color = text_color
        self.text_surface = None
        self.text_rect = None
        self.time = None

        self.setting()

    def reset(self):
        self.elapsed_time = 0

    def update_overlay(self, ms_per_loop):
        if self.finished is False:
            if self.start_timer is True:
                self.elapsed_time += ms_per_loop
        if self.elapsed_time < 60000:
            time_in_sec = self.elapsed_time / 1000
            self.time = f"{time_in_sec:.2f}s"
        else :
            total_seconds = self.elapsed_time / 1000
            minutes = int(total_seconds // 60)
            seconds = total_seconds % 60
            self.time = f"{minutes:02}:{seconds:05.2f}m"

    def draw_overlay(self, screen):
        self.text_surface = self.font.render(self.time, True, self.text_color)
        screen.blit(self.border, (self.rect.x, self.rect.y))
        screen.blit(self.text_surface, self.text_rect)

    def setting(self):
        self.font = pygame.font.SysFont(self.font_name, int(15*self.game.screen_scale))
        self.border = pygame.Surface((self.initial_ratio[0] * self.game.screen_scale,
                                      self.initial_ratio[1] * self.game.screen_scale))  ##DRAW BORDER
        self.border.set_colorkey((0, 0, 0))
        self.rect = self.border.get_rect()
        self.rect.x = ((self.initial_position[0]-(self.initial_ratio[0]/2))
                       *self.game.screen_scale) + self.game.screen_start[0]
        self.rect.y = ((self.initial_position[1]-(self.initial_ratio[1]/2))
                       *self.game.screen_scale) + self.game.screen_start[1]
        time_in_sec = self.elapsed_time / 1000
        self.text_surface = self.font.render(f"{time_in_sec:.2f}s", True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)


class Dialog(Overlay):
    def __init__(self):
        super().__init__()
        self.blocker = True

class Transition(Overlay):
    def __init__(self, game, ms_per1_update, initial_box_size=32, command=None, color=(0,0,0)):
        super().__init__()
        self.game = game
        self.blocker = True
        self.initial_box_size = initial_box_size
        self.ms_per_1update = ms_per1_update
        self.box_size = None
        self.valid_level = []

        self.box_number = {"width":0, "height":0}
        self.grid = None
        self.current_x = 0
        self.current_y = 0

        self.image = None
        self.color = color

        self.state = "fade_in"
        self.finish = {"fade_in":False, "fade_out":False}
        self.command = command

        self.setting()

    def reset(self):
        self.timer_ms = 0
        self.current_y = 0
        self.current_x = 0
        self.state = "fade_in"
        self.finish = {"fade_in": False, "fade_out": False}

    def setting(self):
        self.box_size = self.initial_box_size * self.game.screen_scale
        self.box_number["width"] = math.ceil(self.game.screen_info[0]/ self.box_size)
        self.box_number["height"] = math.ceil(self.game.screen_info[1]/ self.box_size)
        self.grid = []
        for height in range(self.box_number["height"]):
            start_grid = []
            for width in range(self.box_number["width"]):
                start_grid.append(0)
            self.grid.append(start_grid)

        self.image = pygame.Surface((math.ceil(self.box_size),math.ceil(self.box_size)))
        self.image.fill(self.color)

    def transition_update(self):
        if self.finish[self.state] is True:
            if self.state == "fade_in":
                if self.command is not None:
                    self.command()
                self.state = "fade_out"
                self.current_y = 0
                self.current_x = 0
            elif self.state == "fade_out":
                self.reset()
                self.game.overlay_manager.remove_overlay(self)

        if self.state == "fade_in" and self.finish[self.state] is False:
            self.grid[self.current_y][self.current_x] = 1
            if self.current_x < self.box_number["width"]-1:
                self.current_x += 1
            else :
                self.current_x = 0
                self.current_y += 1
            if self.current_x == 0 and self.current_y == self.box_number["height"]:
                self.finish["fade_in"] = True
        elif self.state == "fade_out" and self.finish[self.state] is False:
            self.grid[self.current_y][self.current_x] = 0
            if self.current_x < self.box_number["width"]-1:
                self.current_x += 1
            else :
                self.current_x = 0
                self.current_y += 1
            if self.current_x == 0 and self.current_y == self.box_number["height"]:
                self.finish["fade_out"] = True

    def update_overlay(self, ms_per_loop):
        self.timer_ms += ms_per_loop
        if self.timer_ms >= self.ms_per_1update:
            self.timer_ms -= self.ms_per_1update
            self.transition_update()

        # Only used for blocking overlays

    def draw_overlay(self, screen):
        for box_x in range(self.box_number["width"]):
            for box_y in range(self.box_number["height"]):
                if self.grid[box_y][box_x] == 1:
                    screen.blit(self.image,(box_x * self.box_size + self.game.screen_start[0], box_y * self.box_size + self.game.screen_start[1]))

class TransitionHalf(Transition):
    def __init__(self, game, ms_per1_update, initial_box_size=32, command=None, color=(0,0,0)):
        super().__init__(game, ms_per1_update,initial_box_size, command, color)

    def transition_update(self):
        if self.finish[self.state] is True:
            if self.state == "fade_in":
                if self.command is not None:
                    self.command()
                self.state = "fade_out"
                self.current_y = 0
                self.current_x = 0
            elif self.state == "fade_out":
                self.reset()
                self.game.overlay_manager.remove_overlay(self)

        if self.state == "fade_in" and self.finish[self.state] is False:
            for each in range(self.box_number["height"]):
                self.grid[each][self.current_x] = 1
            if self.current_x < self.box_number["width"]-1:
                self.current_x += 1
            else :
                self.finish["fade_in"] = True
        elif self.state == "fade_out" and self.finish[self.state] is False:
            for each in range(self.box_number["height"]):
                self.grid[each][self.current_x] = 0
            if self.current_x < self.box_number["width"]-1:
                self.current_x += 1
            else :
                self.finish["fade_out"] = True




class Button:

    def __init__(self, name, game, border_position, border_ratio, level, text, command,
                 font_name = None, text_color= (0,0,0), color = (255,255,255) ,hover_color = (100,100,100)):
        self.name = name
        self.game = game
        self.initial_position = border_position
        self.initial_ratio = border_ratio #(width, height)
        self.level = level
        self.border = None
        self.rect = None

        self.font_name = font_name
        self.font = None
        self.text_color = text_color
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.command = command

        self.text_surface = None
        self.text_rect = None
        self.button_setting()
        self.hovered = False


    def button_setting(self):
        self.border = pygame.Surface((self.initial_ratio[0] * self.game.screen_scale,
                                      self.initial_ratio[1] * self.game.screen_scale))  ##DRAW BORDER
        self.border.fill(self.color)
        self.rect = self.border.get_rect()
        self.rect.x = ((self.initial_position[0]-(self.initial_ratio[0]/2))
                       *self.game.screen_scale) + self.game.screen_start[0]
        self.rect.y = ((self.initial_position[1]-(self.initial_ratio[1]/2))
                       *self.game.screen_scale) + self.game.screen_start[1]
        self.font = pygame.font.SysFont(self.font_name, int(self.initial_ratio[1] * self.game.screen_scale ))
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)


    def check_hover(self, event):
        self.hovered = False
        if (self.rect.x <= event.mouse_position[0] <= self.rect.x + self.initial_ratio[0] * self.game.screen_scale and
            self.rect.y <= event.mouse_position[1] <= self.rect.y + self.initial_ratio[1] * self.game.screen_scale):
            self.hovered = True

    def update(self, event, game_level):
        # self.action = False
        if game_level == self.level:
            self.check_hover(event)
            if self.hovered is True and event.mouse_click(1):
                self.command()

    def draw(self, screen, game_level):
        if game_level == self.level:
            if self.hovered is True:
                self.border.fill(self.hover_color)
            else :
                self.border.fill(self.color)
            screen.blit(self.border, (self.rect.x,self.rect.y))
            screen.blit(self.text_surface, self.text_rect)
