import unittest
from engine import SinglePlayerGame, MultiPlayerGame, Field, ShipType, Direction


class TestSinglePlayerGame(unittest.TestCase):
    def test_put_destroyer(self):
        game = SinglePlayerGame()
        game.player.put_ship(ShipType.DESTROYER, 0, 0, Direction.HORIZONTAL)
        self.assertTrue(
            game.player.board ==
            [[Field.TAKEN, Field.TAKEN, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY]])

    def test_put_cruiser(self):
        game = SinglePlayerGame()
        game.player.put_ship(ShipType.CRUISER, 0, 0, Direction.HORIZONTAL)
        self.assertTrue(
            game.player.board ==
            [[Field.TAKEN, Field.TAKEN, Field.TAKEN, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY]])

    def test_put_battleship(self):
        game = SinglePlayerGame()
        game.player.put_ship(ShipType.BATTLESHIP, 0, 0, Direction.HORIZONTAL)
        self.assertTrue(
            game.player.board ==
            [[Field.TAKEN, Field.TAKEN, Field.TAKEN, Field.TAKEN, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY]])

    def test_put_destroyer_vertically(self):
        game = SinglePlayerGame()
        game.player.put_ship(ShipType.DESTROYER, 0, 0, Direction.VERTICAL)
        self.assertTrue(
            game.player.board ==
            [[Field.TAKEN, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.TAKEN, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY]])

    def test_custom_board_size(self):
        game = SinglePlayerGame(4, 4)
        self.assertTrue(
            game.player.board ==
            [[Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY]])

        with self.assertRaises(ValueError):
            SinglePlayerGame(3, 3)

    def test_hit_ship(self):
        game = SinglePlayerGame(4, 4)
        ship = game.player.put_ship(ShipType.DESTROYER, 0, 0, Direction.HORIZONTAL)
        self.assertTrue(
            game.player.board ==
            [[Field.TAKEN, Field.TAKEN, Field.EMPTY, Field.EMPTY],
            [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
            [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
            [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY]]
        )

        hit_shot = game.shoot(0, 1)
        self.assertTrue(hit_shot.hit)
        self.assertTrue(hit_shot.ship == ship)
        self.assertTrue(hit_shot.ships_left == 1)
        self.assertTrue(
            hit_shot.hit_miss_board == [[Field.EMPTY, Field.HIT, Field.EMPTY, Field.EMPTY],
                                        [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
                                        [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
                                        [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY]])

        self.assertTrue(
            game.player.board ==
            [[Field.TAKEN, Field.TAKEN, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY]]
        )

        missed_shot = game.shoot(1, 0)
        self.assertTrue(not missed_shot.hit)
        self.assertTrue(missed_shot.ship is None)
        self.assertTrue(missed_shot.ships_left == 1)
        self.assertTrue(missed_shot.hit_miss_board == [[Field.EMPTY, Field.HIT, Field.EMPTY, Field.EMPTY],
                                                       [Field.MISSED, Field.EMPTY, Field.EMPTY, Field.EMPTY],
                                                       [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
                                                       [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY]])

    def test_destroy_ship(self):
        game = SinglePlayerGame(4, 4)
        ship = game.player.put_ship(ShipType.DESTROYER, 0, 0, Direction.HORIZONTAL)
        game.shoot(0, 1)
        game.shoot(1, 0)
        shot = game.shoot(0, 0)
        self.assertTrue(
            game.player.board ==
            [[Field.TAKEN, Field.TAKEN, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY]]
        )

        self.assertTrue(shot.hit)
        self.assertTrue(shot.ship == ship)
        self.assertTrue(shot.ships_left == 0)
        self.assertTrue(shot.hit_miss_board == [[Field.HIT, Field.HIT, Field.EMPTY, Field.EMPTY],
                                                [Field.MISSED, Field.EMPTY, Field.EMPTY, Field.EMPTY],
                                                [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
                                                [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY]])

    def test_random_spawn(self):
        game = SinglePlayerGame(6, 6)
        game.player.random_spawn(ShipType.DESTROYER)
        self.assertFalse(
            game.player.board == [[Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
                        [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
                        [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
                        [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY]]
        )


class TestMultiPlayerGame(unittest.TestCase):
    def test_create_game(self):
        game = MultiPlayerGame(4, 4)
        self.assertTrue(
            game.player1.board ==
            [[Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY]]
        )

        self.assertTrue(
            game.player2.board ==
            [[Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY]]
        )

    def test_put_ships(self):
        game = MultiPlayerGame(4, 4)
        game.player1.put_ship(ShipType.DESTROYER, 0, 0, Direction.HORIZONTAL)
        self.assertTrue(
            game.player1.board ==
            [[Field.TAKEN, Field.TAKEN, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY]]
        )

        self.assertTrue(
            game.player2.board ==
            [[Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY]]
        )

    def test_shoot_ships(self):
        game = MultiPlayerGame(4, 4)
        game.player1.put_ship(ShipType.DESTROYER, 0, 0, Direction.HORIZONTAL)
        self.assertTrue(
            game.player1.board ==
            [[Field.TAKEN, Field.TAKEN, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY]]
        )

        game.shoot(2, 0, 0)
        self.assertTrue(
            game.player2.hit_miss_board ==
            [[Field.HIT, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY]]
        )

        game.shoot(2, 1, 0)
        self.assertTrue(
            game.player2.hit_miss_board ==
            [[Field.HIT, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.MISSED, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY],
             [Field.EMPTY, Field.EMPTY, Field.EMPTY, Field.EMPTY]]
        )

        with self.assertRaises(ValueError):
            game.shoot(0, 1, 1)


class TestPlayer(unittest.TestCase):
    def test_putting_ship_on_taken_field(self):
        game = SinglePlayerGame(4, 4)
        game.player.put_ship(ShipType.BATTLESHIP, 0, 0, Direction.HORIZONTAL)
        with self.assertRaises(ValueError):
            game.player.put_ship(ShipType.DESTROYER, 0, 1, Direction.VERTICAL)

    def test_putting_ship_outside_the_board(self):
        game = SinglePlayerGame(4, 4)
        with self.assertRaises(ValueError):
            game.player.put_ship(ShipType.BATTLESHIP, 0, 1, Direction.HORIZONTAL)


unittest.main()
