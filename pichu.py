#!/usr/bin/env python
# Author: Hardik Rakholiya

import sys

# Heuristic Functions Used are:
# Move Ordering: Give preference to moves where a opponent's piece is captured by a less weighted player's piece
# https://chessprogramming.wikispaces.com/Move+Ordering
#
# Material: give more weight to a state where the combined weight of all pieces of player is more than the combined
# weight of opponent pieces
#
# Mobility: give more weight to a state where center pieces are controlled by the player's pieces
# http://blog.galvanize.com/learn/learn-to-code/chess-ai/
#
# Pawn Structure: give more weight to a state where a parakeet is protected by another parakeet.
# https://chessprogramming.wikispaces.com/Pawn+Structure

white_pieces = ['P', 'R', 'B', 'Q', 'K', 'N']
black_pieces = ['p', 'r', 'b', 'q', 'k', 'n']
single_move_pieces = ['N', 'n', 'K', 'k']


class State:
    def __init__(self, move, player_turn):
        self.move = move
        self.val = 0.0
        self.player_turn = player_turn
        self.successors = []

    def get_successors(self):
        if len(self.successors) == 0:
            moves = possible_moves(player_color if self.player_turn else opponent_color)
            for move in moves:
                self.successors.append(State(move, False if self.player_turn else True))

        return self.successors


class Move:
    def __init__(self):
        self.changes = {}
        self.undo_changes = {}

    def unmake(self):
        for (r, c) in self.changes:
            board[r][c] = self.undo_changes[r, c]

    def make(self):
        for (r, c) in self.changes:
            board[r][c] = self.changes[r, c]

    def add_change(self, r, c, piece):
        self.undo_changes[r, c] = board[r][c]
        self.changes[r, c] = piece


def possible_moves(color):
    moves = []

    if color == 'w':
        for r in range(0, 8):
            for c in range(0, 8):
                if board[r][c] == 'P':
                    wp_moves(moves, r, c)
                elif board[r][c] == 'R':
                    r_moves(moves, color, r, c)
                elif board[r][c] == 'B':
                    b_moves(moves, color, r, c)
                elif board[r][c] == 'N':
                    n_moves(moves, color, r, c)
                elif board[r][c] == 'Q':
                    q_moves(moves, color, r, c)
                elif board[r][c] == 'K':
                    k_moves(moves, color, r, c)

    elif color == 'b':
        for r in range(0, 8):
            for c in range(0, 8):
                if board[r][c] == 'p':
                    bp_moves(moves, r, c)
                elif board[r][c] == 'r':
                    r_moves(moves, color, r, c)
                elif board[r][c] == 'b':
                    b_moves(moves, color, r, c)
                elif board[r][c] == 'n':
                    n_moves(moves, color, r, c)
                elif board[r][c] == 'q':
                    q_moves(moves, color, r, c)
                elif board[r][c] == 'k':
                    k_moves(moves, color, r, c)
    return moves


def wp_moves(moves, r, c):
    r1 = r + 1

    if r1 < 8:
        # killer moves takes priority
        if c + 1 < 8 and board[r1][c + 1] in black_pieces:
            move = Move()
            move.add_change(r1, c + 1, 'Q' if r1 == 7 else 'P')
            move.add_change(r, c, '.')
            moves.insert(0, move)

        # killer moves takes priority
        if c - 1 > -1 and board[r1][c - 1] in black_pieces:
            move = Move()
            move.add_change(r1, c - 1, 'Q' if r1 == 7 else 'P')
            move.add_change(r, c, '.')
            moves.insert(0, move)

        if board[r1][c] == '.':
            move = Move()
            move.add_change(r1, c, 'Q' if r1 == 7 else 'P')
            move.add_change(r, c, '.')
            moves.append(move)

        # first move of the game
        if r == 1 and board[2][c] == '.' and board[3][c] == '.':
            move = Move()
            move.add_change(r + 2, c, 'P')
            move.add_change(r, c, '.')
            moves.append(move)


def bp_moves(moves, r, c):
    r1 = r - 1

    if r1 > -1:
        # killer moves takes priority
        if c + 1 < 8 and board[r1][c + 1] in white_pieces:
            move = Move()
            move.add_change(r1, c + 1, 'q' if r1 == 0 else 'p')
            move.add_change(r, c, '.')
            moves.insert(0, move)

        # killer moves takes priority
        if c - 1 > -1 and board[r1][c - 1] in white_pieces:
            move = Move()
            move.add_change(r1, c - 1, 'q' if r1 == 0 else 'p')
            move.add_change(r, c, '.')
            moves.insert(0, move)

        if board[r1][c] == '.':
            move = Move()
            move.add_change(r1, c, 'q' if r1 == 0 else 'p')
            move.add_change(r, c, '.')
            moves.append(move)

        # first move of the game
        if r == 6 and board[5][c] == '.' and board[4][c] == '.':
            move = Move()
            move.add_change(r - 2, c, 'p')
            move.add_change(r, c, '.')
            moves.append(move)


def r_moves(moves, color, r, c):
    add_move_in_dir(moves, color, r, c, +1, 0)
    add_move_in_dir(moves, color, r, c, -1, 0)
    add_move_in_dir(moves, color, r, c, 0, +1)
    add_move_in_dir(moves, color, r, c, 0, -1)


def b_moves(moves, color, r, c):
    for dr in (-1, 1):
        for dc in (-1, 1):
            add_move_in_dir(moves, color, r, c, dr, dc)


def q_moves(moves, color, r, c):
    r_moves(moves, color, r, c)
    b_moves(moves, color, r, c)


def n_moves(moves, color, r, c):
    for dr in (-2, -1, 1, 2):
        for dc in (-2, -1, 1, 2):
            if abs(dr) + abs(dc) is 3:
                add_move_in_dir(moves, color, r, c, dr, dc)


def k_moves(moves, color, r, c):
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            if abs(dr) + abs(dc) is 1 or 2:
                add_move_in_dir(moves, color, r, c, dr, dc)


def add_move_in_dir(moves, color, r, c, dr, dc, depth=1):
    r1 = r + depth * dr
    c1 = c + depth * dc

    if r1 not in range(0, 8) or c1 not in range(0, 8):
        return

    # player's own piece is blocking the move
    if (board[r1][c1] in white_pieces and color == 'w') or (board[r1][c1] in black_pieces and color == 'b'):
        return

    # attack opponent's piece
    if (board[r1][c1] in black_pieces and color == 'w') or (board[r1][c1] in white_pieces and color == 'b'):
        move = Move()
        move.add_change(r1, c1, board[r][c])
        move.add_change(r, c, '.')
        if abs(pieces_wgt[board[r1][c1]]) > abs(pieces_wgt[board[r][c]]):
            # kill moves first
            moves.insert(0, move)
        else:
            moves.append(move)
        return

    # move to empty tile r1,c1
    if board[r1][c1] == '.':
        move = Move()
        move.add_change(r1, c1, board[r][c])
        move.add_change(r, c, '.')
        moves.append(move)
        if board[r][c] in single_move_pieces:
            return
        else:
            add_move_in_dir(moves, color, r, c, dr, dc, depth + 1)


material_wgt = 10
pawn_structure_wgt = 1
mobility_wgt = 5


def evaluate(state):
    return material_wgt * material() + pawn_structure_wgt * pawn_structure(state) \
           + mobility_wgt * mobility(state)


# based on values at https://en.wikipedia.org/wiki/Chess_piece_relative_value
pieces_wgt = {'P': +1.0, 'B': +3.5, 'N': +3.5, 'R': +5.25, 'Q': +10.0, 'K': +200.0,
              'p': -1.0, 'b': -3.5, 'n': -3.5, 'r': -5.25, 'q': -10.0, 'k': -200.0}


def material():
    white_pts = 0
    for row in board:
        for piece in row:
            if piece != '.':
                white_pts += pieces_wgt.get(piece)

    return white_pts if player_color == 'w' else -1 * white_pts


square_values = {
    (2, 1): 0.25, (2, 2): 0.5, (2, 3): 0.5, (2, 4): 0.5, (2, 5): 0.5, (2, 6): 0.25,
    (3, 1): 0.25, (3, 2): 0.5, (3, 3): 1.0, (3, 4): 1.0, (3, 5): 0.5, (3, 6): 0.25,
    (4, 1): 0.25, (4, 2): 0.5, (4, 3): 1.0, (4, 4): 1.0, (4, 5): 0.5, (4, 6): 0.25,
    (5, 1): 0.25, (5, 2): 0.5, (5, 3): 0.5, (5, 4): 0.5, (5, 5): 0.5, (5, 6): 0.25,
}


def mobility(state):
    m = 0.0
    for next in state.get_successors():
        for key in next.move.changes:
            if next.move.changes[key] not in ['.', 'K', 'k'] and key in square_values:
                m += square_values[key]

    return m if state.player_turn else -1 * m


def pawn_structure(state):
    pts = 0.0
    if state.player_turn:
        if player_color == 'w':
            for r in range(0, 8):
                for c in range(0, 8):
                    if board[r][c] == 'P':
                        ur = r - 1
                        lc = c - 1
                        rc = c + 1
                        if ur in range(0, 8) and lc in range(0, 8) and board[ur][lc] == 'P':
                            pts += 1
                        if ur in range(0, 8) and rc in range(0, 8) and board[ur][rc] == 'P':
                            pts += 1

        else:
            for r in range(0, 8):
                for c in range(0, 8):
                    if board[r][c] == 'p':
                        dr = r + 1
                        lc = c - 1
                        rc = c + 1
                        if dr in range(0, 8) and lc in range(0, 8) and board[dr][lc] == 'p':
                            pts += 1
                        if dr in range(0, 8) and rc in range(0, 8) and board[dr][rc] == 'p':
                            pts += 1

    return pts


def is_game_over(state):
    if state.move is not None:
        for key in state.move.undo_changes:
            if state.move.undo_changes[key] == 'K' and state.move.changes[key] in black_pieces:
                return True
            elif state.move.undo_changes[key] == 'k' and state.move.changes[key] in white_pieces:
                return True
    return False


def alphabeta(state, depth, alpha=-float('inf'), beta=+float('inf')):
    if depth == 0 or is_game_over(state):
        state.val = evaluate(state)
        return state.val
    if state.player_turn:
        state.val = -float('inf')
        for next_state in state.get_successors():

            # https://chessprogramming.wikispaces.com/Unmake+Move
            next_state.move.make()
            state.val = max(state.val, alphabeta(next_state, depth - 1, alpha, beta))
            next_state.move.unmake()
            alpha = max(alpha, state.val)
            if beta <= alpha:
                break
        return state.val
    else:
        state.val = +float('inf')
        for next_state in state.get_successors():
            next_state.move.make()
            state.val = min(state.val, alphabeta(next_state, depth - 1, alpha, beta))
            next_state.move.unmake()
            beta = min(beta, state.val)
            if beta <= alpha:
                break
        return state.val


def get_2d_board(strBoard):
    tiles = []
    for r in range(0, 8):
        row = []
        for c in range(0, 8):
            row.append(strBoard[r * 8 + c])
        tiles.append(row)

    return tiles


def printout():
    string = ''
    for r in range(0, 8):
        for c in range(0, 8):
            string += board[r][c]

    print string


piece_symbols = {'P': u'\u2659',
                 'R': u'\u2656',
                 'B': u'\u2657',
                 'Q': u'\u2655',
                 'K': u'\u2654',
                 'N': u'\u2658',
                 'p': u'\u265F',
                 'r': u'\u265C',
                 'b': u'\u265D',
                 'q': u'\u265B',
                 'k': u'\u265A',
                 'n': u'\u265E',
                 '.': u'\u25A2'
                 }


def view():
    string = ''
    for r in range(0, 8):
        string += str(r)
        for c in range(0, 8):
            string += ' ' + piece_symbols[board[r][c]]
        string += '\n'

    print string


# get the file path from script parameters
player_color = sys.argv[1]
opponent_color = 'b' if player_color == 'w' else 'w'
board = get_2d_board(sys.argv[2])
current = State(None, True)

# board = get_2d_board('........'
#                      '........'
#                      'R..P....'
#                      'p.k.....'
#                      '........'
#                      '........'
#                      '........'
#                      'k.r.....')

for d in range(2, 102):
    score = alphabeta(current, d)
    for next_state in current.get_successors():
        if next_state.val == current.val:
            next_state.move.make()
            printout()
            next_state.move.unmake()
            break
