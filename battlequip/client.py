import sys
import re
import random
import argparse
import curses
import time

parser = argparse.ArgumentParser(description='Play a game of Battleship.')
#parser.add_argument('integers', metavar='N', type=int,
#                   help='an integer for the accumulator')
#parser.add_argument('--sum', dest='accumulate', action='store_const',
#                   const=sum, default=max,
#                   help='sum the integers (default: find the max)')

args = parser.parse_args()
#print(args.accumulate(args.integers))

class dstate:
    INIT = 0
    HIT  = 1
    MISS = 2
    SHIP_OK = 3
    SHIP_DANGER = 4
    SHIP_SUNK = 5

def print_boards(stdscr, *boards, **kwargs):
    """Prints an ASCII board representation using curses.

    boards:
        One or more Board objects to use in a side-by-side representation.

    kwargs:
        attacks: an array of positions corresponding to attacks
        height: board height
        width: board width
        ship_display: the Ship property to use in the character display
    """
    attacks      = kwargs['attacks']      if 'attacks'      in kwargs else []
    height       = kwargs['height']       if 'height'       in kwargs else 10
    width        = kwargs['width']        if 'width'        in kwargs else 10
    ship_display = kwargs['ship_display'] if 'ship_display' in kwargs else 'size'

    visual_boards = []

    states = {
             '*': dstate.INIT,
             'x': dstate.HIT,
             'o': dstate.MISS
             }

    # Build the internal display structure in layers
    for b in boards:
        # All spaces start out empty (represented by a *)
        visual_boards.append([['*' for x in xrange(width)] for x in xrange(height)])
        # Add in the ships
        for s in b.ships:
            for p in s.positions:
                visual_boards[-1][p[0]][p[1]] = getattr(s, ship_display)

    curses.start_color()
    try:
        curses.curs_set(0)
    except curses.error:
        pass

    offset_y = 2
    offset_x = 2
    display_height = height+offset_y
    display_width = width+offset_x
    display_buffer = 2

    display = curses.newpad(display_height,
            (display_width + display_buffer) * len(boards))

    #curses.init_pair(dstate.INIT, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(dstate.HIT, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(dstate.MISS, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(dstate.SHIP_OK, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(dstate.SHIP_DANGER, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(dstate.SHIP_SUNK, curses.COLOR_BLACK, curses.COLOR_RED)

    for c in range(0, len(visual_boards)):
        for j in range(0, width):
            display.addstr(0, offset_x + c * (width+3) + j, str(j+1))

    for i in range(0, height):
        for c in range(0, len(visual_boards)):
            display.addstr(offset_y + i, c * (width+3), chr(i + 65))
            for j in range(0, width):
                state_chr = str(visual_boards[c][i][j])
                state = states[state_chr] if state_chr in states else dstate.INIT
                display.addstr(offset_y + i, offset_x + c * (width+3) + j, state_chr, curses.color_pair(state))

    for a in attacks:
        char = str(visual_boards[-1][a[0]][a[1]])
        state = dstate.HIT if char != '*' else dstate.MISS
        display.addstr(offset_y + a[0], offset_x + a[1], char, curses.color_pair(state))

    curses.curs_set(2)
    display.move(3,5)
    display.refresh(0, 0, 0, 0, display_height, display_width)

    display.nodelay(1)
    while True:
        try:
            char = display.getstr()
        except:
            pass
        pos = display.getyx()
        display.addstr(1,2, str(char))
        #display.addstr(21,2, str(pos))
        if char == 113: break  # q
        elif char == curses.KEY_RIGHT: display.move(pos[0],pos[1] + 1)
        elif char == curses.KEY_LEFT: display.move(pos[0],pos[1] - 1)
        elif char == curses.KEY_UP: display.move(pos[0] - 1, pos[1])
        elif char == curses.KEY_DOWN: display.move(pos[0] + 1, pos[1])
        display.refresh(0, 0, 0, 0, 1, 20)
        curses.doupdate()
        time.sleep(0.1)

def print_boards2(*boards, **kwargs):
    """Prints an ASCII board representation to stdout. If this were fancier
    we'd be using curses.

    boards:
        One or more Board objects to use in a side-by-side representation.

    kwargs:
        attacks: an array of positions corresponding to attacks
        height: board height
        width: board width
        ship_display: the Ship property to use in the character display
    """
    attacks      = kwargs['attacks']      if 'attacks'      in kwargs else []
    height       = kwargs['height']       if 'height'       in kwargs else 10
    width        = kwargs['width']        if 'width'        in kwargs else 10
    ship_display = kwargs['ship_display'] if 'ship_display' in kwargs else 'size'

    visual_boards = []

    # Build the internal display structure in layers
    for b in boards:
        # All spaces start out empty (represented by a *)
        visual_boards.append([['*' for x in xrange(width)] for x in xrange(height)])
        # Add in the ships
        for s in b.ships:
            for p in s.positions:
                visual_boards[-1][p[0]][p[1]] = getattr(s, ship_display)
        #
        for a in attacks:
            visual_boards[-1][a[0]][a[1]] = bcolors.RED + 'x' + bcolors.ENDC if visual_boards[-1][a[0]][a[1]] != '*' else bcolors.GREEN + 'o' + bcolors.ENDC
    sys.stdout.write('    ')
    for j in range(0, width):
        sys.stdout.write('%-3s' % (j+1))

    for c in range(1, len(visual_boards)):
        sys.stdout.write('         ')
        for j in range(0, width):
            sys.stdout.write('%-3s' % (j+1))
    sys.stdout.write('\n\n')

    for i in range(0, height):
        sys.stdout.write('%-4s' % chr(i + 65))
        for j in range(0, width):
            sys.stdout.write('%-3s' % visual_boards[0][i][j])
        for c in range(1, len(visual_boards)):
            sys.stdout.write('     ')
            sys.stdout.write('%-4s' % chr(i + 65))
            for j in range(0, width):
                sys.stdout.write('%-3s' % visual_boards[c][i][j])
        print '\n'

class Ship(object):
    def __init__(self, size, name='unknown ship'):
        self.name = name
        self.size = size

    @property
    def display_char(self):
        return self.name[0].lower()

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


class InvalidCoordException(Exception):
    def __init__(self, message):
        super(InvalidCoordException, self).__init__()
        self.message = message


class InvalidPositionException(Exception):
    def __init__(self, message):
        super(InvalidPositionException, self).__init__()
        self.message = message


class Coord(object):
    """Class to manage different ways of inputting board positions"""
    def __init__(self, raw_coord):
        if isinstance(raw_coord, tuple):
            # coord tuple must correspond to zero-based matrix (row, column)
            self._set_tuple(raw_coord)
        elif isinstance(raw_coord, str):
            # coord string is alpha & 1-based like 'B3' or 'c10'
            self._set_str(raw_coord)
        else:
            raise InvalidCoordException("Invalid format: " + type(raw_coord))

    def _set_tuple(self, raw_coord):
        """(Row, col) tuples must be zero-based (NUMBER, NUMBER)
        """
        if len(raw_coord) < 2:
            raise InvalidCoordException("coord tuple must have 2 elements")
        self._row = raw_coord[0]
        self._col = raw_coord[1]

    def _set_str(self, raw_coord):
        """"String must be of the format <LETTER><NUMBER>, like 'b2' or 'F10'
        """
        if len(raw_coord) < 2:
            raise InvalidCoordException("coord string must have 2+ elements")

        row = raw_coord[0]
        col = raw_coord[1:]
        if re.match('[a-zA-Z]', row):
            self._row = ord(row.upper()) - 65
        else:
            raise InvalidCoordException("coord elm 1 must be one alpha char")

        try:
            self._col = int(col) - 1
            if self._col < 0:
                raise Error
        except:
            raise InvalidCoordException("coord elm 2 must be column number >= 1")

    def as_tuple(self):
        return (self._row, self._col)

    def as_string(self):
        return chr(self._row + 65) + self._col

def make_coord(coord):
    if isinstance(coord, Coord):
        return coord
    else:
        return Coord(coord)

class Board(object):
    """A local representation of the a board."""

    def __init__(self, ships_and_positions=None, height=10, width=10):
        ships_and_positions = [] if not ships_and_positions else ships_and_positions
        self.ships = []
        self.ship_map = {}

        # This is ugly and wasteful but I'm lazy right now
        #self.theboard = []
        #[self.theboard.append(['*' for i in range(0,width)]) for i in range(0,height)]

        self.height = height
        self.width = width

        for s in ships_and_positions:
            self.add_ship(s[i][0],
                    make_coord(s[i][1]).as_tuple(),
                    s[i][2])

    def add_ship(self, ship, coord, direction='r'):
        """Plops the specified ship at the specified coord with specified direction"""
        ship_id = len(self.ships)
        self.set_ship_to_position(ship_id, ship, make_coord(coord).as_tuple(), direction)
        self.ships.append(ship)

    def set_ship_to_position(self, ship_id, ship, coord, direction):
        """Attempts to update the board to reflect a ship at a specified coord
        with specified direction.
        """
        #print ship_id, ship.name, coord, direction
        positions = []
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

            positions.append((r,c))

        for p in positions:
            for s in self.ships:
                if p in s.positions:
                    raise InvalidPositionException('Ship %s placement conflicts with another at (%s, %s)' % (ship_id, r, c))

        ship.positions = positions


class Strategy(object):
    def __init__(self):
        pass

    def get_move(board):
        """Analyzes the state of the board and returns a letter & number move"""
        pass


class HumanStrategy(Strategy):
    def get_move(board):
        """User analyzes the state of the board and inputs a letter & number
        move. The move is verified before returning.

        Returns:
            One of three things:
                1) A move like 'b3',
                2) 'err' if user was unable to input a move
                3) 'quit' if user wants to end the game prematurely
        """
        user_move_str = raw_input("Enter a move: ")
        try:
            move = Move(user_move_str)
            self.validate_move(board, move)
            return move
        except InvalidMoveException as ex:
            print ex.message
            return 'err'


class BoardHTTPProxy(object):
    """Mechanism by which client sends moves and receives updated state"""
    def __init__(self, url):
        self.url = url
        self.send_move_format = ''
        self.receive_board

    def send_move(move):
        """Sends the move to the server.

        Args:
            move: letter & number tuple just like the game. eg B9"""

        pass

    def receive_state():
        pass

class Game(object):
    def __init__(self, *args, **kwargs):
        """Initialize all configurable parameters before playing"""
        # Configurable options
        self.pieces      = self.initialize_pieces()
        self.positions   = self.initialize_positions()
        self.strategy    = self.initialize_strategy()

        # Game setup
        self.my_board    = self.initialize_board(pieces, positions)
        self.enemy_board = self.initialize_board(pieces)

    def play(self):
        """Executes a full game of battleship with the server"""
        while not done:
            pass

    def take_my_turn(self):
        move = strategy.get_move(board)
        proxy.send_move(move)
        proxy.recieve_board_state()
        return board.get_winner()

    def take_enemy_turn(self):
        proxy.recieve_board_state()
        return board.get_winner()

def random_ship():
    return {
            0: Carrier(),
            1: Battleship(),
            2: Submarine(),
            3: Destroyer(),
            4: Patrol()
            }[random.randint(0,5)]

if __name__ == '__main__':

    random.seed(123)

    SHIP_COUNT = 3
    #ships = [random_ship() for i in range(0,SHIP_COUNT)]
    #ships = [Carrier(), Battleship(), Patrol()]
    #positions = []
    b = Board()
    try:
        b.add_ship(Battleship(), 'a1', 'd')
        b.add_ship(Carrier(), "a2", 'r')
        b.add_ship(Battleship(), 'a9','d')
        b.add_ship(Patrol(), (2,1),'d')
        attacks = map(lambda s: make_coord(s).as_tuple(), ["b2","a9","a10"])
        curses.wrapper(print_boards, b, attacks=attacks, ship_display='size')
    except InvalidCoordException as ex:
        print ex.message
    except InvalidPositionException as e:
        print e.message

