import sys
import os
import random
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from engine import MultiPlayerGame, ShipType, Direction


game = MultiPlayerGame(5, 5)
game.player1.print_board()
print("Bot will have 1 ship of each type spawned in a random spot")
game.player2.random_spawn(ShipType.DESTROYER)
game.player2.random_spawn(ShipType.CRUISER)
game.player2.random_spawn(ShipType.BATTLESHIP)


for i in range(1, 4):
    print(f"Pick a place for {ShipType(i)}")
    y = input("Select row: ")
    x = input("Select column: ")
    direction = input("Select direction (0 - horizontal, 1 - vertical): ")
    game.player1.put_ship(ShipType(i), int(y) - 1, int(x) - 1, Direction(int(direction)))
    game.player1.print_board()

player_moves = 0
player_finished = False
bot_moves = 0
bot_finished = False
game.player2.print_board()
player_used = []
bot_used = []
while True:
    if not player_finished or not bot_finished:
        if not player_finished:
            # obviously there's no input validation, should obviously include that in real application
            print("Pick a field to shoot")
            while True:
                y = input("Choose row: ")
                x = input("Choose column: ")
                if [y, x] not in player_used:
                    break
                else:
                    print("You already shot that field")
            player_used.append([y, x])
            # need to -1 because engine uses 0-indexing
            shot = game.shoot(1, int(y) - 1, int(x) - 1)
            print("\nShot results:")
            print(shot)
            print("\nHits and misses:")
            shot.print_hit_miss_board()
            player_moves += 1
            if shot.ships_left == 0:
                player_finished = True
        if not bot_finished:
            while True:
                bot_y = round(random.random() * 4)
                bot_x = round(random.random() * 4)
                if [bot_y, bot_x] not in bot_used:
                    break
            bot_used.append([bot_y, bot_x])
            bot_shot = game.shoot(2, bot_y, bot_x)
            bot_moves += 1
            if bot_shot.hit:
                print(f"Bot hit your ship at {bot_y}, {bot_x}")
            else:
                print(f"Bot missed at {bot_y + 1}, {bot_x + 1}")
            if bot_shot.ships_left == 0:
                bot_finished = True
    else:
        break

if player_moves < bot_moves:
    print(f"Congratulations! You won! You took: {player_moves}, bot took: {bot_moves}")
elif player_moves > bot_moves:
    print(f"Unfortunately, you lost. You took: {player_moves}, bot took: {bot_moves}")
else:
    print(f"This game was a tie! You both took {player_moves}")
