""" Importing pygame for displaying the board and the moves """
import pygame

# Importing numpy for arrays to represent the board
import numpy as np

# Importing colour for white and black
from antichess.colour import Colour

# Importing all pieces as objects that are on the board
from antichess.pieces import Pawn, Bishop, Knight, Rook, Queen, King

class Board:
    """ Class representing a chess board """
    current_board = np.full((8, 8), None)
    colour = Colour.WHITE
    moves_played = []
    pieces_taken = []
    white_pieces_pos = set({})
    black_pieces_pos = set({})
    promotion_index = 0
    # promotion_index mod 5 -> 0 = rook, 1 = knight, 2 = bishop, 3 = queen, 4 = king

    def __init__(self, colour = Colour.WHITE,
    starting_position = "rnbqkbnr/pppppppp/00000000/00000000/00000000/00000000/PPPPPPPP/RNBQKBNR"):
        """
            Notation for a starting position follows these rules: 

            - We have a 8x8 chess board so it's a string of 8 lines
              separated by '/', where the first line corresponds to the
              top row of the chessboard and the eight one to the bottom of the chessboard
            - For a row in the notation we are going from left to right on the board's row
            - '0' corresponds to an empty square
            - Other letters correspond to chess pieces
                - Upper means a piece of a player's colour
                - Lower means a piece of the other colour

                - R/r means Rook
                - N/n means Knight
                - B/b means Bishop
                - Q/q means Queen
                - K/k means King
                - P/p means Pawn
        """
        self.colour = Colour.WHITE if colour == Colour.WHITE else Colour.BLACK
        player_col = self.colour
        opponent_col = Colour.BLACK if player_col == Colour.WHITE else Colour.WHITE
        self.white_pieces_pos = set({})
        self.black_pieces_pos = set({})

        start_pos_rows = starting_position.split('/')
        pieces = {
          'R' : Rook(player_col),
          'N' : Knight(player_col),
          'B' : Bishop(player_col),
          'Q' : Queen(player_col),
          'K' : King(player_col),
          'P' : Pawn(player_col),

          'r' : Rook(opponent_col),
          'n' : Knight(opponent_col),
          'b' : Bishop(opponent_col),
          'q' : Queen(opponent_col),
          'k' : King(opponent_col),
          'p' : Pawn(opponent_col),
        }

        for row_num, row_pos in enumerate(start_pos_rows):
            for col_num, piece in enumerate(row_pos):
                if piece.upper() in ['R', 'N', 'B', 'Q', 'K', 'P']:
                    piece_to_insert = pieces[piece]
                    if piece_to_insert is not False:
                        self.current_board[row_num, col_num] = piece_to_insert.copy()
                else:
                    self.current_board[row_num, col_num] = False

        for i in range(0, 8):
            for j in range(0, 8):
                piece = self.current_board[i, j]
                if piece is not False:
                    if piece.colour == Colour.WHITE:
                        self.white_pieces_pos.add((i, j))
                    elif piece.colour == Colour.BLACK:
                        self.black_pieces_pos.add((i, j))

    def move (self, move, is_opponent = False):
        """ Makes a move on the board """
        x_from, y_from, x_to, y_to = move
        if x_from == -1:
            self.moves_played.append((x_from, y_from, x_to, y_to))
            self.pieces_taken.append(self.current_board[x_to, y_to])
            prom_ind = self.promotion_index % 5

            op_col, player_col = (Colour.BLACK if self.colour == Colour.WHITE else Colour.WHITE,
                                   self.colour)

            if prom_ind == 0:
                self.current_board[x_to, y_to]=Rook(op_col if is_opponent is True else player_col)
            elif prom_ind == 1:
                self.current_board[x_to, y_to]=Knight(op_col if is_opponent is True else player_col)
            elif prom_ind == 2:
                self.current_board[x_to, y_to]=Bishop(op_col if is_opponent is True else player_col)
            elif prom_ind == 3:
                self.current_board[x_to, y_to]=Queen(op_col if is_opponent is True else player_col)
            else:
                self.current_board[x_to, y_to]=King(op_col if is_opponent is True else player_col)

            self.promotion_index += 1
            return True

        if self.is_move_valid((x_from, y_from, x_to, y_to), is_opponent):
            self.moves_played.append((x_from, y_from, x_to, y_to))
            taken_piece = self.current_board[x_to, y_to]
            self.pieces_taken.append(taken_piece)

            self.black_pieces_pos.discard((x_to, y_to))
            self.white_pieces_pos.discard((x_to, y_to))

            if (x_from, y_from) in self.white_pieces_pos:
                self.white_pieces_pos.discard((x_from, y_from))
                self.white_pieces_pos.add((x_to, y_to))
            else:
                self.black_pieces_pos.discard((x_from, y_from))
                self.black_pieces_pos.add((x_to, y_to))

            self.current_board[x_to, y_to] = self.current_board[x_from, y_from]
            self.current_board[x_from, y_from] = False

            if x_to in [0, 7] and isinstance(self.current_board[x_to, y_to], Pawn):
                self.__promotion(x_to, y_to, is_opponent)

            return True

        return False

    def unmake_last_move(self):
        """ Unmakes the last move that happened """
        if len(self.moves_played) == 0:
            return False

        move_to_undo = self.moves_played.pop()
        piece_to_return = self.pieces_taken.pop()

        if move_to_undo[0] == -1:
            self.current_board[move_to_undo[2], move_to_undo[3]] = piece_to_return
            self.unmake_last_move()
            self.promotion_index -= 1

            return True

        if (move_to_undo[2], move_to_undo[3]) in self.black_pieces_pos:
            self.black_pieces_pos.add((move_to_undo[0], move_to_undo[1]))
            self.black_pieces_pos.remove((move_to_undo[2], move_to_undo[3]))
        else:
            self.white_pieces_pos.add((move_to_undo[0], move_to_undo[1]))
            self.white_pieces_pos.remove((move_to_undo[2], move_to_undo[3]))

        if piece_to_return is not False:
            if piece_to_return.colour == Colour.WHITE:
                self.white_pieces_pos.add((move_to_undo[2], move_to_undo[3]))
            else:
                self.black_pieces_pos.add((move_to_undo[2], move_to_undo[3]))

        self.current_board[move_to_undo[0], move_to_undo[1]] = (
            self.current_board[move_to_undo[2], move_to_undo[3]])
        self.current_board[move_to_undo[2], move_to_undo[3]] = piece_to_return

        return True

    def display_board(self, window):
        """ Displays the board in the pygame window """
        width, height = window.get_size()
        board_center_position = (width / 2, height / 2)
        size_of_board = self.get_size_of_board(window)

        tile_x, tile_y = (board_center_position[0] - size_of_board / 2,
                           board_center_position[1] - size_of_board / 2)
        tile_size = size_of_board / 8

        for row in range(0, 8):
            for col in range(0, 8):
                pygame.draw.rect(
                    window, ((155,76,20)) if ((row * (8 + 1) + col) % 2 == 1) else ((255,240,200)),
                      (tile_x, tile_y, tile_size, tile_size))
                if self.current_board[row, col] is not False:
                    coords = self.get_coords(window, col, row)
                    self.current_board[row, col].display_piece(window, tile_size, *coords)
                tile_x += tile_size
            tile_y += tile_size
            tile_x -= 8 * tile_size

    def display_moves(self, window, x_coord, y_coord, is_opponent):
        """ Displays the moves of a piece on (x, y) """
        if self.current_board[x_coord, y_coord] is False:
            return []
        all_moves = self.current_board[x_coord, y_coord].get_moves(x_coord, y_coord, is_opponent)

        moves_to_display = []
        for move in all_moves:
            if self.is_move_valid((x_coord, y_coord, *move), is_opponent):
                moves_to_display.append(move)

        for move in moves_to_display:
            coords = self.get_coords(window, move[1], move[0])
            self.highlight_tile(window, *coords, (255, 0, 0, 90))

        return moves_to_display

    def get_coords(self, window, x_coord, y_coord):
        """ Returns the coords in px for a tile on (x, y) """
        width, height = window.get_size()
        board_center_position = (width / 2, height / 2)
        tile_size = self.get_tile_size(window)
        left_corner_tile_x, left_corner_tile_y = (board_center_position[0] - 4 * tile_size,
                                                  board_center_position[1] - 4 * tile_size)
        return (left_corner_tile_x + x_coord * tile_size + tile_size / 2,
                 left_corner_tile_y + y_coord * tile_size + tile_size / 2)

    def get_size_of_board(self, window):
        """ Returns a size of a side of a chess board """
        width, height = window.get_size()
        return 0.9 * width if width < height else 0.9 * height

    def get_tile_size(self, window):
        """ Returns a size of a square representing a chess tile """
        return self.get_size_of_board(window) / 8

    def get_tile_based_on_click(self, window, x_coord, y_coord):
        """ Gets coords of a tile based on x,y coords on the window """
        width, height = window.get_size()
        board_center_position = (width / 2, height / 2)
        size_of_board = self.get_size_of_board(window)
        tile_x, tile_y = (board_center_position[0] - size_of_board / 2,
                           board_center_position[1] - size_of_board / 2)
        tile_size = size_of_board / 8
        return (int((y_coord - tile_y) // tile_size), int((x_coord - tile_x) // tile_size))

    def __check_pawn(self, move, is_opponent):
        x_from, y_from, x_to, y_to = move
        if y_to not in {y_from + 1,  y_from - 1,  y_from}:
            return False
        if is_opponent is True:
            if abs(x_to - x_from) == 1 or (abs(x_to - x_from) == 2 and x_from == 1):
                return True
        if is_opponent is False:
            if abs(x_to - x_from) == 1 or (abs(x_to - x_from) == 2 and x_from == 6):
                return True
        return False

    def __check_bishop(self, move):
        x_from, y_from, x_to, y_to = move
        for inc in range(1, 8):
            x_inc, y_inc = (inc * (1 if x_to > x_from else -1),
                            inc * (1 if y_to > y_from else -1))
            if (self.is_in_bounds(x_from + x_inc, y_from + y_inc) is False
                or (x_from + x_inc == x_to and y_from + y_inc == y_to)):
                return True
            if self.current_board[x_from + x_inc, y_from + y_inc] is not False:
                return False
        return True

    def __check_rook(self, move):
        x_from, y_from, x_to, y_to = move
        x_inc_q = 1 if x_to > x_from else (0 if x_to == x_from else -1)
        y_inc_q = 1 if y_to > y_from else (0 if y_to == y_from else -1)
        for inc in range (1, 8):
            x_inc, y_inc = inc * x_inc_q, inc * y_inc_q
            if (self.is_in_bounds(x_from + x_inc, y_from + y_inc) is False
                or (x_from + x_inc == x_to and y_from + y_inc == y_to)):
                return True
            if self.current_board[x_from + x_inc, y_from + y_inc] is not False:
                return False
        return True

    def __check_queen(self, move):
        x_from, y_from, x_to, y_to = move
        if x_to == x_from or y_to == y_from:
            x_inc_q = 1 if x_to > x_from else (0 if x_to == x_from else -1)
            y_inc_q = 1 if y_to > y_from else (0 if y_to == y_from else -1)
            for inc in range (1, 8):
                x_inc, y_inc = inc * x_inc_q, inc * y_inc_q
                if (self.is_in_bounds(x_from + x_inc, y_from + y_inc) is False
                    or (x_from + x_inc == x_to and y_from + y_inc == y_to)):
                    return True
                if self.current_board[x_from + x_inc, y_from + y_inc] is not False:
                    return False
        else:
            for inc in range(1, 8):
                x_inc, y_inc = (inc * (1 if x_to > x_from else -1),
                                inc * (1 if y_to > y_from else -1))
                if (self.is_in_bounds(x_from + x_inc, y_from + y_inc) is False
                    or (x_from + x_inc == x_to and y_from + y_inc == y_to)):
                    return True
                if self.current_board[x_from + x_inc, y_from + y_inc] is not False:
                    return False
        return True

    def is_move_valid(self, move, is_opponent):
        """ Checks if the move is valid returns True/False"""
        x_from, y_from, x_to, y_to = move
        is_move_valid = False

        if ((not (self.is_in_bounds(x_from, y_from)
                  and self.is_in_bounds(x_to, y_to)))
                  or (x_from == x_to and y_from == y_to)
                  or (self.current_board[x_from, y_from] is False)):
            return False

        if isinstance(self.current_board[x_from, y_from], Pawn):
            is_move_valid = self.__check_pawn(move, is_opponent)
        elif isinstance(self.current_board[x_from, y_from], Bishop):
            is_move_valid = self.__check_bishop(move)
        elif isinstance(self.current_board[x_from, y_from], Rook):
            is_move_valid = self.__check_rook(move)
        elif isinstance(self.current_board[x_from, y_from], Queen):
            is_move_valid = self.__check_queen(move)
        else:
            is_move_valid = True

        if is_move_valid is False:
            return False

        ret_val = True
        if (self.current_board[x_to, y_to] is not False
            and self.current_board[x_to, y_to].colour != self.current_board[x_from, y_from].colour):
            if isinstance(self.current_board[x_from, y_from], Pawn) and y_to == y_from:
                ret_val = False
            return ret_val

        if self.current_board[x_to, y_to] is False:
            if isinstance(self.current_board[x_from, y_from], Pawn):
                if ((y_to != y_from) or abs(x_from - x_to) == 2
                    and (self.current_board[int((x_from + x_to) / 2), y_to] is not False)):
                    return False
            return not self.can_take(self.current_board[x_from, y_from].colour, is_opponent)

        return False

    def can_take(self, colour, is_opponent):
        """ Checks if any piece of colour can capture anything """
        coords_col = self.white_pieces_pos if colour == Colour.WHITE else self.black_pieces_pos
        for coords in coords_col:
            moves = self.current_board[coords].get_moves(*coords, is_opponent)
            for move in moves:
                if (self.current_board[move] is not False
                    and self.current_board[move].colour != colour):
                    if self.is_move_valid((*coords, *move), is_opponent):
                        return True
        return False

    def is_in_bounds(self, x_coord, y_coord):
        """ Returns True if the x, y coords are inside a 8x8 board"""
        return 0 <= x_coord <= 7 and 0 <= y_coord <= 7

    def __promotion(self, x_coord, y_coord, is_opponent = False):
        """ Private method used when promotion is happening """
        return self.move((-1,-1, x_coord, y_coord), is_opponent)

    def highlight_tile(self, window, x_coord, y_coord, colour):
        """ Highlights the tile on board at x_coord, y_coord"""
        if self.is_in_bounds(*self.get_tile_based_on_click(window, x_coord, y_coord)) is False:
            return
        tile_size = self.get_tile_size(window)  * 1.02
        tile_surface = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
        tile_surface.fill(colour)
        window.blit(tile_surface, (x_coord - tile_size/ 2, y_coord - tile_size / 2))
