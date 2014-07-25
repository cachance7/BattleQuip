import unittest
import battlequip

def init_board():
    b = battlequip.Board()
    b.add_ship(battlequip.Battleship(), 'a1', 'd')
    b.add_ship(battlequip.Carrier(), "a2", 'r')
    b.add_ship(battlequip.Battleship(), 'a9','d')
    b.add_ship(battlequip.Patrol(), (2,1),'d')
    return b

class ShipConflictTest(unittest.TestCase):
    def test(self):
        b = init_board()
        with self.assertRaises(battlequip.InvalidPositionException):
            b.add_ship(battlequip.Battleship(), 'a1', 'r')

class SunkShipTest(unittest.TestCase):
    def test(self):
        b = init_board()
        a = b.attack(battlequip.make_coord('b9'))
        self.assertEqual(a, battlequip.Attack(battlequip.make_coord('b9'), True))

        a = b.attack(battlequip.make_coord('a9'))
        self.assertIsNone(a.sunk)
        a = b.attack(battlequip.make_coord('c9'))
        self.assertIsNone(a.sunk)
        a = b.attack(battlequip.make_coord('d9'))
        self.assertEqual(a.sunk, 4)

class RunawaySinkFleetTest(unittest.TestCase):
    def test(self):
        b = init_board()
        s = battlequip.HuntTarget(b)
        a = None
        count = 0
        with self.assertRaises(battlequip.StrategyStateException):
            while True:
                c = s.get_coord(a)
                a = b.attack(c)
                count += 1
                if a.sunk:
                    print 'Sunk ship of size %i after %i iterations' % (a.sunk, count)
                if count == b.height * b.width:
                    print 'Unused coords exhausted'

class SinkFleetTest(unittest.TestCase):
    def test(self):
        b = init_board()
        s = battlequip.HuntTarget(b)
        a = None
        count = 0
        while not b.is_fleet_sunk:
            c = s.get_coord(a)
            a = b.attack(c)
            count += 1
            if a.sunk:
                print 'Sunk ship of size %i after %i iterations' % (a.sunk, count)

if __name__ == '__main__':
    unittest.main()
