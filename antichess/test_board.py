""" Importing pytest to create tests """
import pytest
from antichess.board import Board
from antichess.colour import Colour

@pytest.mark.parametrize(
    'colour, start_pos, white_count, black_count',
    [
        # Colour of player, position to begin, number of white pieces, number of black pieces
        (Colour.WHITE,
         "00000000/00000000/00000000/00000000/00000000/00000000/00000000/00000000", 0, 0),
        (Colour.WHITE,
         "rnbqkbnr/pppppppp/00000000/00000000/00000000/00000000/PPPPPPPP/RNBQKBNR", 16, 16),
        (Colour.WHITE,
         "0000k000/00000000/00000000/00000000/00000000/00000000/00000000/PPPPPRK0", 7, 1),
        (Colour.BLACK,
         "00000000/00000000/00000000/00000000/00000000/00000000/00000000/00000000", 0, 0),
        (Colour.BLACK,
         "kkkkkkkk/kkkkkkkk/kkkkkkkk/kkkkkkkk/kkkkkkkk/pppppppp/pppppppp/pppppppp", 64, 0),
        (Colour.BLACK,
         "00000qqq/pppprrbk/00BBbb00/00000000/00000000/0KNQ0000/0000KNQP/00000000", 13, 9),
    ])
def test_board_constructor(colour, start_pos, white_count, black_count):
    """ Tests the constructor of Board """
    test_board = Board(colour, start_pos)

    assert test_board.colour == colour
    assert len(test_board.white_pieces_pos) == white_count
    assert len(test_board.black_pieces_pos) == black_count
    assert len(test_board.moves_played) == 0
    assert len(test_board.pieces_taken) == 0

@pytest.mark.parametrize(
    'colour, start_pos, moves_to_make, moves_to_unmake',
    [
        # Colour of player, board position to begin at, (move, can happen, is done by opponent),
        # could a move be undone
        (
            Colour.WHITE,
            "00000000/00000000/00000000/00000000/00000000/00000000/00000000/00000000",
            [((0,0,1,1), False, True), ((0,0,0,0), False, True), ((5,5,8,64),False, False)],
            [False] * 6
        ),

        (
            Colour.WHITE,
            "rnbqkbnr/pppppppp/00000000/00000000/00000000/00000000/PPPPPPPP/RNBQKBNR",
            [
                ((0,0,1,1), False, False),
                ((6,6,99,6), False, False),
                ((5,5,8,64), False, False),
                ((6,6,4,6), True, False),
                ((1, 7, 3,7), True, True),
                ((4, 6, 3, 6), False, False),
                ((4, 6, 3, 7), True, False),
            ],
            [True, True, True, False, False, False, False]
        ),

        (
            Colour.BLACK,
            "K0000000/00PP0000/00000000/00000000/00000000/k0000000/000pp000/00000000",
            [
                ((1,2,3,2), False, False),
                ((1,3,0,3), True, False),
                ((6,3,7,3), True, True),
                ((0,0,1,1), False, False),
                ((0,3,7,3), True, False),
                ((5,0,5,1), False, True),
                ((6,4,7,3), True, True),
            ],
            [True, True, True, True, False, False]
        )
    ])
def test_board_making_moves(colour, start_pos, moves_to_make, moves_to_unmake):
    """ Tests move() and unmake_last_move() method of Board """
    test_board = Board(colour, start_pos)

    for move in moves_to_make:
        move, return_val, is_op = move
        assert test_board.move(move, is_op) == return_val

    for move in moves_to_unmake:
        assert move == test_board.unmake_last_move()



@pytest.mark.parametrize(
    'colour, start_pos, moves_to_make',
    [
        # colour of player, board position, (move to make, does promotion happen, is it by opponent)
        (
            Colour.WHITE,
            "K0000000/PPPPPPPP/00000000/00000000/00000000/k0000000/ppppk000/00000000",
            [
                ((1,7,0,7), True, False),
                ((5,0,5,1), False, True),
                ((1,6,0,6), True, False),
                ((6,1,7,1), True, True),
            ],
        ),

        (
            Colour.BLACK,
            "K0000000/PPPPPPPP/00000000/00000000/00000000/k0000000/ppppk000/00000000",
            [
                ((1,7,0,7), True, False),
                ((5,0,5,1), False, True),
                ((1,6,0,6), True, False),
                ((6,1,7,1), True, True),
            ],
        )
    ])
def test_board_promotions(colour, start_pos, moves_to_make):
    """ Tests whether the promotions in board work correctly """
    test_board = Board(colour, start_pos)

    prom_index = 0 # promotion_index mod 5 -> 0 = rook, 1 = knight, 2 = bishop, 3 = queen, 4 = king

    for move in moves_to_make:
        move, prom_happen, is_op = move
        test_board.move(move, is_op)

        if prom_happen:
            if prom_index % 5 == 0:
                assert test_board.current_board[move[2], move[3]].get_value() == 5
            elif prom_index % 5 == 1:
                assert test_board.current_board[move[2], move[3]].get_value() == 3
            elif prom_index % 5 == 2:
                assert test_board.current_board[move[2], move[3]].get_value() == 3
            elif prom_index % 5 == 3:
                assert test_board.current_board[move[2], move[3]].get_value() == 9
            else:
                assert test_board.current_board[move[2], move[3]].get_value() == 4
            prom_index += 1

        assert prom_index == test_board.promotion_index

    var_for_pep_to_be_happy = 0
    for move in moves_to_make:
        var_for_pep_to_be_happy = move[0][0]
        var_for_pep_to_be_happy += 1
        test_board.unmake_last_move()

    assert test_board.promotion_index == 0


@pytest.mark.parametrize(
    'colour, start_pos, can_anyone_take, colour_to_play, is_opponent',
    [
        # colour of board, board position, can any piece take a piece, colour to play, is opponent
        (
            Colour.WHITE,
            "00000000/00000000/00000000/00000000/00000000/00000000/00000000/00000000",
            False,
            Colour.WHITE,
            False
        ),

        (
            Colour.WHITE,
            "rnbqkbnr/pppppppp/00000000/00000000/00000000/00000000/PPPPPPPP/RNBQKBNR",
            False,
            Colour.WHITE,
            False
        ),

        (
            Colour.WHITE,
            "rnb0000r/bppppppp/00000000/00000000/00000000/00000000/PPPPPPPP/RNBQKBNR",
            True,
            Colour.BLACK,
            True
        ),


        (
            Colour.BLACK,
            "RR000000/000000K0/00000000/0000k000/00000000/000000b0/0000000P/0000000r",
            True,
            Colour.BLACK,
            False
        ),

        (
            Colour.BLACK,
            "rnbqkbnb/pppppp0p/00000000/00000000/00000000/00000000/P0PPPPPP/RNBQKBNR",
            True,
            Colour.WHITE,
            True
        ),
    ])
def test_board_can_take(colour, start_pos, can_anyone_take, colour_to_play, is_opponent):
    """ Tests the can_take() method of Board """
    test_board = Board(colour, start_pos)
    assert test_board.can_take(colour_to_play, is_opponent) == can_anyone_take



@pytest.mark.parametrize(
    'colour, start_pos, moves_to_test',
    [
        # colour of player, board position, (move, is the move valid, is the opponent playing)
        (
            Colour.BLACK,
            "00000000/00000000/00000000/00000000/00000000/00000000/00000000/00000000",
            [
                ((1,7,0,7), False, False),
                ((91,7,0,7), False, True),
                ((1,7,0,7), False, True),
                ((1,7,-1,7), False, False),
                ((45,7,0,7), False, True),
                ((2,1,7,1), False, False),
            ]
        ),

        (
            Colour.WHITE,
            "rnb0000r/bppppppp/00000000/00000000/00000000/00000000/PPPPPPPP/RNBQKBNR",
            [
                ((1,7,0,7), False, False),
                ((91,7,0,7), False, True),
                ((1,1,2,1), False, True),
                ((1,7,-1,7), False, False),
                ((1,1,3,1), False, True),
                ((2,1,7,1), False, False),
            ]
        ),

        (
            Colour.WHITE,
            "kk00b000/000000PP/00000000/00000000/00000000/00000000/00000000/000000KK",
            [
                ((1,7,0,7), True, True),
                ((1,6,0,6), True, True),
                ((7,7,6,6), True, True),
                ((-991,7,-1,7), False, False),
                ((1,1,3,1), False, True),
                ((0,4,1,3), True, False),
            ]
        ),
    ])
def test_board_check_move_valid(colour, start_pos, moves_to_test):
    """ Function tests the is_move_valid() method of Board """
    test_board = Board(colour, start_pos)

    for item in moves_to_test:
        move, is_valid, is_opponent = item
        assert test_board.is_move_valid(move, is_opponent) == is_valid
