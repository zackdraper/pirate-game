import pygame
from text_wrap import render_textrect
import numpy as np
from ports import PORTS, goods
from actions import exec_naval_action, run_from_naval_action
import random
from init import width, height
from empires import EMPIRES
import pkg_resources

pygame.font.init()

font = pygame.font.Font(pkg_resources.resource_stream('font','TradeWinds-Regular.ttf'), 26)
menu_img = pygame.image.load(pkg_resources.resource_stream('images','tile_map_menu.png'))

MESSAGES = {
    "no_port":("You are not in a square with a port!\n Heave Ho!","no_port.png"),
    "buy_no_gold":("Blimey!\n You don't have enough peices of eight to buy this cargo!",None),
    "port_is_out":("The port is out of goods\n Weigh Anchor!",None),
    "cargo_full":("Belay that!\n The cargo hold is full.",None),
    "sell_no_cargo":("Quartermaster says we're out!\n No goods to sell.",None),
    "random_port_sell":("The local scuttlebutt says the port of {0} is buying {1} for {2} peices of eight.",None),
    "out_of_moves":("Avast!\n The crew be too tired to go on. End your turn.",None),
    "naval_encounter":("Sail Ho!\n Ship on the horizon, shall we engage?","ship_on_horizon.png"),
    "nothing_found":("Nothing has turned up Captain...","no_port.png"),
    "victory":("Victory!\n You won the battle and gained a VP.\n You looted {0} pieces of eight and {1}",None),
    "lost":("You lost the battle and barely escape with your life!\n Goods are confiscated or lost.",None),
    "honor_among_thieves":("Aye, there is honor among thieves.",None),
    "bury_treasure":("Treasure is safe here!\n Gain a victory point.",None),
    "bury_treasure_no_gold":("We've got nothing to stash!\n Gain 10 pieces of 8 to exchange for a VP.",None),
    "not_enough_money":("Blimey!\n Not enough silver in the coffers for that.",None),
    "too_many_guns":("Captain, we can't fit any more guns on her!",None),
}

def display_message(screen,key,input_str,image=None):
    if key in MESSAGES.keys():
        message,image = MESSAGES[key]
    else:
        message = key

    message_size = (600,600)
    message_menu_img = pygame.transform.scale(menu_img,message_size)
    screen.blit(message_menu_img,(width/2-message_size[0]/2,height/2-message_size[1]/2))

    if image:
        message_img = pygame.image.load(pkg_resources.resource_stream('images',image))
        message_img = pygame.transform.scale(message_img,(message_size[0]-100,message_size[1]/2-50))
        screen.blit(message_img,(width/2-message_size[0]/2+50,height/2-message_size[1]/2+100))

    if '{' in message:
        message = message.format(*input_str)

    text_rect = pygame.Rect((width/2-message_size[0]/2+50, height/2+60, message_size[0]-100, 300))
    rendered_text = render_textrect(message, font, text_rect, (0,0,0), (227,203,165,0), 1)

    screen.blit(rendered_text,text_rect.topleft)


def display_naval_action(screen,ship,selected_row,selected_empire):

    message,image = MESSAGES["naval_encounter"]

    message_size = (600,600)

    message_menu_img = pygame.transform.scale(menu_img,message_size)
    screen.blit(message_menu_img,(width/2-message_size[0]/2,height/2-message_size[1]/2))

    message_img = pygame.image.load(pkg_resources.resource_stream('images',image))
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
        menu_1 = ['Search','Port Action','Bury Treasure','Exit']
        menu_2 = ['Buy','Sell','Shipyard','Rumour','Quest']
        menu_5 = ['Buy Galleon','Buy Cannons','Repair']
        
        port = ship.ship_in_port(ports)
        menu_3 = []
        menu_4 = []
        if port:
            menu_3 = list(port.sell_goods_prices.keys())
            menu_4 = list(port.buy_goods_prices.keys())

        menus = [0,len(menu_1),len(menu_2),len(menu_3),len(menu_4),len(menu_5)]
        menu_select = ['black'] * (menus[min(len(menus),selected)])

        if -1 < selected_row and selected_row < len(menu_select):
            menu_select[selected_row] = 'red'

        price_menu = None
        if selected == 1:
            menu = [font.render(s,True,c) for s,c in zip(menu_1,menu_select)]

        elif selected == 2:
            menu = [font.render(s,True,c) for s,c in zip(menu_2,menu_select)]

        elif selected == 3:
            menu = [font.render(s,True,c) for s,c in zip(menu_3,menu_select)]
            prices = [str(x) for x in list(port.sell_goods_prices.values())]
            price_menu = [font.render(s,True,c) for s,c in zip(prices,menu_select)]

        elif selected == 4:
            menu = [font.render(s,True,c) for s,c in zip(menu_4,menu_select)]
            prices = [str(x) for x in list(port.buy_goods_prices.values())]
            price_menu = [font.render(s,True,c) for s,c in zip(prices,menu_select)]
        
        elif selected == 5:
            menu = [font.render(s,True,c) for s,c in zip(menu_5,menu_select)]
            prices = [str(x) for x in [20,10,1]]
            price_menu = [font.render(s,True,c) for s,c in zip(prices,menu_select)]

    
        screen.blit(menu_img, pos)
        for i,m in enumerate(menu):
            screen.blit(m,(pos[0]+10,pos[1]+i*35+35))
        if price_menu:
            for i,m in enumerate(price_menu):
                screen.blit(m,(pos[0]+185,pos[1]+i*35+35))

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
            elif selected_row == 1: # Port Action
                if port:
                    selected = 2
                else:
                    message = "no_port"
                    selected = 99
            elif selected_row == 2: # Bury Treasure
                if ship.gold >= 10:
                    ship.gold -= 10
                    ship.vp += 1
                    selected = 99
                    message = "bury_treasure"
                else:
                    selected = 99
                    message = "bury_treasure_no_gold"
            elif selected_row == 3: # Exit
                selected = 0
        # Port Action
        elif selected == 2:
            if selected_row == 0:
                selected = 3
            elif selected_row == 1:
                selected = 4
            elif selected_row == 2:
                selected = 5
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

        elif selected == 5:
            #purchase = menu_4[selected_row]
            cost = [20,10,5][selected_row]
            if (ship.gold >= cost):
                if selected_row == 0:
                    ship.upgrade_ship()
                    ship.gold -= cost
                elif selected_row == 1:
                    if ship.guns < 6:
                        ship.guns += 1
                        ship.gold -= cost
                    else:
                        message = 'too_many_guns'
                        selected = 99
                elif selected_row == 2:
                    if ship.planks < ship.max_planks:
                        ship.planks += 3
                        ship.planks = min(ship.planks,ship.max_planks)
                        ship.gold -= cost
            else:
                message = "not_enough_money"
                selected = 99

                
        elif selected == 50:
            # if captain is a pirate and encounter is with pirates, go free.
            if (len(ship.captain.pirate_status) > 0) and (selected_empire_naval_action == 'PIRATES'):
                if selected_row in [0,1]:
                    selected = 99
                    message = 'honor_among_thieves'
            else:
                if selected_row == 0:
                    victory = exec_naval_action(ship,selected_empire_naval_action)
                elif selected_row != 0:
                    victory = run_from_naval_action(ship,selected_empire_naval_action)

                # did a victory occur, might be None, which means sailing on, no encounter
                if victory:
                    if victory:
                        p_of_eight = np.random.choice([2,4,6,8,10])
                        loot = np.random.choice(goods+2*['Silver','Slaves'])

                        ship.vp += 1
                        ship.gold += p_of_eight
                        ship.cargo += [loot]

                        if (selected_empire_naval_action not in ship.captain.pirate_status) and (selected_empire_naval_action != 'PIRATES'):
                            ship.captain.pirate_status += [selected_empire_naval_action]

                        selected = 99
                        message = 'victory'
                        input_str = [p_of_eight,loot]
                    else:
                        ship.cargo = []
                        ship.gold = min(ship.gold,10)

                        selected = 99
                        message = 'lost'
                else:
                    selected = 0
                

        else:
            selected = 0
    elif (ship.map_moves == 0):
        message = 'sell_no_cargo'
        selected = 99        

    return selected,execute_menu,message,input_str

