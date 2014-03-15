#!/usr/bin/python
## Rich Meier and Austin Sharp
## Monte Carlo Planning Algorithm to play Othello
###############################################################################
## NOTES:
## 
##
##
###############################################################################

import random
import UCT_tree
import othello
import minimax
import game2
import sys

def random_policy(game):
    return 0, random.choice(game.generate_moves())

def _calculate_value(game, move):
    ## game.player must match values on board.
    ## using othello.directions for getting adjacent positions.

    ## for each vector around the current position
    player = game.player
    totalValue = 0
    for vector in othello.directions:
        current_pos = move
        #print(current_pos)
        adj_pos = (None,None)
        vector_value = 0
        playable = False
        while True:
            adj_pos = [current_pos[0] + vector[0], current_pos[1] + vector[1]]
            #print(adj_pos)
            ## if adjacent position is outside board range exit inner loop
            if adj_pos[0] >= othello.size or adj_pos[1] >= othello.size:
                break
            if adj_pos[0] < 0 or adj_pos[1] < 0:
                break
            ## if adjacent position is my own piece then exit inner loop
            if game.board[adj_pos[0]][adj_pos[1]] == player:
                playable = True
                break
            ## if adjacent position is open then
            if game.board[adj_pos[0]][adj_pos[1]] == 0:
                break
            ## otherwise we know adj_space is opponent
            ## continue moving in direction of vector add 1 to possible value
            current_pos = adj_pos
            vector_value += 1
        if playable == True:
            totalValue += vector_value
    return totalValue

def greedy_policy(game):
    ## Test if no move available
    if None in game.generate_moves():
        return (0,None)
    ## Otherwise there is at least 1 move to take.
    else:
        moves = game.generate_moves()
        ## empty dictionary of (key:val = (move): int value of move)
        moveDict = {key: None for key in moves}
        for move in moves:
            # calculate value of each move.
            value = _calculate_value(game, move)
            ## set dictionary value at specific key.
            moveDict[move] = value
            #print(moveDict)
        ## best key Move according to values.
        bestMove = max(moveDict.iterkeys(), key=lambda x: moveDict[x])
        return (0,bestMove)
    ## Something stupid happened
    raise RuntimeError("Something went wrong in Greedy Policy")


def average(list):
    if len(list) == 0:
        return 0
    return sum(list) / len(list)


if __name__ == "__main__":
    ## for actual UCT training just do:
#    uct_policy = UCT_trainer()

    ## to actually use the trained policy to play against a real person:
#    play(othello.game(), player(lambda x: ourPolicies.UCT_policy(x, SOME_VARIABLE_LEARNED_POLICY)), player(lambda x: user_player(x)), True)
    ## or to use the trained policy to play against their algorithm:
#    play(othello.game(), player(lambda x: ourPolicies.UCT_policy(x, SOME_VARIABLE_LEARNED_POLICY)),
#         player(lambda x: minimax.minimax(x, 3)) , True)

    ## Rich's playing around with functions....
    #game2.play(othello.game(), game2.player(lambda x: minimax.minimax(x, 3)), game2.player(lambda x: random_move_policy(x)), True)

    #t = UCT_tree.Tree(5, random_policy, 1)
    #game2.play(othello.game(), game2.player(lambda x: minimax.minimax(x, 3)), game2.player(t.policy), True)
    #game2.play(othello.game(), game2.player(t.policy), game2.player(lambda x: minimax.minimax(x, 4)), True)

    policies = {"random": random_policy, "greedy": greedy_policy}
    budgets = [1, 2, 5]
    c_vals = [1, 5, 10]#, 20, 50]
    opponents = {"random": game2.player(random_policy),
                 "greedy": game2.player(greedy_policy),
                 "minimax-2": game2.player(lambda x: minimax.minimax(x, 2)),
                 "minimax-3": game2.player(lambda x: minimax.minimax(x, 3)),
                 "minimax-4": game2.player(lambda x: minimax.minimax(x, 4))}
    # number of games going first/second with each configuration
    n = 10

    # run this algorithm with different hard-coded sizes
    # for each policy
        # for each budget (i.e. 1,2,5 seconds)
            # for each opponent
                # run n trials with us first, n trials with them first
    
    ## saving printouts to output.txt
    old_stdout = sys.stdout # keep pointer to original stdout
    sys.stdout = open('output.txt', 'wb')
    
    for pol_key in policies:
        for b in budgets:
            for c in c_vals:
                for opp_key in opponents:
                    t = UCT_tree.Tree(b, policies[pol_key], c)
                    uct_player = game2.player(t.policy)
                    uct_black = []
                    uct_white = []
                    for i in range(n):
                        b_result, b_game = game2.play(othello.game(), uct_player, opponents[opp_key], False)
                        uct_black.append(b_result)
                        #print b_game
                        w_result, w_game = game2.play(othello.game(), opponents[opp_key], uct_player, False)
                        uct_white.append(w_result)
                        #print w_game
                    print("Average score over " + str(n) + "trials for default policy " + str(pol_key) + ", budget " + str(b) + ", c = " + str(c) + ", opponent " + str(opp_key) + ":")
                    print("Results as black (positive = we win):")
                    print(str(average(uct_black)))
                    print("Results as white (negative = we win):")
                    print(str(average(uct_white)))
    
    ## closing output.txt and restore stdout
    sys.stdout.flush()
    sys.stdout.close()
    sys.stdout = old_stdout

