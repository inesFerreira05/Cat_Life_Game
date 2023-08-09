import pygame
from pygame.locals import *

from configs import *
from iterations import *
from cat import *
from vaccum import *
from food import *
from toy import *
from toy_manager import *
from parasite import *
from parasite_manager import *
from button import *
from energy_bar import *

pygame.init()

screen = pygame.display.set_mode([Window.WIDTH, Window.HEIGHT])
pygame.display.set_caption(Window.TITLE)
pygame.display.set_icon(Window.ICON)

Sound.AMBIENCE.play(loops=-1)
Sound.AMBIENCE.set_volume(0.05)

# colors
menu_bg_color = (33, 192, 165)
light_green = (143, 189, 128)
dark_green = (0, 128, 64)
light_yellow = (253, 240, 99)
dark_yellow = (243, 224, 18)
light_red = (245, 131, 136)
dark_red = (239, 50, 60)

#buttons
play_button = Button(80, 230, 130, 40, dark_green)
instructions_button = Button(298, 230, 205, 40, dark_yellow)
close_button = Button(696, 9, 35, 35, dark_red)
exit_button = Button(590, 230, 130, 40, dark_red)
try_again_button = Button(618, 288, 170, 42, dark_green)

cat = Cat(100, 290)
vaccum = Vaccum(200, 310)
food = Food(10, 241)
toys = Toy_manager()
parasites = Parasite_manager()
energy_bar = Energy_bar()

clock = pygame.time.Clock()
game_state = Screen.MAIN_MENU

while 1:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    # Menu
    if game_state == Screen.MAIN_MENU:
        screen.fill(menu_bg_color)
        menu_mensage = Font.CONCERT_50.render("CAT LIFE - MENU", True, "white")
        screen.blit(menu_mensage, [210, 80])
        play_button.draw()
        play_mensage = Font.CONCERT_30.render("PLAY", True, "white")
        screen.blit(play_mensage, [108, 230])
        instructions_button.draw()
        instructions_mensage = Font.CONCERT_30.render("INSTRUTIONS", True, "white")
        screen.blit(instructions_mensage, [312, 230])
        exit_button.draw()
        exit_mensage = Font.CONCERT_30.render("EXIT", True, "white")
        screen.blit(exit_mensage, [630, 230])

        if exit_button.identify_button(light_red):
            pygame.quit()
            quit()
        elif play_button.identify_button(light_green):
            game_state = Screen.GAME_ACTIVE
        elif instructions_button.identify_button(light_yellow):
            game_state = Screen.INSTRUCTIONS_MENU

    elif game_state == Screen.INSTRUCTIONS_MENU:
        screen.blit(Img.INSTRUTIONS, [50, 0])
        close_button.draw()
        close_mensage = Font.CONCERT_30.render("X", True, "white")
        screen.blit(close_mensage, [704, 6])

        if close_button.identify_button(light_red):
            game_state = Screen.MAIN_MENU
    # Play the game
    elif game_state == Screen.GAME_ACTIVE:
        screen.blit(Img.BACKGROUND, [0, 0])
        energy_bar.draw(cat)
        energy_bar.show_energy(cat)

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            cat.move(Direction.LEFT)
        elif key[pygame.K_RIGHT]:
            cat.move(Direction.RIGHT)

        if key[pygame.K_SPACE]:
            cat.jump()

        vaccum.move()
        vaccum.draw(screen)
        vaccum.increase_speed()
        food.move()
        cat.draw(screen)
        cat.update_jump()
        toys.draw_all(screen)
        parasites.draw_all(screen)
        toys.play(cat)
        parasites.get_sick(cat)
        cat.die(vaccum)
        cat.limit_energy()

        if cat.energy > 0 and cat.energy <= 30:             # Ou in range(1, 31)
            food.draw(screen)
            if cat.colides_with(food):
                cat.eat(food)
        elif cat.energy == 0:
            game_state = Screen.GAMEOVER

    elif game_state == Screen.GAMEOVER:
        screen.blit(Img.GAMEOVER, [150, 0])
        try_again_button.draw()
        try_again_mensage = Font.CONCERT_30.render("TRY AGAIN", True, "white")
        screen.blit(try_again_mensage, [627, 290])
        if try_again_button.identify_button(light_green):
            cat.reset()
            vaccum.reset()
            parasites.reset_parasites()
            toys.reset_toys()
            game_state = Screen.MAIN_MENU

    pygame.display.update()

pygame.quit()

