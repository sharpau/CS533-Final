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

'''IDK about any of this... the inheritance between files & file structure
    is a little weird.'''

## Executes adversarial simulation of choosing random actions.
## pick up where the tree policy left off.
## inputs: copy of original game state passed to UCT_trainer
## returns: string indicating winner
## updates: None
def execute_random_actions(rand_trajectory_game):
    return "this will return a winner"


def UCT_trainer(game):
    '''Pseudocode:

    UCT algorithm here.  Not sure how to link the tree to this function...
    
    Should follow according to tree policy until leaf node...
    
    Then execute random actions until terminal state.
    
    '''
    ## Executing random actions
    ## Make a copy of the game at the state were we reached the leaf node
#    rand_trajectory_game = game.copy()
#    winner = execute_random_actions(rand_trajectory_game)
    return

def UCT_policy(game, policy='load something from disk that defines what we have learned?'):
    '''Pseudocode:
    
    moves = game.generate_moves()
    
    move = somehow pick a move from 'moves' according to the state of the game and 
            our stored policy...
    
    return (0,move)
    '''
    return

def random_move_policy(game):
    moves = game.generate_moves()
    print moves #remove
    move_index = random.randint(0,len(moves)-1)
    move = moves[move_index]
    print("I chose move {0}".format(move)) #remove
    return (0,move)



