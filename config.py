import math

class Config:
    frame_delay = 300
    color = {'black': (0, 0, 0), 'white': (255, 255, 255)}
    screen_info = (1024, 576)

    @staticmethod
    def get_degree(A,B):
        if len(A) == 2 and len(B) == 2:
            angle = math.atan2(A[1] - B[1], A[0] - B[0])
            angle_degree = int(angle * 180 / math.pi)
            return angle_degree
        print("Can't compute none x,y value")

    @staticmethod
    def check_direction(degree):
        if 135 <= degree <= 180 or -180 <= degree <= -135:
            angle_is = "WEST"
        elif 45 <= degree <= 135:
            angle_is = "NORTH"
        elif -135 <= degree <= -45:
            angle_is = "SOUTH"
        elif 0 <= degree <= 45 or -45 <= degree <= 0:
            angle_is = "EAST"
        return angle_is

