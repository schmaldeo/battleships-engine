from enum import Enum


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
        self.coordinates.remove([y, x])


class ShotResponse:
    def __init__(self, hit: bool, ship: Ship | None, ships_left: int, hits_misses_board):
        self.hit = hit
        self.ship = ship
        self.ships_left = ships_left
        self.hits_misses_board = hits_misses_board


class Game:
    def __init__(self, width: int = 8, height: int = 8):
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

    def shoot(self, y: int, x: int):
        if self.board[y][x] == Field.TAKEN:
            self.hits_misses_board[y][x] = Field.HIT
            self.board[y][x] = Field.HIT
            for ship in self.ships:
                if [y, x] in ship.coordinates:
                    ship.hit(y, x)
                    return ShotResponse(True, ship, 0, self.hits_misses_board)
        if self.board[y][x] == Field.EMPTY:
            self.hits_misses_board[y][x] = Field.MISSED
            return ShotResponse(False, None, 0, self.hits_misses_board)


