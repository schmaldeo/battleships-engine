"""
:author github.com/schmaldeo
This module contains classes and methods that can be used for coding a battleship board game clone
"""
from enum import Enum
import random
import math


class Field(Enum):
    """
    Contains types of fields on boards
    """
    EMPTY = 1
    TAKEN = 2
    HIT = 3
    MISSED = 4


class Direction(Enum):
    """
    Contains directions in which ships can be headed
    """
    HORIZONTAL = 0
    VERTICAL = 1


class ShipType(Enum):
    """Contains types of ships"""
    DESTROYER = 1
    CRUISER = 2
    BATTLESHIP = 3


class Ship:
    """Contains methods related to a ship"""
    def __init__(self, ship_type: ShipType, x_coordinate: int,
                 y_coordinate: int, direction: Direction):
        self.ship_type = ship_type
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.direction = direction
        match ship_type:
            case ShipType.DESTROYER:
                self.health_points = 2
            case ShipType.CRUISER:
                self.health_points = 3
            case ShipType.BATTLESHIP:
                self.health_points = 4
            case _:
                raise ValueError("Wrong ShipType specified")
        self.sunken = False
        self.coordinates = []
        if direction == Direction.VERTICAL:
            for i in range(y_coordinate, y_coordinate + self.health_points):
                self.coordinates.append([i, x_coordinate])
        if direction == Direction.HORIZONTAL:
            for i in range(x_coordinate, x_coordinate + self.health_points):
                self.coordinates.append([y_coordinate, i])

    def __str__(self):
        return f"Type: {self.ship_type}\nHP: {self.health_points}\nx: {self.x_coordinate}\n\
y: {self.y_coordinate}\nDirection: {self.direction}"

    def hit(self) -> bool:
        """
        Removes one health point from the ship and sinks it if the health points go to 0
        :return: Boolean indicating whether the ship has sunk or not
        """
        self.health_points -= 1
        if self.health_points == 0:
            self.sunken = True
        return self.sunken


class ShotResponse:
    """Response of the ``shoot()`` method of ``SinglePlayerGame`` and ``MultiPlayerGame`` classes"""
    def __init__(self, hit: bool, ship: Ship | None, ships_left: int, hit_miss_board):
        self.hit = hit
        self.ship = ship
        self.ships_left = ships_left
        self.hit_miss_board = hit_miss_board

    def __str__(self):
        return (f"Hit: {self.hit}\n{self.ship.ship_type}, {self.ship.health_points} HP"
                f"\nShips left: {self.ships_left}")

    def print_hit_miss_board(self):
        """
        Prints its own hit-miss board
        :return: void
        """
        for row in self.hit_miss_board:
            print("│", end=" ")
            for field in row:
                match field:
                    case Field.EMPTY:
                        print("•", end=" ")
                    case Field.HIT:
                        print("×", end=" ")
                    case Field.MISSED:
                        print("○", end=" ")
            print("│")
        print("• - empty field, × - hit, ○ - missed")


class Player:
    """Methods related to a player"""
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.board = [[Field.EMPTY for _ in range(width)] for _ in range(height)]
        self.hit_miss_board = [[Field.EMPTY for _ in range(width)] for _ in range(height)]
        self.ships = []

    def put_ship(self, ship_type: ShipType, y_coordinate: int,
                 x_coordinate: int, direction: Direction) -> Ship:
        """
        Puts a ship on the board
        :param ship_type: Type of the ship to be put on the board
        :param y_coordinate: Y coordinate of the field on which the front of the ship will be put
        :param x_coordinate: X coordinate of the field on which the front of the ship will be put
        :param direction: Direction in which the ship will be placed
        :return: Ship that was put on the board
        """
        ship = Ship(ship_type, x_coordinate, y_coordinate, direction)
        # double iteration in this case is better than performing a deep copy of the board because
        # the board has a potentially unlimited size while ships are only 2, 3 or 4 fields long.
        # On top of that it might not even come to the 2nd iteration if an exception
        # is raised in the first one
        for coordinate in ship.coordinates:
            try:
                if self.board[coordinate[0]][coordinate[1]] == Field.TAKEN:
                    raise ValueError("Field already taken")
            except IndexError as exception:
                raise ValueError("Ship cannot be placed outside of the board") from exception
        for coordinate in ship.coordinates:
            self.board[coordinate[0]][coordinate[1]] = Field.TAKEN
        self.ships.append(ship)
        return ship

    def random_spawn(self, ship_type: ShipType) -> Ship:
        """
        Spawns a ship in a random place on the board if there's space for it
        :param ship_type: Type of the ship to be spawned
        :return: Ship that was spawned
        """
        # iterative algorithm that generates random starting position that isn't already taken by
        # another ship, then tries to put the ship on the board, if the remainder of the ship tries
        # to take space already taken by an existing ship which throws an exception in put_ship
        # method, it first tries to put it in another direction, then if that also doesn't work, it
        # reruns the algorithm. it also never runs on the same data

        tried = []
        counter = 0
        while True:
            if counter == self.width * self.height:
                raise RuntimeError("Impossible to put a ship on the board")
            counter += 1

            y_coordinate = math.floor(random.random() * self.height)
            x_coordinate = math.floor(random.random() * self.width)
            if [y_coordinate, x_coordinate] in tried:
                continue

            direction = round(random.random())
            ship_overlap = (
                any(([x_coordinate, y_coordinate] in ship.coordinates for ship in self.ships)))

            if ship_overlap:
                tried.append([y_coordinate, x_coordinate])

            if not ship_overlap:
                try:
                    ship = self.put_ship(
                        ship_type, y_coordinate, x_coordinate, Direction(direction))
                    return ship
                except ValueError:
                    try:
                        ship = self.put_ship(ship_type, y_coordinate, x_coordinate,
                                             Direction(0) if direction == 1 else Direction(1))
                        return ship
                    except ValueError:
                        tried.append([y_coordinate, x_coordinate])
                        continue

    def print_board(self):
        """
        Prints player's board
        :return: void
        """
        # top border
        print("", end=" ")
        for _ in range(self.width):
            print("――", end="")
        print("―")

        # board
        for row in self.board:
            print("│", end=" ")
            for field in row:
                match field:
                    case Field.EMPTY:
                        print("•", end=" ")
                    case Field.TAKEN:
                        print("\u02a4", end=" ")
            print("│")

        # bottom border
        print("", end=" ")
        for _ in range(self.width):
            print("――", end="")
        print("―")
        print("• - empty field, \u02a4 - ship")

    def print_hit_miss_board(self):
        """
        Prints player's hit-miss board
        :return: void
        """
        # top border
        print("", end=" ")
        for _ in range(self.width):
            print("――", end="")
        print("―")

        # board
        for row in self.hit_miss_board:
            print("│", end=" ")
            for field in row:
                match field:
                    case Field.EMPTY:
                        print("•", end=" ")
                    case Field.HIT:
                        print("×", end=" ")
                    case Field.MISSED:
                        print("○", end=" ")
            print("│")

        # bottom border
        print("", end=" ")
        for _ in range(self.width):
            print("――", end="")
        print("―")
        print("• - empty field, × - hit, ○ - missed")


class SinglePlayerGame:
    """Game for one player"""
    def __init__(self, width: int = 8, height: int = 8):
        if width < 4 or height < 4:
            raise ValueError("Board cannot be smaller than 4x4")
        self.player = Player(width, height)

    def random_spawn(self):
        """
        Spawns a destroyer, a cruiser and a battleship in a random spot on the board
        :return: void
        """
        self.player.random_spawn(ShipType.DESTROYER)
        self.player.random_spawn(ShipType.CRUISER)
        self.player.random_spawn(ShipType.BATTLESHIP)

    def shoot(self, y_coordinate: int, x_coordinate: int) -> ShotResponse:
        """
        Shoots a field on board
        :param y_coordinate: Y coordinate of the field
        :param x_coordinate: X coordinate of the field
        :return: ShotResponse object with details about the outcome
        """
        if self.player.board[y_coordinate][x_coordinate] == Field.TAKEN:
            self.player.hit_miss_board[y_coordinate][x_coordinate] = Field.HIT
            for ship in self.player.ships:
                if [y_coordinate, x_coordinate] in ship.coordinates:
                    sunken = ship.hit()
                    if sunken:
                        self.player.ships.remove(ship)
                    return ShotResponse(True, ship, len(self.player.ships),
                                        self.player.hit_miss_board)
        if self.player.board[y_coordinate][x_coordinate] == Field.EMPTY:
            self.player.hit_miss_board[y_coordinate][x_coordinate] = Field.MISSED
            return ShotResponse(False, None, len(self.player.ships),
                                self.player.hit_miss_board)
        raise RuntimeError("Wrong field on board")

    def print_board(self):
        """Prints player's board"""
        self.player.print_board()

    def print_hit_miss_board(self):
        """Prints player's hit-miss board"""
        self.player.print_hit_miss_board()


class MultiPlayerGame:
    """Game for 2 players"""
    def __init__(self, width: int = 8, height: int = 8):
        if width < 4 or height < 4:
            raise ValueError("Board cannot be smaller than 4x4")
        self.player1 = Player(width, height)
        self.player2 = Player(width, height)

    def shoot(self, shooter_index: int, y_coordinate: int, x_coordinate: int):
        """
        Shoots a field on opponent's board
        :param shooter_index: Index of the player which shoots opponent's ship (1 or 2)
        :param y_coordinate: Y coordinate of the field
        :param x_coordinate: X coordinate of the field
        :return: ShotResponse object with details about the outcome
        """
        if shooter_index == 1:
            shooter = self.player1
            receiver = self.player2
        elif shooter_index == 2:
            shooter = self.player2
            receiver = self.player1
        else:
            raise ValueError("Wrong player index passed")

        if receiver.board[y_coordinate][x_coordinate] == Field.TAKEN:
            shooter.hit_miss_board[y_coordinate][x_coordinate] = Field.HIT
            for ship in receiver.ships:
                if [y_coordinate, x_coordinate] in ship.coordinates:
                    sunken = ship.hit()
                    if sunken:
                        receiver.ships.remove(ship)
                    return ShotResponse(True, ship, len(receiver.ships), shooter.hit_miss_board)
        if receiver.board[y_coordinate][x_coordinate] == Field.EMPTY:
            shooter.hit_miss_board[y_coordinate][x_coordinate] = Field.MISSED
            return ShotResponse(False, None, len(receiver.ships), shooter.hit_miss_board)
        return None

    def print_boards(self):
        """Prints both players' boards"""
        print("Player 1:")
        self.player1.print_board()
        print("Player 2:")
        self.player2.print_board()

    def print_hit_miss_boards(self):
        """Prints both players' miss-hit boards"""
        print("Player 1:")
        self.player1.print_hit_miss_board()
        print("Player 2:")
        self.player2.print_hit_miss_board()
