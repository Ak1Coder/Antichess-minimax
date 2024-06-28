""" Import copy to help create a deepcopy of the chess board """
import copy

# Importing a class representing a chess board
from antichess.board import Board

# Importing a colour enum class to represent black and white
from antichess.colour import Colour


class Engine:
    """ Class that represents the engine or the opponent the player is playing against """
    board = Board()
    colour = None
    depth = 5
    MAX_EVAL = 64 * 9 # if all board was filled with white queens (the most powerful piece)

    def __init__(self, board, depth, colour_of_engine):
        self.board = copy.deepcopy(board)
        self.depth = depth
        self.colour = Colour.WHITE if colour_of_engine == Colour.WHITE else Colour.BLACK

    def get_best_move(self):
        """ Returns the best found move in the depth = self.depth """
        best_eval = self.MAX_EVAL if self.colour == Colour.WHITE else -self.MAX_EVAL
        best_move = (0, 0, 0, 0)
        what_col = bool(self.colour == Colour.WHITE)
        pieces_coords = self.board.white_pieces_pos if what_col else self.board.black_pieces_pos
        moves_valid= []

        for coords in pieces_coords:
            moves = self.board.current_board[coords].get_moves(*coords, True)
            for move in moves:
                if self.board.is_move_valid((*coords, *move), True):
                    moves_valid.append((*coords, *move))

        if len(moves_valid) == 1:
            return moves_valid[0]

        if len(moves_valid) > 1:
            for move in moves_valid:
                self.board.move(move, True)
                new_eval=self.__minimax(self.depth,(-self.MAX_EVAL,self.MAX_EVAL), False)
                self.board.unmake_last_move()
                if self.colour == Colour.WHITE and new_eval < best_eval:
                    best_eval = new_eval
                    best_move = move
                elif self.colour == Colour.BLACK and new_eval > best_eval:
                    best_eval = new_eval
                    best_move = move

        return best_move

    def __minimax(self, depth, alpha_beta, is_op):
        play_col = Colour.WHITE if self.colour == Colour.BLACK else Colour.BLACK
        colour_to_play = self.colour if is_op else play_col

        if depth == 0 or abs(self.evaluate(colour_to_play)) == self.MAX_EVAL:
            eval_return = self.evaluate(colour_to_play)
            return eval_return

        what_col = colour_to_play == Colour.WHITE
        best_eval = self.MAX_EVAL if what_col else -self.MAX_EVAL
        pieces_coords = self.board.white_pieces_pos if what_col else self.board.black_pieces_pos

        for coords in pieces_coords:
            what_col = colour_to_play == self.colour
            moves = self.board.current_board[coords].get_moves(*coords, what_col)
            for move in moves:
                if self.board.is_move_valid((*coords, *move), is_op):
                    self.board.move((*coords, *move), is_op)
                    new_eval = self.__minimax(depth - 1, alpha_beta, not is_op)
                    self.board.unmake_last_move()
                    if colour_to_play == Colour.WHITE:
                        if new_eval < best_eval:
                            best_eval = new_eval
                        alpha_beta = max(alpha_beta[0], new_eval), alpha_beta[1]
                        if alpha_beta[0] >= alpha_beta[1]:
                            return best_eval
                    else:
                        if new_eval > best_eval:
                            best_eval = new_eval
                        alpha_beta = alpha_beta[0], min(alpha_beta[1], new_eval)
                        if alpha_beta[0] >= alpha_beta[1]:
                            return best_eval

        return best_eval

    def evaluate(self, colour_to_play):
        """ Returns an evaluation of the board = Black -> wants positive, White -> wants negative"""
        evaluation = 0

        if len(self.board.white_pieces_pos) == 0:
            return -self.MAX_EVAL
        if len(self.board.black_pieces_pos) == 0:
            return self.MAX_EVAL
        if self.__check_stalemate(colour_to_play):
            if colour_to_play == Colour.WHITE:
                return -self.MAX_EVAL
            return self.MAX_EVAL

        for coord in self.board.white_pieces_pos:
            evaluation += self.board.current_board[coord].get_value()

        for coord in self.board.black_pieces_pos:
            evaluation -= self.board.current_board[coord].get_value()

        return evaluation

    def __check_stalemate(self, colour):
        if colour == Colour.WHITE:
            is_op = self.colour == Colour.WHITE
            for coords in self.board.white_pieces_pos:
                moves = self.board.current_board[coords].get_moves(*coords, is_op)
                for move in moves:
                    if self.board.is_move_valid((*coords, *move), is_op):
                        return False
            return True

        is_op = self.colour == Colour.BLACK
        for coords in self.board.black_pieces_pos:
            moves = self.board.current_board[coords].get_moves(*coords, is_op)
            for move in moves:
                if self.board.is_move_valid((*coords, *move), is_op):
                    return False
        return True
