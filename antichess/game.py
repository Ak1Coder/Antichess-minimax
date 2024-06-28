""" Import pygame to draw the game on the window """
import pygame

# Import board that the game is played on
from antichess.board import Board

# Import colour to represent black and white
from antichess.colour import Colour

# Import engine to be the enemy a player plays against
from antichess.engine import Engine

class Game:
    """ Class representing a current game that is being played """
    window = None
    player_colour = Colour.WHITE
    board = Board(player_colour)
    depth = 1
    app_is_running = False

    def __init__(self, window, colour = Colour.WHITE, depth = 1,
                start_pos =
                "rnbqkbnr/pppppppp/00000000/00000000/00000000/00000000/PPPPPPPP/RNBQKBNR"):
        self.window = window
        self.player_colour = Colour.WHITE if colour == Colour.WHITE else Colour.BLACK
        self.board = Board(self.player_colour, start_pos)
        self.depth = depth

    def start_game(self):
        """ Starts the game loop """
        self.app_is_running, moves_displayed, already_checked, player_move = (
            True, False, False, bool(self.player_colour == Colour.WHITE))
        displayed_moves = []
        played_move, current_piece = (0,0,0,0), (0,0)

        self.window.fill((238,238,228))
        self.board.display_board(self.window)
        pygame.display.flip()

        while self.app_is_running:
            if player_move is False:
                played_move = Engine(self.board,
                                   self.depth,
                                   Colour.WHITE if (
                                       self.player_colour != Colour.WHITE
                                       ) else Colour.BLACK
                                  ).get_best_move()
                self.board.move(played_move, True)
                self.board.highlight_tile(self.window, played_move[0],
                                           played_move[1], (0, 0, 255, 90))
                self.board.highlight_tile(self.window, played_move[2],
                                           played_move[3], (0, 0, 255, 90))
                player_move, already_checked = True, False

                self.window.fill((238,238,228))
                self.board.display_board(self.window)

            if already_checked is False and self.check_win(player_move) != "":
                pygame.display.flip()
                return self.check_win(player_move)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.app_is_running = False
                    return "QUIT"
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    x_min = (self.board.get_coords(self.window, 0, 0)[0]
                             - self.board.get_tile_size(self.window) / 2)
                    y_min = (self.board.get_coords(self.window, 0, 0)[1]
                            - self.board.get_tile_size(self.window) / 2)
                    x_max = x_min + self.board.get_size_of_board(self.window)
                    y_max = y_min + self.board.get_size_of_board(self.window)
                    current_click = self.board.get_tile_based_on_click(self.window, *pos)

                    if moves_displayed and current_click in displayed_moves:
                        if self.board.move((*current_piece, *current_click)):
                            played_move = (*current_piece, *current_click)
                            player_move = False
                            already_checked, moves_displayed = False, False
                            displayed_moves = []
                            continue

                    in_bounds = (
                        pos[0] >= x_min and pos[1] >= y_min
                        ) and (
                        pos[0] <= x_max and pos[1] <= y_max
                        )
                    if in_bounds is True:
                        current_piece = self.board.get_tile_based_on_click(self.window, *pos)

                    moves_displayed = bool(
                        in_bounds and self.board.current_board[current_piece] is not False
                        and self.board.current_board[current_piece].colour == self.player_colour)
                    displayed_moves= self.board.display_moves(
                        self.window, *current_piece, False
                        ) if moves_displayed else []

            self.window.fill((238,238,228))
            self.board.display_board(self.window)

            if played_move != (0,0,0,0) :
                self.board.highlight_tile(self.window,
                    *self.board.get_coords(self.window, played_move[1], played_move[0]),
                    (0, 0, 255, 40))
                self.board.highlight_tile(self.window,
                    *self.board.get_coords(self.window, played_move[3], played_move[2]),
                    (0, 0, 255, 40))

            if moves_displayed:
                displayed_moves = self.board.display_moves(
                    self.window,*current_piece, False)

            pygame.display.flip()

            if already_checked is False and self.check_win(player_move) != "":
                return self.check_win(player_move)

            already_checked = True
            pygame.time.Clock().tick(24)

    def check_win(self, player_move):
        """ Returns True if someone already won the game otherwise False """
        white_to_move = True
        if player_move:
            white_to_move = bool(self.player_colour == Colour.WHITE)
        else:
            white_to_move = bool(self.player_colour != Colour.WHITE)

        if len(self.board.white_pieces_pos) == 0:
            return "WHITE WON"
        if len(self.board.black_pieces_pos) == 0:
            return "BLACK WON"
        if self.check_stalemate(Colour.WHITE) and white_to_move:
            return "WHITE WON BY STALEMATE"
        if self.check_stalemate(Colour.BLACK) and not white_to_move:
            return "BLACK WON BY STALEMATE"

        return ""

    def someone_ran_out_of_pieces(self):
        """Return True if someone ran out of pieces if not returns False"""
        return len(self.board.black_pieces_pos) == 0 or len(self.board.white_pieces_pos) == 0

    def check_stalemate(self, colour):
        """ Returns True if a side of colour cannot make any legal moves and still has pieces """
        if colour == Colour.WHITE:
            for coords in self.board.white_pieces_pos:
                is_op = self.player_colour != Colour.WHITE
                moves = self.board.current_board[coords].get_moves(*coords, is_op)
                for move in moves:
                    if self.board.is_move_valid((*coords, *move), is_op):
                        return False
            return not self.someone_ran_out_of_pieces()

        for coords in self.board.black_pieces_pos:
            is_op = self.player_colour == Colour.WHITE
            moves = self.board.current_board[coords].get_moves(*coords, is_op)
            for move in moves:
                if self.board.is_move_valid((*coords, *move), is_op):
                    return False
        return not self.someone_ran_out_of_pieces()
