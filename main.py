from enum import Enum
import random
import math


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

    def __str__(self):
        return f"Type: {self.ship_type}\nHP: {self.hp}\nx: {self.x}\ny: {self.y}\nDirection: {self.direction}"

    def hit(self) -> bool:
        self.hp -= 1
        if self.hp == 0:
            self.sunken = True
        return self.sunken


class ShotResponse:
    def __init__(self, hit: bool, ship: Ship | None, ships_left: int, hit_miss_board):
        self.hit = hit
        self.ship = ship
        self.ships_left = ships_left
        self.hit_miss_board = hit_miss_board

    def __str__(self):
        return f"Hit: {self.hit}\nShip:\n{self.ship}\nShips left: {self.ships_left}"


class Player:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.board = [[Field.EMPTY for _ in range(width)] for _ in range(height)]
        self.hit_miss_board = [[Field.EMPTY for _ in range(width)] for _ in range(height)]
        self.ships = []

    def put_ship(self, ship_type: ShipType, y: int, x: int, direction: Direction) -> Ship:
        ship = Ship(ship_type, x, y, direction)
        # double iteration in this case is better than performing a deep copy of the board because the board has a
        # potentially unlimited size while ships are only 2, 3 or 4 fields long. On top of that it might not even come
        # to the 2nd iteration if an exception is raised in the first one
        for coordinate in ship.coordinates:
            try:
                if self.board[coordinate[0]][coordinate[1]] == Field.TAKEN:
                    raise ValueError("Field already taken")
            except IndexError:
                raise ValueError("Ship cannot be placed outside of the board")
        for coordinate in ship.coordinates:
            self.board[coordinate[0]][coordinate[1]] = Field.TAKEN
        self.ships.append(ship)
        return ship

    def random_spawn(self, ship_type: ShipType) -> Ship:
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
                    ship = self.put_ship(ship_type, y, x, Direction(direction))
                    return ship
                except ValueError:
                    try:
                        ship = self.put_ship(ship_type, y, x, Direction(0) if direction == 1 else Direction(1))
                        return ship
                    except ValueError:
                        tried.append([y, x])
                        continue

    def print_board(self):
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
                        print(u"\u02a4", end=" ")
            print("│")

        # bottom border
        print("", end=" ")
        for _ in range(self.width):
            print("――", end="")
        print("―")
        print(u"• - empty field, \u02a4 - ship")

    def print_hit_miss_board(self):
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
        print(u"• - empty field, × - hit, ○ - missed")


class SinglePlayerGame:
    def __init__(self, width: int = 8, height: int = 8):
        if width < 4 or height < 4:
            raise ValueError("Board cannot be smaller than 4x4")
        self.player = Player(width, height)

    # this method automatically spawns a destroyer, a cruiser and a battleship in a random spot on the board, as
    # described in https://github.com/florinpop17/app-ideas/blob/master/Projects/3-Advanced/Battleship-Game-Engine.md#bge
    # TODO: add presets?
    def random_spawn(self):
        self.player.random_spawn(ShipType.DESTROYER)
        self.player.random_spawn(ShipType.CRUISER)
        self.player.random_spawn(ShipType.BATTLESHIP)

    def shoot(self, y: int, x: int) -> ShotResponse:
        if self.player.board[y][x] == Field.TAKEN:
            self.player.hit_miss_board[y][x] = Field.HIT
            for ship in self.player.ships:
                if [y, x] in ship.coordinates:
                    sunken = ship.hit()
                    if sunken:
                        self.player.ships.remove(ship)
                    return ShotResponse(True, ship, len(self.player.ships), self.player.hit_miss_board)
        if self.player.board[y][x] == Field.EMPTY:
            self.player.hit_miss_board[y][x] = Field.MISSED
            return ShotResponse(False, None, len(self.player.ships), self.player.hit_miss_board)

    def print_board(self):
        self.player.print_board()

    def print_hit_miss_board(self):
        self.player.print_hit_miss_board()


class MultiPlayerGame:
    def __init__(self, width: int = 8, height: int = 8):
        if width < 4 or height < 4:
            raise ValueError("Board cannot be smaller than 4x4")
        self.player1 = Player(width, height)
        self.player2 = Player(width, height)

    def shoot(self, shooter_index: int, y: int, x: int):
        if shooter_index == 1:
            shooter = self.player1
            receiver = self.player2
        elif shooter_index == 2:
            shooter = self.player2
            receiver = self.player1
        else:
            raise ValueError("Wrong player index passed")

        if receiver.board[y][x] == Field.TAKEN:
            shooter.hit_miss_board[y][x] = Field.HIT
            for ship in receiver.ships:
                if [y, x] in ship.coordinates:
                    sunken = ship.hit()
                    if sunken:
                        receiver.ships.remove(ship)
                    return ShotResponse(True, ship, len(receiver.ships), shooter.hit_miss_board)
        if receiver.board[y][x] == Field.EMPTY:
            shooter.hit_miss_board[y][x] = Field.MISSED
            return ShotResponse(False, None, len(receiver.ships), shooter.hit_miss_board)
