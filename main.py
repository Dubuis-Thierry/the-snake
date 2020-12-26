import sys, pygame
import random
pygame.init()

clock = pygame.time.Clock()

size = width, height = 600, 600
black = 50, 14, 14

CELL_SIZE = 40


screen = pygame.display.set_mode(size)

class Movement:
    UP, DOWN, RIGHT, LEFT = 0, 1, 2, 3
movement = random.randint(0, 3)

class Board:
    WIDTH = 15
    HEIGHT = 15
    game_objects = []
    @staticmethod
    def what_is_it_there(position_x, position_y):
        for go in Board.game_objects:
            if go.position_x == position_x and go.position_y == position_y:
                return go
        return Void()

class Void:
    def __init__(self):
        self.type = "nothing"

class PlayerBody:
    id_count = 0
    def __init__(self, position_x=-1, position_y=-1, following=0):
        self.id = PlayerBody.id_count
        PlayerBody.id_count += 1
        self.type = "player"

        if position_x == -1:
            self.position_x = random.randint(0, Board.WIDTH-1)
            self.position_y = random.randint(0, Board.HEIGHT-1)
        else:
            self.position_x, self.position_y = position_x, position_y

        self.next = 0
        self.following=following
    
    def grow(self):
        if self.next == 0:
            new_body = PlayerBody(self.position_x, self.position_y, self)
            Board.game_objects.append(new_body)
            self.next = new_body
            return
        self.next.grow()
        pygame.mixer.music.load("eat.wav")
        pygame.mixer.music.play()

    def change_pos(self, pos_x, pos_y):
        if self.next != 0:
            self.next.change_pos(self.position_x, self.position_y)
        self.position_x, self.position_y = pos_x, pos_y
    
    def cut(self):
        if self.next == 0:
            Board.game_objects.remove(self)
            self.following.next = 0
            return
        self.next.cut()
        Board.game_objects.remove(self)
        self.following.next = 0

    def update(self):
        global movement
        if self.following == 0:
            new_position_x, new_position_y = self.position_x, self.position_y
            # Movement
            if movement == Movement.UP and self.position_y > 0:
                new_position_y -= 1
                if self.next != 0 and self.next.position_y == new_position_y:
                    new_position_y += 2
                    movement = Movement.DOWN
            elif movement == Movement.DOWN and self.position_y < Board.HEIGHT-1:
                new_position_y += 1
                if self.next != 0 and self.next.position_y == new_position_y:
                    new_position_y -= 2
                    movement = Movement.UP
            elif movement == Movement.RIGHT and self.position_x < Board.WIDTH-1:
                new_position_x += 1
                if self.next != 0 and self.next.position_x == new_position_x:
                    new_position_x -= 2
                    movement = Movement.LEFT
            elif movement == Movement.LEFT and self.position_x > 0:
                new_position_x -= 1
                if self.next != 0 and self.next.position_x == new_position_x:
                    new_position_x += 2
                    movement = Movement.RIGHT
            # Collision
            collision = Board.what_is_it_there(new_position_x, new_position_y)
            if collision.type == "food":
                self.grow()
                Board.game_objects.remove(collision)
            elif collision.type == "player" and collision.id != self.id:
                print("collision")
                collision.cut()

            self.change_pos(new_position_x, new_position_y)


        # Rendering
        pygame.draw.rect(
            screen, (255, 10, 10),
            (self.position_x * CELL_SIZE + 2,
                self.position_y * CELL_SIZE + 2,
                CELL_SIZE-4, CELL_SIZE-4)
        )
        if self.following == 0:
            pygame.draw.rect(
            screen, (255, 150, 0),
            (self.position_x * CELL_SIZE + 10,
                self.position_y * CELL_SIZE + 10,
                CELL_SIZE-20, CELL_SIZE-20)
        )


class Food:
    def __init__(self):
        self.type = "food"
        self.position_x = random.randint(0, Board.WIDTH-1)
        self.position_y = random.randint(0, Board.HEIGHT-1)

    def update(self):
        # Rendering
        pygame.draw.circle(
            screen, (10, 200, 100),
            (self.position_x * CELL_SIZE + CELL_SIZE//2,
                self.position_y * CELL_SIZE + CELL_SIZE//2),
            CELL_SIZE//3
        )

Board.game_objects.append(PlayerBody())
time = 0
last_time = time
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()


    # INPUT
    if pygame.key.get_pressed()[pygame.K_UP]:
        movement = Movement.UP
    elif pygame.key.get_pressed()[pygame.K_DOWN]:
        movement = Movement.DOWN
    elif pygame.key.get_pressed()[pygame.K_RIGHT]:
        movement = Movement.RIGHT
    elif pygame.key.get_pressed()[pygame.K_LEFT]:
        movement = Movement.LEFT


    # UPDATE
    if time-last_time > 100:
        last_time = time
        if random.randint(0, 25) == 1:
            Board.game_objects.append(Food())
            print("food")
        screen.fill(black)
        for go in Board.game_objects:
            go.update()

        pygame.display.flip()
    time += clock.get_time()
    clock.tick(60)