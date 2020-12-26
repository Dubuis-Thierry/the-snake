import sys, os, pygame
import random
from config import *
from datamgt import *

from mydbg import *

pygame.init()

clock = pygame.time.Clock()

scores = DataToSave()
if os.path.exists("data/scores.pickle"):
    scores = get_data()
else:
    scores.highest = 0
    save_data(scores)


class GameState:
    PLAYING, GAME_OVER = 0, 1


class Color:
    PINK = 255, 0, 196
    GREEN = 46, 255, 95
    BLUE = 0, 196, 255
    GOLD = 255, 230, 0

game_state = GameState.PLAYING

player_score_display = FONT2.render("SCORE: 0", True, (200, 200, 200))
x, y = player_score_display.get_size()
player_score_display_position = (W_WIDTH//2-x//2, y+2)


def render_score():
    global player_score_display, player_score_display_position
    DISPLAY.blit(player_score_display, player_score_display_position)


class Movement:
    UP, DOWN, RIGHT, LEFT = 0, 1, 2, 3

movement = random.randint(0, 3)

game_objects = []

#sfx
MUSIC = pygame.mixer.Sound("sfx/bg_music.wav")
MUSIC.play(loops=-1)

EAT_SOUND =  pygame.mixer.Sound("sfx/eat.wav")

GAME_OVER_SOUND = pygame.mixer.Sound("sfx/game_over.wav")


def end_game():
    global game_state

    GAME_OVER_SOUND.play()

    MUSIC.fadeout(10)

    game_state = GameState.GAME_OVER
    DISPLAY.fill(BG_COLOR_GAME_OVER)

    render_score()

    # Game over !
    rect_x, rect_y = GAME_OVER_IMG1.get_size()
    DISPLAY.blit(GAME_OVER_IMG1, (W_WIDTH//2 - rect_x//2, W_WIDTH//2-rect_y//2 - 20))

    # Press space to play again
    rect_x, rect_y = GAME_OVER_IMG2.get_size()
    DISPLAY.blit(GAME_OVER_IMG2, (W_WIDTH//2 - rect_x//2, W_WIDTH//2-rect_y//2 + 30))

    # High score
    highest_score_display = 0
    if scores.highest < Player.score:
        scores.highest = Player.score
        save_data(scores)
        high_score_display = FONT2.render(
            "NEW HIGH SCORE: {}".format(Player.score), True, (240, 240, 240)
        )
        x, y = high_score_display.get_size()
    else:
        high_score_display = FONT2.render(
            "Your high score: {}".format(scores.highest), True, (240, 240, 240)
        )
        x, y = high_score_display.get_size()
    DISPLAY.blit(high_score_display, (W_WIDTH//2 - x//2, W_WIDTH//2-y//2 + 70))


def what_is_it_there(position_x, position_y):
    """
    Returns the object located at the given position
    """
    for go in game_objects:
        if go.position_x == position_x and go.position_y == position_y:
            return go
    return Void()


class Void:
    def __init__(self):
        self.type = "nothing"


class Player:
    id_count = 0
    score = 0
    def __init__(self, position_x=-1, position_y=-1, following=0):

        self.type = "player"
        self.color = (200, 20, 20)
        self.next_player = 0
        self.following = following

        # Assigning ID
        self.ID = Player.id_count
        Player.id_count += 1

        # Setting position
        if position_x == -1:
            self.position_x = COLS//2
            self.position_y = ROWS//2
        else:
            self.position_x, self.position_y = position_x, position_y
        
    
    def grow(self, size=1, init=True):
        """
        Grow after eating food
        """
        global player_score_display
        # Sound
        if init:
            EAT_SOUND.play()
            Player.score += size
            player_score_display = FONT2.render("SCORE: {}".format(Player.score), True, (200, 200, 200))

        # Recursion
        if self.next_player == 0:
            new_body = Player(self.position_x, self.position_y, self)
            game_objects.append(new_body)
            self.next_player = new_body
            if size > 1:
                new_body.grow(size - 1, False)
            return
        self.next_player.grow(size, False)

    def change_pos(self, pos_x, pos_y):
        if self.next_player != 0:
            self.next_player.change_pos(self.position_x, self.position_y)
        self.position_x, self.position_y = pos_x, pos_y

    def update(self):
        global movement, player_score_display

        if self.following == 0:  # e.g. PlayerBody is the head
            new_position_x, new_position_y = self.position_x, self.position_y

            # Movement
            if movement == Movement.UP:
                new_position_y -= 1
                if self.next_player != 0 and self.next_player.position_y == new_position_y:
                    new_position_y += 2
                    movement = Movement.DOWN

            elif movement == Movement.DOWN:
                new_position_y += 1
                if self.next_player != 0 and self.next_player.position_y == new_position_y:
                    new_position_y -= 2
                    movement = Movement.UP

            elif movement == Movement.RIGHT:
                new_position_x += 1
                if self.next_player != 0 and self.next_player.position_x == new_position_x:
                    new_position_x -= 2
                    movement = Movement.LEFT

            elif movement == Movement.LEFT:
                new_position_x -= 1
                if self.next_player != 0 and self.next_player.position_x == new_position_x:
                    new_position_x += 2
                    movement = Movement.RIGHT

            if new_position_y < 0 or new_position_y >= ROWS or\
                new_position_x < 0 or new_position_x >= COLS:
                end_game()

            # Collision
            collision = what_is_it_there(new_position_x, new_position_y)
            if collision.type == "food":
                self.grow(collision.value)
                game_objects.remove(collision)
            elif collision.type == "player" and collision.ID != self.ID:
                end_game()
                return

            self.change_pos(new_position_x, new_position_y)


        # Rendering
        pygame.draw.rect(
            DISPLAY, self.color,
            (self.position_x * CELL_SIZE_PX + 2,
                self.position_y * CELL_SIZE_PX + 2,
                CELL_SIZE_PX-4, CELL_SIZE_PX-4)
        )
        if self.following == 0:
            pygame.draw.rect(
            DISPLAY, (255, 150, 0),
            (self.position_x * CELL_SIZE_PX + 10,
                self.position_y * CELL_SIZE_PX + 10,
                CELL_SIZE_PX-20, CELL_SIZE_PX-20)
        )


class Food:
    def __init__(self):
        self.type = "food"
        # Deciding value
        v_factor = random.randint(1, 100)
        if v_factor < 75:
            self.value = 1
            self.color = Color.BLUE
        elif v_factor < 95:
            self.value = 2
            self.color = Color.GREEN
        elif v_factor < 100:
            self.value = 3
            self.color = Color.PINK
        else:
            self.value = 5
            self.color = Color.GOLD
        while 1:
            self.position_x = random.randint(0, COLS-1)
            self.position_y = random.randint(0, ROWS-1)
            if what_is_it_there(self.position_x, self.position_y).type == "nothing":
                break

    def update(self):
        # Rendering
        pygame.draw.circle(
            DISPLAY, self.color,
            (self.position_x * CELL_SIZE_PX + CELL_SIZE_PX//2,
                self.position_y * CELL_SIZE_PX + CELL_SIZE_PX//2),
            CELL_SIZE_PX//3
        )

def restart():
    global game_objects, game_state, movement, player_score, player_score_display
    Player.score = 0
    player_score_display = FONT2.render("SCORE: 0", True, (200, 200, 200))
    render_score()
    game_objects = [Player()]
    game_state = GameState.PLAYING
    MUSIC.play(loops=-1)
    movement = random.randint(0, 3)

def draw_map():
    color = (5, 1, 1)
    DISPLAY.fill(BG_COLOR)
    for i in range(ROWS):
        pygame.draw.line(
            DISPLAY, color, (0, i*CELL_SIZE_PX), (W_WIDTH, i*CELL_SIZE_PX)
        )
        pygame.draw.line(
            DISPLAY, color, (0, (i+1)*CELL_SIZE_PX-1), (W_WIDTH, (i+1)*CELL_SIZE_PX-1)
        )
    for i in range(COLS):
        pygame.draw.line(
            DISPLAY, color, (i*CELL_SIZE_PX, 0), (i*CELL_SIZE_PX, W_HEIGHT)
        )
        pygame.draw.line(
            DISPLAY, color, ((i+1)*CELL_SIZE_PX-1, 0), ((i+1)*CELL_SIZE_PX-1, W_HEIGHT)
        )

game_objects.append(Player())


time = 0
last_time = time
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    # INPUT
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w]:
        movement = Movement.UP
    elif pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]:
        movement = Movement.DOWN
    elif pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
        movement = Movement.RIGHT
    elif pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]:
        movement = Movement.LEFT


    # UPDATE
    if time - last_time > GAME_SPEED_MS and game_state == GameState.PLAYING:
        last_time = time
        if random.randint(0, 25) == 1:
            game_objects.append(Food())
            debug("Food appeared")
        draw_map()
        for go in game_objects:
            go.update()
            if game_state == GameState.GAME_OVER:
                break
        render_score()
        pygame.display.flip()

    elif game_state == GameState.GAME_OVER:
        if pressed_keys[pygame.K_SPACE]:
            restart()
    
    time += clock.get_time()
    clock.tick(100)