import random
import game
from constants import *
from blitmgt import *

class Player:
    movement = 4
    movement1 = 4
    movement2 = 4
    
    id_count = 0
    score = 0
    def __init__(self, position_x=-1, position_y=-1, following=0, INPUT=0, color=(200, 20, 20)):
        self.input = INPUT

        self.type = "player"
        self.color = color
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

        # Recursion
        if self.next_player == 0:
            new_body = Player(self.position_x, self.position_y, self, color=self.color)
            game.game_objects.append(new_body)
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
        if self.following == 0:  # e.g. PlayerBody is the head
            new_position_x, new_position_y = self.position_x, self.position_y

            if self.input == 1:
                movement = Player.movement1
            elif self.input == 2:
                movement = Player.movement2
            else:
                movement = Player.movement

            # Movement
            if movement == Movement.UP:
                new_position_y -= 1
                if self.next_player != 0 and self.next_player.position_y == new_position_y:
                    new_position_y += 2

            elif movement == Movement.DOWN:
                new_position_y += 1
                if self.next_player != 0 and self.next_player.position_y == new_position_y:
                    new_position_y -= 2

            elif movement == Movement.RIGHT:
                new_position_x += 1
                if self.next_player != 0 and self.next_player.position_x == new_position_x:
                    new_position_x -= 2

            elif movement == Movement.LEFT:
                new_position_x -= 1
                if self.next_player != 0 and self.next_player.position_x == new_position_x:
                    new_position_x += 2

            if new_position_y < 0 or new_position_y >= ROWS or\
                new_position_x < 0 or new_position_x >= COLS:
                game.end_game()

            # Collision
            collision = game.what_is_it_there(new_position_x, new_position_y)
            if collision.type == "food":
                self.grow(collision.value)
                game.game_objects.remove(collision)
                game.spawn_food(collision.value)
            elif collision.type == "player" and collision.ID != self.ID:
                game.end_game()
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
    @staticmethod
    def render_score():
        blit_centered(text_img(f"SCORE: {Player.score}"), offset_y=-W_HEIGHT//2 + 20)