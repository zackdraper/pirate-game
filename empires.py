import pygame
import pkg_resources

_EMPIRES = ['ENGLISH','SPANISH','FRENCH','DUTCH']

empire_color = {
    'ENGLISH':(220,20,60),
    'SPANISH':(207,206,211),
    'FRENCH':(255,219,81),
    'DUTCH':(255,165,0),
    'PIRATES':(0,0,0),
}

empire_flag = {
    'ENGLISH':pygame.image.load(pkg_resources.resource_stream('images','flags/ENGLISH.png')),
    'SPANISH':pygame.image.load(pkg_resources.resource_stream('images','flags/SPANISH.png')),
    'FRENCH':pygame.image.load(pkg_resources.resource_stream('images','flags/FRENCH.png')),
    'DUTCH':pygame.image.load(pkg_resources.resource_stream('images','flags/DUTCH.png')),
    'PIRATES':pygame.image.load(pkg_resources.resource_stream('images','flags/pirate_flag5.png'))
}

empire_long_name = {
    'ENGLISH':'Kingdom of England',
    'SPANISH':'Spanish Empire',
    'FRENCH':'Kingdom of France',
    'DUTCH':'Dutch Republic', 
    'PIRATES':'Pirates',
}

class Empire():
    def __init__(self,name) -> None:
        self.name = name
        self.long_name = empire_long_name[self.name]
        self.color = empire_color[self.name]
        self.flag = empire_flag[self.name]
        self.flag_small = pygame.transform.scale(self.flag,(45,30))
        self.flag_ex_small = pygame.transform.scale(self.flag,(15,10))

EMPIRES = {}
for e in _EMPIRES+['PIRATES']:
    EMPIRES[e] = Empire(e)
