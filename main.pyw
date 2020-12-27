import sys, random
import tkinter

import pygame

import game
from player import Player
from constants import *
from datamgt import *

GAMEMODE = 1 # 1 = solo, 2 = duo

# Window setup
pygame.init()
pygame.display.set_caption("TT Snake")

clock = pygame.time.Clock()

def restart():
    Player.score = 0
    Player.render_score()
    if GAMEMODE==1:
        game.game_objects = [
            Player()
        ]
    else:
        game.game_objects = [
            Player(position_x=5, position_y=5, INPUT=1), Player(INPUT=2, color=(20, 20, 200))
        ]
    game.spawn_food(2)
    game.game_state = GameState.PLAYING
    MUSIC.play(loops=-1)
    

def launch():
    restart()

    time = 0
    last_time = time
    # MAINLOOP
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        # INPUT
        pressed_keys = pygame.key.get_pressed()

        if GAMEMODE == 2:
            if pressed_keys[pygame.K_UP]:
                Player.movement1 = Movement.UP
            elif pressed_keys[pygame.K_DOWN]:
                Player.movement1 = Movement.DOWN
            elif pressed_keys[pygame.K_RIGHT]:
                Player.movement1 = Movement.RIGHT
            elif pressed_keys[pygame.K_LEFT]:
                Player.movement1 = Movement.LEFT
            
            if pressed_keys[pygame.K_w]:
                Player.movement2 = Movement.UP
            elif pressed_keys[pygame.K_s]:
                Player.movement2 = Movement.DOWN
            elif pressed_keys[pygame.K_d]:
                Player.movement2 = Movement.RIGHT
            elif pressed_keys[pygame.K_a]:
                Player.movement2 = Movement.LEFT
        else:
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
            # if random.randint(0, 25) == 1:
            #     game.spawn_food()
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
    launch()