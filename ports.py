import pygame
import numpy as np
from init import width,height,divisions_x,divisions_y,PADDING
from empires import empire_color

class Port:
    def __init__(self,name,location,empire):
        self.location = location
        self.empire = empire
        self.name = name
        self.sell_goods_prices = {}
        self.buy_goods_prices = {}
        self.goods_quantities = {}
        self.posx = 0
        self.posy = 0


goods = [
    'Sugarcane',
    'Tobbacco',
    'Fruit',
    'Food',
    'Rum',
    'Silver',
    'Slaves',
    'Coffee',
    'Indigo',
    'Cotton',
    'Wood',
]

prices = {
    'Sugarcane':4,
    'Tobbacco':4,
    'Fruit':4,
    'Food':1,
    'Rum':4,
    'Silver':10,
    'Slaves':6,
    'Coffee':4,
    'Indigo':6,
    'Cotton':4,
    'Wood':1,
}

for g in goods:
    assert g in prices.keys()

ports = {
    ("Port Royal",(420,370),'ENGLISH'),
    ("Nassau",(402,110),'ENGLISH'),
    ("Tortuga",(555,290),'FRENCH'),
    ("Porto Bello",(320,670),'SPANISH'),
    ("Havanna",(225,180),'SPANISH'),
    ("Cartagena",(460,640),'SPANISH'),
    ("Santiago",(455,295),'SPANISH'),
    ("Santo Domingo",(655,350),'SPANISH'),
    ("Trinidad",(940,635),'SPANISH'),
    ("San Juan",(785,350),'SPANISH'),
    ("Barbados",(1005,545),'ENGLISH'),
    #("Mosquito Coast",(0,0),'ENGLISH'),
    ("Providence",(260,535),'ENGLISH'),
    ("Belize",(25,385),'ENGLISH'),
    ("St Kitts & Nevis",(900,395),'ENGLISH'),
    ("Petit-Goâve",(555,350),'FRENCH'),
    ("Curaçao",(685,580),'DUTCH'),
    #("Montserrat",(0,0),'ENGLISH'),
    #("Antigua",(0,0),'ENGLISH'),
    ("Guadeloupe",(937,430),'FRENCH'),
    ("Martinique",(955,490),'FRENCH'),
    #("Sint Eustatius",(0,0),'DUTCH'),
    ("St Maarten",(885,370),'DUTCH'),
}

def plot_ports(screen):
    font = pygame.font.SysFont(None, 20)
    for name,location,empire in ports:
        pygame.draw.circle(screen, empire_color[empire], location, 4)
        title = font.render(name,True,empire_color[empire])
        offset_x = 45
        offset_y = 20
        if name == 'Belize':
            offset_x -= 50
        screen.blit(title, (location[0]-offset_x,location[1]-offset_y))

def ports_init(width,height,divisions_x,divisions_y,PADDING):
    PORTS = [Port(name,location,empire) for name,location,empire in ports]

    # initialize economy for Ports
    for port in PORTS:
        # Port Sells
        _goods = list(set(goods) - set(['Silver','Slaves']))
        _goods = np.random.choice(_goods,4)
        for _g in _goods:
            port.sell_goods_prices.update({_g:max(prices[_g]-2,1)})
            port.goods_quantities.update({_g:np.random.choice([8,10,12,14])})
        # Major Good to Sell
        port.goods_quantities[_goods[0]] = np.inf  

        # Port Buys
        _goods = list(set(goods) - set(_goods))
        _goods = np.random.choice(_goods,4)        
        for _g in _goods:    
            port.buy_goods_prices.update({_g:prices[_g]+2})


        # determine grid cell
        horizontal_cellsize = (width - (PADDING[1]*2))/divisions_x
        vertical_cellsize = (height - (PADDING[0]*2))/divisions_y

        port.posx = np.floor((port.location[0] - PADDING[1]) / horizontal_cellsize)
        port.posy = np.floor((port.location[1] - PADDING[0]) / vertical_cellsize)

        #print(port.name,port.posx,port.posy)

    #print(PORTS[0].sell_goods_prices)
    #print(PORTS[0].buy_goods_prices)

    return PORTS

PORTS = ports_init(width,height,divisions_x,divisions_y,PADDING)