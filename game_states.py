
class GameState:
    def __init__(self, game):
        self.game = game # game object

    def draw_screen(self):
        pass

    def clean_state(self):
        pass


class MainMenu(GameState):
    def __init__(self, game):
        super().__init__(game)

    def draw_screen(self):
        self.game.window.fill((0, 0, 100))


class Gameplay(GameState):
    def __init__(self, game, bg):
        super().__init__(game)
        self.background = bg

    def draw_screen(self):
        # background = pygame.transform.scale(pygame.image.load("sprites\grass.jpg"), Config.screen_info) #depend on game state
        self.game.window.blit(self.background, (0, 0))
        self.game.player_group.draw(self.game.window)
        self.game.attack_group.draw(self.game.window)