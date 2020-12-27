import sys, random

import pygame

import game
import mydbg
from player import Player
from food import Food
from constants import *
from datamgt import *

# Window setup
pygame.init()
pygame.display.set_caption("TT Snake")

clock = pygame.time.Clock()

def restart():
    Player.score = 0
    Player.render_score()
    game.game_objects = [Player()]
    game.game_state = GameState.PLAYING
    MUSIC.play(loops=-1)
    Player.movement = random.randint(0, 3)


def main():
    game.game_objects.append(Player())

    time = 0
    last_time = time
    # MAINLOOP
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        # INPUT
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w]:
            Player.movement = Movement.UP
        elif pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]:
            Player.movement = Movement.DOWN
        elif pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
            Player.movement = Movement.RIGHT
        elif pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]:
            Player.movement = Movement.LEFT


        # UPDATE
        if time - last_time > GAME_SPEED_MS and game.is_playing():
            last_time = time
            if random.randint(0, 25) == 1:
                game.game_objects.append(Food())
                mydbg.debug("Food appeared")
            game.draw_map()
            for go in game.game_objects:
                go.update()
                if game.is_over():
                    break
            Player.render_score()
            pygame.display.flip()

        elif game.is_over():
            if pressed_keys[pygame.K_SPACE]:
                restart()
        
        time += clock.get_time()
        clock.tick(100)


if __name__ == "__main__":
    main()