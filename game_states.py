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
                    if type(bullet.maker) != type(entities) and entities not in bullet.already_hit:
                        # print(f"Bullet from {bullet.maker.name} hit Enemy {entities.name}!")
                        entities.health -= bullet.damage
                        bullet.already_hit.append(entities)
                # self.game.attack_group.remove(bullet)

    def check_boundary(self):
        # Check do their is the screen boundary or other entities or not it NO so the entities can allow to move
        pass