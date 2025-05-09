import math

import pygame
from config import Config
from event_handle import event_object
from overlay import *
from Enemy_factory import BossFactory

# @abstractproperty
class GameState:
    def __init__(self, game):
        self.game = game # game object
        self.current_level = 0
        self.change_level = False
        # self.game_level = None
        self.button_list = []

    def draw_state(self, screen, frame, event):
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
    def __init__(self, game):
        super().__init__(game)
        # self.game_level = {"Title_screen": 0, "Main_menu": 1, "Pause": 2, "Game_over":3}
        self.build_button()

    def load_assert(self):
        pass

    def build_button(self):
        self.button_list.append(Widget("menu_start_game" , self.game, (65,52), (136,22),
                                   0, "Start", widget_type="button"))
        self.button_list.append(Widget("menu_2" , self.game, (65,90), (136,22),
                                   0, "2", widget_type="button"))
        self.button_list.append(Widget("menu_game_over", self.game, (65,90), (150,20),
                                       level=3, text="GO to Menu", widget_type="button"))


    def draw_state(self, screen, frame, event):
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


    def update_state(self, frame, event):
        self.key_handle(event)
        # print(self.game.game_state["Gameplay"].current_level)

    def key_handle(self, event):
        ## Check button push
        for button in self.button_list:
            button.update(event, self.current_level)
            if button.action is True:
                self.game.state_manager.set_state("Gameplay")
                # if button.name == "menu_start_game":
                #     self.game.current_state = "Gameplay"
                # elif button.name == "menu_2":
                #     print("2")
                # elif button.name == "menu_game_over":
                #     print("run")
                #     self.current_level = 0
        ## check key push that relate with the state
        if self.game.current_state == "Menu" and self.current_level == 0 and event.is_keypress(pygame.K_e):
            self.game.current_state = "Gameplay"


# class ScreenTransition(GameState):
#
#     def __init__(self, game, box_size=16):
#         super().__init__(game)
#         self.game = game
#         self.finish_load = False
#         # self.current_state = self.game.current_state
#         self.box_size = box_size
#         self.next_state = None
#         self.next_level = None
#         self.progress_number = -1
#
#         self.grid = []
#         self.image = None
#         self.width_number = None
#         self.height_number = None
#         self.full_progress = None
#         self.background = None
#         self.load_assert()
#
#         self.current_x = 0
#         self.current_y = 0
#         self.screen_delay = 10
#         self.transition_tracker = None
#         self.transition_type = "fill"
#
#         self.truly_finish = False
#
#     def load_assert(self):
#         self.width_number = math.ceil(self.game.screen_info[0]/ (self.box_size * self.game.screen_scale))
#         self.height_number = math.ceil(self.game.screen_info[1]/ (self.box_size * self.game.screen_scale))
#         self.full_progress =  self.width_number + self.height_number - 1
#         self.background = pygame.transform.scale(pygame.image.load("sprites\\1x1_grid.png"), self.game.screen_info)
#
#         for height in range(self.height_number):
#             start_grid = []
#             for width in range(self.width_number):
#                 start_grid.append(0)
#             self.grid.append(start_grid)
#
#         # print(self.grid[8][15])
#
#         scale_x = math.ceil(self.box_size*self.game.screen_scale)
#         scale_y = math.ceil(self.box_size*self.game.screen_scale)
#         scale = max(scale_x, scale_y)
#         self.image = pygame.Surface((scale,scale))
#         self.image.fill((0, 0, 0))
#
#     def process_update(self, frame):
#         if (self.current_x == self.width_number - 1 and self.current_y == self.height_number - 1
#                 and self.transition_type == "clean"):
#             self.truly_finish = True
#
#         if self.current_x != self.width_number-1 or self.current_y != self.height_number-1:
#             self.finish_load = False
#         else :
#             self.grid[self.current_y][self.current_x] = 1
#             self.finish_load = True
#             self.current_x = 0
#             self.current_y = 0
#             self.transition_type = "clean"
#
#         if self.finish_load is False and self.transition_type == "fill":
#             self.grid[self.current_y][self.current_x] = 1
#             if self.current_x < self.width_number-1:
#                 self.current_x +=1
#             else :
#                 self.current_x = 0
#                 self.current_y += 1
#
#         elif self.finish_load is False and self.transition_type == "clean":
#             self.game.window.blit(self.background, self.game.screen_start)
#             self.grid[self.current_y][self.current_x] = 0
#             if self.current_x < self.width_number-1:
#                 self.current_x +=1
#             else :
#                 self.current_x = 0
#                 self.current_y += 1
#
#     def update_state(self, frame, event):
#         ## WHEN OUT DON'T FORGET TO SENT IT BACK TO NONE
#         if self.transition_tracker is None:
#             self.transition_tracker = pygame.time.get_ticks()
#
#         if self.game.tracker2 - self.transition_tracker >= self.screen_delay:
#             self.process_update(frame)
#             self.transition_tracker = self.game.tracker2
#
#         if self.truly_finish is True:
#             self.game.window.fill((0, 0, 0))
#             self.game.current_state = self.next_state
#             self.game.game_state[self.game.current_state].current_level = self.next_level
#
#
#
#     def draw_state(self, screen, frame, event):
#         if self.finish_load is False:
#             for x in range(self.width_number):
#                 for y in range(self.height_number):
#                     if self.grid[y][x] == 1:
#                         screen.blit(self.image,
#                                               (x * self.box_size * self.game.screen_scale + self.game.screen_start[0],
#                                                y * self.box_size * self.game.screen_scale + self.game.screen_start[1]))
#         else :
#             if self.finish_load is True:
#                 screen.blit(self.background, self.game.screen_start)
#                 screen.fill((0, 0, 0))

########################################################################################################################

class Gameplay(GameState):
    def __init__(self, game, bg):
        super().__init__(game)
        self.background = bg
        self.bg_animation = {0:[],1:[],2:[],3:[]}
        # self.game_level = {"dummy":0, "Boss1":1, "Boss2":2, "Boss3":3}
        self.death_list = []
        self.kill_require = {0:1,1:1,2:1,3:3}
        self.kill_count = 0
        self.enemy_factory = BossFactory(game)
        self.build_button()

    def load_assert(self):
        """
        sent sprite location and key of each level to Sprite handle

        self.bg_animation[level] = [animation]

        """
        pass

    def enter(self, level):
        self.current_level = level
        self.game.entities_group.add(self.game.player)

    def exit(self):
        self.game.entities_group.empty()
        self.game.attack_group.empty()
        self.death_list = []

    def animated(self, screen, frame):
        screen.fill((0, 0, 0))
        screen.blit(pygame.transform.scale(self.background, self.game.screen_info), self.game.screen_start)

    def build_button(self):
        self.button_list.append(Widget("Gameplay_go_next", self.game, (238, 124), (12, 12),
                                       0, "GO", widget_type="button"))

    def draw_state(self, screen, frame, event):
        # FILL COLOR OUTSIDE BORDER
        self.animated( screen, frame)
        # screen.fill((0, 0, 0))
        # screen.blit(pygame.transform.scale(self.background, self.game.screen_info), self.game.screen_start)
        self.game.entities_group.draw(self.game.window)
        self.game.attack_group.draw(self.game.window)
        for button in self.button_list:
            button.draw(screen, self.current_level)

    def update_state(self, frame, event):
        self.key_handle(event)

        self.enemy_factory.create_boss(self.current_level)
        self.game.entities_group.update(frame, self.game.attack_group, event_object)
        self.game.attack_group.update(frame, self.game.attack_group)
        Config.check_attack_collision(self.game.attack_group, self.game.entities_group)

        self.check_kill(frame)
        self.level_handle()


    def key_handle(self, event):
        ## Check button push
        for button in self.button_list:
            button.update(event, self.current_level)
            if button.action is True:

                # button that has this name got push
                if button.name == "Gameplay_go_next":
                    self.change_level = True
        ## check key push that relate with the state
        if self.game.current_state == "Gameplay" and event.is_keypress(pygame.K_e):
            self.game.current_state = "Menu"

    def check_kill(self, frame):
        if frame != 1:
            return

        for each in self.game.entities_group:
            ## someone death
            if each.death is True and each not in self.death_list:
                # print(each.name)
                if each == self.game.player:
                    self.game.state_manager.set_stage("Menu")

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

        if len(self.death_list) == self.kill_require[self.current_level]:
            self.change_level = True



    def level_switch(self, next_level = 0):
        if self.change_level is False:
            return

        if self.current_level == 0:
            ## COUNT KILL COUNT ??
            # self.game.entities_group.remove(self.hostile)
            for each in self.game.entities_group:
                if each != self.game.player:
                    self.game.entities_group.remove(each)
            # self.current_level = 1
            self.game.current_state = "transition"
            self.game.game_state["transition"].next_level = 1
            self.game.game_state["transition"].next_state = "Gameplay"

            self.enemy_factory.already_create = False
            self.change_level = False
            self.game.attack_group.empty()
        elif self.change_level == 1:
            for each in self.death_list:
                self.death_list.remove(each)
                self.game.entities_group.remove(each)
            self.current_level = 2
            self.enemy_factory.already_create = False
            self.change_level = False