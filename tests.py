import unittest
from main import *


class TestGame(unittest.TestCase):
    def test_put_destroyer(self):
        game = Game()
        game.put_ship(ShipType.DESTROYER, 0, 0, Direction.HORIZONTAL)
        self.assertTrue(
            game.board,
            [[Field.TAKEN, Field.TAKEN, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY]])

    def test_put_cruiser(self):
        game = Game()
        game.put_ship(ShipType.CRUISER, 0, 0, Direction.HORIZONTAL)
        self.assertTrue(
            game.board,
            [[Field.TAKEN, Field.TAKEN, Field.TAKEN, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY]])

    def test_put_battleship(self):
        game = Game()
        game.put_ship(ShipType.BATTLESHIP, 0, 0, Direction.HORIZONTAL)
        self.assertTrue(
            game.board,
            [[Field.TAKEN, Field.TAKEN, Field.TAKEN, Field.TAKEN, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY]])

    def test_put_destroyer_vertically(self):
        game = Game()
        game.put_ship(ShipType.DESTROYER, 0, 0, Direction.HORIZONTAL)
        self.assertTrue(
            game.board,
            [[Field.TAKEN, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.TAKEN, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY]])

    def test_custom_board_size(self):
        game = Game(2, 2)
        self.assertTrue(
            game.board,
            [[Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY]])

    def test_hit_ship(self):
        game = Game(4, 4)
        ship = game.put_ship(ShipType.DESTROYER, 0, 0, Direction.HORIZONTAL)
        self.assertTrue(
            game.board,
            [[Field.TAKEN, Field.TAKEN, Field.EMPTY, Field.EMPTY],
            [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
            [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
            [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY]]
        )

        hit_shot = game.shoot(0, 1)
        self.assertTrue(
            hit_shot, ShotResponse(True, ship, 1, 
                                   [[Field.EMPTY, Field.HIT, Field.EMPTY, Field.EMPTY],
                                    [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
                                    [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
                                    [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY]]))

        missed_shot = game.shoot(1, 0)
        self.assertTrue(
            missed_shot, ShotResponse(False, None, 1,
                                      [[Field.EMPTY, Field.HIT, Field.EMPTY, Field.EMPTY],
                                       [Field.MISSED, Field.EMPTY, Field.EMPTY, Field.EMPTY],
                                       [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
                                       [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY]]))


unittest.main()
