import pygame
pygame.init()

W_SIZE = W_WIDTH, W_HEIGHT = 640, 640
BG_COLOR = 50, 14, 14
BG_COLOR_GAME_OVER = 30, 8, 8

CELL_SIZE_PX = 40
COLS = 16
ROWS = 16
GAME_SPEED_MS = 100

FONT1 = pygame.font.SysFont(None, 60)
FONT2 = pygame.font.SysFont(None, 24)

GAME_OVER_IMG1 = FONT1.render("Game over !", True, (240, 240, 240))
GAME_OVER_IMG2 = FONT2.render("Press space to play again ...", True, (200, 200, 200))


DISPLAY = pygame.display.set_mode(W_SIZE)