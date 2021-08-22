import math as Math
import pygame
from pygame import *


class Plane:
    def __init__(self, screen, image, movement, rotation, pos_x, pos_y):
        self.screen = screen
        self.surface = pygame.display.get_surface()

        self.image = image
        self.size = 54
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.Movement = movement
        self.movement = self.Movement
        self.teleported = False
        self.rotating = rotation
        self.angle = 0

        self.dead = False

        self.id = pygame.image.load(self.image)
        self.id = pygame.transform.scale(self.id, (self.size, self.size))
        self.id = pygame.transform.rotate(self.id, -90)
        self.screen.blit(self.id, (self.pos_x, self.pos_y))

    # walls teleporter:
    def walls(self):
        # left side
        if self.pos_x <= (self.size/2):
            self.pos_x = (self.surface.get_width() - (self.size / 2))
            self.teleported = True
        # right side:
        elif self.pos_x >= ((self.surface.get_width()) - (self.size / 2 - 1)):
            self.pos_x = (self.size/2)
            self.teleported = True

        # up side
        elif self.pos_y <= (self.size/2-1):
            self.pos_y = (self.surface.get_height() - (self.size/2))
            self.teleported = True
        # down side:
        elif self.pos_y >= ((self.surface.get_height()) - (self.size/2-1)):
            self.pos_y = (self.size/2)
            self.teleported = True

    # makes the angle from 0 to 360 instead of from 0 to forever
    def do_angle(self):
        if self.angle >= 360:
            self.angle = 0
        if self.angle < 0:
            self.angle = 359

    # let the player control the plane
    def movement_controls(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_RIGHT]:
            self.angle -= self.rotating
        if pressed_keys[K_LEFT]:
            self.angle += self.rotating
        if pressed_keys[K_UP]:
            if self.movement < (self.Movement - 0.1):
                self.movement += 0.0208333333333333
        if pressed_keys[K_DOWN]:
            if self.movement > 3.1:
                self.movement -= 0.0208333333333333

    # moves the plane to the direction its heading
    def move(self):
        x_move = (Math.cos(Math.radians(self.angle)) * self.movement)
        y_move = (Math.sin(Math.radians(self.angle)) * self.movement)
        y_move -= y_move * 2
        self.pos_x = self.pos_x + x_move
        self.pos_y = self.pos_y + y_move

    # draws the plane with the new updates(of its position and that things)
    def draw(self):
        # movement and rotation:
        self.movement_controls()
        self.do_angle()
        self.move()

        rotated_id = pygame.transform.rotate(self.id, self.angle)
        rotated_rect = rotated_id.get_rect(center=(round(self.pos_x), round(self.pos_y)))
        self.screen.blit(rotated_id, rotated_rect)

        self.walls()
