__author__ = 'Austin'

import othello
import random
import math


class Tree(object):
    def __init__(self, time):
        """
        time is the number of simulated trajectories before returning a move
        """
        self.nodes = []
        self.time = time

    def policy(self, game):
        # TODO if we want a version that reuses trajectories, replace the next two LOC
        self.nodes = []
        self.nodes.append(Node(-1, len(self.nodes), game))

        # run time # of trajectories
        # while current_time() < start_time + time
        for i in range(self.time):
            self.trajectory(self.nodes[0])

        # pick action from root with highest Q-value
        actions = self.nodes[0].state.generate_moves()
        max_index, _ = max([(self.nodes[0].action_values[x]/self.nodes[0].action_counts[x]) for x in [str(y) for y in actions]])

        return actions[max_index]

    def trajectory(self, start_node):
        """
        Somebody pulled the 'bandit arm' that is start_node.
        This is a recursive function (if this isn't a leaf node).
        Propagating up the tree takes place as the recursion unwinds.
        """

        actions = start_node.generate_moves()
        not_yet_taken = [x for x in actions if start_node.action_counts[str(x)] == 0]
        if len(not_yet_taken) > 0:
            # take an action that we haven't yet taken
            action = random.choice(not_yet_taken)
            state = start_node.state.copy()
            state.play_move(action)

            # make a new node for this state
            new_idx = len(self.nodes)
            self.nodes.append(Node(start_node.idx, new_idx, state))

            # simulate trajectory from this node
            new_node_action = random.choice(state.generate_moves())
            state.play_move(new_node_action)
            result = self.simulate(self.nodes[new_idx].state.copy())

            # update child
            self.update(self.nodes[new_idx], new_node_action, result)
            # update self
            self.update(start_node, action, result)
            # update action -> child mapping
            start_node.child_idxs[str[action]] = new_idx

            # unwind recursion
            return result
        else:
            c = 1
            # determine action to take based on start_node.action_counts and start_node.action_values and start_node.visits
            max_index, _ = max([(start_node.action_values[x]/start_node.action_counts[x] + c * math.sqrt(math.log(start_node.visits) / start_node.action_counts[x])) for x in [str(y) for y in actions]])
            action = actions[max_index]

            result = self.trajectory(self.nodes[start_node.child_idxs[str(action)]])

            # update own state
            self.update(start_node, action, result)

            return result

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

    def update(self, node, action, result):
        # black = player 1, first to go, positive scores
        # white = player 2, second to go, negative scores
        rel_score = result * node.state.player
        node.visits += 1
        node.action_counts[str(action)] += 1
        node.action_values[str(action)] += result
    
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
