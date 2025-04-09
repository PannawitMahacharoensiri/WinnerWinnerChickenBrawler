import pygame
from event_handle import event_object

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
        # self.game.window.fill((0, 0, 100))
        font = pygame.font.SysFont(None, 72)
        text = font.render("Main Menu", True, (255, 255, 255))
        self.game.window.blit(text, (250, 250))

    def update_screen(self, frame):
        pass


class Gameplay(GameState):
    def __init__(self, game, bg):
        super().__init__(game)
        self.background = bg

    def draw_screen(self):
        # background = pygame.transform.scale(pygame.image.load("sprites\grass.jpg"), Config.screen_info) #depend on game state
        self.game.window.blit(self.background, (0, 0))
        self.game.player_group.draw(self.game.window)
        self.game.attack_group.draw(self.game.window)

    def update_screen(self, frame):
        self.game.player_group.update(frame, self.game.attack_group, event_object)
        self.game.attack_group.update(frame, self.game.attack_group)
        self.check_collision()

    def check_collision(self):
        collide = pygame.sprite.groupcollide(self.game.attack_group, self.game.player_group, False, False)
        if collide != {}:
            for bullet, hit_enemies in collide.items():
                for enemy in hit_enemies:
                    print(f"Bullet from {bullet.maker.name} hit Enemy {enemy.name}!")
                    enemy.health -= bullet.damage
                self.game.attack_group.remove(bullet)
            # for player,attack in collide.items():
            #
            #     for each in attack:
            #         if type(player) != type(each.maker):
            #             player.health -= each.damage
            #             each.damage = 0
                        # self.game.attack_group.remove(each)