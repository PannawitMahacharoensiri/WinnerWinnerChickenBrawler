from chickfight_player import Player
from event_handle import event_object
from Sprite_handle import *
from config import *
import pygame
import math
from game_states import *

class Main:
    def __init__(self):
        pygame.init()
        self.tracker1 = pygame.time.get_ticks()
        self.tracker2 = None
        self.clock = pygame.time.Clock()
        self.program_running = True
        self.player = None
        self.entities_group = EntitiesGroup()
        self.attack_group = pygame.sprite.Group()

        self.debug_mode = True
        self.before_scale = None
        self.screen_scale = 1
        self.change_size = {"window":False, "screen":False}
        self.screen_info = (320 * self.screen_scale, 180 * self.screen_scale)#(256*self.screen_scale, 144*self.screen_scale)
        self.window = pygame.display.set_mode(self.screen_info, pygame.RESIZABLE)
        self.screen_start = (0,0)
        self.screen_start_before = self.screen_start

        self.arena_area = {"start_x":self.screen_start[0] + (32 * self.screen_scale),
                           "end_x": self.screen_start[0] + self.screen_info[0] - (32 * self.screen_scale),
                           "start_y":self.screen_start[1] + (24 * self.screen_scale),
                           "end_y": self.screen_start[1] + self.screen_info[1] - (4 * self.screen_scale)}  # ([start_x,end_x],[start_y, end_y])

        pygame.display.set_caption('Winner Winner Chicken Brawler')
        self.game_state = dict()
        self.current_state = "Menu"
        self.all_frame = 0

    def get_frame(self):
        frame = 0
        if self.tracker2 - self.tracker1 >= Config.frame_delay:
            frame = 1
            self.tracker1 = self.tracker2
        return frame

    def change_window_size(self, new_size):
        self.screen_start_before = self.screen_start
        self.before_scale = self.screen_scale
        result_change_ratio = Config.screen_ratio(new_size, self.screen_scale)

        if result_change_ratio[0] is True:
            self.change_size["screen"] = result_change_ratio[0]
            self.screen_info = result_change_ratio[1]
            self.screen_scale = result_change_ratio[2]
        valid_window = Config.window_to_screen(new_size, self.screen_info)
        self.window = pygame.display.set_mode(valid_window, pygame.RESIZABLE)
        self.screen_start = ((round(valid_window[0] - self.screen_info[0]) / 2),
                             (round(valid_window[1] - self.screen_info[1]) / 2))
        self.arena_area = {"start_x":self.screen_start[0] + (32 * self.screen_scale),
                           "end_x": self.screen_start[0] + self.screen_info[0] - (32 * self.screen_scale),
                           "start_y":self.screen_start[1] + (24 * self.screen_scale),
                           "end_y": self.screen_start[1] + self.screen_info[1] - (4 * self.screen_scale)}

        if self.screen_start != self.screen_start_before:
            self.change_size["window"] = True

        if True in self.change_size.values():
            self.change_sprite_scale()

    def change_sprite_scale(self):
        # print(f"Here is screen_scale {self.screen_scale}, Here screen info {self.screen_info}")
        if self.change_size["window"] is True:
            for each in self.entities_group:
                each.rect.x += self.screen_start[0] - self.screen_start_before[0]
                each.rect.y += self.screen_start[1] - self.screen_start_before[1]
            for each_attack in self.attack_group:
                each_attack.rect.x += self.screen_start[0] - self.screen_start_before[0]
                each_attack.rect.y += self.screen_start[1] - self.screen_start_before[1]
        if self.change_size["screen"] is True:
            for each in self.entities_group:
                location = (each.rect.x, each.rect.y)
                each.load_sprite(each.sprites_key)
                each.rect.x = (location[0]/self.before_scale) * self.screen_scale
                each.rect.y = (location[1]/self.before_scale) * self.screen_scale
            for each_attack in self.attack_group:
                attack_location = (each_attack.rect.x, each_attack.rect.y)
                each_attack.change_scale(self.screen_scale)
                each_attack.rect.x = (attack_location[0]/self.before_scale) * self.screen_scale
                each_attack.rect.y = (attack_location[1]/self.before_scale) * self.screen_scale
            ## UPDATE TO EVERY STATE NOW
            for each_state in self.game_state.values():
                each_state.load_assert()
                if len(each_state.button_list) != 0:
                    for each_button in each_state.button_list:
                        each_button.widget_setting()
        # reset the value
        self.change_size = {"window":False, "screen":False}

    def main_loop(self):
        background = pygame.transform.scale(pygame.image.load("sprites\\scale1-screen.png"),self.screen_info)  # depend on game state

        ## ENTITIES CREATION WILL SEE HOW I BUILD BOSS LATER: may be check len(self.entities_group) need to > 1
        self.player = Player(self.screen_info, game = self, name="jim")
        self.entities_group.add(self.player)

        # build state (contain all level all button in that state)
        self.game_state["Menu"] = Menu(self)
        self.game_state["Gameplay"] = Gameplay(self, background)
        self.game_state["transition"] = ScreenTransition(self)

        while self.program_running:
            self.clock.tick(Config.game_fps)
            self.tracker2 = pygame.time.get_ticks()
            frame = self.get_frame()
            self.all_frame += frame

            ##KEYPRESS OF MAINLOOP
            keys = pygame.key.get_pressed()
            if event_object.quit_press():
                self.program_running = False
            if event_object.is_keypress(pygame.K_q):
                show_health = []
                for i in self.entities_group.sprites():
                    show_health.append(i.health)
                print(show_health)
            if keys[pygame.K_LSHIFT] and event_object.is_keypress(pygame.K_1):
                if self.debug_mode is True:
                    self.debug_mode = False
                else :
                    self.debug_mode = True
            if self.current_state == "Gameplay":
                if self.debug_mode is True:
                    Config.open_debug(self.window, self.player, event_object.mouse_position)

            # self.change_state(event_object)
            self.game_state[self.current_state].update_state(frame, event_object)
            self.game_state[self.current_state].draw_state(frame, event_object)

            event_object.update_event(self)
            # if True in self.change_size.values() :
            #     self.change_sprite_scale()
            pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    main = Main()
    main.main_loop()
