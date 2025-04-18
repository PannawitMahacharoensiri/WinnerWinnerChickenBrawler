import math
import pygame

class Config:
    frame_delay = 300
    color = {'black': (0, 0, 0), 'white': (255, 255, 255), 'green':(0, 255, 0)}
    screen_info = (1024, 576)

    @staticmethod
    def get_degree(A,B):
        if len(A) == 2 and len(B) == 2:
            angle = math.atan2(A[1] - B[1], A[0] - B[0])
            angle_degree = int(angle * 180 / math.pi)
            return angle_degree
        print("Can't compute none x,y value")

    @staticmethod
    def debug_mode(screen, A, B):

        # MOUSE
        my_font = pygame.font.SysFont('Comic Sans MS', 50)
        pygame.draw.line(screen, Config.color["green"] , A.rect.center, B, 2)

        test_degree = Config.get_degree(A.rect.center,B)
        angle = Config.check_8direction(test_degree)

        screen.blit(my_font.render(str(test_degree), False, (100, 100, 100)), (0, 0))
        screen.blit(my_font.render(angle, False, (100, 100, 100)), (0, 120))


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