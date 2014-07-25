import random

class RepeatAttackException(Exception):
    def __init__(self, coord):
        super(RepeatAttackException, self).__init__()
        self.coord = coord
        self.message = 'Coord %s was already attacked' % str(coord)

class Ship(object):
    def __init__(self, size, name='unknown ship'):
        self.name = name
        self.size = size
        self.coords = []
        self.attacks = []

    @property
    def is_sunk(self):
        return len(self.attacks) == self.size

    @property
    def display_char(self):
        return self.name[0].lower()

    def attack(self, coord):
        """Peforms a stateful attack on the ship.

        Args:
            coord (Coord): the coordinate attacked

        Returns:
            True if ship was hit (coord was in list of ship's positions),
            False if ship was not hit,
            Raises an exception for repeat attacks at same hit coord

        Raises:
            RepeatAttackException: if ship was already hit at coord
        """
        if coord in self.coords:
            if coord in self.attacks:
                raise RepeatAttackException(coord)

            self.attacks.append(coord)
            return True
        else:
            return False


class Carrier(Ship):
    def __init__(self):
        super(Carrier,self).__init__(5, 'Carrier')
class Battleship(Ship):
    def __init__(self):
        super(Battleship,self).__init__(4, 'Battleship')
class Submarine(Ship):
    def __init__(self):
        super(Submarine,self).__init__(3, 'Submarine')
class Destroyer(Ship):
    def __init__(self):
        super(Destroyer,self).__init__(3, 'Destroyer')
class Patrol(Ship):
    def __init__(self):
        super(Patrol,self).__init__(2, 'Patrol boat')

def random_ship():
    return {
            0: Carrier(),
            1: Battleship(),
            2: Submarine(),
            3: Destroyer(),
            4: Patrol()
            }[random.randint(0,5)]
