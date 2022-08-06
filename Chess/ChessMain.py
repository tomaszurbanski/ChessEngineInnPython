"""
This is main driver file. It will be responsible for handing user and displaying the current gameState obect.
"""

import pygame as p
from Chess import ChessEngine

WIDTH = HEIGHT = 512   # 400 is another option
DIMENSION = 8   # dimension of a chess board are 8x8
SQ_SIZE = HEIGHT // 8
MAX_FPS = 15   # for animation later on
IMAGES = {}

"""
Initialize a global dictionary of images. This will be called exactly ones in the main
"""
def loadImages():
    pieces = ['wR', 'wQ', 'wp', 'wN', 'wK', 'wB', 'bR', 'bQ', 'bp', 'bN', 'bK', 'bB']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # Note: we can access an image by saying "IMAGES['wp']"

"""
The main driver for our code. This will handle user input and updating graphics. 
"""
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    # print(gs.board)
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made

    loadImages()  # only do this once, before the while loop
    running = True
    sqSelected = ()   # no square is selected, keep track of the last click of the user (tuple: (row, col))
    playerCliks = []   # keep track of player clicks (two tuples: [(6, 4), (4, 4)]
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()   # (x, y) location of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col):   # the user clicked the square twice
                    sqSelected = ()   # deselekted
                    playerCliks = []   # clear player clicks
                else:
                    sqSelected = (row, col)
                    playerCliks.append(sqSelected)   # append for both 1st and 2nd clicks
                if len(playerCliks) == 2:   # after 2 clicks
                    move = ChessEngine.Move(playerCliks[0], playerCliks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = () #reset user cliks
                    playerCliks = []
            #key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  #undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()



"""
Responsible for all the graphics within game state.
"""

def drawGameState(screen, gs):
    drawBoard(screen)   # draw squares on the board
    # add in piece highlighting or move suggestions (later)
    drawPieces(screen, gs.board)   # draw pieces on top of those squares

"""
Draw the squares on the board.
"""

def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

"""
Draw the pieces on the board using the current GameState.board
"""
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":   # not empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()

