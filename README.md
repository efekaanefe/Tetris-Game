# Tetris-Game
![](Images/1.png)
![](Images/2.png)
PROS:
Pieces get faster depending on level (level system depends on how many pieces came to the game)(i.e. after every 10 pieces level increases +1)(not a pro or con).
Keeps your best score in a .txt file.
Soundtrack and clear-line-effect included.
Score system is dynamic (depends on level, and how many lines you clear).


CONS:
Pieces are inactivated immediately after touching, there is no delay which limits possible piece end-locations.
When moving a piece left/right, clock keeps ticking which again limits possible piece end-locations.
No animation.
Rotation system doesn´t allow to rotate a piece that is at the edge, it would be better if it allows but shifts the piece a little.


REQUIREMENTS:
pygame.

HOW TO PLAY:
run main.py,
press any key to start playing.

CONTROLS
-down arrow -> fast down
-up arrow -> rotate
-left arrow -> left
-right arrow -> right
-space -> inactivates the current piece (player shouldn´t use it)

