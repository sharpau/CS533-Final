# game2: play a 2 person game

from time import time
from time import sleep
## Rich Added, need reference to our policies...
import CS533_Final as ourPolicies

class IllegalMove(Exception):
    pass

def play(game, player1, player2, verbose = True):
    """Play a game between two players. Can raise IllegalMove"""

    next = 1 # player 1 has to move first
    player1_think = 0.0 # total think time
    player1_ply = 0
    player2_think = 0.0
    player2_ply = 0

    if verbose:
        print game
        
    last_move = None
    while not game.terminal_test():
        # make a temp copy of the game so that the player doesn't mess
        # with it
        temp = game.copy()
        # compute the next move for the player
        t1 = time()
        if next == 1:
            (value, move) = player1.play(temp, last_move)
        else:
            (value, move) = player2.play(temp, last_move)
        t2 = time()
        last_move = move
        # update player think time statistics
        if next == 1:
            player1_ply += 1
            player1_think += t2-t1
        else:
            player2_ply += 1
            player2_think += t2-t1

        if verbose:            
            print ("player %d plays %s (in %.1f s) evaluation value %d"
                   % (next, str(move), t2-t1, value))
        #check that the move is valid before applying it
        if move not in game.generate_moves():
            raise IllegalMove
        game.play_move(move)
        if verbose:
            print game
            print "(player", next, "score", -1*game.score(), ")"
        
        ## Rich Added for troublshooting... pause between each move to see what is going on.
        #sleep(3)
        
        # switch the next player and continue the game play loop
        next = 3 - next


    score = game.score()
    if score > 0:
        print "player "+str(next)+" won with score", score
    elif score < 0:
        print "player "+str(3-next)+" won with score", -1*score
    else:
        winner = 0
        print "DRAW!!"

    temp = game.copy()
    player1.gameover(temp, last_move)
    player2.gameover(temp, last_move)

    if player1_ply and player2_ply:
        print "%d ply: Player 1 %.1f s per ply. Player2 %.1f s per ply" % (
            player1_ply+player2_ply, player1_think/player1_ply,
            player2_think/player2_ply)

def user_player(game):
    """Make a user player to play the game."""

    while True:
        inp = raw_input("Your Move")
        try:
            move = eval(inp)
        except SyntaxError:
            print "Error: garbage move"
            continue
        if move not in game.generate_moves():
            print "Error: illegal move", move, type(move)
            print "Valid moves are", game.generate_moves()
            continue
        break

    return (0, move)    

class player:
    def __init__(self, play_fn):
        self.play_fn = play_fn

    def play(self, game, opp_move):
        return self.play_fn(game)

    def gameover(self, game, last_move):
        pass

## this function trains a tree-structured policy learned by monte-carlo UCT algorithm
## inputs: None
## returns: root of learned tree? or string of filename saved to disk? both?
## updates: None
def UCT_trainer():
    '''Pseudocode:

    Init Tree root
    
    while(checking some flag to know when done training... or just i < bigNumber)
        use the game2.play function to train UCT against some opponent:
        something like:
        play(othello.game(), player(lambda x: minimax.minimax(x,3)), player(lambda x: ourAgents.UCT_trainer(x)), False)
        or we could just play against a random policy:
        play(othello.game(), player(lambda x: ourAgents.random_move_policy(x)), player(lambda x: ourAgents.UCT_trainer(x)), False)
        
    somehow store learned tree to disk
    return tree as well?  
    
    
    '''
    return
   
if __name__ == "__main__":
    import othello
    import minimax

    ## for actual UCT training just do:
#    uct_policy = UCT_trainer()
    
    ## to actually use the trained policy to play against a real person:
#    play(othello.game(), player(lambda x: ourPolicies.UCT_policy(x, SOME_VARIABLE_LEARNED_POLICY)), player(lambda x: user_player(x)), True) 
    ## or to use the trained policy to play against their algorithm:
#    play(othello.game(), player(lambda x: ourPolicies.UCT_policy(x, SOME_VARIABLE_LEARNED_POLICY)), 
#         player(lambda x: minimax.minimax(x, 3)) , True)
    
    
    ## Rich's playing around with functions....    
    play(othello.game(), player(lambda x: minimax.minimax(x, 3)), player(lambda x: ourPolicies.random_move_policy(x)), True)
    
    play(othello.game(), player(lambda x: minimax.minimax(x, 3)), player(lambda x: user_player(x)), True)

   
############################################################################################################################################
## From Original file...

    # Experiment 1:
    # Player 1 and Player 2 are evenly matched with 3-ply deep search
    # player 2 wins with a final score of 28
    # player 1 0.2 s per ply player 2 0.4 s per ply
#    play(othello.game(), player(lambda x: minimax.minimax(x, 3)),
#         player(lambda x: minimax.minimax(x, 3)), True)
    
    # Experiment 2:
    # now we show the significance of an evaluation function
    # we weaken player1 to 2 ply deep but use the edge eval fun
    # player 1 now beats player 2 with a score of 58!
    # player 1 0.1 s per ply player 2 0.4 s per ply
#    play(othello.game(), player(lambda x: minimax.minimax(x, 2, othello.edge_eval)),
#         player(lambda x: minimax.minimax(x, 3)), False)

    # Experiment 1 (with alpha-beta):
    # player 1 0.1 s per ply, player 2 0.1 s per ply
#    play(othello.game(), player(lambda x: minimax.alphabeta(x, 3)),
#         player(lambda x: minimax.alphabeta(x, 3)), False)

    # Experiment 2 (with alpha-beta):
    # player 1 0.0 s per ply player 2 0.1 s per ply
#    play(othello.game(), player(lambda x: minimax.alphabeta(x, 2, othello.edge_eval)),
#         player(lambda x: minimax.alphabeta(x, 3)), False)