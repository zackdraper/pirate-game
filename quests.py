from init import divisions_x, divisions_y, alphabet, numbers, forbidden_tiles
import numpy as np

class Quest:
    def __init__(initiation,completion):
        self.message_initiation = initiation
        self.message_completion = completion

    def reward(self,ship):
        ship.vp += 1

    def random_location(self):
        def rand_coord():
            rx = np.radint(0,divisions_x)
            ry = np.radint(0,divisions_y)
            return(rx, ry)

        rx, ry = rand_coord()
        while (rx, ry) in forbidden_tiles:
            rx, ry = rand_coord()

        c1 = alphabet[rx]
        c2 = numbers[ry]

        return c1+c2, rx, ry

    def random_location_land(self):
        pass

    def random_location_sea(self):
        pass
    
    def condition_success(self):
        pass


Quests = [
    Quest("",""),
    Quest("",""),
]