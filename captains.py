import pygame

_CAPTAINS = ['Black Sam','Calico Jack','Stede Bonnet','Edward Low']

captain_flag = {
    'Black Sam':pygame.image.load('images/flags/pirate_flag1.png'),
    'Stede Bonnet':pygame.image.load('images/flags/pirate_flag2.png'),
    'Calico Jack':pygame.image.load('images/flags/pirate_flag3.png'),
    'Edward Low':pygame.image.load('images/flags/pirate_flag4.png'),
}

class Captain():
    def __init__(self,name) -> None:
        self.name = name
        self.flag = captain_flag[self.name]
        self.flag_small = pygame.transform.scale(self.flag,(45,30))
        self.pirate_status = []

CAPTAINS = [Captain(c) for c in _CAPTAINS]