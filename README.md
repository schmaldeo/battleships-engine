# Battleships Game Engine
This is my implementation of [florinpop17's app idea](https://github.com/florinpop17/app-ideas/blob/master/Projects/3-Advanced/Battleship-Game-Engine.md). It's written in Python and makes extensive use of OOP
features built into the language.

The engine itself doesn't contain any interactive layer, as I want to just make it a core for
actual interactive battleships games that might want to use features that are ready.
There are, however, 2 interactive examples in the `examples` directory of this repo. If you want
to try them out, pull this repository and run them with Python 3.10 or newer.

## Features
- Single- and multiplayer
- Using custom board width and height (at least 4x4)
- 3 types of ships
- Putting ships on the board manually and automatically (in a random spot)
- Shooting ships on board
- Tracking ships' HP
- Unicode printing current game board as well as hit-miss board