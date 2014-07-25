import random
import argparse
import time
import collections
from ship import *
from util import *

parser = argparse.ArgumentParser(description='Play a game of Battleship.')
#parser.add_argument('integers', metavar='N', type=int,
#                   help='an integer for the accumulator')
#parser.add_argument('--sum', dest='accumulate', action='store_const',
#                   const=sum, default=max,
#                   help='sum the integers (default: find the max)')

args = parser.parse_args()
#print(args.accumulate(args.integers))


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


if __name__ == '__main__':
    pass
