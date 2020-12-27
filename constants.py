import pygame
pygame.init()

class Movement:
    UP, DOWN, RIGHT, LEFT = 0, 1, 2, 3

class GameState:
    PLAYING, GAME_OVER = 0, 1

# Colors
class Color:
    PINK = 255, 0, 196
    GREEN = 46, 255, 95
    BLUE = 0, 196, 255
    GOLD = 255, 230, 0
    GREY = (240, 240, 240)
    LIGHT_GREY = (200, 200, 200)

BG_COLOR = 50, 14, 14
BG_COLOR_GAME_OVER = 30, 8, 8

CELL_SIZE_PX = 40
COLS = 16
ROWS = 16

W_SIZE = W_WIDTH, W_HEIGHT = 640, 640


GAME_SPEED_MS = 110

FONTS = {
    "big" : pygame.font.SysFont(None, 60),
    "small" : pygame.font.SysFont(None, 24)
}

DISPLAY = pygame.display.set_mode(W_SIZE)

#sfx
MUSIC = pygame.mixer.Sound("sfx/bg_music.wav")
MUSIC.play(loops=-1)

EAT_SOUND =  pygame.mixer.Sound("sfx/eat.wav")

GAME_OVER_SOUND = pygame.mixer.Sound("sfx/game_over.wav")