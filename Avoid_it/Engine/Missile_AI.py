import math as Math
import pygame

class AI_Missile:
    def __init__(self, screen, image, movement, rotation, pos_x, pos_y, cicles_limit, plane_x, plane_y):
        self.screen = screen

        self.image = image
        self.angle = 0

        # the position of the plane
        self.plane_x = plane_x
        self.plane_y = plane_y
        # the position of the missile
        self.pos_x = pos_x
        self.pos_y = pos_y

        # how much the missile is far away from the plane (x,y):
        self.difference_pos_x = self.pos_x - plane_x
        self.difference_pos_y = self.pos_y - plane_y

        self.missile_teleported = False
        self.last_plane_x_y = (plane_x, plane_y)

        # cicles is for how many frames the missile can live for.
        self.cicles = 0
        self.cicles_limit = cicles_limit
        self.over_cicles_limit = False

        self.plane_dead = False
        self.missile_dead = False

        # how much it should move each frame:
        self.Movement = movement
        # how much it should rotate each frame:
        self.rotation = rotation

        # making the missile image and setting its locations
        self.id = pygame.image.load(self.image)
        self.id = pygame.transform.scale(self.id, (10, 34))
        self.id = pygame.transform.rotate(self.id, -90)
        self.screen.blit(self.id, (self.pos_x, self.pos_y))

    # this function teleports the missile when the plane teleports, where I don't use camera :(.
    def teleport(self, plane_teleported):
        if plane_teleported:
            x_change = self.last_plane_x_y[0]-self.plane_x
            y_change = self.last_plane_x_y[1]-self.plane_y
            self.pos_x -= x_change
            self.pos_y -= y_change
        self.missile_teleported = False

    '''
    the angle for the head pointing can go more than 360 degs,
    so this function (do_angle) can prevent that from happening,
    where it sets the angle back to 0 if its more that 360 and the same for the other side.
    '''
    def do_angle(self):
        if self.angle >= 360:
            self.angle = 0
        if self.angle < 0:
            self.angle = 359

    # this function convert an angle from a 360 circle to 180,-180 circle
    def convert_to_360_circle(self, angle):
        if angle < 0:
            remainder = -180 - angle
            angle -= angle*2
            angle = angle - (remainder*2)
        return angle

    # this function converts an angle from a 180,-180 circle to a 360 circle
    def convert_to_180_circle(self, angle):
        if angle < 180:
            remainder = angle - 180
            angle -= angle * 2
            angle = angle + (remainder * 2)
        return angle

    # this function kills the missile and the other missile when they toutch each other.
    def check_missiles(self,  other_missile_rect):
        '''
        first we check the left and side of the missile is empty
        and then we check the up and down side of the missile is empty too.
        '''
        if other_missile_rect.bottom >= self.missile_rect.top and other_missile_rect.top <= self.missile_rect.bottom:
            if other_missile_rect.right >= self.missile_rect.left and other_missile_rect.left <= self.missile_rect.right:
                self.missile_dead = True

    # this function kill the missile and the plane when they touch each other.
    def check_plane(self,  plane_pos_x, plane_pos_y):
        if self.pos_x > plane_pos_x:
            x_arc = self.pos_x-plane_pos_x
        else:
            x_arc = plane_pos_x-self.pos_x

        if self.pos_y > plane_pos_y:
            y_arc = self.pos_y-plane_pos_y
        else:
            y_arc = plane_pos_y-self.pos_y

        if x_arc <= 28 and y_arc <= 37:
            self.plane_dead = True

    # this function if the cicles is over the cicles limit.
    def check_cicles(self):
        if not self.over_cicles_limit and self.cicles > self.cicles_limit:
            self.over_cicles_limit = True
        elif self.over_cicles_limit and self.id.get_alpha() > 0:
            self.id.set_alpha((self.id.get_alpha())-1.5)

        if self.id.get_alpha() <= 0:
            self.missile_dead = True


    # this function tries to head the missile's angle to the plane.
    def angle_missile_to_plane(self, angle, plane_x, plane_y):
        # distances between the target and the missile
        self.difference_pos_x = self.pos_x - plane_x
        self.difference_pos_y = self.pos_y - plane_y
        self.difference_pos_x -= self.difference_pos_x*2
        # angle between the missile and the plane:
        angle_to_plane = Math.degrees(Math.atan2(self.difference_pos_y, self.difference_pos_x))
        angle_to_plane = self.convert_to_360_circle(angle_to_plane)

        # angle between the missile's angle and the plane's angle:
        right = self.convert_to_360_circle(angle_to_plane - angle)
        left = self.convert_to_360_circle(angle - angle_to_plane)

        # left or right decision
        if right < left:
            missile_to_plane_angle = self.rotation
        elif left < right:
            rotation_reversed = self.rotation - self.rotation*2
            missile_to_plane_angle = rotation_reversed
        else:
            missile_to_plane_angle = 0

        return missile_to_plane_angle

    # this function move the missile to its heading point.
    def move(self):
        # move:
        x_move = (Math.cos(Math.radians(self.angle)) * self.Movement)
        y_move = (Math.sin(Math.radians(self.angle)) * self.Movement)
        y_move -= y_move * 2
        self.pos_x = self.pos_x + x_move
        self.pos_y = self.pos_y + y_move

    # this function draws the missile on the screen and update its position and all that work
    def draw(self, plane_x, plane_y, plane_teleported):
        self.plane_x = plane_x
        self.plane_y = plane_y

        self.teleport(plane_teleported)

        if not self.over_cicles_limit:
            self.do_angle()
            self.angle += self.angle_missile_to_plane(self.angle, self.plane_x, self.plane_y)

        self.move()

        self.cicles += 1
        self.check_cicles()

        self.rotated_id = pygame.transform.rotate(self.id, self.angle)
        self.missile_rect = self.rotated_id.get_rect(center=(round(self.pos_x), round(self.pos_y)))
        self.screen.blit(self.rotated_id, self.missile_rect)
        if not self.over_cicles_limit:
            self.check_plane(self.plane_x, self.plane_y)

        self.last_plane_x_y = (self.plane_x, self.plane_y)

    '''
    this function should work just when the plane is dead we its called instead of the draw function 
        were it(the missile) just move around its self like it doesn't knows where to go
    '''
    def wonder(self):
        self.angle += self.rotation
        self.move()
        self.check_cicles()
        self.rotated_id = pygame.transform.rotate(self.id, self.angle)
        self.missile_rect = self.rotated_id.get_rect(center=(round(self.pos_x), round(self.pos_y)))
        self.screen.blit(self.rotated_id, self.missile_rect)
