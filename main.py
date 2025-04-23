from chickfight_player import Player
from event_handle import event_object
from Sprite_handle import *
from config import Config
import pygame
import math
from game_states import *
from Enemy import *

class Main:
    def __init__(self):
        pygame.init()
        self.tracker1 = pygame.time.get_ticks()
        self.tracker2 = None
        self.clock = pygame.time.Clock()
        self.program_running = True
        self.player = None
        self.entities_group = pygame.sprite.Group()
        self.attack_group = pygame.sprite.Group()

        self.debug_mode = True
        self.screen_scale = 1
        self.screen_info = (1024, 576)
        self.window = pygame.display.set_mode(self.screen_info, pygame.RESIZABLE)

        pygame.display.set_caption('Winner Winner Chicken Brawler')
        self.game_state = dict()
        self.current_state = None

    def get_frame(self):
        frame = 0
        if self.tracker2 - self.tracker1 >= Config.frame_delay:
            frame = 1
            self.tracker1 = self.tracker2
        return frame

    def change_state(self, event):
        if len(event.key_press) != 0:
            self.current_state = "Gameplay"
        if event.is_keypress(pygame.K_e):
            self.current_state = "Menu"


    def main_loop(self):
        background = pygame.transform.scale(pygame.image.load("sprites\\grass.jpg"),
                                            self.screen_info)  # depend on game state
        # chicken_jokey = Boss1("chick jokey",400, 250, self)
        player = Player(self.screen_info, game = self, name="jim")
        jokey = Boss1((450,250),game = self, name = "jokey")
        self.player = player
        self.entities_group.add(self.player)
        # self.entities_group.add(chicken_jokey)
        self.entities_group.add(jokey)

        self.game_state["Menu"] = MainMenu(self)
        self.game_state["Gameplay"] = Gameplay(self, background)
        self.current_state = "Menu"

        while self.program_running:
            keys = pygame.key.get_pressed()
            if event_object.is_keypress(pygame.K_q):
                show_health = []
                for i in self.entities_group.sprites():
                    show_health.append(i.health)
                print(show_health)
            self.tracker2 = pygame.time.get_ticks()
            # event_object.update_event(self)

            if keys[pygame.K_LSHIFT] and event_object.is_keypress(pygame.K_1):
                if self.debug_mode is True:
                    self.debug_mode = False
                else :
                    self.debug_mode = True


            # print(self.tracker1, "||||||||||||||" ,self.tracker2)
            # print(f"FPS: {self.clock.get_fps():.2f}")
            # frame update calculate
            frame = self.get_frame()
            self.change_state(event_object)
            self.game_state[self.current_state].update_screen(frame)
            self.game_state[self.current_state].draw_screen()

            if self.current_state == "Gameplay":
                if self.debug_mode is True:
                    Config.open_debug(self.window, self.player, event_object.mouse_position)

            if event_object.quit_press():
                self.program_running = False

            event_object.update_event(self)
            self.clock.tick(60)
            pygame.display.update()
        pygame.quit()


if __name__ == '__main__':
    main = Main()
    main.main_loop()
