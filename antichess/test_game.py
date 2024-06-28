""" Import pytest to create tests """
import pytest
import pygame
from antichess.game import Game
from antichess.colour import Colour

@pytest.mark.parametrize(
    'colour, start_pos, is_player_playing, has_winner',
    [
        (Colour.WHITE,
         "rnbqkbnr/pppppppp/00000000/00000000/00000000/00000000/PPPPPPPP/RNBQKBNR",
         True, ""),
        (Colour.WHITE,
         "rnbqkbnr/pppppppp/00000000/kkkkkkkk/qqQQqqQQ/00000000/PPP000PP/RNBQKBNR",
         False, ""),
        (Colour.WHITE,
         "00k00000/p0pppppp/00000000/00000000/00000000/00000000/00000000/00000000",
         False, "WHITE WON"),
        (Colour.WHITE,
         "rnbqkbnr/pppppppp/00000000/00000000/00000000/00000000/PPPPPPPP/RNBQKBNR",
         True, ""),
        (Colour.BLACK,
         "00000qqq/pppprrbk/00bbbb00/00000000/00000000/00000000/00000000/00000000",
         False, "BLACK WON"),
        (Colour.BLACK,
         "0000P0P0/K0000000/00000000/00000000/000000P0/00000Pp0/00000pP0/00000K0n",
         False, "WHITE WON BY STALEMATE"),
        (Colour.BLACK,
         "00000qqq/p0pprrbk/P0bb0b00/00000000/00000000/00000000/00000000/00000000",
         True, "BLACK WON BY STALEMATE"),
    ])
def test_check_win(colour, start_pos, is_player_playing, has_winner):
    """ Tests the check_win() method of Game """
    test_game = Game(pygame.display, colour, 1, start_pos)

    assert test_game.check_win(is_player_playing) == has_winner


@pytest.mark.parametrize(
    'colour, start_pos, someone_ran_out',
    [
        (Colour.WHITE,
         "rnbqkbnr/pppppppp/00000000/00000000/00000000/00000000/rnbqkbnr/rnbqkbnr", True),
        (Colour.WHITE,
         "rnbqkbnr/pppppppp/00000000/kkkkkkkk/qqQQqqQQ/00000000/PPP000PP/RNBQKBNR", False),
        (Colour.BLACK,
         "00000qqq/pppprrbk/00bbbb00/00000000/00000000/00000000/00000000/00000000", True),
        (Colour.BLACK,
         "0000P0P0/K0000000/00000000/00000000/000000P0/00000Pp0/00000pP0/00000K0n", False),
    ])
def test_someone_ran_out_of_pieces(colour, start_pos, someone_ran_out):
    """ Tests the someone_ran_out_of_pieces() method of Game """
    test_game = Game(pygame.display, colour, 1, start_pos)
    assert test_game.someone_ran_out_of_pieces() == someone_ran_out


@pytest.mark.parametrize(
    'colour, start_pos, colour_to_check, is_stalemate',
    [
        (Colour.WHITE,
         "rnbqkbnr/pppppppp/0p0000p0/0Pp00pP0/00P00P00/N0p00000/0pP00000/0P000000",
         Colour.WHITE, True),
        (Colour.WHITE,
         "rnbqkbnr/pppppppp/0p0000p0/0Pp00pP0/00P00P00/N0p00000/0pP00000/0P000000",
         Colour.BLACK, False),
        (Colour.WHITE,
         "0p000000/0P000000/00000000/00000K00/00000000/00000000/00000000/00000000",
         Colour.WHITE, False),
        (Colour.WHITE,
         "0p000000/0P000000/00000000/00000000/p0p00000/P0P00000/00000000/00000000",
         Colour.BLACK, True),
        (Colour.BLACK,
         "00000000/0000000p/0000000P/00000000/00000000/00000000/KKR00000/00000000",
         Colour.WHITE, True),
        (Colour.BLACK,
         "00000000/0000000p/0000000P/00000000/00000000/00000000/KKR00000/00000000",
         Colour.BLACK, False),
        (Colour.BLACK,
         "rnbqkbnr/pppppppp/00000000/00000000/00000000/00000000/PPPPPPPP/RNBQKBNR",
         Colour.WHITE, False),
        (Colour.BLACK,
         "rnbqkbnr/pppppppp/00000000/00000000/00000000/00000000/PPPPPPPP/RNBQKBNR",
         Colour.BLACK, False),
    ])
def test_stalemate(colour, start_pos, colour_to_check, is_stalemate):
    """ Tests the check_stalemate() method of Game """
    test_game = Game(pygame.display, colour, 1, start_pos)
    assert test_game.check_stalemate(colour_to_check) == is_stalemate
