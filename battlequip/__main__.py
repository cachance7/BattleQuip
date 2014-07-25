from board import Board
from ship import *
import display
from strategy import HuntTarget
from connection import ConnectionZ
import time
import sys

def init_board():
    b = Board()
    b.add_ship(Carrier(), "a2", 'r')
    b.add_ship(Battleship(), 'a1', 'd')
    b.add_ship(Submarine(), 'j10', 'u')
    b.add_ship(Destroyer(), 'c5', 'r')
    b.add_ship(Patrol(), (2,1),'d')
    #b.add_ship(Battleship(), 'i8', 'l')
    #b.add_ship(Patrol(), 'i9', 'r')
    return b

def main(me, host, name):
    print "Game started"
    print 'Connecting to %s as %s' % (host, name)
    b = init_board()
    enemy_board = Board()

    connection = ConnectionZ(host)
    connection.join(b, name)

    s = HuntTarget(b)
    a = None
    count = 0
    status = connection.status()
    while status.game_status == 'playing':
        wait = 0
        while not status.my_turn:
            if wait > 5:
                sys.stdout.write("Waiting on foe...")
            wait += 1
            time.sleep(1)
            status = connection.status()
            if status.game_status != 'playing':
                print "You " + status.game_status
                sys.exit(0)

        if wait > 5:
            print 'READY!'
        wait = 0

        c = s.get_coord(a)
        a = connection.fire(c)
        sys.stdout.flush()
        enemy_board.attack(*a)
        display.print_boards2(enemy_board)
        sys.stdout.write("Attacking %s..." % str(c))
        print '%s' % 'HIT' if a.hit else 'MISS'
        sys.stdout.flush()
        status = connection.status()
        count += 1
        time.sleep(.1)
    print 'It took %i turns to find all the ships' % count
    #d = Display(b)

if __name__ == '__main__':
    main(*sys.argv)
