from chickfight_player import Player
from event_handle import event_object
from Sprite_handle import *
from config import Config
import pygame
import math
from game_states import *

class Main:
    def __init__(self):
        pygame.init()
        self.tracker1 = pygame.time.get_ticks()
        self.tracker2 = None
        self.clock = pygame.time.Clock()
        self.program_running = True
        self.player_group = pygame.sprite.Group()
        self.attack_group = pygame.sprite.Group()
        self.window = pygame.display.set_mode(Config.screen_info)
        pygame.display.set_caption('Winner Winner Chicken Brawler')

        self.game_state = dict()
        self.current_state = None

    def get_frame(self):
        frame = 0
        if self.tracker2 - self.tracker1 >= Config.frame_delay:
            frame = 1
            self.tracker1 = self.tracker2
        return frame

    def update_screen(self, frame):
        event_object.update_event()
        self.player_group.update(frame, self.attack_group, event_object)
        self.attack_group.update(frame, self.attack_group)


    def render_screen(self):
        # background = pygame.transform.scale(pygame.image.load("sprites\grass.jpg"), Config.screen_info) #depend on game state
        self.window.blit(background, (0, 0))
        self.player_group.draw(self.window)
        self.attack_group.draw(self.window)



    def main_loop(self):
        background = pygame.transform.scale(pygame.image.load("sprites\grass.jpg"),
                                            Config.screen_info)  # depend on game state
        player = Player(Config.screen_info, name="jim")
        self.player_group.add(player)
        self.game_state["Menu"] = MainMenu(self)
        self.game_state["Gameplay"] = Gameplay(self, background)

        while self.program_running:
            self.tracker2 = pygame.time.get_ticks()

            # print(tracker1, "||||||||||||||" ,tracker2)
            # print(f"FPS: {clock.get_fps():.2f}")

            # frame update calculate
            frame = self.get_frame()

            self.update_screen(frame)
            self.render_screen()

            if event_object.quit_press():
                self.program_running = False
            self.clock.tick(60)
            pygame.display.update()
        pygame.quit()


if __name__ == '__main__':
    main = Main()
    main.main_loop()
