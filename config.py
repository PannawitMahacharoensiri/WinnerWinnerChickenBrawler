import math
import pygame

class Config:
    color = {'black': (0, 0, 0), 'white': (255, 255, 255), 'green':(0, 255, 0)}

    @staticmethod
    def screen_ratio(curr_screen_info, current_scale):
        change_scale = False
        valid_screen_info = curr_screen_info
        valid_scale = current_scale

        if curr_screen_info[0] > 1920 or curr_screen_info[1] > 1080 or curr_screen_info == (1920, 1080) :
            valid_screen_info = (1920, 1080)
            valid_scale = 6
        elif curr_screen_info[0] > 1600 or curr_screen_info[1] > 900 or curr_screen_info == (1600, 900):
            valid_screen_info = (1600, 900)
            valid_scale = 5
        elif curr_screen_info[0] > 1366 or curr_screen_info[1] > 768 or curr_screen_info == (1366, 768):
            valid_screen_info = (1366, 768)
            valid_scale = 4.26875
        elif curr_screen_info[0] > 1280 or curr_screen_info[1] > 720 or curr_screen_info == (1280, 720):
            valid_screen_info = (1280, 720)
            valid_scale = 4
        elif curr_screen_info[0] > 1024 or curr_screen_info[1] > 576 or curr_screen_info == (1024, 576):
            valid_screen_info = (1024, 576)
            valid_scale = 3.2
        elif curr_screen_info[0] > 960 or curr_screen_info[1] > 540 or curr_screen_info == (960, 540):
            valid_screen_info = (960, 540)
            valid_scale = 3
        elif curr_screen_info[0] > 640 or curr_screen_info[1] > 360 or curr_screen_info == (640, 360):
            valid_screen_info = (640, 360)
            valid_scale = 2
        elif curr_screen_info[0] > 320 or curr_screen_info[1] > 180 or curr_screen_info == (320, 180):
            valid_screen_info = (320, 180)
            valid_scale = 1

        if valid_scale/current_scale != 1:
            change_scale = True
        ## Screen_width / classic_character&screen_ratio(=16) -> sprite_pixel in that screen_width / classic character pixel -> scale
        return [change_scale, valid_screen_info, valid_scale]

    @staticmethod
    def get_length(start_pos, end_pos):
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        length = math.sqrt(dx ** 2 + dy ** 2)
        return length, dx, dy

    @staticmethod
    def window_to_screen(window, screen):
        new_window = window
        if window[0] < screen[0] or window[1] < screen[1]:
            new_window = screen
        return new_window

    @staticmethod
    def check_overlay(each_one, entities):
        overlay = False
        if each_one.death is False:
            if (each_one.rect.x < entities.rect.center[0] < each_one.rect.x + each_one.size and
                    each_one.rect.y < entities.rect.center[1] < each_one.rect.y + each_one.size):
                overlay = True
        return overlay

    @staticmethod
    def entities_overlay(entities, new_position, old_position):
        valid_x = new_position[0]
        valid_y = new_position[1]

        for each_one in entities.game.entities_group:
            if each_one != entities:
                overlay = Config.check_overlay(each_one, entities)
                if overlay is True:
                    valid_x = old_position[0]
                    valid_y = old_position[1]
        return valid_x, valid_y

    @staticmethod
    def check_boundary(entities, arena_area):
        # Save position, if the value not exceed boundaries can just use the start position
        valid_x = entities.rect.x
        valid_y = entities.rect.y
        wall_direction = None
        hit_wall = False

        # Check then set new position x
        if entities.rect.x < arena_area["start_x"]:
            hit_wall = True
            wall_direction = 1
            valid_x = arena_area["start_x"]
        elif entities.rect.x + entities.rect.width > arena_area["end_x"]:
            hit_wall = True
            wall_direction = 3
            valid_x = arena_area["end_x"] - entities.rect.width

        # Check then set new position y
        if entities.rect.y < arena_area["start_y"]:
            hit_wall = True
            wall_direction = 0
            valid_y = arena_area["start_y"]
        elif entities.rect.y + entities.rect.height > arena_area["end_y"]:
            hit_wall = True
            wall_direction = 2
            valid_y = arena_area["end_y"] - entities.rect.height
        return valid_x, valid_y, hit_wall, wall_direction

    @staticmethod
    def get_degree(A,B):
        if len(A) == 2 and len(B) == 2 :
            if not all(isinstance(each, (int, float)) for each in A):
                return 0
            if not all(isinstance(each, (int, float)) for each in B):
                return 0
            angle = math.atan2(A[1] - B[1], A[0] - B[0])
            angle_degree = int(angle * 180 / math.pi)
            return angle_degree
        return 0

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
            angle_is = "E"
        elif 45 <= degree <= 135:
            angle_is = "N"
        elif -135 <= degree <= -45:
            angle_is = "S"
        elif 0 <= degree <= 45 or -45 <= degree <= 0:
            angle_is = "W"
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
    def shift_position(angle, attack_width, attack_height, maker_size):
        x = 0
        y = 0

        if angle == "N":
            y = -(attack_height/2) -(maker_size/2)
        elif angle == "E":
            x = (attack_width/2) + (maker_size/2)
        elif angle == "W":
            x =  - attack_width/2 - maker_size/2
        elif angle == "S":
            y = attack_height/2 + maker_size/2
        elif angle == "NE":
            x = (attack_width / 2) + (maker_size / 2)
            y = -(attack_height/2) -(maker_size/2)
        elif angle == "SE":
            x = (attack_width / 2) + (maker_size / 2)
            y = attack_height / 2 + maker_size / 2
        elif angle == "SW":
            x = - attack_width/2 - maker_size/2
            y = attack_height / 2 + maker_size / 2
        elif angle == "NW":
            x = - attack_width/2 - maker_size/2
            y = -(attack_height/2) -(maker_size/2)
        return [x,y]

    @staticmethod
    def check_attack_collision(attack_group, entities_group):
        collide = pygame.sprite.groupcollide(attack_group, entities_group, False, False)
        if collide != {}:
            for bullet, entities_group in collide.items():
                for entities in entities_group:
                    if (type(bullet.maker) != type(entities) and entities not in bullet.already_hit
                                                and entities.action != "hurt" and entities.cooldown["hurt"] == 0):
                        entities.health_reduce(bullet.damage)
                        bullet.already_hit.append(entities)


class EntitiesGroup(pygame.sprite.Group):

    """
    DRAW SPRITE IN ORDER(Y-value)
        how it works : modify build-in class(pygame.sprite.Group) to add more behaviour to draw function of it
    CREDIT:
        Author(stackoverflow account) : sloth
        from post : https://stackoverflow.com/questions/55233448/pygame-overlapping-sprites-draw
                -order-based-on-location
    """

    @staticmethod
    def get_y(entities):
        return entities.rect.y

    def draw(self, surface):
        sprites = self.sprites()
        surface_blit = surface.blit
        for entity in sorted(sprites, key=self.get_y):
            self.spritedict[entity] = surface_blit(entity.image, entity.rect)