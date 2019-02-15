"""UCT algorithm for two-player, zero-sum games."""

import math
import random

C = 1 / math.sqrt(2)


class Node:
    def __init__(self, state, parent=None, parent_action=None):
        self.N = 1
        self.Q = 0
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = set()
        self._node_actions = state.valid_actions.copy()

    def is_expandable(self):
        return not self.is_terminal() and len(self._node_actions) != 0

    def is_terminal(self):
        return self.state.is_terminal

    def get_node_actions(self):
        if not isinstance(self._node_actions, list):
            return list(self._node_actions)
        else:
            return self._node_actions

    def remove_node_action(self, action):
        self._node_actions.remove(action)

    def increment_visit_count(self):
        self.N += 1

    def increment_value(self, increment):
        self.Q += increment

    def add_child(self, child):
        self.children.add(child)

    @staticmethod
    def next_state(state, a):
        return state.next_state(state, a)


def uct_search(init_state, num_simulations):
    root = Node(init_state)
    t = 0
    while t < num_simulations:
        node = tree_policy(root)
        reward = default_policy(node.state)
        # Reflecting whose turn it was.
        reward *= node.state.curr_player * -1
        backup(node, reward)
        t += 1
    return best_child(root, 0).parent_action


def expand(node):
    a = random.choice(node.get_node_actions())
    child_state = node.next_state(node.state, a)
    child = Node(child_state, node, a)
    node.add_child(child)
    node.remove_node_action(a)
    return child


def tree_policy(node):
    while not node.is_terminal():
        if node.is_expandable():
            return expand(node)
        else:
            node = best_child(node, C)
    return node


def default_policy(state):
    while not state.is_terminal:
        a = random.choice(list(state.valid_actions))
        state = state.next_state(state, a)
    return state.reward


def backup(node, reward):
    while node is not None:
        node.increment_visit_count()
        node.increment_value(reward)
        reward *= -1
        node = node.parent


def ucb(parent, child, c):
    return child.Q / child.N + c * math.sqrt(2 * math.log(parent.N) / child.N)


def best_child(node, c):
    ucbs = [(child, ucb(node, child, c)) for child in node.children]
    best_tup = max(ucbs, key=lambda x: x[1])
    return best_tup[0]
