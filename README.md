# Antichess Game With AI Based On The Minimax Algorithm

**Rules**

The app realizes a chess variant called the antichess. There are more variants of antichess following slightly different rules, these are the rules for the implemented game:

- The objective of each player is to lose all of their pieces or be stalemated
- There is not such a thing as a check or even checkmate
- Promotions are done automatically but deterministically, whenever a pawn moves to the last rank a promotion occurs, the order of pieces that pawns are promoted to is Rook, Knight, Bishop, Queen, King (then it repeats). This order is shared by both players so that players can come up with strategies around this game mechanic. Also, promotion to King is a thing as in Antichess it is just another piece like any other.
- Capturing is compulsory. When more than one capture is available, the player may choose what piece to capture first
- There is no castling
- There is no en passant captures

**How to play**

When you run the app you see a game menu.
When you want to quit the app click 'Quit'.
When you want to play you first need to choose the colour and the AI difficulty which correponds to the depth of search of the Minimax algorithm, to choose a colour you just click either 'W' as white or 'B' as black, the letter you picked should turn red, which means you will play as that colour. To pick the difficulty just type on the keyboard the number you want the difficulty to be (if there already is a number use a backspace to delete it because you can only type 1 digit difficulties). The difficulty is 0 to 5 where both 0 and 5 are included (higher depths would be too computionally expensive).
Once you click 'Play' you get into the game, when you want to move a piece click on it and all legal moves appear highlighted by the red colour, those are the only ones you can legally play (sometimes if a piece unexpectedly has no moves it means there is another one that can capture making these moves illegal). A move is played by clicking on one of the highlighted squares. Once a move is played it gets highlighted by a blue colour, mainly for the player to see the AI make a move better. 
Once the game finishes a result appears on the screen and you can click any keyboard button to move back into the menu.  

**How to run the app**

To run the app from the CLI do:

python3 main.py

in the same directory as the main.py is.

**How to run the tests**

To run the tests from the CLI do:

pytest

from the same directory as the main.py is.
