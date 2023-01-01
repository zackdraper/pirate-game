import pygame
import pygame_menu
import sys
import pygame.mixer as mixer

# screen resolution
res = (1024,768)

pygame.init()
screen = pygame.display.set_mode(res)

# white color
color = (255,255,255)

# light shade of the button
color_light = (170,170,170)

# dark shade of the button
color_dark = (100,100,100)

# stores the width of the
# screen into a variable
width = screen.get_width()

# stores the height of the
# screen into a variable
height = screen.get_height()

# defining a font
smallfont = pygame.font.SysFont('Corbel',35)

# rendering a text written in
# this font
text = smallfont.render('quit' , True , color)

def set_number_of_players(value, difficulty):
    # Do the job here !
    pass

def start_the_game():
    # Do the job here !
    pass

# Play Intro Music
mixer.init()
mixer.music.load("music/intro.mp3")
mixer.music.set_volume(0.7)
mixer.music.play()

menu = pygame_menu.Menu('Welcome', 400, 300,
                       theme=pygame_menu.themes.THEME_BLUE)

menu.add.text_input('Name :', default='John Doe')
menu.add.selector('Players :', [('1', 1), ('2', 2), ('3', 3), ('4', 4)], onchange=set_number_of_players)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(screen)