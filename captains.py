import pygame
from empires import EMPIRES
import pkg_resources

_CAPTAINS = ['Black Sam','Calico Jack','Stede Bonnet','Edward Low']

captain_flag = {
    'Black Sam':pygame.image.load(pkg_resources.resource_stream('images','flags/pirate_flag1.png')),
    'Stede Bonnet':pygame.image.load(pkg_resources.resource_stream('images','flags/pirate_flag2.png')),
    'Calico Jack':pygame.image.load(pkg_resources.resource_stream('images','flags/pirate_flag3.png')),
    'Edward Low':pygame.image.load(pkg_resources.resource_stream('images','flags/pirate_flag4.png')),
}

generic_pirate_flag = pygame.image.load(pkg_resources.resource_stream('images','flags/pirate_flag5.png'))

class Captain():
    def __init__(self,name,flag) -> None:
        self.name = name
        self.flag = flag
        self.flag_small = pygame.transform.scale(self.flag,(45,30))
        self.pirate_status = []

CAPTAINS = [Captain(c,captain_flag[c]) for c in _CAPTAINS]

EMPIRE_CAPTAINS = {}

for k,e in EMPIRES.items():
    EMPIRE_CAPTAINS[k] = Captain(e.name,e.flag)

EMPIRE_CAPTAINS['PIRATES'] = Captain('PIRATES',generic_pirate_flag)