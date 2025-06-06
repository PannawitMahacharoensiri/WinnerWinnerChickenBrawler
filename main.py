from chickfight_player import Player
from event_handle import event_object
from state_management import *
from config import *
import pygame
import math
from game_states import *
from information_record import *
from tkinter_opener import *

class Main:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.game_fps = 60
        self.tracker1 = 0
        self.ms_per_1frame = 250
        self.nickname = ""
        self.round = 0

        self.program_running = True
        self.player = None
        self.entities_group = EntitiesGroup()
        self.attack_group = pygame.sprite.Group()

        self.data = {"name":"", "success_defeat":[], "health_remain":[], "win_in":[], "score":[]}
        self.debug_mode = True
        self.before_scale = None
        self.screen_scale = 3
        self.change_size = {"window":False, "screen":False}
        self.screen_info = (320 * self.screen_scale, 180 * self.screen_scale)
        self.window = pygame.display.set_mode(self.screen_info, pygame.RESIZABLE)
        pygame.display.set_caption('Winner Winner Chicken Brawler')
        self.screen_start = (0,0)
        self.screen_start_before = self.screen_start
        self.arena_area = {"start_x":self.screen_start[0] + (32 * self.screen_scale),
                           "end_x": self.screen_start[0] + self.screen_info[0] - (32 * self.screen_scale),
                           "start_y":self.screen_start[1] + (24 * self.screen_scale),
                           "end_y": self.screen_start[1] + self.screen_info[1] - (4 * self.screen_scale)}
        self.state_manager = GameStateManage(self)
        self.overlay_manager = OverlayManage()
        self.data_record = GameDataExporter(self.data)

    def get_global_frame(self, ms_per_loop):
        frame = 0
        self.tracker1 += ms_per_loop
        if self.tracker1 >= self.ms_per_1frame:
            frame = 1
            self.tracker1 -= self.ms_per_1frame
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

    @staticmethod
    def open_stat_window():
        window = GameDataViewer("game_data.csv")
        window.mainloop()

    def change_sprite_scale(self):
        if self.change_size["window"] is True:
            if self.player is not None:
                self.player.rect.x += (self.screen_start[0] - self.screen_start_before[0])/self.screen_scale
                self.player.rect.y += (self.screen_start[1] - self.screen_start_before[1])/self.screen_scale
            for each in self.entities_group:
                if each != self.player:
                    each.rect.x += (self.screen_start[0] - self.screen_start_before[0])/self.screen_scale
                    each.rect.y += (self.screen_start[1] - self.screen_start_before[1])/self.screen_scale
            for each_attack in self.attack_group:
                each_attack.rect.x += (self.screen_start[0] - self.screen_start_before[0])/self.screen_scale
                each_attack.rect.y += (self.screen_start[1] - self.screen_start_before[1])/self.screen_scale
        if self.change_size["screen"] is True:
            if self.player is not None:
                player_location = (self.player.rect.x, self.player.rect.y)
                self.player.load_sprite(self.player.sprites_key)
                self.player.rect.x = (player_location[0] / self.before_scale) * self.screen_scale
                self.player.rect.y = (player_location[1] / self.before_scale) * self.screen_scale
            for each in self.entities_group:
                if each != self.player:
                    location = (each.rect.x, each.rect.y)
                    each.load_sprite(each.sprites_key)
                    each.rect.x = (location[0]/self.before_scale) * self.screen_scale
                    each.rect.y = (location[1]/self.before_scale) * self.screen_scale
            for each_attack in self.attack_group:
                attack_location = (each_attack.rect.x, each_attack.rect.y)
                each_attack.change_scale(self.screen_scale)
                each_attack.rect.x = (attack_location[0]/self.before_scale) * self.screen_scale
                each_attack.rect.y = (attack_location[1]/self.before_scale) * self.screen_scale
        if self.state_manager.current_state == "Gameplay":
            self.player.rect.x, self.player.rect.y, hit_wall, direct = Config.check_boundary(self.player, self.arena_area)
            for each in self.entities_group:
                if each.status != "enter_arena":
                    each.rect.x, each.rect.y, hit_wall, hit_dir = Config.check_boundary(each, self.arena_area)

        self.state_manager.resize()
        self.change_size = {"window":False, "screen":False}

    def main_loop(self):
        self.state_manager.register_state("Menu",Menu(self))
        self.state_manager.register_state("Gameplay", Gameplay(self))
        self.state_manager.set_state("Menu", 4)

        while self.program_running:
            ms_per_loop = self.clock.tick(self.game_fps)
            frame = self.get_global_frame(ms_per_loop)

            keys = pygame.key.get_pressed()
            if event_object.quit_press():
                self.program_running = False
            if event_object.is_keypress(pygame.K_q):
                show_health = []
                for i in self.entities_group.sprites():
                    show_health.append(i.health)
                print(show_health)
            if self.overlay_manager.block_update is False:
                self.state_manager.update(frame, ms_per_loop, event_object)
            self.overlay_manager.update(ms_per_loop)
            self.state_manager.draw(self.window, event_object)
            self.overlay_manager.draw(self.window)

            event_object.update_event(self)
            pygame.display.update()
        pygame.quit()


if __name__ == '__main__':
    main = Main()
    main.main_loop()
