import pygame
from config import Config
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

    def draw_screen(self):
        # FILL COLOR OUTSIDE BORDER
        self.game.window.fill((0, 0, 0))
        self.game.window.blit(pygame.transform.scale(self.background, self.game.screen_info), self.game.screen_start)
        self.game.entities_group.draw(self.game.window)
        self.game.attack_group.draw(self.game.window)

    def update_screen(self, frame):
        self.game.entities_group.update(frame, self.game.attack_group, event_object)
        self.game.attack_group.update(frame, self.game.attack_group)
        self.check_collision()

    def check_collision(self):
        collide = pygame.sprite.groupcollide(self.game.attack_group, self.game.entities_group, False, False)
        if collide != {}:
            for bullet, entities_group in collide.items():
                for entities in entities_group:
                    if type(bullet.maker) != type(entities) and entities not in bullet.already_hit and entities.action != "hurt":
                        bullet.already_hit.append(entities)
                        entities.health_reduce(bullet.damage)

                        # if self.game.debug_mode is True :
                        #     print(f"Bullet from {bullet.maker.name} hit Enemy {entities.name}! : {entities.health}")
