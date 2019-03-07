import argparse
import random

from board import Board
from uct import uct_search


parser = argparse.ArgumentParser(description='Configuration.')
parser.add_argument('-m', '--mode', default='human', type=str,
                    help='Play vs human or computer.')
parser.add_argument('-b', '--board', default=3, type=int,
                    help='Board size.')
parser.add_argument('-s', '--simulations', default=100, type=int,
                    help='Number of simulations to run for UCT.')


def get_human_move(board, player):
    while True:
        print('Player controlling {}, enter your move.'.format(
              board.get_piece(player)))
        move = int(input())
        if not board.is_valid_action(move):
            print('Invalid move. Try again.')
            continue
        return move


def get_computer_move(state, num_simulations):
    print('Calculating move.')
    move = uct_search(state, num_simulations)
    return move


def make_move(state, board, turn, num_simulations):
    game_ended = False
    player = state.curr_player
    if 'P' in turn:
        move = get_human_move(board, player)
    else:
        move = get_computer_move(state, num_simulations)
    state = board.step(move, render=True)
    if state.reward != 0:
        print('Player controlling {} wins!'.format(
              board.get_piece(player)))
        game_ended = True
    return state, game_ended


def game(mode, board_size, num_simulations):
    board = Board(board_size)
    print(board)
    state = board.get_state()
    players = ['P1', 'P2'] if mode == 'human' else ['P1', 'AI']
    goes_first = random.choice(players)
    goes_second = [player for player in players if player != goes_first][0]
    while not state.is_terminal:
        state, game_ended = make_move(
            state, board, goes_first, num_simulations)
        if game_ended:
            return
        if state.is_terminal:
            continue
        state, game_ended = make_move(
            state, board, goes_second, num_simulations)
        if game_ended:
            return
    print('Game ended in a draw.')


if __name__ == '__main__':
    args = parser.parse_args()
    game(args.mode, args.board, args.simulations)
