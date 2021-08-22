import pygame
import os

class Explosion:
    def __init__(self, path, screen):
        self.screen = screen
        self.folder_path = path
        self.explosion_images = os.listdir(path)
        self.explosion_anim = []
        self.animation = 0
        self.animation_frames = 4
        self.animation_done = False

    # makes the images(load it and this things)
    def create_images(self, size):
        for each_img in self.explosion_images:
            img = pygame.image.load(self.folder_path+each_img)
            img = pygame.transform.scale(img, (size, size))
            for i in range(self.animation_frames):
                self.explosion_anim.append(img)

    # draws the explosion withe the new position
    def draw(self, img_size, pos_x, pos_y):
        if len(self.explosion_anim) == 0:
            self.create_images(img_size)

        if not self.animation_done:
            if self.animation < (len(self.explosion_anim)-1):
                self.animation += 1

            img = self.explosion_anim[self.animation]
            self.screen.blit(img, (pos_x, pos_y))

            # if all the images animation loop done make the animation done
            if self.animation >= (len(self.explosion_anim)-1):
                self.animation_done = True

    # resets the animation again from 0.
    def reset_animation(self):
        self.animation_done = False
        self.animation = 0
