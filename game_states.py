import math

import pygame
from config import Config
from event_handle import event_object
from overlay import *
from Sprite_handle import SpriteHandler
from Enemy_factory import BossFactory

# @abstractproperty
class GameState:
    def __init__(self, game):
        self.game = game # game object
        self.current_level = 0
        self.change_level = False
        # self.game_level = None
        self.button_list = []
        self.overlay_dict =dict()
        self.timer_ms = 0

    def asset_update(self):
        self.load_sprite(self.sprites_key)
        if len(self.button_list) != 0:
            for each_button in self.button_list:
                each_button.button_setting()
        if len(self.overlay_dict) != 0:
            for each_overlay in self.overlay_dict.values():
                each_overlay.setting()

    def update_state(self, frame, ms_per_loop, event):
        pass

    def draw_state(self, screen, event):
        pass

    def clean_state(self):
        pass

    def exit(self):
        pass

    def enter(self, level):
        pass

    def level_switch(self, new_level=0):
        pass

########################################################################################################################

class Menu(GameState):
    sprites_key = {"Title_screen":[[1, 4, 0, 320, 180]], "Main_menu":[[1, 4, 0, 320, 180]],
                   "Pause":[[1, 4, 0, 320, 180]], "Game_over":[[1, 4, 0, 320, 180]]}

    def __init__(self, game):
        super().__init__(game)
        self.game_level = {0:"Title_screen", 1:"Main_menu", 2:"Pause", 3:"Game_over"}
        self.sprite_dir = "sprites\\scale1-screen - animated.png"
        self.bg_animation = dict()
        self.image = None
        self.frame_animation = 0
        self.build_asset()

    def load_sprite(self, sprites_key):
        Menu_sprite = SpriteHandler(pygame.image.load(self.sprite_dir))
        self.bg_animation = Menu_sprite.pack_sprite(sprites_key, self.game.screen_scale)
        self.image = self.bg_animation[self.game_level[self.current_level]][0][self.frame_animation]

    def asset_update(self):
        self.load_sprite(self.sprites_key)
        if len(self.button_list) != 0:
            for each_button in self.button_list:
                each_button.button_setting()
        if len(self.overlay_dict) != 0:
            for each_overlay in self.overlay_dict.values():
                each_overlay.setting()

    def build_asset(self):
        self.load_sprite(self.sprites_key)
        self.button_list.append(Button("start_game", self.game, (160,60), (136,22),
                                       0, "start",
                                       command= lambda:self.game.state_manager.set_state("Gameplay")))
        # self.button_list.append(Widget("menu_start_game" , self.game, (65,52), (136,22),
        #                            0, "Start", widget_type="button"))
        # self.button_list.append(Widget("menu_2" , self.game, (65,90), (136,22),
        #                            0, "2", widget_type="button"))
        # self.button_list.append(Widget("menu_game_over", self.game, (65,90), (150,20),
        #                                level=3, text="GO to Menu", widget_type="button"))


    def draw_state(self, screen, event):
            # self.game.window.fill((0,0,0))
        for button in self.button_list:
            button.draw(screen, self.current_level)
        # elif self.current_level == 2:
        #     self.game.window.fill((0, 0, 100))
        #     font = pygame.font.SysFont(None, 72)
        #     text = font.render("Main Menu", True, (255, 255, 255))
        #     text2 = font.render("Press any button to continue", True, (255, 255, 255))
        #     self.game.window.blit(text, (250, 250))
        #     self.game.window.blit(text2, (50,350))
        #     if self.game.debug_mode is True:
        #         font_small = pygame.font.SysFont(None, 40)
        #         tell_debug = font_small.render("Debug mode", False, (255, 255, 255))
        #         self.game.window.blit(tell_debug, (50, 100))


    def update_state(self, frame, ms_per_loop, event):
        for button in self.button_list:
            button.update(event, self.current_level)
        # print(self.game.game_state["Gameplay"].current_level)

    # def key_handle(self, event):
    #     ## Check button push
    #     for button in self.button_list:
    #         button.update(event, self.current_level)
    #         if button.action is True:
    #             self.game.state_manager.set_state("Gameplay")
    #             # if button.name == "menu_start_game":
    #             #     self.game.current_state = "Gameplay"
    #             # elif button.name == "menu_2":
    #             #     print("2")
    #             # elif button.name == "menu_game_over":
    #             #     print("run")
    #             #     self.current_level = 0
    #     ## check key push that relate with the state
    #     if self.current_level == 0 and event.is_keypress(pygame.K_e):
    #         self.game.state_manager.set_state("Gameplay")


class Gameplay(GameState):
    sprites_key = {"dummy":[[3, 0, 0, 320, 180]], "Boss1":[[3, 0, 0, 320, 180]], "Boss2":[[3, 0, 0, 320, 180]],
                   "Boss3":[[3, 0, 0, 320, 180]]}


    def __init__(self, game):
        super().__init__(game)

        self.sprite_dir = "sprites\\scale1-screen - animated.png"
        self.bg_animation = dict()
        self.image = None
        self.frame_animation = 0

        self.game_level = {0:"dummy", 1:"Boss1", 2:"Boss2", 3:"Boss3"}
        self.death_list = []
        self.kill_require = {"dummy":1,"Boss1":1,"Boss2":1,"Boss3":3}
        self.kill_count = 0
        self.enemy_factory = BossFactory(game)
        self.ms_per_frame = 500
        self.build_asset()

    def load_sprite(self, sprites_key):
        Map_sprite = SpriteHandler(pygame.image.load(self.sprite_dir))
        self.bg_animation = Map_sprite.pack_sprite(sprites_key, self.game.screen_scale)
        self.image = self.bg_animation[self.game_level[self.current_level]][0][self.frame_animation]

    def build_asset(self):
        self.load_sprite(self.sprites_key)
        self.button_list.append(Button("next_level", self.game, (280, 150), (15, 15),
                                       0, "GO", command= lambda: self.game.overlay_manager.add_overlay(self.overlay_dict["transition"])))
        self.overlay_dict["transition"] = TransitionHalf(self.game, 2,16, command=lambda :self.level_switch(1))

    def asset_update(self):
        self.load_sprite(self.sprites_key)
        if len(self.button_list) != 0:
            for each_button in self.button_list:
                each_button.button_setting()
        if len(self.overlay_dict) != 0:
            for each_overlay in self.overlay_dict.values():
                each_overlay.setting()

    def enter(self, level):
        self.current_level = level
        self.game.entities_group.add(self.game.player)
        for each_entity in self.game.entities_group:
            each_entity.status = "enter_arena"

    # def entry_new_level(self):
    #     for each_entity in self.game.entities_group:
    #         ##X,Y
    #         each_entity.status = "enter_arena"

    def exit(self):
        self.game.entities_group.empty()
        self.game.attack_group.empty()
        self.death_list = []

    def animated(self, screen):
        screen.fill((0, 0, 0))
        if self.frame_animation > len(self.bg_animation[self.game_level[self.current_level]][0])-1:
            self.frame_animation = 0
        self.image = self.bg_animation[self.game_level[self.current_level]][0][self.frame_animation]
        screen.blit(self.image, self.game.screen_start)

    def draw_state(self, screen, event):
        self.animated(screen)
        self.game.entities_group.draw(self.game.window)
        self.game.attack_group.draw(self.game.window)
        for button in self.button_list:
            button.draw(screen, self.current_level)

    def update_state(self, frame, ms_per_loop, event):
        self.timer_ms += ms_per_loop
        if self.timer_ms >= self.ms_per_frame:
            self.timer_ms -= self.ms_per_frame
            self.frame_animation += 1

        for button in self.button_list:
            button.update(event, self.current_level)

        self.enemy_factory.create_boss(self.current_level)
        self.game.entities_group.update(frame, ms_per_loop, self.game.attack_group, event_object)
        self.game.attack_group.update(frame, ms_per_loop, self.game.attack_group)
        Config.check_attack_collision(self.game.attack_group, self.game.entities_group)

        self.check_kill(frame)
        # self.level_switch()

    def check_kill(self, frame):
        if frame != 1:
            return

        for each in self.game.entities_group:
            ## someone death
            if each.death is True and each not in self.death_list:
                # print(each.name)
                if each == self.game.player:
                    self.game.state_manager.set_state("Menu")

                    # self.game.current_state = "Menu"
                    # self.game.game_state["Menu"].current_level = 3
                    ## it only change current level of gameplay object not menu
                    # self.current_level = 0

                else :
                    ## KEY TO CHANGE LEVEL
                    """
                    THERE ARE SOME PROBLEM THAT THE ENEMY GOT REMOVE TO FAST BECAUSE THE FRAME THAT ENEMY STATUS UPDATE TO DEATH
                    IS HAPPEN BEFORE EVEN DRAW THE SCREEN SO THE ANIMATION GOT CUT OUT 1 FRAME THE LAZY WAY TO DEAL WITH IT IS
                    MAKE DEATH ANIMATION HAS MORE 1 FRAME
                    """
                    self.death_list.append(each)

        if len(self.death_list) == self.kill_require[self.game_level[self.current_level]]:
            self.change_level = True



    def level_switch(self, next_level = 0):
        # if self.change_level is False:
        #     return

        if next_level == 1:
            if self.current_level == 0:
                ## COUNT KILL COUNT ??
                # self.game.entities_group.remove(self.game.player)
                for each in self.game.entities_group:
                    if each != self.game.player:
                        self.game.entities_group.remove(each)
                self.current_level = 1
            # self.game.current_state = "transition"
            # self.game.game_state["transition"].next_level = 1
            # self.game.game_state["transition"].next_state = "Gameplay"

            self.enemy_factory.already_create = False
            self.change_level = False
            self.game.attack_group.empty()
        # elif self.change_level == 1:
        #     for each in self.death_list:
        #         self.death_list.remove(each)
        #         self.game.entities_group.remove(each)
        #     self.current_level = 2
        #     self.enemy_factory.already_create = False
        #     self.change_level = False