__author__ = 'Austin'

import othello
import random
import math
import game2
import operator
import time


class Tree(object):
    def __init__(self, budget):
        """
        time is the number of seconds we can think before moving
        """
        self.nodes = []
        self.budget = budget

    def policy(self, game):
        # TODO if we want a version that reuses trajectories, replace the next two LOC
        self.nodes = []
        self.nodes.append(Node(-1, len(self.nodes), game))

        start_time = time.time()

        # run time # of trajectories
        while time.time() < start_time + self.budget:
            self.trajectory(self.nodes[0])

        # pick action from root with highest Q-value
        actions = self.nodes[0].state.generate_moves()
        max_index, max_value = max(enumerate([(float(self.nodes[0].action_values[x]) / float(self.nodes[0].action_counts[x])) for x in [str(y) for y in actions]]), key=operator.itemgetter(1))

        return max_value, actions[max_index]

    def build_child_node(self, start_node, action):
        """
        Taking a start node and an action, builds a new child node and simulates one game from one of its actions.
        """
        state = start_node.state.copy()
        state.play_move(action)
        # make a new node for this state
        new_idx = len(self.nodes)
        self.nodes.append(Node(start_node.idx, new_idx, state))
        moves = state.generate_moves()

        if len(moves) > 0:
            # simulate trajectory from this node
            new_node_action = random.choice(moves)
            state.play_move(new_node_action)
            result = self.simulate_random(self.nodes[new_idx].state.copy())
            # update child
            self.update(self.nodes[new_idx], new_node_action, result)
        else:
            # the value at this node IS the simulated value
            result = state.abs_score()
            #print "(childnode)Game score: " + str(result)

        return new_idx, result

    def trajectory(self, start_node):
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
        #   result = simulate(self.nodes(new_idx).state.copy())
        #   update local state of node at new_idx
        #   update own local state
        #   return result
        # else
        #   action = tree_policy(start_node)
        #   figure out which of start_node's child states corresponds to this node
        #   result = trajectory(that_child_state, time??)
        #   update own local state based on result
        #   return result

        #print "trajectory at node: "
        #print start_node.state

        actions = start_node.state.generate_moves()
        if len(actions) == 0:
            result = start_node.state.abs_score()
            #print "(noactions) Game score: " + str(result)
            return result

        not_yet_taken = [x for x in actions if start_node.action_counts[str(x)] == 0]
        if len(not_yet_taken) > 0:
            # take an action that we haven't yet taken
            action = random.choice(not_yet_taken)
            new_idx, result = self.build_child_node(start_node, action)
            # update self
            self.update(start_node, action, result)
            # update action -> child mapping
            start_node.child_idxs[str(action)] = new_idx

            # unwind recursion
            return result
        else:
            c = 1
            # determine action to take based on start_node.action_counts and start_node.action_values and start_node.visits
            max_index, _ = max(enumerate([self.tree_search_value(start_node, x, c) for x in [str(y) for y in actions]]), key=operator.itemgetter(1))
            action = actions[max_index]

            if start_node.child_idxs[str(action)] >= 0:
                result = self.trajectory(self.nodes[start_node.child_idxs[str(action)]])
            else:
                new_idx, result = self.build_child_node(start_node, action)
                start_node.child_idxs[str(action)] = new_idx

            # update own state
            self.update(start_node, action, result)

            return result

    def tree_search_value(self, node, action_key, c):
        q = float(node.action_values[action_key]) / float(node.action_counts[action_key])
        explore = math.log(node.visits) / float(node.action_counts[action_key])
        result = q + c * math.sqrt(explore)
        return result

    def update(self, node, action, result):
        # black = player 1, first to go, positive scores
        # white = player 2, second to go, negative scores
        rel_score = result * node.state.player
        node.visits += 1
        node.action_counts[str(action)] += 1
        node.action_values[str(action)] += result
    
    def _random_policy(self, game):
        return 0, random.choice(game.generate_moves())
    
    def simulate_random(self, start_state):
        ''' 
        This simulates the random policy that occurs outside of the tree
        policy. Simulates adversarial othello playing until end of game.
        inputs: start_state = a 'game' object
        returns: winner score (- for player 2)(+ for player 1)
        '''
        return game2.play(start_state, game2.player(lambda x: self._random_policy(x)), game2.player(lambda x: self._random_policy(x)), False)
    
    def _greedy_policy(self, game):
        return 0, random.choice(game.generate_moves())
    
    def simulate_greedy(self, start_state):
        return game2.play(start_state, game2.player(lambda x: self.greedy_policy(x)), game2.player(lambda x: self._greedy_policy(x)), False)

class Node(object):
    def __init__(self, parent_idx, idx, state):
        """
        parent_idx and idx are the positions of the node in some global array of nodes
        they're kind of important to maintaining a tree, doncha know
        state is the othello.game type
        """
        # index of parent node, is -1 for root
        self.parent_idx = parent_idx
        # own index
        self.idx = idx
        self.state = state.copy()
        # don't need self.turn, game.player = -1 white, 1 black

        # how many times this node has been visited
        self.visits = 0

        # dict of {"action": child_idx} # TODO it's either this or parent_action
        # TODO this does allow indexing to child by action
        self.child_idxs = {str(k): -1 for k in self.state.generate_moves()}

        # dict of {"action": times taken}
        self.action_counts = {str(k): 0 for k in self.state.generate_moves()}

        # dict of {"action": rewards received}
        self.action_values = {str(k): 0 for k in self.state.generate_moves()}
