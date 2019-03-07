import random

from game_mechanics import State, simulated_step


class Board:
    def __init__(self, n=3):
        self._state = self.reset(n)

    def reset(self, n):
        board = [0] * n * n
        curr_player = random.choice([1, -1])
        is_terminal = False
        valid_actions = set(range(n * n))
        board_stats = {
            'board_size': n,
            'row_counts': [[0, 0] for _ in range(n)],
            'col_counts': [[0, 0] for _ in range(n)],
            'diag': [0, 0],
            'off_diag': [0, 0]
        }
        reward = 0
        return State(board, curr_player, valid_actions, is_terminal,
                     board_stats, reward)

    def is_valid_action(self, action):
        try:
            return self._state.board[action] == 0
        except Exception:
            return False

    def step(self, action, render=False):
        """Modifies local state."""
        self._state = simulated_step(self._state, action)
        if render:
            print(self)
        return self._state

    def get_state(self):
        return self._state

    def get_curr_player(self):
        return self._state.curr_player

    @staticmethod
    def get_piece(x):
        return 'X' if x == 1 else 'O'

    def _render(self, board, board_size):
        rows = ['============']
        n = board_size
        for row in range(n):
            offset = n * row
            rows.append(' '.join(
                map(lambda x: '_' if x == 0 else self.get_piece(x),
                    [board[offset + col] for col in range(n)])
             ))
            rows[-1] += '  ' + (' '.join(
                map(str, range(offset, offset + n))))
        return '\n'.join(rows)

    def __str__(self):
        return self._render(
            self._state.board, self._state.board_stats['board_size'])
