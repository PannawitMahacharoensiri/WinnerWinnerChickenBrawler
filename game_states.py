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

    def enter(self, to_level):
        pass

    def level_switch(self, new_level=0):
        pass

########################################################################################################################

class Menu(GameState):
    sprites_key = {"Title_screen":[[1, 4, 0, 320, 180]], "Main_menu":[[1, 4, 0, 320, 180]],
                   "Game_over":[[1, 4, 0, 320, 180]], "Statistic":[[1, 4, 0, 320, 180]]}

    def __init__(self, game):
        super().__init__(game)
        self.game_level = {0:"Title_screen", 1:"Main_menu", 2:"Game_over", 3:"Statistic"}
        self.sprite_dir = "sprites\\scale1-screen - animated.png"
        self.bg_animation = dict()
        self.image = None
        self.frame_animation = 0
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
        if to_level is not None:
            self.level_switch(to_level)



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
                                       1, "start",
                                       command= lambda:self.game.state_manager.set_state("Gameplay", 0)))
        self.button_list.append(Button("statistic", self.game, (160,90), (136,22),
                                       1, "statistic",
                                       command= lambda:self.level_switch(3)))
        self.overlay_dict["back_to_title"] = Transition(self.game, 10,20, command=lambda :self.level_switch(0))


    def draw_state(self, screen, event):
        if self.current_level == 2:
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            overlay.set_alpha(10)
            screen.blit(overlay, (self.game.screen_start[0], self.game.screen_start[1]))

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

    def key_handle(self, event):
        if self.current_level == 0:
            if len(event.key_press) != 0 or len(event.mouse_button) != 0:
                event.reset_event("mouse_pos")
                self.level_switch(1)

    def update_state(self, frame, ms_per_loop, event):
        self.timer_ms += ms_per_loop
        if self.timer_ms >= self.ms_per_frame:
            self.timer_ms -= self.ms_per_frame
            self.frame_animation += 1

        if self.frame_animation > 1:
            self.key_handle(event)
            for button in self.button_list:
                button.update(event, self.current_level)


    def level_switch(self, new_level=0):
        self.frame_animation = 0
        self.current_level = new_level
        if new_level == 0 :
            pass

class Gameplay(GameState):
    sprites_key = {"dummy":[[3, 0, 0, 320, 180]], "Boss1":[[3, 0, 0, 320, 180]], "Boss2":[[3, 0, 0, 320, 180]],
                   "Boss3":[[3, 0, 0, 320, 180]], "pause_menu":[[3, 0, 0, 320, 180]]}


    def __init__(self, game):
        super().__init__(game)

        self.sprite_dir = "sprites\\scale1-screen - animated.png"
        self.bg_animation = dict()
        self.image = None
        self.frame_animation = 0

        self.former_level = 0
        self.game_level = {0:"dummy", 1:"Boss1", 2:"Boss2", 3:"Boss3", 4:"pause_menu"}
        self.death_list = []
        self.kill_require = {"dummy":1,"Boss1":1,"Boss2":1,"Boss3":3}
        self.kill_count = 0
        self.enemy_factory = BossFactory(game, self)
        self.ms_per_frame = 500
        self.build_asset()
        self.pause = False

    def load_sprite(self, sprites_key):
        Map_sprite = SpriteHandler(pygame.image.load(self.sprite_dir))
        self.bg_animation = Map_sprite.pack_sprite(sprites_key, self.game.screen_scale)
        self.image = self.bg_animation[self.game_level[self.current_level]][0][self.frame_animation]

    def build_asset(self):
        self.load_sprite(self.sprites_key)
        self.button_list.append(Button("next_level", self.game, (280, 150), (15, 15),
                                       0, "GO", command= lambda: self.game.overlay_manager.add_overlay(self.overlay_dict["transition"])))
        self.overlay_dict["player_health"] = HealthBarOverlay(self.game, self.game.player)
        self.overlay_dict["timer"] = TimerOverlay(self.game, (150,20), (45,15))
        self.overlay_dict["transition"] = TransitionHalf(self.game, 32,16, command=lambda :self.level_switch(1))
        self.button_list.append(Button("exit", self.game, (150,60), (100,20), 4,
                                       "exit", command=lambda:self.game.overlay_manager.add_overlay(self.overlay_dict["back_to_title"])))
        self.button_list.append(Button("continue", self.game, (150,90), (100,20), 4,
                                       "continue", command=lambda:self.level_switch(self.former_level)))
        self.overlay_dict["back_to_title"] = Transition(self.game, 10, 20, command=lambda: self.game.state_manager.set_state("Menu",0))

    def draw_state(self, screen, event):
        self.animated(screen)
        self.game.entities_group.draw(self.game.window)
        self.game.attack_group.draw(self.game.window)
        for button in self.button_list:
            button.draw(screen, self.current_level)
        if self.pause is True:
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((128, 128, 128, 150))
            screen.blit(overlay, (self.game.screen_start[0], self.game.screen_start[1]))

    def update_state(self, frame, ms_per_loop, event):

        self.key_handle(event)
        for button in self.button_list:
            button.update(event, self.current_level)
        if self.pause is True:
            return

        self.timer_ms += ms_per_loop
        if self.timer_ms >= self.ms_per_frame:
            self.timer_ms -= self.ms_per_frame
            self.frame_animation += 1

        self.enemy_factory.create_boss(self.current_level)
        self.game.entities_group.update(frame, ms_per_loop, self.game.attack_group, event_object)
        self.game.attack_group.update(frame, ms_per_loop, self.game.attack_group)
        Config.check_attack_collision(self.game.attack_group, self.game.entities_group)
        self.check_kill(frame)

    def asset_update(self):
        self.load_sprite(self.sprites_key)
        if len(self.button_list) != 0:
            for each_button in self.button_list:
                each_button.button_setting()
        if len(self.overlay_dict) != 0:
            for each_overlay in self.overlay_dict.values():
                each_overlay.setting()

    def key_handle(self, event):
        if event.is_keypress(pygame.K_e):
            if self.pause is False:
                self.pause = True
                self.overlay_dict["timer"].start_timer = False
                self.level_switch(4)
            else:
                self.pause = False
                self.overlay_dict["timer"].start_timer = True


    def enter(self, to_level):
        self.enemy_factory.already_create = False
        if self.game.player not in self.game.entities_group:
            self.game.entities_group.add(self.game.player)
            self.game.player.status = "enter_arena"
        self.level_switch(to_level)

    def exit(self):
        self.current_level = 0
        self.game.entities_group.empty()
        self.game.attack_group.empty()
        self.death_list = []
        for overlay in self.overlay_dict.values():
            overlay.reset()
            self.game.overlay_manager.remove_overlay(overlay)

    def animated(self, screen):
        screen.fill((0, 0, 0))
        if self.frame_animation > len(self.bg_animation[self.game_level[self.current_level]][0])-1:
            self.frame_animation = 0
        self.image = self.bg_animation[self.game_level[self.current_level]][0][self.frame_animation]
        screen.blit(self.image, self.game.screen_start)

    def check_kill(self, frame):
        if frame != 1:
            return

        for each in self.game.entities_group:
            ## someone death
            if each.death is True and each not in self.death_list:
                if each == self.game.player:
                    self.game.state_manager.set_state("Menu")
                    self.overlay_dict["timer"].start_timer = False
                else :
                    ## KEY TO CHANGE LEVEL
                    """
                    THERE ARE SOME PROBLEM THAT THE ENEMY GOT REMOVE TO FAST BECAUSE THE FRAME THAT ENEMY STATUS UPDATE TO DEATH
                    IS HAPPEN BEFORE EVEN DRAW THE SCREEN SO THE ANIMATION GOT CUT OUT 1 FRAME THE LAZY WAY TO DEAL WITH IT IS
                    MAKE DEATH ANIMATION HAS MORE 1 FRAME
                    """
                    self.death_list.append(each)

        if len(self.death_list) == self.kill_require[self.game_level[self.current_level]]:
            if self.current_level != 2:
                self.level_switch(self.current_level+1)
            else :
                ## WINNING SCREEN
                pass



    def level_switch(self, next_level=0):
        if self.current_level != 4:
            if next_level != 4:
                print("run")
                if next_level == 0:
                    self.game.overlay_manager.add_overlay(self.overlay_dict["player_health"])
                    self.game.overlay_manager.add_overlay(self.overlay_dict["timer"])
                    self.enemy_factory.already_create = False
                elif next_level == 1:
                    self.overlay_dict["timer"].start_timer = True
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
                    self.game.overlay_manager.remove_overlay(self.overlay_dict["enemy1_health"])
                    self.current_level = 2
                    self.enemy_factory.already_create = False
            else:
                self.former_level = self.current_level
                self.current_level = next_level
        else:
            self.pause = False
            will_change = self.current_level
            self.current_level = self.former_level
            self.former_level = will_change
