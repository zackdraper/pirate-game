import pygame
from text_wrap import render_textrect
import numpy as np
from ports import PORTS
from actions import exec_naval_action, run_from_naval_action
import random
from init import width, height
from empires import EMPIRES
from actions import select_empire

pygame.font.init()

font = pygame.font.Font('font/TradeWinds-Regular.ttf', 26)
menu_img = pygame.image.load('images/tile_map_menu.png')

MESSAGES = {
    "no_port":("You are not in a square with a port!\n Heave Ho!","images/no_port.png"),
    "buy_no_gold":("Blimey!\n You don't have enough peices of eight to buy this cargo!",None),
    "port_is_out":("The port is out of goods\n Weigh Anchor!",None),
    "cargo_full":("Belay that!\n The cargo hold is full.",None),
    "sell_no_cargo":("Quartermaster says we're out!\n No goods to sell.",None),
    "random_port_sell":("The local scuttlebutt says the port of {0} is buying {1} for {2} peices of eight.",None),
    "out_of_moves":("Avast!\n The crew be too tired to go on. End your turn.",None),
    "naval_encounter":("Sail Ho!\n Ship on the horizon, shall we engage?","images/ship_on_horizon.png"),
    "nothing_found":("Nothing has turned up Captain...","images/no_port.png"),
}

def display_message(screen,key,input_str):
    message,image = MESSAGES[key]

    message_size = (600,600)
    message_menu_img = pygame.transform.scale(menu_img,message_size)
    screen.blit(message_menu_img,(width/2-message_size[0]/2,height/2-message_size[1]/2))

    if image:
        mesage_img = pygame.image.load(image)
        message_img = pygame.transform.scale(message_img,(message_size[0]-100,message_size[1]/2-50))
        screen.blit(message_img,(width/2-message_size[0]/2+50,height/2-message_size[1]/2+100))

    if key in ['random_port_sell']:
        message = message.format(*input_str)

    text_rect = pygame.Rect((width/2-message_size[0]/2+50, height/2+60, message_size[0]-100, 300))
    rendered_text = render_textrect(message, font, text_rect, (0,0,0), (227,203,165,0), 1)

    screen.blit(rendered_text,text_rect.topleft)


def display_naval_action(screen,ship,selected_row,selected_empire):

    message,image = MESSAGES["naval_encounter"]

    message_size = (600,600)

    message_menu_img = pygame.transform.scale(menu_img,message_size)
    screen.blit(message_menu_img,(width/2-message_size[0]/2,height/2-message_size[1]/2))

    message_img = pygame.image.load(image)
    message_img = pygame.transform.scale(message_img,(message_size[0]-100,message_size[1]/2-50))
    screen.blit(message_img,(width/2-message_size[0]/2+50,height/2-message_size[1]/2+100))

    screen.blit(EMPIRES[selected_empire].flag_small,(width/2-23,height/2))

    text_rect = pygame.Rect((width/2-message_size[0]/2+50, height/2+60, message_size[0]-100, 300))
    rendered_text = render_textrect(message, font, text_rect, (0,0,0), (227,203,165,0), 1)
    screen.blit(rendered_text,text_rect.topleft)

    menu = ['Raise Black Flag', 'Sail On']
    menu_select = ['black'] * 2
    selected_row = max([min([selected_row,1]),0])
    menu_select[selected_row] = 'red'
    menu = [font.render(s,True,c) for s,c in zip(menu,menu_select)]

    for i,m in enumerate(menu):
        screen.blit(m,(300+i*300,550))


def menu_move(pressed_keys,selected_row):
    if pressed_keys["UP"] or pressed_keys["LEFT"]:
        selected_row -= 1
    if pressed_keys["DOWN"] or pressed_keys["RIGHT"]:
        selected_row += 1

    selected_row = min([max([0,selected_row]),5])

    return selected_row


def action_search_square(screen,ship):
    # Finish a mission
    if False:
        return 99,None
    else:
        if random.random() < 0.4:
            return 50,None
    return 99,"nothing_found"


def port_action_rumor(local_port):
    _ports = [port for port in PORTS if port.name != local_port.name]
    random_port = np.random.choice(_ports)

    goods = list(random_port.buy_goods_prices.keys())

    random_good = np.random.choice(goods,1)[0]

    input_str = [random_port.name,random_good,random_port.buy_goods_prices[random_good]]
    message = 'random_port_sell'
    selected = 99

    return message,selected,input_str


def port_action_mission():
    pass


def display_menu(screen,ship,ports,selected,selected_row,execute_menu,divisions_x,message,input_str,selected_empire_naval_action):

    # background image for menu
    if ship.posx >= divisions_x/2:
        pos = (50,150)
    else:
        pos = (700,150)

    if selected < 50:
        # select menu
        menu_1 = ['Search','Port Action','Exit']
        menu_2 = ['Buy','Sell','Upgrade Ship','Rumour','Quest']
        
        port = ship.ship_in_port(ports)
        menu_3 = []
        menu_4 = []
        if port:
            menu_3 = list(port.sell_goods_prices.keys())
            menu_4 = list(port.buy_goods_prices.keys())

        menus = [0,len(menu_1),len(menu_2),len(menu_3),len(menu_4)]
        menu_select = ['black'] * (menus[min(len(menus),selected)])

        if -1 < selected_row and selected_row < len(menu_select):
            menu_select[selected_row] = 'red'

        menu = [font.render(s,True,c) for s,c in zip(menu_1,menu_select)]
        price_menu = None

        if selected == 2:
            menu = [font.render(s,True,c) for s,c in zip(menu_2,menu_select)]

        if selected == 3:
            menu = [font.render(s,True,c) for s,c in zip(menu_3,menu_select)]
            prices = [str(x) for x in list(port.sell_goods_prices.values())]
            price_menu = [font.render(s,True,c) for s,c in zip(prices,menu_select)]

        if selected == 4:
            menu = [font.render(s,True,c) for s,c in zip(menu_4,menu_select)]
            prices = [str(x) for x in list(port.buy_goods_prices.values())]
            price_menu = [font.render(s,True,c) for s,c in zip(prices,menu_select)]
    
        screen.blit(menu_img, pos)
        for i,m in enumerate(menu):
            screen.blit(m,(pos[0]+10,pos[1]+i*35+35))
        if price_menu:
            for i,m in enumerate(price_menu):
                screen.blit(m,(pos[0]+160,pos[1]+i*35+35))

    if selected == 50:
        display_naval_action(screen,ship,selected_row,selected_empire_naval_action)

    if selected == 99:
        display_message(screen,message,input_str)

    if execute_menu and (ship.map_moves > 0):
        execute_menu = False

        if selected == 1:
            if selected_row == 0: # Search
                ship.map_moves -= 1
                selected = 0
                selected,message = action_search_square(screen,ship)
            elif selected_row == 1: 
                if port:
                    selected = 2
                else:
                    message = "no_port"
                    selected = 99
            elif selected_row == 2: #Exit
                selected = 0
        # Port Action
        elif selected == 2:
            if selected_row == 0:
                selected = 3
            elif selected_row == 1:
                selected = 4
            elif selected_row == 2:
                pass
            elif selected_row == 3:
                port = ship.ship_in_port(ports)
                message,selected,input_str = port_action_rumor(port)
                ship.map_moves -= 1
            elif selected_row == 4:
                port_action_mission()
                ship.map_moves -= 1
        # Ship Buy
        elif selected == 3:
            good = menu_3[selected_row]
            cost = list(port.sell_goods_prices.values())[selected_row]
            quantity = port.goods_quantities[good]

            if (quantity < 1):
                message = 'port_is_out'
                selected = 99
            elif (ship.gold <= cost):
                message = 'buy_no_gold'
                selected = 99
            elif (len(ship.cargo) >= ship.cargo_capacity):
                message = 'cargo_full'
                selected = 99
            else:
                ship.cargo += [good]
                ship.gold -= cost
                port.goods_quantities[good] = quantity - 1
                ship.map_moves -= 1

        # Ship Sell
        elif selected == 4:
            good = menu_4[selected_row]
            cost = list(port.buy_goods_prices.values())[selected_row]
            if good in ship.cargo:
                ship.cargo.remove(good)
                ship.gold += cost
                ship.map_moves -= 1
            else:
                message = 'sell_no_cargo'
                selected = 99
                
        elif selected == 50:
            if selected_row == 0:
                exec_naval_action(ship,selected_empire_naval_action)
            elif selected_row == 1:
                run_from_naval_action(ship,selected_empire_naval_action)
            selected = 0

        else:
            selected = 0
    elif (ship.map_moves == 0):
        message = 'sell_no_cargo'
        selected = 99        

    return selected,execute_menu,message,input_str

