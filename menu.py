import pygame
import pygame_menu
import pygame.mixer as mixer
from pygame_menu import sound
from ship_battle import main as ship_battle
from tile_map import main as tile_map 

res = (1024,768)
pygame.init()
screen = pygame.display.set_mode(res)

color = (255,255,255)
color_light = (170,170,170)
color_dark = (100,100,100)
width = screen.get_width()
height = screen.get_height()

global NUM_PLAYERS

def set_number_of_players(value, players):
    NUM_PLAYERS = value

def start_the_game():
    pygame.mixer.music.stop()
    tile_map()
    menu_music()

def start_ship_battle():
    pygame.mixer.music.stop()
    ship_battle()
    menu_music()

def game_credits():
    pass

def menu_music():
    mixer.music.load("music/intro.mp3")
    mixer.music.set_volume(0.7)
    mixer.music.play(loops=-1)

pirate_font = pygame.font.Font("font/TradeWinds-Regular.ttf", 36)

# Play Intro Music
mixer.init()
menu_music()

# Sounds
menu_sound = sound.Sound()
menu_sound.set_sound(pygame_menu.sound.SOUND_TYPE_WIDGET_SELECTION, sound_file='music/sword.mp3')


game_theme = pygame_menu.themes.THEME_DARK
title_image = pygame_menu.baseimage.BaseImage(
    image_path="images/title_page.png",
)
game_theme.background_color = title_image
game_theme.title_bar_style = title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
game_theme.widget_font = pirate_font
game_theme.widget_font_color = (0, 0, 0)
game_theme.selection_color = (255, 215, 0)
game_theme.widget_selection_effect = pygame_menu.widgets.LeftArrowSelection()
game_theme.widget_font_shadow = True
game_theme.widget_font_shadow_color = (0, 0, 0)
game_theme.widget_font_shadow_offset = 1
game_theme.widget_font_size = 36
game_theme.widget_offset = (0.0, 0.35)
menu = pygame_menu.Menu('', width, height, theme=game_theme)

menu.set_sound(menu_sound, recursive=True)

menu.add.button('Play Game', start_the_game)
menu.add.selector('Players :', [('1', 1), ('2', 2), ('3', 3), ('4', 4)], onchange=set_number_of_players)
menu.add.button('Ship Battle', start_ship_battle)
menu.add.button('Credits', game_credits)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(screen)