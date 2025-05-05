import pygame
from config import Config
from event_handle import event_object, Widget
from Enemy_factory import BossFactory

class GameState:
    def __init__(self, game):
        self.game = game # game object
        self.current_level = 0
        self.change_level = False
        # self.game_level = None
        self.button_list = []
        self.death_list = []

    def draw_state(self, frame, event):
        pass

    def clean_state(self):
        pass

########################################################################################################################

class Menu(GameState):
    def __init__(self, game):
        super().__init__(game)
        # self.game_level = {"Title_screen": 0, "Main_menu": 1, "Pause": 2}
        self.load_asset()

    def load_asset(self):
        self.button_list.append(Widget("menu_start_game" , self.game, (65,52), (136,22),
                                   0, "Start", widget_type="button"))
        self.button_list.append(Widget("menu_2" , self.game, (65,90), (136,22),
                                   0, "2", widget_type="button"))


    def draw_state(self, frame, event):
            # self.game.window.fill((0,0,0))
        for button in self.button_list:
            button.draw(self.game.window, self.current_level)
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

    def key_handle(self, event):
        ## Check button push
        for button in self.button_list:
            button.update(event, self.current_level)
            if button.action is True:
                if button.name == "menu_start_game":
                    self.game.current_state = "Gameplay"
                elif button.name == "menu_2":
                    print("2")
        ## check key push that relate with the state
        if self.game.current_state == "Menu" and self.current_level == 0 and event.is_keypress(pygame.K_e):
            self.game.current_state = "Gameplay"

    def level_handle(self):
        pass


########################################################################################################################

class Gameplay(GameState):
    def __init__(self, game, bg):
        super().__init__(game)
        self.background = bg
        # self.game_level = {"dummy":0, "Boss1":1, "Boss2":2, "Boss3":3}
        self.hostile = None
        self.enemy_factory = BossFactory(game)
        self.load_asset()

    def load_asset(self):
        self.button_list.append(Widget("Gameplay_go_next", self.game, (238, 124), (12, 12),
                                       0, "GO", widget_type="button"))

    def draw_state(self,frame, event):
        # FILL COLOR OUTSIDE BORDER
        self.game.window.fill((0, 0, 0))
        self.game.window.blit(pygame.transform.scale(self.background, self.game.screen_info), self.game.screen_start)
        self.game.entities_group.draw(self.game.window)
        self.game.attack_group.draw(self.game.window)
        for button in self.button_list:
            button.draw(self.game.window, self.current_level)

    def update_state(self, frame, event):
        self.key_handle(event)
        # if len(dead_list) != 0:
        #     for each in dead_list:
        #         if each == self.game.player:
        #             pass
        #             # print("NOOOOOOOOOO")
        #         else :
        #             self.death_list.append(each)
        #             self.change_level = True

        self.enemy_factory.create_boss(self.current_level)
        self.game.entities_group.update(frame, self.game.attack_group, event_object)
        self.game.attack_group.update(frame, self.game.attack_group)
        Config.check_attack_collision(self.game.attack_group, self.game.entities_group)

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


    def level_handle(self):
        if self.change_level is False:
            return

        if self.current_level == 0:
            ## COUNT KILL COUNT ??
            self.game.entities_group.remove(self.hostile)
            self.current_level = 1
            self.enemy_factory.already_create = False
            self.change_level = False
            self.game.attack_group.empty()
        elif self.change_level == 1:
            print("bye")