import random
import copy


class State:
    def __init__(self, board, curr_player, valid_actions, is_terminal,
                 board_stats, reward):
        self.board = board
        self.curr_player = curr_player
        self.is_terminal = is_terminal
        self.valid_actions = valid_actions
        self.board_stats = board_stats
        self.reward = reward

    @staticmethod
    def next_state(init_state, action):
        return BoardManager.simulated_step(init_state, action)


class BoardManager:
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

    @staticmethod
    def _update_board(board, action, player):
        new_board = board.copy()
        new_board[action] = player
        return new_board

    @staticmethod
    def _update_curr_player(curr_player):
        return curr_player * -1

    @staticmethod
    def _update_valid_actions(valid_actions, action):
        new_valid_actions = valid_actions.copy()
        new_valid_actions.remove(action)
        return new_valid_actions

    @staticmethod
    def _is_terminal(valid_actions):
        return not valid_actions

    @staticmethod
    def _update_board_stats(board_stats, action, player):
        new_board_stats = copy.deepcopy(board_stats)
        n = board_stats['board_size']
        row, col = BoardManager._get_row_col(action, n)
        ind_to_inc = 0 if player == 1 else 1
        new_board_stats['row_counts'][row][ind_to_inc] += 1
        new_board_stats['col_counts'][col][ind_to_inc] += 1
        if row == col:
            new_board_stats['diag'][ind_to_inc] += 1
        if row == n - 1 - col:
            new_board_stats['off_diag'][ind_to_inc] += 1
        return new_board_stats

    @staticmethod
    def _get_reward(board_stats, action):
        n = board_stats['board_size']
        row, col = BoardManager._get_row_col(action, n)
        if any([n in board_stats['row_counts'][row],
                n in board_stats['col_counts'][col],
                n in board_stats['diag'],
                n in board_stats['off_diag']]):
            return 1
        return 0

    @staticmethod
    def _get_row_col(action, board_size):
        return action // board_size, action % board_size

    def is_valid_action(self, action):
        try:
            return self._state.board[action] == 0
        except Exception as e:
            return False

    def step(self, action, render=False):
        """Modifies local state."""
        self._state = self.simulated_step(self._state, action)
        if render:
            print(self)
        return self._state

    @staticmethod
    def simulated_step(state, action):
        """Single simulated step which returns a new state object."""
        board = BoardManager._update_board(
            state.board, action, state.curr_player)
        curr_player = BoardManager._update_curr_player(state.curr_player)
        valid_actions = BoardManager._update_valid_actions(
            state.valid_actions, action)
        is_terminal = BoardManager._is_terminal(valid_actions)
        board_stats = BoardManager._update_board_stats(
            state.board_stats, action, state.curr_player)
        reward = BoardManager._get_reward(board_stats, action)
        # Reflecting who won the game.
        reward *= state.curr_player
        is_terminal |= (reward != 0)
        return State(board, curr_player, valid_actions, is_terminal,
                     board_stats, reward)

    def get_state(self):
        return self._state

    def get_curr_player(self):
        return self._state.curr_player

    @staticmethod
    def get_piece(x):
        return 'X' if x == 1 else 'O'

    @staticmethod
    def _render(board, board_size):
        print('============')
        rows = []
        n = board_size
        for row in range(n):
            offset = n * row
            rows.append(' '.join(
                map(lambda x: '_' if x == 0 else BoardManager.get_piece(x),
                    [board[offset + col] for col in range(n)])
                ))
            rows[-1] += '  ' + (' '.join(
                map(str, range(offset, offset + n))))
        return '\n'.join(rows)

    def __str__(self):
        return BoardManager._render(
            self._state.board, self._state.board_stats['board_size'])
