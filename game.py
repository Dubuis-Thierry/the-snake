from constants import *
from blitmgt import *
from datamgt import *
from player import Player
from food import Food

game_objects = []
game_state = GameState.PLAYING

def is_over():
    return game_state == GameState.GAME_OVER


def is_playing():
    return game_state == GameState.PLAYING

def end_game():
    global game_state

    GAME_OVER_SOUND.play()

    MUSIC.fadeout(10)

    game_state = GameState.GAME_OVER
    get_display().fill(BG_COLOR_GAME_OVER)

    # Game over !
    blit_centered(text_img("Game over !", "big", Color.GREY), offset_y=-20)

    # Press space to play again
    blit_centered(text_img("Press space to restart.", "small", Color.LIGHT_GREY), offset_y=30)

    # High score
    if scores.highest < Player.score:
        scores.highest = Player.score
        save_data(scores)
        blit_centered(
            text_img(f"NEW HIGH SCORE: {Player.score}", color=Color.GREY), offset_y=70
        )
    else:
        blit_centered(text_img(f"Your score: {Player.score}", color=Color.GREY), offset_y=70)
        blit_centered(text_img(f"High score: {scores.highest}", color=Color.GREY), offset_y=110)


def spawn_food(n=1):
    for i in range(n):
        game_objects.append(Food())


class Void:
    def __init__(self):
        self.type = "nothing"


def what_is_it_there(position_x, position_y):
    """
    Returns the object located at the given position
    """
    for go in game_objects:
        if go.position_x == position_x and go.position_y == position_y:
            return go
    return Void()


def draw_map():
    color = (5, 1, 1)
    get_display().fill(BG_COLOR)
    for i in range(ROWS):
        pygame.draw.line(
            get_display(), color, (0, i*CELL_SIZE_PX), (W_WIDTH, i*CELL_SIZE_PX)
        )
        pygame.draw.line(
            get_display(), color, (0, (i+1)*CELL_SIZE_PX-1), (W_WIDTH, (i+1)*CELL_SIZE_PX-1)
        )
    for i in range(COLS):
        pygame.draw.line(
            get_display(), color, (i*CELL_SIZE_PX, 0), (i*CELL_SIZE_PX, W_HEIGHT)
        )
        pygame.draw.line(
            get_display(), color, ((i+1)*CELL_SIZE_PX-1, 0), ((i+1)*CELL_SIZE_PX-1, W_HEIGHT)
        )