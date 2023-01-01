import pygame
import random
import numpy as np
from pygame.locals import *

width_buffer = 100
height_buffer = 0

screen_width = 1024
screen_height = 768

class PlayerShip(pygame.sprite.Sprite):
    def __init__(self, x0, y0, angle):
        super(PlayerShip, self).__init__()
        image = pygame.image.load('ship.png').convert()

        image = pygame.transform.rotate(image, -90)
        image.set_colorkey((255, 255, 255), RLEACCEL)
        self.image_original = image
        self.image = self.image_original
        print("image angle: ", angle)
        self.rect = self.image.get_rect()
        self.x = x0
        self.y = y0
        self.size = self.image.get_size()
        self.port_shoot = 0
        self.starboard_shoot = 0


        # Ship Properties
        self.hull = 5
        self.hull_speed = 1.
        self.speed = 0
        self.aoa = angle
        self.reload_time = 60*60

        self.rotate(self.aoa)

    def shoot(self,shoot_angle):
        ball = CanonBall(self.x,self.y,self.aoa-shoot_angle)
        all_sprites.add(ball)
        balls.add(ball)

    def hit(self):
        if self.hull > 1:
            self.hull -= 1
        else:
            self.hull = 0
            self.kill()

    def rotate(self,angle):
        # rotate image of boat
        pos = (self.x, self.y)
        image = self.image_original
        originPos = (self.size[0]/2,self.size[1]/2)

        image_rect = image.get_rect(topleft = (pos[0]-originPos[0], pos[1]-originPos[1]))
        offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
        rotated_offset = offset_center_to_pivot.rotate(angle)
        rotated_image_center = (pos[0]-rotated_offset.x, pos[1]-rotated_offset.y)
        rotated_image = pygame.transform.rotate(image, -angle)
        rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

        return rotated_image,rotated_image_rect

    def update(self, pressed_keys, screen, opponent=None):

        # set wind conditions
        a=0.05
        aoa = self.aoa

        # fire cannons
        if pressed_keys["L"]:
            if (pygame.time.get_ticks() - self.port_shoot) > self.reload_time:
                self.shoot(90)
                self.port_shoot = pygame.time.get_ticks()

        if pressed_keys["R"]:
            if (pygame.time.get_ticks() - self.starboard_shoot) > self.reload_time:
                self.shoot(-90)
                self.starboard_shoot = pygame.time.get_ticks()

        # control movement

        if pressed_keys["UP"]:
            v = self.speed + a
            self.speed = min(v,self.hull_speed)
        if pressed_keys["DOWN"]:
            s = self.speed - 0.1
            self.speed = max(s,0)
        if pressed_keys["LEFT"]:
            aoa -= 1.0
        if pressed_keys["RIGHT"]:
            aoa += 1.0

        self.aoa = aoa % 360

        ship_rad = np.radians(self.aoa)
        x = self.x + self.speed * np.sin(ship_rad)
        y = self.y - self.speed * np.cos(ship_rad)

        self.x = max(width_buffer,min(x,screen_width-width_buffer))
        self.y = max(height_buffer,min(y,screen_height-height_buffer))

        self.rect.x = round(self.x)
        self.rect.y = round(self.y)

        rotated_image,rotated_image_rect = self.rotate(self.aoa)

        # Keep player on the screen
        if rotated_image_rect.left < width_buffer:
            rotated_image_rect.left = width_buffer
        elif rotated_image_rect.right > screen_width-width_buffer:
            rotated_image_rect.right = screen_width-width_buffer
        if rotated_image_rect.top <= height_buffer:
            rotated_image_rect.top = height_buffer
        elif rotated_image_rect.bottom >= screen_height-height_buffer:
            rotated_image_rect.bottom = screen_height-height_buffer

        screen.blit(rotated_image, rotated_image_rect)

        self.image = rotated_image
        self.rect = rotated_image_rect  

class CanonBall(pygame.sprite.Sprite):
    def __init__(self,x0,y0,angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((3,3))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        self.x = x0
        self.y = y0
        self.angle = angle
        self.speed = 3
        
    def update(self):
        ship_rad = np.radians(self.angle)

        self.x = self.x + self.speed * np.sin(ship_rad)
        self.y = self.y - self.speed * np.cos(ship_rad)

        self.rect.x = round(self.x)
        self.rect.y = round(self.y)

class Controller():
    def __init__(self,joystick):
        self.joystick = None

        self.button_map = {
            "X":0,
            "A":1,
            "B":2,
            "Y":3,
            "L":4,
            "R":5,
            "SEL":8,
            "STRT":9,
        }

        self.button_map_keyboard = {
            "X":K_w,
            "A":K_d,
            "B":K_s,
            "Y":K_a,
            "L":K_q,
            "R":K_e,
            "SEL":K_x,
            "STRT":K_c,
        }

        self.axis_map = {
            "LEFT":(0,"({:1f} < -0.5)"),
            "RIGHT":(0,"({:1f} > 0.5)"),
            "UP":(1,"({:1f} < -0.5)"),
            "DOWN":(1,"({:1f} > 0.5)"),
        }

        self.axis_map_keyboard = {
            "LEFT":K_LEFT,
            "RIGHT":K_RIGHT,
            "UP":K_UP,
            "DOWN":K_DOWN,
        }

        self.pressed_keys = dict.fromkeys(self.button_map, False)
        self.pressed_keys.update(dict.fromkeys(self.axis_map, False))
    
    def read_input(self):
        if self.joystick:
            for k,v in self.button_map.items():
                self.pressed_keys[k] = self.joystick.get_button(v)

            for k,(v,c) in self.axis_map.items():
                axis_cond = None
                axis_cond = eval(c.format(self.joystick.get_axis(v)))
                self.pressed_keys[k] = axis_cond
        else:
            keys = pygame.key.get_pressed()
            for k,v in self.button_map_keyboard.items():
                self.pressed_keys[k] = keys[v]

            for k,v in self.axis_map_keyboard.items():
                self.pressed_keys[k] = keys[v]

class AIShip(PlayerShip):
    def update(self, pressed_keys, screen, opponent=None):

        a = 0.05

        v = self.speed + a
        self.speed = min(v,self.hull_speed)
        self.aoa = 0

        ship_rad = np.radians(self.aoa)
        x = self.x + self.speed * np.sin(ship_rad)
        y = self.y - self.speed * np.cos(ship_rad)

        self.x = max(width_buffer,min(x,screen_width-width_buffer))
        self.y = max(height_buffer,min(y,screen_height-height_buffer))

        self.rect.x = round(self.x)
        self.rect.y = round(self.y)

        rotated_image,rotated_image_rect = self.rotate(self.aoa)

        # Keep player on the screen
        if rotated_image_rect.left < width_buffer:
            rotated_image_rect.left = width_buffer
        elif rotated_image_rect.right > screen_width-width_buffer:
            rotated_image_rect.right = screen_width-width_buffer
        if rotated_image_rect.top <= height_buffer:
            rotated_image_rect.top = height_buffer
        elif rotated_image_rect.bottom >= screen_height-height_buffer:
            rotated_image_rect.bottom = screen_height-height_buffer

        screen.blit(rotated_image, rotated_image_rect)

        self.image = rotated_image
        self.rect = rotated_image_rect

class AI_Control():
    pass

def player_stats(screen,PlayerShip,num,side):

    strings = [
        "Player: "+str(int(num)),
        "Hull: % 1.0f" % PlayerShip.hull,
        "Knts: % 2.2f" % PlayerShip.speed,
        "AOA: % 3.0f" % PlayerShip.aoa,
    ]

    font = pygame.font.Font('freesansbold.ttf', 24)
    
    if side == 'right':
        for dy,s in enumerate(strings):
            stat = font.render(s, True, (255,255,255), (0,0,0))
            screen.blit(stat, (screen_width-150,dy*25))
    else:
        for dy,s in enumerate(strings):
            stat = font.render(s, True, (255,255,255), (0,0,0))
            screen.blit(stat, (0,dy*25))

def main():
    pygame.display.set_caption('Ship Battle')

    # initialize pygame
    pygame.init()

    # create the screen object
    screen = pygame.display.set_mode((screen_width, screen_height))

    #background
    background = pygame.Surface(screen.get_size())
    background.fill((0, 154, 255))

    # create players
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

    rand_num = random.random()
    a1 = np.floor(rand_num * 360)
    a2 = a1 - 180 % 360

    a1_rad = np.deg2rad(a1)
    a2_rad = np.deg2rad(a2)

    r = (screen_height-100)/2
    x1 = r * np.sin(a1_rad) + screen_width/2
    y1 = -1 * r * np.cos(a1_rad) + screen_height/2

    x2 = r * np.sin(a2_rad) + screen_width/2
    y2 = -1 * r * np.cos(a2_rad) + screen_height/2

    if False:
        # 2 player battle
        player1 = PlayerShip(x1, y1, (a1-180) % 360)
        if len(joysticks) > 1:    
            controller1 = Controller(joysticks[0])

        player2 = PlayerShip(x2, y2, (a2-180) % 360)
        if len(joysticks) > 2:
            controller2 = Controller(joysticks[1])

        players = [(player1,controller1,player2),(player2,controller2,player1)]
    else:
        # 1 player vs AI
        player1 = PlayerShip(x1, y1, (a1-180) % 360)
        controller1 = Controller(None)

        player2 = AIShip(x2, y2, (a2-180) % 360)
        ai_controller = AI_Control()

        players = [(player1,controller1,player2),(player2,ai_controller,player1)]

    #draw wind arrow
    wind_direction = 135

    wind_arrow = pygame.Surface((300,300), SRCALPHA, 32)
    wind_arrow = wind_arrow.convert_alpha()
    pygame.draw.polygon(wind_arrow, (0, 0, 0), ((0, 100), (0, 200), (200, 200), (200, 300), (300, 150), (200, 0), (200, 100)), width=0)
    wind_arrow = pygame.transform.rotate(wind_arrow, -wind_direction+90)
    wind_arrow = pygame.transform.scale(wind_arrow,(30,30))

    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    balls = pygame.sprite.Group()

    running = True

    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            elif event.type == QUIT:
                running = False
        
        for p,c,o in players:
            if isinstance(c, Controller):
                c.read_input()
                

        screen.blit(background, (0, 0))
        pos = (screen.get_width()/2, screen.get_height()/2)
        screen.blit(wind_arrow, (screen_width/2,0))
        
        #enemies.update()
        balls.update()

        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)

        for i,(p,c,o) in enumerate(players):
            if isinstance(c, Controller):
                pressed_keys = c.pressed_keys
            else:
                pressed_keys = []
            p.update(pressed_keys,screen,opponent=o)
            #Display Ship Stats
            if i == 0:
                player_stats(screen,p,1,'left')
            else:
                player_stats(screen,p,2,'right')
            pygame.draw.rect(screen, (255, 0, 0), (*p.rect.topleft, *p.image.get_size()),2)
            if pygame.sprite.spritecollideany(p, balls):
                p.hit()

        pygame.display.flip()

        clock.tick(60)

if __name__ == '__main__':
    main()