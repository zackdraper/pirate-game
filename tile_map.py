import pygame
import pygame.mixer as mixer
from pygame.locals import KEYDOWN,QUIT,K_ESCAPE
from tile_map_menu import display_menu, menu_move
from ports import plot_ports, PORTS
from controller import Controller
from ship import Ship
from math import floor
import random
from init import BLACK,PADLEFTRIGHT,PADTOPBOTTOM
from init import height,width,alphabet,numbers,divisions_x,divisions_y,lw
from empires import EMPIRES
from captains import CAPTAINS
from actions import select_empire
import pkg_resources

plank_img = pygame.image.load(pkg_resources.resource_stream('images','plank.png'))
cannon_img = pygame.image.load(pkg_resources.resource_stream('images','cannon.png'))

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

    font = pygame.font.Font(pkg_resources.resource_stream('font','TradeWinds-Regular.ttf'), 18)
    font2 = pygame.font.Font(pkg_resources.resource_stream('font','TradeWinds-Regular.ttf'), 32)

    padleft = 10
    padtop = height - (PADTOPBOTTOM-5)

    empires_display = list(EMPIRES.keys())
    empires_display.remove('PIRATES')
    for i,e in enumerate(empires_display):
        empire = EMPIRES[e]
        y = [0,1][floor(i/2)]
        x = [0,1][(i+1) % 2]
        ship_text = font.render(empire.long_name,True,empire.color)
        screen.blit(ship_text,(padleft+200*(x),padtop+30*(y)))
        screen.blit(empire.flag_small,(padleft+150+240*(x),padtop+5+33*(y)))

    text = font.render("Turns: "+str(TURN_COUNT),True,(255,255,255))
    screen.blit(text,(width/2,padtop+40))

    text = font2.render("Black Flag",True,(255,255,255))
    screen.blit(text,(width/2-50,padtop))
    

def display_ship_stats(screen,ship):

    surface = pygame.surface.Surface((width,PADTOPBOTTOM-5))
    surface.fill((227,203,165))
    screen.blit(surface,(0,0))
    
    font = pygame.font.Font(pkg_resources.resource_stream('font','TradeWinds-Regular.ttf'), 18)

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

    ship_text = font.render(": "+str(ship.guns),True,'black')
    screen.blit(ship_text,(width-225,5))
    screen.blit(cannon_img,(width-265,5))

    ship_text = font.render(": "+str(ship.planks),True,'black')
    screen.blit(ship_text,(width-150,5))
    screen.blit(plank_img,(width-190,10))

def display_no_go(screen):
    from init import forbidden_tiles

    horizontal_cellsize = (width - (PADLEFTRIGHT*2))/divisions_x
    vertical_cellsize = (height - (PADTOPBOTTOM*2))/divisions_y

    for tile in forbidden_tiles:
        x = tile[0]
        y = tile[1]
        pygame.draw.circle(screen, (0,0,0), ((PADLEFTRIGHT + (horizontal_cellsize*x) + horizontal_cellsize/2),(PADTOPBOTTOM + (vertical_cellsize*y) + vertical_cellsize/2)), 20)

def display_land(screen):
    from init import land_tiles

    horizontal_cellsize = (width - (PADLEFTRIGHT*2))/divisions_x
    vertical_cellsize = (height - (PADTOPBOTTOM*2))/divisions_y

    for tile in land_tiles:
        x = tile[0]
        y = tile[1]
        pygame.draw.circle(screen, (255,0,0), ((PADLEFTRIGHT + (horizontal_cellsize*x) + horizontal_cellsize/2),(PADTOPBOTTOM + (vertical_cellsize*y) + vertical_cellsize/2)), 15)

def display_ocean(screen):
    from init import ocean_tiles

    horizontal_cellsize = (width - (PADLEFTRIGHT*2))/divisions_x
    vertical_cellsize = (height - (PADTOPBOTTOM*2))/divisions_y

    for tile in ocean_tiles:
        x = tile[0]
        y = tile[1]
        pygame.draw.circle(screen, (0,255,0), ((PADLEFTRIGHT + (horizontal_cellsize*x) + horizontal_cellsize/2),(PADTOPBOTTOM + (vertical_cellsize*y) + vertical_cellsize/2)), 15)

def display_cant_go(screen):
    from init import cant_move

    horizontal_cellsize = (width - (PADLEFTRIGHT*2))/divisions_x
    vertical_cellsize = (height - (PADTOPBOTTOM*2))/divisions_y

    for tile in cant_move:
        x = tile[0]
        y = tile[1]
        pygame.draw.circle(screen, (0,0,0), ((PADLEFTRIGHT + (horizontal_cellsize*x) + horizontal_cellsize/2),(PADTOPBOTTOM + (vertical_cellsize*y) + vertical_cellsize/2)), 5)


def main(NUM_PLAYERS=1,SOUND_ON=False,DEBUG=False):
    pygame.display.set_caption('Pirate Game')

    # initialize pygame
    pygame.init()

    mixer.init()
    mixer.music.load(pkg_resources.resource_stream('music','the_coast_of_high_barbary.mp3'))
    mixer.music.set_volume(0.15)
    if SOUND_ON:
        mixer.music.play(loops=-1)

    # create the screen object
    screen = pygame.display.set_mode((width, height))

    bg = pygame.image.load(pkg_resources.resource_stream('images','carribbean_map_v2.png'))
    bg = pygame.transform.scale(bg,(width,height))

    clock = pygame.time.Clock()
    running = True
    selected = 0
    execute_menu = False
    message = ""
    input_str = ""

    #CAPTAINS[0].pirate_status = ["SPANISH","ENGLISH","DUTCH","FRENCH"]

    players = [
        (Controller(None),Ship(CAPTAINS[0])),
        (Controller(None),Ship(CAPTAINS[1])),
        (Controller(None),Ship(CAPTAINS[2])),
        (Controller(None),Ship(CAPTAINS[3])),
    ]

    #NUM_PLAYERS = 4
    PLAYER_SELECT = 1
    TURN_COUNT = 1
    selected_row = 0
    selected_empire_naval_action = None

    while running:

        controller,player_ship = players[PLAYER_SELECT-1]

        # Next Turn
        if player_ship.map_moves <= 0:
            clock.tick(180)
            PLAYER_SELECT += 1
            player_ship.map_moves = player_ship.turn_moves
            if PLAYER_SELECT > NUM_PLAYERS:
                TURN_COUNT += 1
                PLAYER_SELECT = 1

        screen.blit(bg, (0,0))

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                controller.read_input()
                pressed_keys = controller.pressed_keys
                if selected == 0: 
                    if any([pressed_keys[key] for key in ['UP','DOWN','LEFT','RIGHT']]):
                        succed = player_ship.move(pressed_keys)
                        # Random Encounter
                        if succed:
                            if random.random() < 0.2:
                                selected = 50
                                selected_empire_naval_action = select_empire(player_ship.posx,player_ship.posy)
                    elif pressed_keys['B'] or pressed_keys ['Y']:
                        selected = True
                        selected_row = 0
                elif selected in [50]:
                    # Force a selection to resolve
                    if any([pressed_keys[key] for key in ['UP','DOWN','LEFT','RIGHT']]):
                        selected_row = menu_move(pressed_keys,selected_row)
                    elif pressed_keys['B'] or pressed_keys['Y']:
                        execute_menu = True
                elif selected >= 1:
                    # Allow a key to back out
                    if any([pressed_keys[key] for key in ['UP','DOWN','LEFT','RIGHT']]):
                        selected_row = menu_move(pressed_keys,selected_row)
                    elif pressed_keys['A'] or pressed_keys['X']:
                        selected = 0
                    elif pressed_keys['B'] or pressed_keys['Y']:
                        execute_menu = True


            elif event.type == QUIT:
                running = False

        if DEBUG:
            display_no_go(screen)
            display_land(screen)
            display_ocean(screen)
            display_cant_go(screen)

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
    main(DEBUG=True)