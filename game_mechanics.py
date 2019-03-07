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
        return simulated_step(init_state, action)


def _update_board(board, action, player):
    new_board = board.copy()
    new_board[action] = player
    return new_board


def _update_curr_player(curr_player):
    return curr_player * -1


def _update_valid_actions(valid_actions, action):
    new_valid_actions = valid_actions.copy()
    new_valid_actions.remove(action)
    return new_valid_actions


def _is_terminal(valid_actions):
    return not valid_actions


def _update_board_stats(board_stats, action, player):
    new_board_stats = copy.deepcopy(board_stats)
    n = board_stats['board_size']
    row, col = _get_row_col(action, n)
    ind_to_inc = 0 if player == 1 else 1
    new_board_stats['row_counts'][row][ind_to_inc] += 1
    new_board_stats['col_counts'][col][ind_to_inc] += 1
    if row == col:
        new_board_stats['diag'][ind_to_inc] += 1
    if row == n - 1 - col:
        new_board_stats['off_diag'][ind_to_inc] += 1
    return new_board_stats


def _get_reward(board_stats, action):
    n = board_stats['board_size']
    row, col = _get_row_col(action, n)
    if any([n in board_stats['row_counts'][row],
            n in board_stats['col_counts'][col],
            n in board_stats['diag'],
            n in board_stats['off_diag']]):
        return 1
    return 0


def _get_row_col(action, board_size):
    return action // board_size, action % board_size


def simulated_step(state, action):
    """Single simulated step which returns a new state object."""
    board = _update_board(
        state.board, action, state.curr_player)
    curr_player = _update_curr_player(state.curr_player)
    valid_actions = _update_valid_actions(
        state.valid_actions, action)
    is_terminal = _is_terminal(valid_actions)
    board_stats = _update_board_stats(
        state.board_stats, action, state.curr_player)
    reward = _get_reward(board_stats, action)
    # Reflecting who won the game.
    reward *= state.curr_player
    is_terminal |= (reward != 0)
    return State(board, curr_player, valid_actions, is_terminal,
                 board_stats, reward)
