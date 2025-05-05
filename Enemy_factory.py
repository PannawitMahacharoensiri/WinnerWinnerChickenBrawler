from Enemy import  *

class BossFactory:
    def __init__(self, game):
        self.game = game
        self.already_create = False

    def create_boss(self, game_level):
        if self.already_create is True:
            return

        if game_level == 0 and len(self.game.entities_group) <= 1:
            DummyKUNG = Dummy((self.game.screen_info[0]/2 ,self.game.screen_info[1]/2), game=self.game)
            self.game.entities_group.add(DummyKUNG)
            self.already_create = True

        # elif game_level == 1 and len(self.game.entities_group) <= 1:
        #     jokey = Boss1((self.game.screen_info[0]/2 ,self.game.screen_info[1]/2), game=self.game, name="jokey")
        #     self.game.entities_group.add(jokey)
        #     self.already_create = True

        elif game_level == 1 and len(self.game.entities_group) <= 1:
            jim = Boss2((self.game.screen_info[0]/2 ,self.game.screen_info[1]/2), game=self.game, name="jim")
            self.game.entities_group.add(jim)
            self.already_create = True
