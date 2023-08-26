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

    shots_game = Game(4, 4)
    shots_ship = shots_game.put_ship(ShipType.DESTROYER, 0, 0, Direction.HORIZONTAL)

    def test_hit_ship(self):
        self.assertTrue(
            self.shots_game.board,
            [[Field.TAKEN, Field.TAKEN, Field.EMPTY, Field.EMPTY],
            [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
            [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
            [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY]]
        )

        hit_shot = self.shots_game.shoot(0, 1)
        self.assertTrue(
            hit_shot, ShotResponse(True, self.shots_ship, 1, 
                                   [[Field.EMPTY, Field.HIT, Field.EMPTY, Field.EMPTY],
                                    [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
                                    [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
                                    [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY]]))

        self.assertTrue(
            self.shots_game.board,
            [[Field.TAKEN, Field.HIT, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY]]
        )

        missed_shot = self.shots_game.shoot(1, 0)
        self.assertTrue(
            missed_shot, ShotResponse(False, None, 1,
                                      [[Field.EMPTY, Field.HIT, Field.EMPTY, Field.EMPTY],
                                       [Field.MISSED, Field.EMPTY, Field.EMPTY, Field.EMPTY],
                                       [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
                                       [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY]]))

    def test_destroy_ship(self):
        shot = self.shots_game.shoot(0, 0)
        self.assertTrue(
            self.shots_game.board,
            [[Field.HIT, Field.HIT, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY]]
        )

        self.assertTrue(
            shot, ShotResponse(
                True, self.shots_ship, 0,
                [[Field.HIT, Field.HIT, Field.EMPTY, Field.EMPTY],
                 [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
                 [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
                 [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY]])
        )


unittest.main()
