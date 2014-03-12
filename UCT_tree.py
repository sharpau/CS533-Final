__author__ = 'Austin'

import othello
import random


class Tree(object):
    def __init__(self, game):
        """
        game is an othello.game position for which we're going to build a tree
        """
        self.nodes = []
        self.nodes.append(Node(-1, len(self.nodes), game))

    def trajectory(self, start_node, time):
        """
        Somebody pulled the 'bandit arm' that is start_node.
        This is a recursive function (if this isn't a leaf node).
        Propagating up the tree takes place as the recursion unwinds.
        """

        # if start_node has actions that have never been taken
        #   action = random.choice(start_node.never_taken())
        #   state = start_node.state.copy()
        #   state.take_action(action)
        #   new_idx = len(self.nodes)
        #   self.nodes.append(new Node(start_node.idx, new_idx, state))
        #   TODO simulate trajectory from new Node and propagate back up
        #   result = simulate(self.nodes(new_idx).state.copy())
        #   update local state of node at new_idx TODO need some way to update based on action
        #   update own local state
        #   return result
        # else
        #   action = tree_policy(start_node)
        #   figure out which of start_node's child states corresponds to this node
        #   result = trajectory(that_child_state, time??)
        #   update own local state based on result
        #   return result

    
    def _random_policy(self, game)
        moves = game.generate_moves()
        return moves[random.randint(0, len(moves)-1)]
    
    def simulate_random(self, start_state):
        ''' 
        This simulates the random policy that occurs outside of the tree
        policy. Simulates adversarial othello playing until end of game.
        inputs: start_state = a 'game' object
        returns: winner score (- for player 2)(+ for player 1)
        '''
        return game2.play(start_state, (lambda x: self._random_policy(x)), (lambda x: self._random_policy(x)), False)
    
    def _greedy_policy(self, game):
        return        
    
    def simulate_greedy(self, start_state):
        return game2.play(start_state, (lambda x: self.greedy_policy(x)), (lambda x: self._greedy_policy(x)), False)

class Node(object):
    def __init__(self, parent_idx, parent_action, idx, state):
        """
        parent_idx and idx are the positions of the node in some global array of nodes
        they're kind of important to maintaining a tree, doncha know
        state is the othello.game type
        """
        # index of parent node, is -1 for root
        self.parent_idx = parent_idx
        # how did we get here (for propagating up the tree)
        self.parent_action = parent_action # seems more generalizable than dict below
        # own index
        self.idx = idx
        self.state = state.copy()
        # self.turn = turn(self.state) # TODO do we want or need this?

        # how many times this node has been visited
        self.visits = 0

        # dict of {"action": child_idx} # TODO it's either this or parent_action
        # TODO this does allow indexing to child by action
        self.child_idxs = {str(k): -1 for k in self.state.generate_moves()}

        # dict of {"action": times taken}
        self.action_counts = {str(k): 0 for k in self.state.generate_moves()}

        # dict of {"action": rewards received}
        self.action_values = {str(k): 0 for k in self.state.generate_moves()}
