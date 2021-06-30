
import pygame.font
import pygame.mixer

pygame.font.init()
pygame.mixer.init()

SCORE_FONT = pygame.font.SysFont('comicsans', 50)
LEVEL_FONT = pygame.font.SysFont('comicsans', 50)
BEST_SCORE_FONT = pygame.font.SysFont('comicsans', 45)



TETRIS_FONT = pygame.font.SysFont('comicsans', 100)
TETRIS_FONT_2 = pygame.font.SysFont('comicsans', 50)
TETRIS_FONT_3 = pygame.font.SysFont('comicsans', 50)


GAMEOVER_FONT = pygame.font.SysFont('comicsans', 70)

BACKGROUND_IMAGE = pygame.image.load("background.jpg")
TETRIS_SOUNDTRACK = pygame.mixer.music.load("tetris soundtrack.mp3")
CLEAR_LINE_SOUND_EFFECT = pygame.mixer.Sound("clear line sound effect.mp3")


FPS = 60
PIECE_REQUIRED_TO_INCREASE_LEVEL= 25
TIME_INCREMENT = 0.05

BEST_SCORE_X = 20
BEST_SCORE_Y = 250

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 700
PLAYGROUND_WIDTH = 300  # meaning 300 // 10 = 30 width per block
PLAYGROUND_HEIGHT = 600  # meaning 600 // 20 = 30 height per block
SCORE_WIDTH = SCORE_HEIGHT = 150
BEST_SCORE_WIDTH =  200
BEST_SCORE_HEIGHT = 150

NEXT_SHAPE_WIDTH = NEXT_SHAPE_HEIGHT = 150

SQUARE_SIZE = 30
GRID_SIZE = 3
VERTICAL_GRID_LENGTH = PLAYGROUND_HEIGHT+GRID_SIZE
HORIZONTAL_GRID_LENGTH = PLAYGROUND_WIDTH+GRID_SIZE

WHITE = (255, 255, 255)
ORANGE = (255,140,0)
PURPLE = (128,0,128)
RED = (255, 0, 0)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)


# SHAPE FORMATS
#row = center´s row
#shape = [[rotation1],[rotation2]]
row = 0
col = 0
S = [[(row-1, col), (row-1, row+1), (row, col-1)],
    [(row-1, col), (row, col+1), (row+1, col+1)]]


Z = [[(row-1, col), (row-1, row-1), (row, col+1)],
    [(row-1, col), (row, col-1), (row+1, col-1)]]


I = [[(row-2, col), (row-1, col), (row+1, col)],
    [(row, col-2), (row, col-1), (row, col+1)]]


O = [[(row-1, col), (row-1, col-1), (row, col-1)]]


J = [
    [(row-1, col), (row-1, col+1), (row+1, col)],
    [(row, col-1), (row, col+1), (row+1, col+1)],
    [(row-1, col), (row+1, col), (row+1, col-1)],
    [(row-1, col-1), (row, col-1), (row, col+1)]
    ]


L = [
    [(row-1, col), (row-1,col-1),(row+1, col)],
    [(row-1, col+1), (row, col-1), (row, col+1)],
    [(row-1, col), (row+1, col+1), (row+1,col)],
    [(row, col-1), (row, col+1),(row+1,col-1)]
    ]


T = [
    [(row, col-1), (row, col+1),(row+1,col)],
    [(row-1, col), (row, col-1),(row+1,col)],
    [(row-1, col), (row, col-1), (row, col+1)],
    [(row-1, col), (row, col+1), (row+1,col)]
    ]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
#index 0 - 6 represent shape
#shapes = [I]