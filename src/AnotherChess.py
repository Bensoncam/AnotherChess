from math import trunc
from sqlite3 import IntegrityError
from Board import *
from Graphics import *
from enum import Enum
import pygame, sys
import pygame_gui

pygame.init()
size = WIDTH, HEIGHT = 625, 600
SQUARE_SIZE = 60
black = 0, 0, 0

piece = 0
assets = loadAssets(SQUARE_SIZE)
gameState = Enum('gameState', ['REFRESH', 'STANDBY', 'PICKUP', 'HOLDPIECE', 'PUTDOWN'])

currentState = gameState.REFRESH

screen = pygame.display.set_mode(size)
manager = pygame_gui.UIManager((WIDTH, HEIGHT))
clock = pygame.time.Clock()
board = Board()

button1 = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 100), (100, 50)), text='button', manager=manager)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN: currentState = gameState.PICKUP
        if event.type == pygame.MOUSEBUTTONUP: currentState = gameState.PUTDOWN
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == button1:
                print('hi')
        manager.process_events(event)

    if (currentState == gameState.PICKUP):
        pos = pygame.mouse.get_pos()
        coords = calculateSquare(pos, SQUARE_SIZE)
        if (coords[0] < 0 or coords[0] > 7 or coords[1] < 0 or coords[1] > 7):
            currentState = gameState.STANDBY
            continue
        if (board.board[coords[0]][coords[1]]): 
            piece = board.pickupPiece(coords)
        currentState = gameState.HOLDPIECE

    elif (currentState == gameState.HOLDPIECE):
        if (piece):
            pos = pygame.mouse.get_pos()
            printBoard(screen, assets, board, manager, 0, SQUARE_SIZE)
            screen.blit(assets[piece], (pos[0] - SQUARE_SIZE/2, pos[1] - SQUARE_SIZE/2))

    elif (currentState == gameState.PUTDOWN):
        if (piece):
            pos = pygame.mouse.get_pos()
            coords = calculateSquare(pos, SQUARE_SIZE)
            if (coords[0] < 0 or coords[0] > 7 or coords[1] < 0 or coords[1] > 7):
                piece = 0
                board.placePiece()
                currentState = gameState.REFRESH
                continue
            if board.availableMoves(board.heldPiece[0], board.heldPiece[1])[coords[0]][coords[1]]: 
                board.move(board.heldPiece, coords)                 
                board.turn = not board.turn
        piece = 0
        board.placePiece()
        currentState = gameState.REFRESH

    elif (currentState == gameState.REFRESH):
        printBoard(screen, assets, board, manager, 0, SQUARE_SIZE)
        currentState = gameState.STANDBY
        
    pygame.display.update()