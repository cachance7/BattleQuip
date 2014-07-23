import curses, sys, time

class dstate:
    INIT = 0
    HIT  = 1
    MISS = 2
    SUNK = 3

def start(stdscr):
    curses.start_color()
    try:
        curses.curs_set(0)
    except curses.error:
        pass
    movement = curses.newpad(10, 10)

    curses.init_pair(dstate.HIT, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(dstate.MISS, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(dstate.SUNK, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

    movement.addstr(8, 9, '+')
    movement.addstr(9, 8, '+', curses.color_pair(1))
    text = sys.argv[1] if len(sys.argv) > 1 else '+'
    try:
        movement.addstr(9, 9, text)
        y, x = movement.getyx()
    except curses.error:
        y, x = movement.getyx()
        movement.addstr(0, 0, 'CAUGHT')
    if y >= 10 and x > 0:
        movement.addstr(1, 0, 'toolong')
    movement.refresh(0, 0, 0, 0, 9, 9)
    curses.doupdate()
    time.sleep(1)

if __name__ == '__main__':
    curses.wrapper(start)
