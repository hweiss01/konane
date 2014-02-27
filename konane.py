#!/usr/bin/env python
""" Tufts Comp 131 Konane Skeleton

Play a game of Konane between two players, either of whom can be 1) Human 2) Random or 3) A Minimax AI of your construction!
Requires python2.6+ or python3+

Usage:
  ./konane.py [-r <rows>] [-c <cols>] [-1 <p1type>] [-2 <p2type>] [-i <iter>] [-v] [-t <timeout>]

Options:
  -1 <p1type>                        Sets the player type ([H]uman, [R]andom, or [M]inimax) for player 1.  [default: R]
  -2 <p2type>                        Sets the player type for player 2.       [default: R]
  -c <cols>, --cols=<cols>           Sets the number of columns on the board. [default: 10]
  -h, --help                         Show this screen.
  -i <iter>, --iterations=<iter>     Sets the number of games to run.         [default: 1]
  -r <rows>, --rows=<rows>           Sets the number of rows on the board.    [default: 10]
  -t <timeout>, --timeout=<timeout>  How many seconds does each player have to make a move?   [default: 60]
  -v, --verbose                      Verbose mode, prints the intermediate game states.
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
from subprocess_player import ExternalPlayer

import game_manager
import os
import signal

def makePlayer(playerType, symbol, timeout=0):
  if playerType[0] == 'H':
    return HumanPlayer(symbol)
  elif playerType[0] == 'R':
    return RandomPlayer(symbol)
  elif playerType[0] == 'M':
    return MinimaxPlayer(symbol)
  elif os.path.exists(playerType):
    return ExternalPlayer(playerType, symbol, timeout)
  else:
    print("Unrecognized playerType %s for player %s" % (playerType, symbol))

if __name__ == "__main__":
  arguments = docopt(__doc__, version="Konane v1.0")
  iterations = int(arguments["--iterations"])
  timeout = int(arguments["--timeout"])
  rows = int(arguments["--rows"])
  cols = int(arguments["--cols"])
  p1 = arguments["-1"].capitalize()
  p2 = arguments["-2"].capitalize()
  gm = game_manager.GameManager(rows, cols
                                , makePlayer(p1, 'x', timeout)
                                , makePlayer(p2, 'o', timeout)
                                , "--verbose" in arguments and arguments["--verbose"])
  signal.signal(signal.SIGABRT, gm.interrupt)
  signal.signal(signal.SIGINT, gm.interrupt)
  signal.signal(signal.SIGQUIT, gm.interrupt)
  for _ in range(int(arguments["--iterations"])):
    gm.reset()
    gm.play()
    if gm.state == game_manager.X_VICTORY:
      print("X Wins!!")
    if gm.state == game_manager.O_VICTORY:
      print("O Wins!!")
