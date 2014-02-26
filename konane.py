#!/usr/bin/env python
""" Tufts Comp 131 Konane Skeleton

Play a game of Konane between two players, either of whom can be 1) Human 2) Random or 3) A Minimax AI of your construction!
Requires python2.6+ or python3+

Usage:
  ./konane.py [-r <rows>] [-c <cols>] [-1 <p1type>] [-2 <p2type>] [-i <iter>] [-v]

Options:
  -1 <p1type>                      Sets the player type ([H]uman, [R]andom, or [M]inimax) for player 1.  [default: R]
  -2 <p2type>                      Sets the player type for player 2.       [default: R]
  -c <cols>, --cols=<cols>         Sets the number of columns on the board. [default: 10]
  -h, --help                       Show this screen.
  -i <iter>, --iterations=<iter>   Sets the number of games to run.         [default: 1]
  -r <rows>, --rows=<rows>         Sets the number of rows on the board.    [default: 10]
  -v, --verbose                    Verbose mode, prints the intermediate game states.
"""

###########################################################################
# Explanation of the types:
# The board is represented by a row-major 2D list of characters, 0 indexed
# A point is a tuple of (int, int) representing (row, column)
# A move is a tuple of (point, point) representing (origin, destination)
# A jump is a move of length 2
###########################################################################

from docopt import docopt
from player import HumanPlayer, MinimaxPlayer, RandomPlayer

import game_manager

def makePlayer(playerType, symbol):
  if playerType[0] == 'H':
    return HumanPlayer(symbol)
  elif playerType[0] == 'R':
    return RandomPlayer(symbol)
  elif playerType[0] == 'M':
    return MinimaxPlayer(symbol)
  else:
    print("Unrecognized playerType %s for player %s" % (playerType, symbol))

if __name__ == "__main__":
  arguments = docopt(__doc__, version="Konane v1.0")
  iterations = int(arguments["--iterations"])
  rows = int(arguments["--rows"])
  cols = int(arguments["--cols"])
  p1 = arguments["-1"].capitalize()
  p2 = arguments["-2"].capitalize()
  gm = game_manager.GameManager(rows, cols
                                , makePlayer(p1, 'x')
                                , makePlayer(p2, 'o')
                                , "--verbose" in arguments and arguments["--verbose"])
  # TODO: run the game for the appropriate number of iterations
  gm.reset()
  gm.play()
  if gm.state == game_manager.X_VICTORY:
    print("X Wins!!")
  if gm.state == game_manager.O_VICTORY:
    print("O Wins!!")
