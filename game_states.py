import math
import pygame
from config import Config
from event_handle import event_object
from overlay import *
from Sprite_handle import SpriteHandler
from Enemy_factory import BossFactory
from chickfight_player import *

class GameState:
    def __init__(self, game):
        self.game = game # game object
        self.current_level = 0
        self.change_level = False
        # self.game_level = None
        self.button_list = []
        self.main_overlay = dict()
        self.timer_ms = 0
        self.frame_animation = 0
        self.image = None

    def animated(self, screen):
        screen.fill((0, 0, 0))
        if self.frame_animation > len(self.bg_animation[self.game_level[self.current_level]][0])-1:
            self.frame_animation = 0
        self.image = self.bg_animation[self.game_level[self.current_level]][0][self.frame_animation]
        screen.blit(self.image, self.game.screen_start)

    def asset_update(self):
        self.load_sprite(self.sprites_key)
        if len(self.button_list) != 0:
            for each_button in self.button_list:
                each_button.button_setting()
        if len(self.main_overlay) != 0:
            for each_overlay in self.main_overlay.values():
                each_overlay.setting()

    def update_state(self, frame, ms_per_loop, event):
        pass

    def draw_state(self, screen, event):
        pass

    def clean_state(self):
        pass

    def exit(self):
        pass

    def enter(self, to_level):
        pass

    def level_switch(self, new_level=0):
        pass

class Menu(GameState):
    sprites_key = {"Title_screen":[[3, 0, 0, 320, 180]], "Main_menu":[[3, 0, 1, 320, 180]],
                    "Statistic":[[2, 0, 2, 320, 180]], "name":[[1, 1, 0, 320, 180]]}

    def __init__(self, game):
        super().__init__(game)
        self.game_level = {0:"Title_screen", 1:"Main_menu", 2:"Statistic", 4:"name"}
        self.sprite_dir = "sprites\\menu_state_screen.png"
        self.bg_animation = dict()
        self.image = None
        self.frame_animation = 0
        self.font = None
        self.build_asset()
        self.ms_per_frame = 500



    def load_sprite(self, sprites_key):
        Menu_sprite = SpriteHandler(pygame.image.load(self.sprite_dir))
        self.bg_animation = Menu_sprite.pack_sprite(sprites_key, self.game.screen_scale)
        self.frame_animation = 0
        self.image = self.bg_animation[self.game_level[self.current_level]][0][self.frame_animation]

    def exit(self):
        self.current_level = 0

    def enter(self, to_level):
        self.game.round += 1
        self.game.data_record.export_to_csv("game_data.csv")

        if to_level == 4:
            self.current_level = 4
        else:
            self.current_level = 0

    def asset_update(self):
        self.font = pygame.font.Font(None, int(12 * self.game.screen_scale))
        self.load_sprite(self.sprites_key)
        if len(self.button_list) != 0:
            for each_button in self.button_list:
                each_button.button_setting()
        if len(self.main_overlay) != 0:
            for each_overlay in self.main_overlay.values():
                each_overlay.setting()

    def build_asset(self):
        self.font = pygame.font.Font(None, int(12*self.game.screen_scale))
        self.load_sprite(self.sprites_key)
        self.button_list.append(Button("start_game", self.game, (160,60), (136,22),
                                       1, "start",
                                       command= lambda:self.game.state_manager.set_state("Gameplay", 0)))
        self.button_list.append(Button("statistic", self.game, (160,90), (136,22),
                                       1, "statistic",
                                       command= lambda:self.game.open_stat_window()))


    def draw_state(self, screen, event):
        if self.current_level == 4:
            return

        self.animated(screen)
        if self.current_level == 1:
            font = pygame.font.Font(None, int(20*self.game.screen_scale))
            name = font.render(f"FIGHT THEM : {self.game.nickname} !!!", True, (255, 255, 255))
            screen.blit(name, (50 * self.game.screen_scale + self.game.screen_start[0],
                               120 * self.game.screen_scale+ self.game.screen_start[1]))

        for button in self.button_list:
            button.draw(screen, self.current_level)


    def key_handle(self, event):
        if self.current_level == 0:
            if len(event.key_press) != 0 or len(event.mouse_button) != 0:
                event.reset_event("mouse_pos")
                self.level_switch(1)

    def update_state(self, frame, ms_per_loop, event):
        if self.current_level == 4:
            self.timer_ms += ms_per_loop
            self.game.window.fill((0,0,0))
            prompt = self.font.render("Enter your nickname:", True, (255, 255, 255))
            name_render = self.font.render(self.game.nickname, True, (0, 255, 0))
            self.game.window.blit(prompt, (100 * self.game.screen_scale + self.game.screen_start[0],
                                           60 * self.game.screen_scale + self.game.screen_start[1]))
            self.game.window.blit(name_render, (100* self.game.screen_scale + self.game.screen_start[0],
                                            70 * self.game.screen_scale + self.game.screen_start[1]))

            for key in list(event.key_press):
                if event.is_keypress(pygame.K_RETURN):
                    self.timer_ms = 0
                    self.game.data["name"] = self.game.nickname
                    self.game.overlay_manager.add_overlay(TransitionHalf(self.game, 32,16,
                                                                         command=lambda :self.level_switch(0)))
                    break
                if self.timer_ms >= 150:
                    if event.is_keypress(pygame.K_BACKSPACE):
                        self.game.nickname = self.game.nickname[:-1]
                    else:
                        char = event.key_to_char(key)
                        if char:
                            self.game.nickname += char
                    self.timer_ms = 0

        self.timer_ms += ms_per_loop
        if self.timer_ms >= self.ms_per_frame:
            self.timer_ms -= self.ms_per_frame
            self.frame_animation += 1
        self.key_handle(event)
        for button in self.button_list:
            button.update(event, self.current_level)

    def level_switch(self, new_level=0):
        self.frame_animation = 0
        self.current_level = new_level


class Gameplay(GameState):
    sprites_key = {"dummy":[[2, 0, 1, 320, 180]], "Boss1":[[4, 0, 0, 320, 180]], "Boss2":[[4, 0, 0, 320, 180]],
                   "Game_over":[[1, 3, 1, 320, 180]], "Winning":[[3, 0, 2, 320, 180]]}

    def __init__(self, game):
        super().__init__(game)

        self.sprite_dir = "sprites\\scale1-screen.png"
        self.bg_animation = dict()
        self.image = None
        self.frame_animation = 0

        self.game_level = {0:"dummy", 1:"Boss1", 2:"Boss2", 3:"Game_over", 4:"Winning"}
        self.death_list = []
        self.kill_require = {"dummy":1,"Boss1":1,"Boss2":1,"Game_over":3, 4:"Winning"}
        self.kill_count = 0
        self.enemy_factory = BossFactory(game, self)
        self.ms_per_frame = 500
        self.main_overlay = dict()
        self.build_asset()
        self.pause = False
        self.game_over = False

    def enter(self, to_level):
        self.pause = False
        self.game.player = Player([0, self.game.arena_area["end_y"] / 2], game=self.game,
                                  name=self.game.nickname)
        self.game.player.status = "enter_arena"
        self.enemy_factory.already_create = False

        self.game.entities_group.add(self.game.player)
        self.main_overlay["player_health"] = HealthBarOverlay(self.game, self.game.player)
        self.main_overlay["timer"] = TimerOverlay(self.game, (150, 20), (45, 15))

        self.game.overlay_manager.add_overlay(self.main_overlay["player_health"])
        self.game.overlay_manager.add_overlay(self.main_overlay["timer"])

    def key_handle(self, event):
        if event.is_keypress(pygame.K_e):
            if self.pause is True:
                self.pause = False
            else :
                self.pause = True

    def exit(self):
        self.current_level = 0
        self.game.entities_group.empty()
        self.game.attack_group.empty()
        self.death_list = []
        for each in self.main_overlay.values():
            self.game.overlay_manager.remove_overlay(each)
        self.main_overlay = dict()


    def load_sprite(self, sprites_key):
        Map_sprite = SpriteHandler(pygame.image.load(self.sprite_dir))
        self.bg_animation = Map_sprite.pack_sprite(sprites_key, self.game.screen_scale)
        self.image = self.bg_animation[self.game_level[self.current_level]][0][self.frame_animation]

    def build_asset(self):
        self.load_sprite(self.sprites_key)
        self.button_list.append(Button("next_level", self.game, (280, 150), (15, 15),
                                       0, "GO", command= lambda: self.game.overlay_manager.add_overlay(
                                        TransitionHalf(self.game, 32,16,
                                        command=lambda :self.level_switch(1)))))
        self.button_list.append(Button("exit", self.game, (10,165), (10,10), 0,
                                       "<<", command=lambda:self.game.overlay_manager.add_overlay(
                                        Transition(self.game, 10, 20,
                                        command=lambda: self.game.state_manager.set_state("Menu",0))),level_set=[1,2]))
        self.button_list.append(Button("loss", self.game, (150,125), (150,20), 3,
                                       "exit", command=lambda:self.game.overlay_manager.add_overlay(
                                        Transition(self.game, 10, 20,
                                        command=lambda: self.game.state_manager.set_state("Menu",0))),level_set=[3,4]))

    def draw_state(self, screen, event):
        if self.pause is True:
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((128, 128, 128, 150))
            screen.blit(overlay, (self.game.screen_start[0], self.game.screen_start[1]))
        if self.current_level != 3:
            self.animated(screen)
            self.game.entities_group.draw(self.game.window)
            self.game.attack_group.draw(self.game.window)
        elif self.current_level == 3:
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0))
            font = pygame.font.Font(None, int(20*self.game.screen_scale))
            text = font.render(f"GAME OVER", True, (255, 255, 255))
            overlay.set_alpha(10)
            screen.blit(overlay, (self.game.screen_start[0], self.game.screen_start[1]))
            screen.blit(text, (100 * self.game.screen_scale + self.game.screen_start[0]
                                   , 70 * self.game.screen_scale + self.game.screen_start[1]))

        for button in self.button_list:
            button.draw(screen, self.current_level)


    def update_state(self, frame, ms_per_loop, event):

        self.key_handle(event)
        for button in self.button_list:
            button.update(event, self.current_level)
        if self.pause is True or self.current_level == 3:
            return

        self.timer_ms += ms_per_loop
        if self.timer_ms >= self.ms_per_frame:
            self.timer_ms -= self.ms_per_frame
            self.frame_animation += 1

        self.enemy_factory.create_boss(self.current_level)
        self.game.entities_group.update(frame, ms_per_loop, self.game.attack_group, event_object)
        self.game.attack_group.update(frame, ms_per_loop, self.game.attack_group)
        Config.check_attack_collision(self.game.attack_group, self.game.entities_group)
        if self.current_level != 4:
            self.check_kill(frame)

    def asset_update(self):
        self.load_sprite(self.sprites_key)
        if len(self.button_list) != 0:
            for each_button in self.button_list:
                each_button.button_setting()
        if len(self.main_overlay) != 0:
            for each_overlay in self.main_overlay.values():
                each_overlay.setting()

    def check_kill(self, frame):
        if frame != 1:
            return

        for each in self.game.entities_group:
            if each.death is True and each not in self.death_list:
                if each == self.game.player:
                    self.main_overlay["timer"].start_timer = False
                    self.game.data["success_defeat"].append([self.game.round, self.current_level-1])
                    self.game.data["score"].append([self.game.round, 0])
                    self.level_switch(3)
                else :
                    self.death_list.append(each)

        if len(self.death_list) == self.kill_require[self.game_level[self.current_level]]:
            if self.current_level != 2:
                self.level_switch(self.current_level+1)
            else :
                self.main_overlay["timer"].start_timer = False
                self.game.data["health_remain"].append([self.game.round, self.game.player.health])
                self.game.data["success_defeat"].append([self.game.round, 2])
                self.game.data["win_in"].append([self.game.round, self.main_overlay["timer"].elapsed_time])
                score_value = round((4 * self.game.player.health) - (self.main_overlay["timer"].elapsed_time / 500), 2)
                self.game.data["score"].append((self.game.round, score_value))
                self.game.overlay_manager.add_overlay(Transition(self.game, 10, 20,
                                                                 command=lambda: self.level_switch(4)))



    def level_switch(self, next_level=0):
        self.enemy_factory.already_create = False
        self.current_level = next_level

        if next_level == 1:
            self.main_overlay["timer"].start_timer = True
            for each in self.game.entities_group:
                if each != self.game.player:
                    self.game.entities_group.remove(each)
            self.current_level = 1
            self.enemy_factory.already_create = False
            self.game.attack_group.empty()
        elif next_level == 2:
            for each in self.game.entities_group:
                if each != self.game.player:
                    self.death_list.remove(each)
                    self.game.entities_group.remove(each)
            self.game.overlay_manager.remove_overlay(self.main_overlay["enemy1_health"])
            self.current_level = 2
            self.enemy_factory.already_create = False
