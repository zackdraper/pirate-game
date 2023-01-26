import pygame
import string 

pygame.init()
res = (1024,768)
screen = pygame.display.set_mode(res)
width = screen.get_width()
height = screen.get_height()
BLACK = (0, 0, 0, 0)
PADDING = PADTOPBOTTOM, PADLEFTRIGHT = 75, 5
lw = 1
divisions_x = 19
divisions_y = 16

alphabet = list(string.ascii_uppercase)
numbers = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18']