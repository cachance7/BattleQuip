from util import *
import random

class StrategyStateException(Exception):
    def __init__(self, message):
        super(StrategyStateException, self).__init__()
        self.message = message

class Strategy(object):
    """Class to encapsulate logic of analyzing the state of a board and returning
    a valid coordinate to next attack."""

    def get_coord(board):
        """Analyzes the state of the board and returns a Coord"""
        pass

class HuntTarget(Strategy):
    """This class implements the Hunt/Target strategy outlined by Nick Berry:
    http://www.datagenetics.com/blog/december32011/index.html

    In this strategy, we don't care about sunk ships, only hits and misses.
    """
    def __init__(self, board):
        """Initialize with empty stack -> Hunt mode. If stack is nonempty,
        then object is in Target mode."""
        self.stack = []
        self.height = board.height
        self.width = board.width

        # This board will reflect 4 different states:
        # 0 - untested
        # 1 - to be tested
        # 2 - miss
        # 3 - hit
        # Initialize with 0s at start
        self.board = []
        [self.board.append([0]*self.width) for i in xrange(0, self.height)]

    def get_coord(self, last_attack=None):
        if last_attack:
            new_coords = self._mark_hit_or_miss(*last_attack)

            # Mark new coords to be inspected and push onto stack
            while len(new_coords) > 0:
                c = new_coords.pop()
                self._mark_inspect(c)
                self.stack.append(c)

            if len(self.stack) > 0:
                # target mode
                return self.stack.pop()

        # hunt mode
        return self._next_untested_random()

    def _mark_inspect(self, coord):
        self.board[coord.row][coord.col] = 1

    def _mark_hit_or_miss(self, coord, hit, sunk):
        """Marks the coord on the board as either hit or miss and returns new
        set of coords if appropriate."""
        self.board[coord.row][coord.col] = 3 if hit else 2
        if hit:
            # N,S,W,E
            new_coords = [make_coord(coord.row-1,coord.col),
                    make_coord(coord.row+1, coord.col),
                    make_coord(coord.row, coord.col-1),
                    make_coord(coord.row, coord.col+1)]
            # Now filter based on criteria
            # Within bounds
            new_coords = filter(lambda x: x[0] >= 0 and x[1] >= 0, new_coords)
            new_coords = filter(lambda x: x[0] < self.height and x[1] < self.width, new_coords)

            # Only untested
            new_coords = filter(lambda x: self.board[x.row][x.col] == 0, new_coords)
            return new_coords
        else:
            return []

    def _next_untested(self):
        """Grabs the next untested coord in W->E, N->S order."""
        for r in xrange(0, self.height):
            for c in xrange(0, self.width):
                if self.board[r][c] == 0:
                    return make_coord(r,c)

        raise StrategyStateException('Game is over')

    def _next_untested_random(self):
        """Grabs the next untested coord randomly."""
        choices = []
        for r in xrange(0, self.height):
            for c in xrange(0, self.width):
                if self.board[r][c] == 0:
                    choices.append((r,c))

        if len(choices) == 0:
            raise StrategyStateException('Game is over')

        return make_coord(choices[random.randint(0, len(choices)-1)])


class HumanStrategy(Strategy):
    def get_coord(board):
        """User analyzes the state of the board and inputs a letter & number
        move. The move is verified before returning.

        Returns:
            A Coord cooresponding to the desired attack.

        Raises:
            InputAbortException: if user aborts
        """
        user_move_str = raw_input("Enter a move: ")
        try:
            move = Move(user_move_str)
            self.validate_move(board, move)
            return move
        except InvalidMoveException as ex:
            print ex.message
            return 'err'

