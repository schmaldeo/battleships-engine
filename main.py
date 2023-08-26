from enum import Enum
import random
import math


class Field(Enum):
    EMPTY = 1
    TAKEN = 2
    HIT = 3
    MISSED = 4


class Direction(Enum):
    HORIZONTAL = 1
    VERTICAL = 2


class ShipType(Enum):
    DESTROYER = 1
    CRUISER = 2
    BATTLESHIP = 3


class Ship:
    def __init__(self, ship_type: ShipType, x: int, y: int, direction: Direction):
        self.ship_type = ship_type
        self.x = x
        self.y = y
        self.direction = direction
        match ship_type:
            case ShipType.DESTROYER:
                self.hp = 2
            case ShipType.CRUISER:
                self.hp = 3
            case ShipType.BATTLESHIP:
                self.hp = 4
            case _:
                raise Exception("Wrong ShipType specified")
        self.sunken = False
        self.coordinates = []
        if direction == Direction.VERTICAL:
            for i in range(y, y + self.hp):
                self.coordinates.append([i, x])
        if direction == Direction.HORIZONTAL:
            for i in range(x, x + self.hp):
                self.coordinates.append([y, i])

    def hit(self, y, x):
        self.hp -= 1
        if self.hp == 0:
            self.sunken = True
        return self.sunken


class ShotResponse:
    def __init__(self, hit: bool, ship: Ship | None, ships_left: int, hits_misses_board):
        self.hit = hit
        self.ship = ship
        self.ships_left = ships_left
        self.hits_misses_board = hits_misses_board


class Game:
    def __init__(self, width: int = 8, height: int = 8):
        # TODO limit on width and height
        self.width = width
        self.height = height
        self.board = [[Field.EMPTY for _ in range(self.width)] for _ in range(self.height)]
        self.hits_misses_board = [[Field.EMPTY for _ in range(self.width)] for _ in range(self.height)]
        self.ships = []

    def put_ship(self, ship_type: ShipType, y: int, x: int, direction: Direction):
        ship = Ship(ship_type, x, y, direction)
        self.ships.append(ship)
        temp_board = self.board.copy()
        for coordinate in ship.coordinates:
            if temp_board[coordinate[0]][coordinate[1]] == Field.TAKEN:
                raise Exception("Field already taken")
            temp_board[coordinate[0]][coordinate[1]] = Field.TAKEN
        self.board = temp_board
        return ship

    def shoot(self, y: int, x: int):
        if self.board[y][x] == Field.TAKEN:
            self.hits_misses_board[y][x] = Field.HIT
            self.board[y][x] = Field.HIT
            for ship in self.ships:
                if [y, x] in ship.coordinates:
                    sunken = ship.hit(y, x)
                    if sunken:
                        self.ships.remove(ship)
                    return ShotResponse(True, ship, len(self.ships), self.hits_misses_board)
        if self.board[y][x] == Field.EMPTY:
            self.hits_misses_board[y][x] = Field.MISSED
            return ShotResponse(False, None, len(self.ships), self.hits_misses_board)

    def random_spawn(self, ship_type: ShipType):
        # recursive algorithm that generates random starting position that isn't already taken by another ship,
        # then tries to put the ship on the board, if the remainder of the ship tries to take space already taken
        # by an existing ship which throws an exception in put_ship method, it first tries to put it
        # in another direction, then if that also doesn't work it reruns the algorithm. it also doesn't run the
        # algorithm twice on the same data

        tried = []

        def get_random():
            y = math.floor(random.random() * self.height)
            x = math.floor(random.random() * self.width)
            if [y, x] in tried:
                get_random()
            direction = math.ceil(random.random() * 2)
            for ship in self.ships:
                if [y, x] in ship.coordinates:
                    get_random()
            try:
                self.put_ship(ship_type, y, x, Direction(direction))
            except Exception:
                try:
                    self.put_ship(ship_type, y, x, Direction(1) if direction == 2 else Direction(2))
                except Exception:
                    tried.append([y, x])
                    get_random()

        get_random()
