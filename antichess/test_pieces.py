""" Import pytest to create tests """
import pytest
from antichess.pieces import Pawn, Rook, Bishop, King, Queen, Knight
from antichess.colour import Colour


@pytest.mark.parametrize(
    'colour',
    [
        # Colour of piece
        Colour.WHITE, Colour.BLACK
    ])
def test_pawn(colour):
    """ Tests the pawn class """
    pawn = Pawn(colour)
    pawn_copy = pawn.copy()

    assert pawn.colour == colour
    assert pawn_copy.colour == colour
    assert pawn.image_black is not None
    assert pawn.image_white is not None
    assert pawn_copy.image_black is not None
    assert pawn_copy.image_white is not None
    assert pawn_copy.image_white == pawn.image_white
    assert pawn_copy.image_black == pawn.image_black

@pytest.mark.parametrize(
    'colour',
    [
        # Colour of piece
        Colour.WHITE, Colour.BLACK
    ])
def test_rook(colour):
    """ Tests the rook class """
    rook = Rook(colour)
    rook_copy = rook.copy()

    assert rook.colour == colour
    assert rook_copy.colour == colour
    assert rook.image_black is not None
    assert rook.image_white is not None
    assert rook_copy.image_black is not None
    assert rook_copy.image_white is not None
    assert rook_copy.image_white == rook.image_white
    assert rook_copy.image_black == rook.image_black

@pytest.mark.parametrize(
    'colour',
    [
        # Colour of piece
        Colour.WHITE, Colour.BLACK
    ])
def test_bishop(colour):
    """ Tests the bishop class """
    bishop = Bishop(colour)
    bishop_copy = bishop.copy()

    assert bishop.colour == colour
    assert bishop_copy.colour == colour
    assert bishop.image_black is not None
    assert bishop.image_white is not None
    assert bishop_copy.image_black is not None
    assert bishop_copy.image_white is not None
    assert bishop_copy.image_white == bishop.image_white
    assert bishop_copy.image_black == bishop.image_black

@pytest.mark.parametrize(
    'colour',
    [
        # Colour of piece
        Colour.WHITE, Colour.BLACK
    ])
def test_knight(colour):
    """ Tests the knight class """
    knight = Knight(colour)
    knight_copy = knight.copy()

    assert knight.colour == colour
    assert knight_copy.colour == colour
    assert knight.image_black is not None
    assert knight.image_white is not None
    assert knight_copy.image_black is not None
    assert knight_copy.image_white is not None
    assert knight_copy.image_white == knight.image_white
    assert knight_copy.image_black == knight.image_black

@pytest.mark.parametrize(
    'colour',
    [
        # Colour of piece
        Colour.WHITE, Colour.BLACK
    ])
def test_queen(colour):
    """ Tests the queen class """
    queen = Queen(colour)
    queen_copy = queen.copy()

    assert queen.colour == colour
    assert queen_copy.colour == colour
    assert queen.image_black is not None
    assert queen.image_white is not None
    assert queen_copy.image_black is not None
    assert queen_copy.image_white is not None
    assert queen_copy.image_white == queen.image_white
    assert queen_copy.image_black == queen.image_black

@pytest.mark.parametrize(
    'colour',
    [
        # Colour of piece
        Colour.WHITE, Colour.BLACK
    ])
def test_king(colour):
    """ Tests the king class """
    king = King(colour)
    king_copy = king.copy()

    assert king.colour == colour
    assert king_copy.colour == colour
    assert king.image_black is not None
    assert king.image_white is not None
    assert king_copy.image_black is not None
    assert king_copy.image_white is not None
    assert king_copy.image_white == king.image_white
    assert king_copy.image_black == king.image_black
