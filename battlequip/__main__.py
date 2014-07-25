from board import Board
from ship import *
import display
from strategy import HuntTarget
import time

def init_board():
    b = Board()
    b.add_ship(Battleship(), 'a1', 'd')
    b.add_ship(Carrier(), "a2", 'r')
    b.add_ship(Battleship(), 'a9','d')
    b.add_ship(Patrol(), (2,1),'d')
    #b.add_ship(Battleship(), 'i8', 'l')
    #b.add_ship(Patrol(), 'i9', 'r')
    return b

def main():
    b = init_board()
    display.print_boards2(b)

    s = HuntTarget(b)
    a = None
    count = 0
    while not b.is_fleet_sunk:
        c = s.get_coord(a)
        a = b.attack(c)
        display.print_boards2(b)
        count += 1
        time.sleep(1)
    #d = Display(b)

if __name__ == '__main__':
    main()
