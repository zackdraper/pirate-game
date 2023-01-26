import pygame
import pygame.mixer as mixer
import string
from pygame.locals import KEYDOWN,QUIT,K_ESCAPE
from tile_map_menu import display_menu, menu_move, display_naval_action
from ports import plot_ports, PORTS
from controller import Controller
from ship import Ship
from math import floor
import random

from init import BLACK,PADLEFTRIGHT,PADTOPBOTTOM
from init import height,width,alphabet,numbers,divisions_x,divisions_y,lw
from empires import EMPIRES,empire_color
from captains import CAPTAINS

from actions import select_empire

def drawGrid(surface, divisions_x, divisions_y):
    # DRAW Rectangle
    # TOP lEFT TO RIGHT
    pygame.draw.line(
      surface, BLACK,
      (0 + PADLEFTRIGHT, 0 + PADTOPBOTTOM),
      (width - PADLEFTRIGHT, 0 + PADTOPBOTTOM), lw)
    # BOTTOM lEFT TO RIGHT
    pygame.draw.line(
      surface, BLACK,
      (0 + PADLEFTRIGHT, height - PADTOPBOTTOM),
      (width - PADLEFTRIGHT, height - PADTOPBOTTOM), lw)
    # LEFT TOP TO BOTTOM
    pygame.draw.line(
      surface, BLACK,
      (0 + PADLEFTRIGHT, 0 + PADTOPBOTTOM),
      (0 + PADLEFTRIGHT, height - PADTOPBOTTOM), lw)
    # RIGHT TOP TO BOTTOM
    pygame.draw.line(
      surface, BLACK,
      (width - PADLEFTRIGHT, 0 + PADTOPBOTTOM),
      (width - PADLEFTRIGHT, height - PADTOPBOTTOM), lw)

    # Get cell size
    horizontal_cellsize = (width - (PADLEFTRIGHT*2))/divisions_x
    vertical_cellsize = (height - (PADTOPBOTTOM*2))/divisions_y

    # VERTICAL DIVISIONS: (0,1,2) for grid(3) for example
    font = pygame.font.SysFont(None, 20)
    for x in range(divisions_x):
        pygame.draw.line(
           surface, BLACK,
           (0 + PADLEFTRIGHT+(horizontal_cellsize*x), 0 + PADTOPBOTTOM),
           (0 + PADLEFTRIGHT+horizontal_cellsize*x, height - PADTOPBOTTOM), lw)
        # Display Map Grid Labels
        title = font.render(alphabet[x],True,'black')
        surface.blit(title, (PADLEFTRIGHT+(horizontal_cellsize*x)+2,PADTOPBOTTOM))
    # HORITZONTAL DIVISION
    for x in range(divisions_y):
        pygame.draw.line(
          surface, BLACK,
          (0 + PADLEFTRIGHT, 0 + PADTOPBOTTOM + (vertical_cellsize*x)),
          (width - PADLEFTRIGHT, 0 + PADTOPBOTTOM + (vertical_cellsize*x)), lw)
        # Display Map Grid Labels
        title = font.render(numbers[x],True,'black')
        surface.blit(title, (PADLEFTRIGHT+2, PADTOPBOTTOM + (vertical_cellsize*(x+0.7))))

def display_static_screen(screen,TURN_COUNT):
    surface = pygame.surface.Surface((width,PADTOPBOTTOM-5))
    #surface.fill((227,203,165))
    surface.fill((0,0,0))
    screen.blit(surface,(0,height - (PADTOPBOTTOM-5)))

    font = pygame.font.Font('font/TradeWinds-Regular.ttf', 18)

    padleft = 10
    padtop = height - (PADTOPBOTTOM-5)

    for i,empire in enumerate(list(EMPIRES.values())):
        y = [0,1][floor(i/2)]
        x = [0,1][(i+1) % 2]
        ship_text = font.render(empire.long_name,True,empire.color)
        screen.blit(ship_text,(padleft+200*(x),padtop+30*(y)))
        screen.blit(empire.flag_small,(padleft+150+240*(x),padtop+5+33*(y)))

    text = font.render("Turns: "+str(TURN_COUNT),True,(255,255,255))
    screen.blit(text,(width/2,padtop))
    

def display_ship_stats(screen,ship):

    surface = pygame.surface.Surface((width,PADTOPBOTTOM-5))
    surface.fill((227,203,165))
    screen.blit(surface,(0,0))
    
    font = pygame.font.Font('font/TradeWinds-Regular.ttf', 18)

    ship_text = font.render('Captain '+ship.captain.name,True,'black')
    screen.blit(ship_text,(150,5))
    screen.blit(ship.captain.flag_small,(100,5))

    for i,s in enumerate(ship.captain.pirate_status):
        screen.blit(EMPIRES[s].flag_ex_small,(100+17*i,40))

    ship_text = font.render(ship.ship_class,True,'black')
    screen.blit(ship_text,(width-600,5))

    ship_text = font.render("P. of 8 :"+str(ship.gold),True,'black')
    screen.blit(ship_text,(width-500,5))

    ship_text = font.render("Moves :"+str(ship.map_moves),True,'black')
    screen.blit(ship_text,(width-500,35))

    ship_text = font.render("VP :"+str(ship.vp),True,'black')
    screen.blit(ship_text,(width-350,5))

    ship_text = font.render("Cargo :"+str(', '.join(ship.cargo)),True,'black')
    screen.blit(ship_text,(width-350,35))


def main():
    pygame.display.set_caption('Pirate Game')

    # initialize pygame
    pygame.init()

    mixer.init()
    mixer.music.load("music/the_coast_of_high_barbary.mp3")
    mixer.music.set_volume(0.15)
    #mixer.music.play(loops=-1)

    # create the screen object
    screen = pygame.display.set_mode((width, height))

    bg = pygame.image.load('images/carribbean_map_v2.png')
    bg = pygame.transform.scale(bg,(width,height))

    clock = pygame.time.Clock()
    running = True
    selected = 0
    execute_menu = False
    message = ""
    input_str = ""

    CAPTAINS[0].pirate_status = ["SPANISH","ENGLISH","DUTCH","FRENCH"]

    players = [
        (Controller(None),Ship(CAPTAINS[0])),
        (Controller(None),Ship(CAPTAINS[1])),
        (Controller(None),Ship(CAPTAINS[2])),
        (Controller(None),Ship(CAPTAINS[3])),
    ]

    NUM_PLAYERS = 4
    PLAYER_SELECT = 1
    TURN_COUNT = 1
    selected_row = 0
    selected_empire_naval_action = None

    while running:

        # Next Turn
        if player_ship.map_moves <= 0:
            clock.tick(180)
            PLAYER_SELECT += 1
            player_ship.map_moves = player_ship.turn_moves
            if PLAYER_SELECT > NUM_PLAYERS:
                TURN_COUNT += 1
                PLAYER_SELECT = 1

        controller,player_ship = players[PLAYER_SELECT-1]

        screen.blit(bg, (0,0))

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                controller.read_input()
                pressed_keys = controller.pressed_keys
                if selected == 0: 
                    if any([pressed_keys[key] for key in ['UP','DOWN','LEFT','RIGHT']]):
                        player_ship.move(pressed_keys)
                        # Random Encounter
                        if random.random() < 0.2:
                            selected = 50
                            selected_empire_naval_action = select_empire(player_ship.posx,player_ship.posy)
                    elif pressed_keys['B'] or pressed_keys ['Y']:
                        selected = True
                        selected_row = 0
                elif selected >= 1:
                    if any([pressed_keys[key] for key in ['UP','DOWN','LEFT','RIGHT']]):
                        selected_row = menu_move(pressed_keys,selected_row)
                    elif pressed_keys['A'] or pressed_keys['X']:
                        selected = 0
                    elif pressed_keys['B'] or pressed_keys['Y']:
                        execute_menu = True


            elif event.type == QUIT:
                running = False

        display_ship_stats(screen,player_ship)
        display_static_screen(screen,TURN_COUNT)
        drawGrid(screen,divisions_x,divisions_y)
        plot_ports(screen)
        player_ship.update(screen)

        if selected > 0:
            selected,execute_menu,message,input_str = display_menu(screen,player_ship,PORTS,selected,selected_row,execute_menu,divisions_x,message,input_str,selected_empire_naval_action)

        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()