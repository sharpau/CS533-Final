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

import random
import UCT_tree
import othello
import minimax
import game2


def random_policy(game):
    return 0, random.choice(game.generate_moves())

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

    policies = [random_policy] # TODO add greedy
    budgets = [0.1, 0.5, 1]
    c_vals = [1, 5, 10, 20, 50]
    # TODO add greedy
    opponents = [game2.player(random_policy), game2.player(lambda x: minimax.minimax(x, 2))]#, game2.player(lambda x: minimax.minimax(x, 3)), game2.player(lambda x: minimax.minimax(x, 4))]
    # number of games going first/second with each configuration
    n = 10

    # run this algorithm with different hard-coded sizes
    # for each policy
        # for each budget (i.e. 1,2,5 seconds)
            # for each opponent
                # run n trials with us first, n trials with them first

    for p in policies:
        for b in budgets:
            for c in c_vals:
                for o in opponents:
                    t = UCT_tree.Tree(b, p, c)
                    uct_player = game2.player(t.policy)
                    uct_black = []
                    uct_white = []
                    for i in range(n):
                        b_result = game2.play(othello.game(), uct_player, o, False)
                        uct_black.append(b_result)
                        w_result = game2.play(othello.game(), o, uct_player, False)
                        uct_white.append(w_result)
                    print "For policy " + str(p) + ", budget " + str(b) + ", c = " + str(c) + ", opponent " + str(o) + ":"
                    print "Results as black (positive = we win):"
                    print str(b_result)
                    print "Results as white (negative = we win):"
                    print str(w_result)

