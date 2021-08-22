import pygame

class Button:
    def __init__(self, screen, image, image_pressed, color_alpha, width_size, height_size, pos_x, pos_y):
        self.screen = screen
        self.image = image
        self.image_pressed = image_pressed
        self.height_size = height_size
        self.width_size = width_size

        self.color_alpha = color_alpha

        self.on_click = False
        self.done_click = False
        self.clicked = False

        self.pos_x = pos_x-(self.width_size/2)
        self.pos_y = pos_y-(self.height_size/2)

        self.id = pygame.image.load(self.image)
        self.id = pygame.transform.scale(self.id, (self.width_size, self.height_size))
        self.id.set_alpha(self.color_alpha)

        self.id_pressed = pygame.image.load(self.image_pressed)
        self.id_pressed = pygame.transform.scale(self.id_pressed, (self.width_size, self.height_size))
        self.id_pressed.set_alpha(self.color_alpha)

    # resets the button settings
    def reset(self):
        self.clicked = False
        self.on_click = False
        self.done_click = False

    # checks if the button have been clicked.
    def check_click(self):
        # checks if the mouse is inside the button
        self.mouse_pos = pygame.mouse.get_pos()
        if self.mouse_pos[1] >= self.pos_y and self.mouse_pos[1] <= (self.pos_y+self.height_size):
            if self.mouse_pos[0] >= self.pos_x and self.mouse_pos[0] <= (self.pos_x+self.width_size):
                if pygame.mouse.get_pressed()[0]:
                    self.on_click = True
                else:
                    self.on_click = False
            else:
                self.on_click = False
                self.done_click = False
        else:
            self.on_click = False
            self.done_click = False

    # draws the button with new image if pressed
    def draw(self, color_alpha):
        if color_alpha != self.color_alpha:
            self.color_alpha = color_alpha
            self.id.set_alpha(self.color_alpha)
            self.id_pressed.set_alpha(self.color_alpha)

        self.check_click()
        if not self.on_click:
            self.screen.blit(self.id, (self.pos_x, self.pos_y))
            if self.done_click:
                self.clicked = True

        else:
            self.screen.blit(self.id_pressed, (self.pos_x, self.pos_y))
            self.done_click = True
