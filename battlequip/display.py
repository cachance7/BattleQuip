import curses
import sys
import os

class dstate:
    INIT = 0
    HIT  = 1
    MISS = 2
    SHIP_OK = 3
    SHIP_DANGER = 4
    SHIP_SUNK = 5

class Display(object):
    def __init__(self, board, **kwargs):
        self.board = board
        self.ship_display = kwargs['ship_display'] if 'ship_display' in kwargs else 'size'
        self.states = {
                      '*': dstate.INIT,
                      'x': dstate.HIT,
                      'o': dstate.MISS
                      }
        curses.wrapper(run, board, )

def run(stdscr, board, ):
    """Initializes an ASCII board representation using curses.

    Args:
        stdscr (...):
        board (Board): The Board object this Display will visualize
        **kwargs:
            ship_display: the Ship property to use in the character display
    """
    #attacks      = kwargs['attacks']      if 'attacks'      in kwargs else []
    #height       = kwargs['height']       if 'height'       in kwargs else 10
    #width        = kwargs['width']        if 'width'        in kwargs else 10

    visual_boards = []

    # Build the internal display structure in layers
    #for b in boards:
    #    # All spaces start out empty (represented by a *)
    #    visual_boards.append([['*' for x in xrange(width)] for x in xrange(height)])
    #    # Add in the ships
    #    for s in b.ships:
    #        for p in s.positions:
    #            visual_boards[-1][p[0]][p[1]] = getattr(s, ship_display)

    #curses.start_color()
    #try:
    #    curses.curs_set(0)
    #except curses.error:
    #    pass

    #offset_y = 2
    #offset_x = 2
    self.display_height = self.board.height
    self.display_width = self.board.width
    self.display_buffer = 2

    self.display = curses.newpad(self.display_height,
            (self.display_width + self.display_buffer))

    #curses.init_pair(dstate.INIT, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(dstate.HIT, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(dstate.MISS, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(dstate.SHIP_OK, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(dstate.SHIP_DANGER, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(dstate.SHIP_SUNK, curses.COLOR_BLACK, curses.COLOR_RED)

    #for c in range(0, len(visual_boards)):
    #    for j in range(0, width):
    #        display.addstr(0, offset_x + c * (width+3) + j, str(j+1))

    #for i in range(0, height):
    #    for c in range(0, len(visual_boards)):
    #        display.addstr(offset_y + i, c * (width+3), chr(i + 65))
    #        for j in range(0, width):
    #            state_chr = str(visual_boards[c][i][j])
    #            state = states[state_chr] if state_chr in states else dstate.INIT
    #            display.addstr(offset_y + i, offset_x + c * (width+3) + j, state_chr, curses.color_pair(state))

    #for a in attacks:
    #    char = str(visual_boards[-1][a[0]][a[1]])
    #    state = dstate.HIT if char != '*' else dstate.MISS
    #    display.addstr(offset_y + a[0], offset_x + a[1], char, curses.color_pair(state))

    #curses.curs_set(1)
    #display.move(3,5)
    self.display.refresh(0, 0, 0, 0, self.display_height, self.display_width)

def get_coord(self):
    display = self.display
    display.nodelay(1)
    while True:
        try:
            char = display.getch()
        except:
            pass

        pos = display.getyx()
        newpos = pos

        display.addstr(1,2, str(char))

        if char == 033:
            display.getch()
            char = display.getch()
            if char == 65:  # up
                newpos = (pos[0] - 1, pos[1])
            elif char == 66:  # down
                newpos = (pos[0] + 1, pos[1])
            elif char == 67:  # right
                newpos = (pos[0], pos[1] + 1)
            elif char == 68:  # left
                newpos = (pos[0], pos[1] - 1)
            #display.addstr(4, 3, ' %s ' % char)

        if newpos:
            display.move(*newpos)

        for i in range(0, self.display_width):
            display.chgat(newpos[0], i, 1, curses.A_REVERSE)
        for i in range(0, self.display_height):
            display.chgat(i, newpos[1], 1, curses.A_REVERSE)

        #display.hline(newpos[0], 0, '-', 10)
        #display.vline(0, newpos[1], '|', 10)

        display.refresh(0, 0, 0, 0, self.display_height, self.display_width)
        time.sleep(0.01)

# {{{ Obsolete
def print_boards3(stdscr, *boards, **kwargs):
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
            char = display.getch()
        except:
            pass

        pos = display.getyx()
        newpos = pos

        display.addstr(1,2, str(char))

        if char == ord('\033'):
            display.getch()
            char = display.getch()
            if char == 65:  # up
                newpos = (pos[0] - 1, pos[1])
            elif char == 66:  # down
                newpos = (pos[0] + 1, pos[1])
            elif char == 67:  # right
                newpos = (pos[0], pos[1] + 1)
            elif char == 68:  # left
                newpos = (pos[0], pos[1] - 1)
            #display.addstr(4, 3, ' %s ' % char)

        if newpos:
            display.move(*newpos)


        #display.hline(newpos[0], 0, '-', 10)
        #display.vline(0, newpos[1], '|', 10)

        display.refresh(0, 0, 0, 0, display_height, display_width)
        time.sleep(0.01)

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
    height       = boards[0].height
    width        = boards[0].width
    ship_display = kwargs['ship_display'] if 'ship_display' in kwargs else 'size'

    visual_boards = []

    os.system('clear')

    # Build the internal display structure in layers
    for b in boards:
        # All spaces start out empty (represented by a *)
        visual_boards.append([['*' for x in xrange(width)] for x in xrange(height)])
        # Add in the ships
        for s in b.ships:
            for p in s.coords:
                visual_boards[-1][p[0]][p[1]] = getattr(s, ship_display)
        #
        for a in b.attacks:
            visual_boards[-1][a.coord[0]][a.coord[1]] = 'X' if visual_boards[-1][a.coord[0]][a.coord[1]] != '*' else 'O'
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
# }}}


