""" Import pytest to create tests for antichess """
import pytest
from antichess.engine import Engine
from antichess.colour import Colour
from antichess.board import Board

MAX_EVAL = 64 * 9

@pytest.mark.parametrize(
    'colour, start_pos, colour_to_play, real_evaluation',
    [
        # Colour of player, position to begin, colour to play
        (Colour.WHITE,
         "rnbqkbnr/pppppppp/00000000/00000000/00000000/00000000/PPPPPPPP/RNBQKBNR",
         Colour.WHITE, 0),
        (Colour.WHITE,
         "rnbqkbnr/pppppppp/00000000/00000000/00000000/00000000/00000000/00000000",
         Colour.WHITE, -MAX_EVAL),
        (Colour.WHITE,
         "rnbqkbnr/pppppppp/00000000/00000000/00000000/00000000/00000000/00000000",
         Colour.BLACK, -MAX_EVAL),
        (Colour.WHITE,
         "rnbqkbnr/p0pppppp/P0000000/00000000/00000000/00000000/00000000/00000000",
         Colour.BLACK, -40),
        (Colour.WHITE,
         "rnbqkbnr/p0pppppp/P0000000/00000000/00000000/00000000/00000000/00000000",
         Colour.WHITE, -MAX_EVAL),
        (Colour.BLACK,
         "qqqqqqqq/qqqqqqqq/qqqqqqqq/qqqqqqqq/qqqqqqqq/qqqqqqqq/qqqqqqqq/QQQQQQQQ",
         Colour.BLACK, 432),
        (Colour.BLACK,
         "pppp00bb/00000000/0000k000/00000000/00000000/00000000/00000000/00000000",
         Colour.WHITE, MAX_EVAL),
        (Colour.BLACK,
         "qqqk0000/00000000/00000000/Q0P0P0P0/00000000/00000000/00000000/00000000",
         Colour.BLACK, 18),
        (Colour.BLACK,
         "0000BRNK/PPPP0P0P/00000000/00000000/00000000/00000000/000b0b0b/00000000",
         Colour.WHITE, -11),
    ])
def test_engine_evaluate(colour, start_pos, colour_to_play, real_evaluation):
    """ Test evaluate() method of Engine """
    test_board = Board(colour, start_pos)
    engine_colour = Colour.WHITE if colour == Colour.BLACK else Colour.BLACK
    # when using evaluate() method depth is not needed do I chose depth 1 for no reason
    test_engine = Engine(test_board, 1, engine_colour)

    assert real_evaluation == test_engine.evaluate(colour_to_play)

@pytest.mark.parametrize(
    'colour, start_pos, depth, best_moves',
    [
        # Colour of player, position to begin, depth of engine, best move or moves at given depth
        (Colour.WHITE,
         "R0000000/00000000/00000000/00000000/00000000/00000000/00000000/000r0000",
         4, [(7,3,0,3), (7,3,7,0)]),
        (Colour.WHITE,
         "R0000000/00000000/00000000/00000000/00000000/00000000/00000000/000r0000",
         6, [(7,3,0,3), (7,3,7,0)]),
        (Colour.WHITE,
         "R0000000/00000000/00000000/00000000/00000000/00000000/00000000/0000000r",
         1, [(7,7,0,7), (7,7,7,0)]),
        (Colour.BLACK,
         "r0000000/0P000000/00000000/00000000/00000000/00000000/00000000/0000000R",
         2, [(0,0,0,2)]),
        (Colour.BLACK,
         "00r00000/0P000000/00000000/00000000/00000000/00000000/00000000/0000000R",
         2, [(0,2,0,0)]),
        (Colour.BLACK,
         "R000000r/0PP00000/00000000/00000000/00000000/0KR00000/00000000/0000000R",
         2, [(0,7,0,0)]),
    ])
def test_engine_best_move(colour, start_pos, depth, best_moves):
    """ Test get_best_move() method of Engine """
    test_board = Board(colour, start_pos)
    engine_colour = Colour.WHITE if colour == Colour.BLACK else Colour.BLACK
    test_engine = Engine(test_board, depth, engine_colour)

    # sometimes more than one move is optimal at a given depth
    assert test_engine.get_best_move() in best_moves
