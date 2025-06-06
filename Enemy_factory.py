from Enemy import  *
from overlay import *

class BossFactory:
    def __init__(self, game, state):
        self.game = game
        self.state = state
        self.already_create = False

    def create_boss(self, game_level):
        if self.already_create is True:
            return

        if game_level == 0 and len(self.game.entities_group) <= 1:
            DummyKUNG = Dummy((self.game.screen_info[0]/2 ,self.game.screen_info[1]/2), game=self.game)
            self.game.entities_group.add(DummyKUNG)
            self.already_create = True

        elif game_level == 1 and len(self.game.entities_group) <= 1:
            jokey = Boss1((self.game.screen_info[0]+self.game.screen_start[0], self.game.screen_info[1]/2), game=self.game, name="jokey")
            self.game.entities_group.add(jokey)
            self.already_create = True
            self.state.main_overlay["enemy1_health"] = HealthBarOverlay(self.game, jokey, position=(230,10))
            self.game.overlay_manager.add_overlay(self.state.main_overlay["enemy1_health"])
        #
        elif game_level == 2 and len(self.game.entities_group) <= 1:
            jim = Boss2((self.game.screen_info[0]+self.game.screen_start[0], self.game.screen_info[1]/2), game = self.game, name = "jim")
            self.game.entities_group.add(jim)
            self.already_create = True
            self.state.main_overlay["enemy2_health"] = HealthBarOverlay(self.game, jim, position=(230, 10))
            self.game.overlay_manager.add_overlay(self.state.main_overlay["enemy2_health"])
