from util import *

class InvalidAttackException(Exception):
    def __init__(self, message):
        super(InvalidAttackException, self).__init__()
        self.message = message

class Board(object):
    """Local representation of board state.
    This includes:
        ships (and positions when known),
        coords of past attacks,
        functions to modify the board using domain terminology."""

    def __init__(self, ships_and_positions=None, height=10, width=10):
        """Initializes the board for play with optional parameters.
        Args:
            ships_and_positions (array of tuples, optional):
                Initializes the board with ships at positions calculated from
                tuple. Format is (Ship, Coord, Direction)
            height (int, optional): # of rows in the board, default is 10
            width (int, optional): # of cols in the board, default is 10
            """
        self.ships = []
        self.attacks = []

        self.height = height
        self.width = width

        # Put ships on the board if provided
        ships_and_positions = [] if not ships_and_positions else ships_and_positions
        for s in ships_and_positions:
            self.add_ship(s[i][0],
                    make_coord(s[i][1]),
                    s[i][2])

    @property
    def is_fleet_sunk(self):
        if len(self.ships) > 0:
            return reduce(lambda x, y: x and y.is_sunk, self.ships, True)
        return False

    def to_array(self):
        """Constructs an array of arrays representation of the board.

        Returns:
            array of arrays of ints and strings
        """
        board = []
        [board.append([""]*self.width) for x in xrange(0, self.height)]
        for s in self.ships:
            for c in s.coords:
                board[c[0]][c[1]] = s.size
        return board

    def add_ship(self, ship, coord, direction='r'):
        """Plops a ship on the board.
        Args:
            ship (Ship): A Ship object to add to the board.
            coord (Coord or tuple or str): location on the board
            direction (str): orientation of the ship

        Raises:
            InvalidPositionException: If ship would collide with existing ship
        """
        ship_id = len(self.ships)
        self._set_ship_to_position(ship_id, ship, make_coord(coord), direction)
        self.ships.append(ship)

    def attack(self, coord, hit=None, sunk=None):
        """Logs an attack at coord. This has the following effects:
            1) An Attack object is added to the list of known attacks
            2) If board has ships with known positions, an Attack object
               is returned

            Args:
                coord (Coord): the coordinate to attack or log attack
                hit (bool, optional): ignored if attack on local fleet;
                                      mandatory if logging attack on foe
                sunk (int, optional): ignored if attack on local fleet
                                      mandatory if logging attack on foe

            Returns:
                An Attack object corresponding to status of attack

            Raises:
                RepeatAttackException: if coord resulted in a prior hit
        """
        if len(self.ships) > 0:
            # hit and sunk are ignored, this is an attack on local fleet
            for s in self.ships:
                if s.attack(coord):
                    # It's a hit!
                    a = Attack(coord, True, s.size if s.is_sunk else None)
                    self.attacks.append(a)
                    return a

            # No ship was hit
            a = Attack(coord, False)
            return a
        else:
            # hit MUST be a bool, we are logging an attack on foreign fleet
            if not isinstance(hit, bool):
                raise InvalidAttackException()

            a = Attack(coord, hit, sunk)
            self.attacks.append(a)
            return a  # Not useful in this case...

    def _set_ship_to_position(self, ship_id, ship, coord, direction):
        """Attempts to update the board to reflect a ship at a specified coord
        with specified direction.
        """
        #print ship_id, ship.name, coord, direction
        coords = []
        for x in range(0, ship.size):
            if direction == 'r':
                r = coord[0]
                c = coord[1] + x
            elif direction == 'd':
                r = coord[0] + x
                c = coord[1]
            elif direction == 'u':
                r = coord[0] - x
                c = coord[1]
            elif direction == 'l':
                r = coord[0]
                c = coord[1] - x
            else:
                raise InvalidPositionException('%s is not a valid direction' % direction)

            if r >= self.height or r < 0:
                raise InvalidPositionException('Ship %s placement is beyond row boundary' % ship_id)

            if c >= self.width or r < 0:
                raise InvalidPositionException('Ship %s placement is beyond column boundary' % ship_id)

            coords.append(make_coord(r, c))

        for c in coords:
            for s in self.ships:
                if c in s.coords:
                    raise InvalidPositionException('Ship %s placement conflicts with another at (%s, %s)' % (ship_id, r, c))

        ship.coords = coords

