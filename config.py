import math
import pygame

class Config:
    frame_delay = 300
    color = {'black': (0, 0, 0), 'white': (255, 255, 255), 'green':(0, 255, 0)}

    @staticmethod
    def screen_ratio(curr_screen_info, current_scale):
        change_scale = False
        valid_screen_info = curr_screen_info
        valid_scale = current_scale

        if curr_screen_info[0] > 1920 or curr_screen_info[1] > 1080:
            valid_screen_info = (1920, 1080)
            valid_scale = 7.5
        elif curr_screen_info[0] > 1600 or curr_screen_info[1] > 900:
            valid_screen_info = (1600, 900)
            valid_scale = 6.25
        elif curr_screen_info[0] > 1366 or curr_screen_info[1] > 768:
            valid_screen_info = (1366, 768)
            valid_scale = 5.3359375
        elif curr_screen_info[0] > 1280 or curr_screen_info[1] > 720:
            valid_screen_info = (1280, 720)
            valid_scale = 5
        elif curr_screen_info[0] > 1024 or curr_screen_info[1] > 576:
            valid_screen_info = (1024, 576)
            valid_scale = 4
        elif curr_screen_info[0] > 854 or curr_screen_info[1] > 480:
            valid_screen_info = (854, 480)
            valid_scale = 3.3359375

        if valid_scale/current_scale != 1:
            change_scale = True
        ## Screen_width / classic_character&screen_ratio(=16) -> sprite_pixel in that screen_width / classic character pixel -> scale
        return [change_scale, valid_screen_info, valid_scale]

    @staticmethod
    def window_to_screen(window, screen):
        new_window = window
        if window[0] < screen[0] or window[1] < screen[1]:
            new_window = screen
        return new_window

    @staticmethod
    def check_boundary(corner_position, entities_size, screen_info, screen_start):
        # Save position, if the value not exceed boundaries can just use the start position
        valid_x = corner_position[0]
        valid_y = corner_position[1]

        # Check then set new position x
        if corner_position[0] <= 0 + screen_start[0]:
            valid_x = 0 + screen_start[0]
        elif corner_position[0]+ entities_size >= screen_info[0] + screen_start[0]:
            valid_x = screen_info[0] + screen_start[0] -entities_size

        # Check then set new position y
        if corner_position[1] <= 0 + screen_start[1]:
            valid_y = 0 + screen_start[1]
        elif corner_position[1]+ entities_size >= screen_info[1] + screen_start[1]:
            valid_y = screen_info[1] + screen_start[1] - entities_size

        return valid_x,valid_y

    @staticmethod
    def get_degree(A,B):
        if len(A) == 2 and len(B) == 2:
            angle = math.atan2(A[1] - B[1], A[0] - B[0])
            angle_degree = int(angle * 180 / math.pi)
            return angle_degree
        print("Can't compute none x,y value")

    @staticmethod
    def open_debug(screen, A, B):

        # MOUSE
        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        pygame.draw.line(screen, Config.color["green"] , A.rect.center, B, 2)

        test_degree = Config.get_degree(A.rect.center,B)
        angle = Config.check_8direction(test_degree)

        screen.blit(my_font.render(str(test_degree), False, (100, 100, 100)), (0, 0))
        screen.blit(my_font.render(angle, False, (100, 100, 100)), (0, 120))
        screen.blit(my_font.render(str(B), False, (100, 100, 100)), (0, 60))


    ## THIS IS 4 DIRECTION
    @staticmethod
    def check_4direction(degree):
        angle_is = None
        if 135 <= degree <= 180 or -180 <= degree <= -135:
            angle_is = "W"
        elif 45 <= degree <= 135:
            angle_is = "N"
        elif -135 <= degree <= -45:
            angle_is = "S"
        elif 0 <= degree <= 45 or -45 <= degree <= 0:
            angle_is = "E"
        return angle_is

    @staticmethod
    def check_8direction(degree):
        angle_is = "Not working"
        if -22 < degree <= 22:
            angle_is = "W"
        elif -67 < degree <= -22:
            angle_is = "SW"
        elif -112 < degree <= -67:
            angle_is = "S"
        elif -157 < degree <= -112:
            angle_is = "SE"
        elif -180 <= degree <= -157 or 157 <= degree <= 180:
            angle_is = "E"
        elif 112 < degree <= 157:
            angle_is = "NE"
        elif 67 < degree <= 112 :
            angle_is = "N"
        elif 22 < degree <= 67:
            angle_is = "NW"
        return angle_is

    @staticmethod
    def direction_position(angle, attack_height, maker_size):
        x = 0
        y = 0

        if angle == "N":
            y = -(attack_height/2) -(maker_size/2)
        elif angle == "E":
            x = (attack_height/2) + (maker_size/2)
        elif angle == "W":
            x =  - attack_height/2 - maker_size/2
        elif angle == "S":
            y = attack_height/2 + maker_size/2
        elif angle == "NE":
            x = (attack_height / 2) + (maker_size / 2)
            y = -(attack_height/2) -(maker_size/2)
        elif angle == "SE":
            x = (attack_height / 2) + (maker_size / 2)
            y = attack_height / 2 + maker_size / 2
        elif angle == "SW":
            x = - attack_height/2 - maker_size/2
            y = attack_height / 2 + maker_size / 2
        elif angle == "NW":
            x = - attack_height/2 - maker_size/2
            y = -(attack_height/2) -(maker_size/2)

        return [x,y]