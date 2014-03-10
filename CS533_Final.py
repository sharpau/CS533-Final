#!/usr/bin/python
## Rich Meier and Austin Sharp
## Monte Carlo Planning Algorithm to play Othello
###############################################################################
## NOTES:
## I think this .py file will be very similar to the 'minimax.py' file that is
##    provided in the game files....?
##
##
###############################################################################

import time
import random

def UCT():
    print "DO uct Algorithm"

def random_move(game):
    moves = game.generate_moves()
    print moves #remove
    move_index = random.randint(0,len(moves)-1)
    move = moves[move_index]
    print("I chose move {0}".format(move)) #remove
    return (0,move)



