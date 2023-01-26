import pygame
from sprite_sheet import SpriteSheet
import pygame.mixer as mixer
from ports import PORTS

from init import PADLEFTRIGHT,PADTOPBOTTOM,height,width,divisions_x,divisions_y

sloop_sprite = SpriteSheet('images/sloop_map_sprite_v2.png')
sloop_images = sloop_sprite.load_strip((0,0,40,40), 6, colorkey=-1)

def screen_pos(x,y):
    # Get cell size
    horizontal_cellsize = (width - (PADLEFTRIGHT*2))/divisions_x
    vertical_cellsize = (height - (PADTOPBOTTOM*2))/divisions_y

    return (PADLEFTRIGHT + (horizontal_cellsize*x) + horizontal_cellsize/2)-18,(PADTOPBOTTOM + (vertical_cellsize*y) + vertical_cellsize/2)-18

SHIP_CLASS_SPRITES = {
    'Sloop':sloop_images,
}

SHIP_CLASS_CP = {
    'Sloop':3,
}

mixer.init()
sound_boat_move = mixer.Sound('music/boat_move.mp3')
sound_boat_move.set_volume(0.5)

sound_seagulls_in_port = mixer.Sound('music/seagulls.mp3')
sound_seagulls_in_port.set_volume(0.5)

class Ship:
    def __init__(self,captain):
        self.map_moves = 5
        self.turn_moves = 5
        self.posx = 0
        self.posy = 0
        self.pirate_status = []
        self.cargo = []
        self.gold = 10
        self.ship_class = 'Sloop'
        self.sprites = SHIP_CLASS_SPRITES[self.ship_class]
        self.img = 0
        self.vp = 0
        self.cargo_capacity = SHIP_CLASS_CP[self.ship_class]
        self.captain = captain

    def move(self,pressed_keys):
        x = self.posx
        y = self.posy

        if self.map_moves > 0:
            if pressed_keys["UP"]:
                y -= 1
                if self.img in [0,3,4]:
                    img = 4
                elif self.img in [1,2,5]:
                    img = 5
            if pressed_keys["DOWN"]:
                y += 1
                if self.img in [0,3,4]:
                    img = 3
                elif self.img in [1,2,5]:
                    img = 2
            if pressed_keys["LEFT"]:
                x -= 1
                img = 1
            if pressed_keys["RIGHT"]:
                x += 1
                img = 0

            x = min(max(0,x),divisions_x)
            y = min(max(0,y),divisions_y)

            if self.move_allowed((x,y),(self.posx,self.posy)):
                sound_boat_move.play()
                self.map_moves -= 1
                self.posx = x
                self.posy = y
                self.img = img

                if self.ship_in_port(PORTS):
                    sound_seagulls_in_port.play()


    def move_allowed(self,move_to,move_from):
        return True

    def update(self,screen):
        loc = screen_pos(self.posx,self.posy)
        screen.blit(self.sprites[self.img], loc)

    def ship_in_port(self,ports):
        for p in ports:
            if p.posx == self.posx and p.posy == self.posy:
                return p
        return False

