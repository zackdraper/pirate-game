import pygame
from pygame.locals import *

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