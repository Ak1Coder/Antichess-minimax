""" Importing ABC and abstractmethod to create abstract Piece class """
from abc import ABC, abstractmethod

# Importing pygame for drawing the pieces on the app window
import pygame

# Importing enum class which contains colours BLACK and WHITE
from antichess.colour import Colour

PATH = "antichess/images/"

class Piece(ABC):
    """ Abstract class representing a chess piece"""
    colour = None
    image_white = None
    image_black = None

    def __init__(self, colour):
        self.colour = Colour.WHITE if colour == Colour.WHITE else Colour.BLACK

    @abstractmethod
    def get_moves(self, x_coord, y_coord, is_opponent = False):
        """ Returns all possible moves of a piece that are in range of a 8x8 chess board """

    def is_in_range(self, x_coord, y_coord):
        """ Checks if the coordinates are in range of 8x8 chess board """
        return 0 <= x_coord <= 7 and 0 <= y_coord <= 7

    def copy(self):
        """ Returns a copy of a piece with the same colour """
        return type(self)(self.colour)

    def display_piece(self, window, piece_size, x_coord, y_coord):
        """ Displays the piece on the window in row = x_coord, column = y_coord """
        image_address = self.image_white if self.colour == Colour.WHITE else self.image_black
        pawn_picture = pygame.image.load(image_address)
        pawn_picture = pygame.transform.scale(pawn_picture, (piece_size, piece_size))
        window.blit(pawn_picture, (x_coord - piece_size / 2, y_coord - piece_size / 2))

class Pawn(Piece):
    """ Class representing a pawn """
    image_white = PATH + "pawn_white.png"
    image_black = PATH + "pawn_black.png"

    def get_moves(self, x_coord, y_coord, is_opponent = False):
        direction = 1 if is_opponent is True else -1
        all_moves = [
            (x_coord + 2 * direction, y_coord),
            (x_coord + direction, y_coord),
            (x_coord + direction, y_coord + direction),
            (x_coord + direction, y_coord - direction)
            ]
        return [move for move in all_moves if self.is_in_range(*move)]

    def get_value(self):
        """ Method returning the value of pawn used when evaluating the position """
        return 1

class Bishop(Piece):
    """ Class representing a bishop """
    image_white = PATH + "bishop_white.png"
    image_black = PATH + "bishop_black.png"

    def get_moves(self, x_coord, y_coord, is_opponent = False):
        all_moves = []

        for inc in range (1,8):
            all_moves += [
              (x_coord + inc, y_coord + inc),
              (x_coord - inc, y_coord - inc),
              (x_coord + inc, y_coord - inc),
              (x_coord - inc, y_coord + inc)
              ]

        return [move for move in all_moves if self.is_in_range(*move)]

    def get_value(self):
        """ Method returning the value of bishop used when evaluating the position """
        return 3

class Knight(Piece):
    """ Class representing a knight """
    image_white = PATH + "knight_white.png"
    image_black = PATH + "knight_black.png"

    def get_moves(self, x_coord, y_coord, is_opponent = False):
        all_moves = []

        for nums in [(2, 1), (1, 2)]:
            for first_sign in [1, -1]:
                for second_sign in [1, -1]:
                    all_moves.append(
                        (x_coord + nums[0] * first_sign, y_coord + nums[1] * second_sign)
                        )

        return [move for move in all_moves if self.is_in_range(*move)]

    def get_value(self):
        """ Method returning the value of knight used when evaluating the position """
        return 3

class Rook(Piece):
    """ Class representing a rook """
    image_white = PATH + "rook_white.png"
    image_black = PATH + "rook_black.png"

    def get_moves(self, x_coord, y_coord, is_opponent = False):
        all_moves = []

        for inc in range (1, 8):
            for sign in [1, -1]:
                all_moves.append((x_coord + inc * sign, y_coord))
                all_moves.append((x_coord, y_coord + inc * sign))

        return [move for move in all_moves if self.is_in_range(*move)]

    def get_value(self):
        """ Method returning the value of rook used when evaluating the position """
        return 5

class Queen(Piece):
    """ Class representing a queen """
    image_white = PATH + "queen_white.png"
    image_black = PATH + "queen_black.png"

    def get_moves(self, x_coord, y_coord, is_opponent = False):
        bishop = Bishop(self.colour)
        rook = Rook(self.colour)
        return bishop.get_moves(x_coord, y_coord) + rook.get_moves(x_coord, y_coord)

    def get_value(self):
        """ Method returning the value of queen used when evaluating the position """
        return 9

class King(Piece):
    """ Class representing a king """
    image_white = PATH + "king_white.png"
    image_black = PATH + "king_black.png"

    def get_moves(self, x_coord, y_coord, is_opponent = False):
        all_moves = []

        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == j == 0:
                    continue
                all_moves.append((x_coord + i, y_coord + j))

        return [move for move in all_moves if self.is_in_range(*move)]

    def get_value(self):
        """ Method returning the value of king used when evaluating the position """
        return 3
