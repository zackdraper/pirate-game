import pygame
from empires import EMPIRES

_CAPTAINS = ['Black Sam','Calico Jack','Stede Bonnet','Edward Low']

captain_flag = {
    'Black Sam':pygame.image.load('images/flags/pirate_flag1.png'),
    'Stede Bonnet':pygame.image.load('images/flags/pirate_flag2.png'),
    'Calico Jack':pygame.image.load('images/flags/pirate_flag3.png'),
    'Edward Low':pygame.image.load('images/flags/pirate_flag4.png'),
}

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