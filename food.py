import random

from constants import *
import game

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
            if game.what_is_it_there(self.position_x, self.position_y).type == "nothing":
                break

    def update(self):
        # Rendering
        pygame.draw.circle(
            DISPLAY, self.color,
            (self.position_x * CELL_SIZE_PX + CELL_SIZE_PX//2,
                self.position_y * CELL_SIZE_PX + CELL_SIZE_PX//2),
            CELL_SIZE_PX//3
        )