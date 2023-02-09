from init import divisions_x,divisions_y
from ports import PORTS
from empires import _EMPIRES
import numpy as np
import random
from ship_battle import main as ship_battle
from captains import EMPIRE_CAPTAINS

empire_square_prob = {}
for e in _EMPIRES:
    empire_square_prob[e] = 0.1

SQUARE_PROB = {}
for x in np.arange(divisions_x):
    for y in np.arange(divisions_y):
        distances = [((x-p.posx)**2+(y-p.posy)**2)**0.5 for p in PORTS]
        nearby_ports = sorted(zip(distances,PORTS), key = lambda x: x[0])[0:2]

        _empire_square_prob = empire_square_prob.copy()

        for distance,port in nearby_ports:
            _empire_square_prob[port.empire] += 1/max(distance,0.25)

        SQUARE_PROB[(x,y)] = _empire_square_prob

def select_empire(x,y):
    _probs = SQUARE_PROB[(x,y)] 
    choice = random.choices(list(_probs.keys()),weights=_probs.values(),k=1)
    return choice[0]

        
def exec_naval_action(ship,empire):
    victory = ship_battle({"captain":ship.captain,"guns":ship.guns},{"captain":EMPIRE_CAPTAINS[empire],"guns":3})
    if victory:
        ship.vp += 1


def run_from_naval_action(ship,empire):
    if empire in ship.captain.pirate_status:
        victory = ship_battle({"captain":ship.captain,"guns":ship.guns},{"captain":EMPIRE_CAPTAINS[empire],"guns":3})
        if victory:
            ship.vp += 1