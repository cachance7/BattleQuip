import collections
import re

def namedtuple_with_defaults(typename, field_names, default_values=[]):
    T = collections.namedtuple(typename, field_names)
    T.__new__.__defaults__ = (None,) * len(T._fields)
    if isinstance(default_values, collections.Mapping):
        prototype = T(**default_values)
    else:
        prototype = T(*default_values)
    T.__new__.__defaults__ = tuple(prototype)
    return T

# Immutable battleship coordinate class
def _coord_as_string(self):
    return chr(self.row + 65) + str(self.col + 1)

Coord = namedtuple_with_defaults('Coord', ['row', 'col'])
Coord.__str__ = _coord_as_string

Status = namedtuple_with_defaults('Status', ['game_status', 'my_turn'])

Attack = namedtuple_with_defaults('Attack', ['coord', 'hit', 'sunk'])

class InvalidCoordException(Exception):
    def __init__(self, message):
        super(InvalidCoordException, self).__init__()
        self.message = message

class InvalidPositionException(Exception):
    def __init__(self, message):
        super(InvalidPositionException, self).__init__()
        self.message = message

def make_coord(*raw_coord):
    if len(raw_coord) == 1:
        return _make_coord(raw_coord[0])
    elif len(raw_coord) == 2:
        return _make_coord(raw_coord)

def _make_coord(raw_coord):
    if isinstance(raw_coord, Coord):
        return raw_coord
    elif isinstance(raw_coord, tuple):
        # coord tuple must correspond to zero-based matrix (row, column)
        if len(raw_coord) < 2:
            raise InvalidCoordException("coord tuple must have 2 elements")
        elif isinstance(raw_coord[0], str):
            return make_coord(raw_coord[0] + str(raw_coord[1]))
        return Coord(raw_coord[0], raw_coord[1])
    elif isinstance(raw_coord, str):
        # coord string is alpha & 1-based like 'B3' or 'c10'
        if len(raw_coord) < 2:
            raise InvalidCoordException("coord string must have 2+ elements")
        row = raw_coord[0]
        col = raw_coord[1:]
        if re.match('[a-zA-Z]', row):
            row = ord(row.upper()) - 65
        else:
            raise InvalidCoordException("coord elm 1 must be one alpha char")

        try:
            col = int(col) - 1
            if col < 0:
                raise Error
        except:
            raise InvalidCoordException("coord elm 2 must be column number >= 1")
        return Coord(row, col)
    else:
        raise InvalidCoordException("Invalid format: " + type(raw_coord))


