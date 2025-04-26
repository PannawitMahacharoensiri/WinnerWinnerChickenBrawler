import pygame
from config import Config
from event_handle import event_object
from Enemy_factory import BossFactory

class GameState:
    def __init__(self, game):
        self.game = game # game object
        self.current_level = 0
        self.game_level = None

    def draw_screen(self):
        pass

    def clean_state(self):
        pass

class Menu(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.game_level = {"Title_screen": 0, "Main_menu": 1, "Pause": 2}

    def draw_screen(self):
        self.game.window.fill((0, 0, 100))
        font = pygame.font.SysFont(None, 72)
        text = font.render("Main Menu", True, (255, 255, 255))
        text2 = font.render("Press any button to continue", True, (255, 255, 255))
        self.game.window.blit(text, (250, 250))
        self.game.window.blit(text2, (50,350))
        if self.game.debug_mode is True:
            font_small = pygame.font.SysFont(None, 40)
            tell_debug = font_small.render("Debug mode", False, (255, 255, 255))
            self.game.window.blit(tell_debug, (50, 100))


    def update_screen(self, frame):
        pass


class Gameplay(GameState):
    def __init__(self, game, bg):
        super().__init__(game)
        self.background = bg
        self.game_level = {"dummy":0, "Boss1":1, "Boss2":2, "Boss3":3}
        self.enemy_factory = BossFactory(game)

    def draw_screen(self):
        # FILL COLOR OUTSIDE BORDER
        self.game.window.fill((0, 0, 0))
        self.game.window.blit(pygame.transform.scale(self.background, self.game.screen_info), self.game.screen_start)
        self.game.entities_group.draw(self.game.window)
        self.game.attack_group.draw(self.game.window)

    def update_screen(self, frame):
        self.enemy_factory.create_boss(self.current_level)
        self.game.entities_group.update(frame, self.game.attack_group, event_object)
        self.game.attack_group.update(frame, self.game.attack_group)
        Config.check_collision(self.game.attack_group, self.game.entities_group)

