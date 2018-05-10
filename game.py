import pygame
import math
from pygame.locals import *
import time

pygame.init()
width, height = 1000, 500
screen = pygame.display.set_mode((width, height))
screen.fill(0)

cellSize = width / 250
gridHeight = height / cellSize
gridWidth = width / cellSize

blue = (0, 0, 255)
blue_sec = (0, 0, 128)
red = (255, 0, 0)
red_sec = (128, 0, 0)
white = (255, 255, 255)

player1_color = red
player1_color_sec = red_sec
player2_color = blue
player2_color_sec = blue_sec


def start_game():
    keys_p1 = [False, False, False, False]
    keys_p2 = [False, False, False, False]
    trail_p1 = [(math.floor(gridWidth/3), math.floor(gridHeight/2))]
    trail_p2 = [(2*math.floor(gridWidth/3), math.floor(gridHeight/2))]

    counter = 0
    game_over = False
    player1_winner = False
    player2_winner = False
    while not game_over:
        screen.fill(0)

        for trail_p1_Tile in trail_p1:
            tile_coords = (trail_p1_Tile[0]*cellSize, trail_p1_Tile[1]*cellSize)
            if trail_p1_Tile == trail_p1[0]:
                pygame.draw.rect(screen, player1_color, (tile_coords[0], tile_coords[1], cellSize, cellSize), 0)
            else:
                pygame.draw.rect(screen, player1_color_sec, (tile_coords[0], tile_coords[1], cellSize, cellSize), 0)

        for trail_p2_Tile in trail_p2:
            tile_coords = (trail_p2_Tile[0]*cellSize, trail_p2_Tile[1]*cellSize)
            if trail_p2_Tile == trail_p2[0]:
                pygame.draw.rect(screen, player2_color, (tile_coords[0], tile_coords[1], cellSize, cellSize), 0)
            else:
                pygame.draw.rect(screen, player2_color_sec, (tile_coords[0], tile_coords[1], cellSize, cellSize), 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == K_w:
                    keys_p1 = [True, False, False, False]
                elif event.key == K_a:
                    keys_p1 = [False, True, False, False]
                elif event.key == K_s:
                    keys_p1 = [False, False, True, False]
                elif event.key == K_d:
                    keys_p1 = [False, False, False, True]
                elif event.key == K_UP:
                    keys_p2 = [True, False, False, False]
                elif event.key == K_LEFT:
                    keys_p2 = [False, True, False, False]
                elif event.key == K_DOWN:
                    keys_p2 = [False, False, True, False]
                elif event.key == K_RIGHT:
                    keys_p2 = [False, False, False, True]

        if counter % 20:
            if keys_p1[0]:
                trail_p1.insert(0, (trail_p1[0][0], trail_p1[0][1] - 1))
            elif keys_p1[1]:
                trail_p1.insert(0, (trail_p1[0][0] - 1, trail_p1[0][1]))
            elif keys_p1[2]:
                trail_p1.insert(0, (trail_p1[0][0], trail_p1[0][1] + 1))
            elif keys_p1[3]:
                trail_p1.insert(0, (trail_p1[0][0] + 1, trail_p1[0][1]))

            if keys_p2[0]:
                trail_p2.insert(0, (trail_p2[0][0], trail_p2[0][1] - 1))
            elif keys_p2[1]:
                trail_p2.insert(0, (trail_p2[0][0] - 1, trail_p2[0][1]))
            elif keys_p2[2]:
                trail_p2.insert(0, (trail_p2[0][0], trail_p2[0][1] + 1))
            elif keys_p2[3]:
                trail_p2.insert(0, (trail_p2[0][0] + 1, trail_p2[0][1]))

        # Check wall collisions for player 1
        if (trail_p1[0][0] < 0) or (trail_p1[0][0] >= gridWidth) or (trail_p1[0][1] < 0) \
                or (trail_p1[0][1] >= gridHeight):
            # player 2 wins
            game_over = True
            player2_winner = True
            print("P1 wall coll")
        # Check self-collision for player 1
        if trail_p1.count(trail_p1[0]) >= 2:
            # player 2 wins
            game_over = True
            player2_winner = True
            print("P1 self coll")
        # Check enemy collision for player 1
        if trail_p2.count(trail_p1[0]) >= 1:
            # player 2 wins
            game_over = True
            player2_winner = True
            print("P1 enemy coll")
        # Check wall collisions for player 2
        if (trail_p2[0][0] < 0) or (trail_p2[0][0] >= gridWidth) or (trail_p2[0][1] < 0)\
                or (trail_p2[0][1] >= gridHeight):
            # player 1 wins
            game_over = True
            player1_winner = True
            print("P2 wall coll")
        # Check self-collision for player 2
        if trail_p2.count(trail_p2[0]) >= 2:
            # player 1 wins
            game_over = True
            player1_winner = True
            print("P2 self coll")
        # Check enemy collision for player 2
        if trail_p1.count(trail_p2[0]) >= 1:
            # player 1 wins
            game_over = True
            player1_winner = True
            print("P2 enemy coll")

        pygame.display.flip()

        time.sleep(0.001)
        counter += 1
    display_winner(player1_winner, player2_winner)


def display_winner(player1_winner, player2_winner):
    game_status = "None"
    game_status_color = white
    if player2_winner and player1_winner:
        game_status = "Draw"
    elif player1_winner and not player2_winner:
        game_status = "Player 1 wins"
        game_status_color = player1_color
    elif player2_winner and not player1_winner:
        game_status = "Player 2 wins"
        game_status_color = player2_color

    pygame.font.init()
    my_font = pygame.font.SysFont("Comic Sans MS", 60)

    text_surface = my_font.render(game_status, True, game_status_color)
    text_rect = text_surface.get_rect()
    text_rect.center = (width/2, height/2)
    screen.blit(text_surface, text_rect)

    my_font = pygame.font.SysFont("Comic Sans MS", 20)
    instruct_text = my_font.render("Press any key to restart game", True, white)
    text_rect = instruct_text.get_rect()
    text_rect.center = (width/2, height-20)
    screen.blit(instruct_text, text_rect)

    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                start_game()
        time.sleep(0.001)

start_game()
exit(0)
