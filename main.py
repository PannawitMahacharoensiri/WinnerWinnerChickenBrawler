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
        self.screen_scale = 4
        self.change_size = {"window":False, "screen":False}
        self.screen_info = (256*self.screen_scale, 144*self.screen_scale)
        self.window = pygame.display.set_mode(self.screen_info, pygame.RESIZABLE)
        self.screen_start = (0,0)
        self.screen_start_before = self.screen_start

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

    def change_state(self, event):
        if self.current_state == "Menu" and event.key_press != set():
            self.current_state = "Gameplay"
        if self.current_state == "Gameplay" and event.is_keypress(pygame.K_e):
            self.current_state = "Menu"

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
            for each_button in self.game_state[self.current_state].button_list:
                each_button.widget_setting()
        # reset the value
        self.change_size = {"window":False, "screen":False}

    def main_loop(self):
        background = pygame.transform.scale(pygame.image.load("sprites\\grass.jpg"),self.screen_info)  # depend on game state

        ## ENTITIES CREATION WILL SEE HOW I BUILD BOSS LATER: may be check len(self.entities_group) need to > 1
        self.player = Player(self.screen_info, game = self, name="jim")
        self.entities_group.add(self.player)

        self.game_state["Menu"] = Menu(self)
        self.game_state["Gameplay"] = Gameplay(self, background)

        while self.program_running:
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
            self.game_state[self.current_state].update_screen(frame, event_object)
            self.game_state[self.current_state].draw_screen(frame, event_object)

            event_object.update_event(self)
            self.clock.tick(60)
            if True in self.change_size.values() :
                self.change_sprite_scale()
            pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    main = Main()
    main.main_loop()
