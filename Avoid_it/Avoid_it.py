from Engine import Missile_AI, Plane, Explosion, Button
import random
import pygame

pygame.init()

screen = pygame.display.set_mode((1280, 964))
pygame.display.set_caption('Avoid it')
# pygame window icon
icon = pygame.image.load('Images_png/Plane.png')
pygame.display.set_icon(icon)

background_colour = (0, 120, 255)
screen.fill(background_colour)

# set_up:
# sounds:
plane_flying_sound = pygame.mixer.Sound('Sounds/Plane_flying.mp3')
explosion_sound = pygame.mixer.Sound('Sounds/Explosion.wav')

# images for the game
plane_img_path = 'Images_png/Plane.png'
missile_img_path = 'Images_png/Missile.png'
explosion_img_path = 'Explosion_png/'

start_button_img = 'Images_png/Start.png'
start_button_img_pressed = 'Images_png/Start_pressed.png'

quit_button_img = 'Images_png/Quit.png'
quit_button_img_pressed = 'Images_png/Quit_pressed.png'

pause_button_img = 'Images_png/Pause.png'
pause_button_img_pressed = 'Images_png/Pause_pressed.png'

resume_button_img = 'Images_png/Resume.png'
resume_button_img_pressed = 'Images_png/Resume_pressed.png'

menu_button_img = 'Images_png/Menu.png'
menu_button_img_pressed = 'Images_png/Menu_pressed.png'


pointer_img_path = 'Images_png'


def start():
    clock = pygame.time.Clock()
    FPS = 60
    cover = screen.fill(background_colour)

    start_button = Button.Button(screen, start_button_img, start_button_img_pressed, color_alpha=255, width_size=280, height_size=115,
                                 pos_x=(screen.get_width()/2), pos_y=screen.get_height()/2-250)

    menu_button = Button.Button(screen, menu_button_img, menu_button_img_pressed, 255, 225, 100,
                                 (screen.get_width()/2), screen.get_height()/2)
    quit_button = Button.Button(screen, quit_button_img, quit_button_img_pressed, 255, 225, 100,
                                 (screen.get_width()/2-5), screen.get_height()/2-110)

    pause_button = Button.Button(screen, pause_button_img, pause_button_img_pressed, 150, 75, 75,
                                 (screen.get_width()-75), screen.get_height()-75)
    resume_button = Button.Button(screen, resume_button_img, resume_button_img_pressed, 255, 75, 75,
                                 (screen.get_width()-75), screen.get_height()-75)

    # resets all the values in the buttons
    def reset_buttons():
        start_button.reset()
        menu_button.reset()
        pause_button.reset()
        resume_button.reset()

    def start_menu():
        quit_menu = False
        while not start_button.clicked and not quit_menu:
            cover = screen.fill(background_colour)
            start_button.draw(start_button.color_alpha)

            quit_button.draw(quit_button.color_alpha)
            if quit_button.clicked:
                quit_menu = True

            pygame.display.update()
            clock.tick(FPS)
            for event_pygame in pygame.event.get():
                if event_pygame.type == pygame.QUIT:
                    quit_menu = True

    start_menu()

    if start_button.clicked:
        running_game = True
    else:
        running_game = False

    if running_game:
        plane = Plane.Plane(screen, plane_img_path, movement=5.5, rotation=2.5, pos_x=200, pos_y=313)

        missiles = []
        missiles_hits = 0
        last_missile_spawn = 0
        basic_missile_speed = 6.5

        explosions = []
        missile_explosions = {}

        def make_new_missile(movement, rotation, cicles_limit):
            missile_x_spawn = random.choice(
                [random.randint(-700, -300), random.randint((screen.get_width() + 300), (screen.get_width()) + 700)])
            missile_y_spawn = random.choice(
                [random.randint(-700, -300), random.randint((screen.get_width() + 300), (screen.get_width()) + 700)])

            missile_AI = Missile_AI.AI_Missile(screen, missile_img_path, movement=movement, rotation=rotation,
                                               pos_x=missile_x_spawn, pos_y=missile_y_spawn, cicles_limit=cicles_limit, plane_x=plane.pos_x,
                                               plane_y=plane.pos_y)

            missiles.append(missile_AI)

        pygame.font.init()
        font = pygame.font.SysFont('arial', 30)
        text_color = (75, 75, 75)

        # the game's loop
        plane_dead = False
        pygame.mixer.unpause()
        start_tick = pygame.time.get_ticks()
        pause_seconds = 0
        seconds = 0

    while running_game:
        if not plane_dead:
            if seconds > 0:
                seconds_changed = ((((pygame.time.get_ticks()-start_tick)/1000)-last_seconds)-pause_seconds)
                seconds += seconds_changed
            else:
                seconds = (pygame.time.get_ticks()-start_tick)/1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_game = False

        cover = screen.fill(background_colour)

        # seconds display text:
        text_seconds = font.render(('time: '+(str(int(seconds)))), True, (text_color))
        screen.blit(text_seconds, (50, 50))

        # missiles_hits display text:
        missiles_hits_text = font.render('missiles hit: '+(str(missiles_hits)), True, (text_color))
        screen.blit(missiles_hits_text, ((screen.get_width()-(missiles_hits_text.get_width()+50)), 50))

        # score text display:
        if plane_dead:
            score_text = font.render('score: '+(str(int(seconds)+missiles_hits)), True, (text_color))
            screen.blit(score_text,(((screen.get_width()/2)-(score_text.get_width()/2)), 150))

        if len(missiles) > 0:
            for each_missile in missiles:
                if each_missile.plane_dead:
                    plane_dead = True
                    missiles.remove(each_missile)
                    break

        if not plane_dead:
            plane.draw()
            if not pygame.mixer.Channel(0).get_busy():
                pygame.mixer.Channel(0).play(plane_flying_sound)
            loop_plane = 1
        else:
            if pygame.mixer.Channel(0).get_busy():
                pygame.mixer.Channel(0).stop()
            if loop_plane == 1:
                pygame.mixer.Channel(2).play(explosion_sound)
                plane_explosion = Explosion.Explosion(explosion_img_path, screen)
                explosions.append(plane_explosion)
                explosion_name = plane_explosion

            if explosion_name in explosions:
                plane_explosion.draw(100, (plane.pos_x - 60), (plane.pos_y - 80))
                loop_plane += 1
                if plane_explosion.animation_done:
                    explosions.remove(plane_explosion)
                    del plane_explosion

        # creating missiles:
        if (seconds-last_missile_spawn) > 1 and seconds < 20 and len(missiles) < 1:
            make_new_missile(6, 1.5, 1100)
            last_missile_spawn = seconds
        
        elif (seconds-last_missile_spawn) > 2 and seconds > 20 and seconds < 60 and len(missiles) < 2:
            make_new_missile(6.25, 1.75, 1200)
            last_missile_spawn = seconds

        elif (seconds-last_missile_spawn) > 2 and len(missiles) < 3 and seconds > 60:
            in_seconds_20 = int(seconds//20)
            missile_speed = basic_missile_speed

            for i in range((in_seconds_20+1)):
                if i > 3:
                    missile_speed += 0.5

            make_new_missile(missile_speed, 1.75, 1500)
            last_missile_spawn = seconds

        # draw missiles:
        if len(missiles) > 0:
            for missile in missiles:
                if not missile.missile_dead:
                    if not plane_dead:
                        missile.draw(plane.pos_x, plane.pos_y, plane.teleported)
                    else:
                        if not missile.over_cicles_limit:
                            missile.wonder()

            for missile in missiles:
                for each_missile_check in missiles:
                    if each_missile_check != missile and not missile.missile_dead and not missile.over_cicles_limit:
                        missile.check_missiles(each_missile_check.missile_rect)
                        if missile.missile_dead:
                            missile_explosion = Explosion.Explosion(explosion_img_path, screen)

                            missile_explosions[missile] = missile_explosion
                            missiles_hits += 1
                            pygame.mixer.Channel(1).play(explosion_sound)

                    elif each_missile_check.missile_dead and missile.over_cicles_limit:
                        missiles.remove(each_missile_check)
                        del each_missile_check

                if missile.missile_dead:
                    # explosion animation and delete missile:
                    try:
                        missile_test = missile_explosions[missile]
                        done = False
                    except:
                        done = True

                    if not done:
                        missile_explosions[missile].draw(100, (missile.pos_x - 60), (missile.pos_y - 80))
                        if missile_explosions[missile].animation_done:
                            # end the explosion drawing:
                            # remove the explosion
                            del missile_explosions[missile]
                            # remove the missile
                            missiles.remove(missile)
                            del missile

        if len(missiles) > 0:
            plane.teleported = missiles[0].missile_teleported


        if not plane_dead:
            restart_program = False
            pause_button.draw(pause_button.color_alpha) # this draws the pause button

            if pause_button.clicked and not restart_program and not menu_button.clicked:
                seconds_stoped = seconds

            while pause_button.clicked and not restart_program and not menu_button.clicked: # this loop runs when paused
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running_game = False
                        pause_button.clicked = False
                pygame.mixer.pause()

                cover = screen.fill(background_colour)
                resume_button.draw(resume_button.color_alpha)  # draws the resume button
                menu_button.draw(menu_button.color_alpha) # draws the menu button

                if menu_button.clicked:
                    reset_buttons()
                    del missiles
                    del plane
                    running_game = False
                    start()

                # resets the buttons to make it use able for another time after finishing from the buttons
                if resume_button.clicked:
                    pause_seconds = (((pygame.time.get_ticks() - start_tick) / 1000)-seconds_stoped)
                    reset_buttons()
                    pygame.mixer.unpause()

                pygame.display.update()
                clock.tick(FPS)

        else:
            menu_button.draw(175)  # draws the menu button
            if menu_button.clicked:
                reset_buttons()
                del missiles
                del plane
                running_game = False
                start()

        last_seconds = seconds

        pygame.display.update()
        clock.tick(FPS)

start()
