from enum import Enum
import random
import math
import copy


class Field(Enum):
    EMPTY = 1
    TAKEN = 2
    HIT = 3
    MISSED = 4


class Direction(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


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

    def hit(self):
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
        if width < 4 or height < 4:
            raise ValueError("Board cannot be smaller than 4x4")
        self.width = width
        self.height = height
        self.board = [[Field.EMPTY for _ in range(self.width)] for _ in range(self.height)]
        self.hits_misses_board = [[Field.EMPTY for _ in range(self.width)] for _ in range(self.height)]
        self.ships = []

    def put_ship(self, ship_type: ShipType, y: int, x: int, direction: Direction):
        ship = Ship(ship_type, x, y, direction)
        temp_board = copy.deepcopy(self.board)
        for coordinate in ship.coordinates:
            try:
                if temp_board[coordinate[0]][coordinate[1]] == Field.TAKEN:
                    raise Exception("Field already taken")
                temp_board[coordinate[0]][coordinate[1]] = Field.TAKEN
            except IndexError:
                raise IndexError("Ship cannot be placed outside of the board")
        self.board = temp_board
        self.ships.append(ship)
        return ship

    def shoot(self, y: int, x: int):
        if self.board[y][x] == Field.TAKEN:
            self.hits_misses_board[y][x] = Field.HIT
            for ship in self.ships:
                if [y, x] in ship.coordinates:
                    sunken = ship.hit()
                    if sunken:
                        self.ships.remove(ship)
                    return ShotResponse(True, ship, len(self.ships), self.hits_misses_board)
        if self.board[y][x] == Field.EMPTY:
            self.hits_misses_board[y][x] = Field.MISSED
            return ShotResponse(False, None, len(self.ships), self.hits_misses_board)

    def random_spawn(self, ship_type: ShipType):
        # iterative algorithm that generates random starting position that isn't already taken by another ship,
        # then tries to put the ship on the board, if the remainder of the ship tries to take space already taken
        # by an existing ship which throws an exception in put_ship method, it first tries to put it
        # in another direction, then if that also doesn't work, it reruns the algorithm. it also never runs
        # on the same data

        tried = []
        counter = 0
        while True:
            if counter == self.width * self.height:
                raise Exception("Impossible to put a ship on the board")
            counter += 1

            y = math.floor(random.random() * self.height)
            x = math.floor(random.random() * self.width)
            if [y, x] in tried:
                continue

            direction = round(random.random())
            ship_overlap = any(([x, y] in ship.coordinates for ship in self.ships))

            if ship_overlap:
                tried.append([y, x])

            if not ship_overlap:
                try:
                    self.put_ship(ship_type, y, x, Direction(direction))
                    break
                except Exception:
                    try:
                        self.put_ship(ship_type, y, x, Direction(0) if direction == 1 else Direction(1))
                        break
                    except Exception:
                        tried.append([y, x])
                        continue

    def print_board(self):
        print("", end=" ")
        for _ in range(self.width):
            print("――", end="")
        print("―")
        for row in self.board:
            print("│", end=" ")
            for field in row:
                match field:
                    case Field.EMPTY:
                        print("•", end=" ")
                    case Field.TAKEN:
                        print(u"\u02a4", end=" ")
            print("│")

        print("", end=" ")
        for _ in range(self.width):
            print("――", end="")
        print("―")
        print(u"• - empty field, \u02a4 - ship")

    def print_hit_miss_board(self):
        print("", end=" ")
        for _ in range(self.width):
            print("――", end="")
        print("―")
        for row in self.hits_misses_board:
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

        print("", end=" ")
        for _ in range(self.width):
            print("――", end="")
        print("―")
        print(u"• - empty field, × - hit, ○ - missed")
