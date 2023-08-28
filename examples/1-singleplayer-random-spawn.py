import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from engine import SinglePlayerGame


game = SinglePlayerGame(5, 5)
print("Created a 5x5 board")
game.player.print_board()
# randomly spawn 1 ship of each type
game.random_spawn()

moves = 0
while True:
    # obviously there's no input validation, should obviously include that in real application
    y = input("Choose row: ")
    x = input("Choose column: ")
    # need to -1 because engine uses 0-indexing
    shot = game.shoot(int(y) - 1, int(x) - 1)
    print("\nShot results:")
    print(shot)
    print("\nHits and misses:")
    shot.print_hit_miss_board()
    moves += 1
    if shot.ships_left == 0:
        break

print(f"Congratulations, you won in {moves} moves")
