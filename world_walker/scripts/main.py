import pygame
import random


def main():

    # initialize game
    pygame.init()

    # create display & run update
    width = 640
    height = 480
    display = pygame.display.set_mode((width, height))

    pygame.display.update()
    pygame.display.set_caption("World walker BETA")

    # define colors
    colors = {
        "snake_head": (0, 255, 0),
        'apple': (255, 0, 0)
    }

    # snake position with offsets
    player_pos = {
        "x": width / 2 - 10,
        "y": height / 2 - 10,
        "x_change": 0,
        "y_change": 0
    }

    # player size
    player_size = (10, 10)

    # current player movement speed
    player_speed = 2

    # food
    food_pos = {
        "x": round(random.randrange(0, width - player_size[0]) / 10) * 10,
        "y": round(random.randrange(0, height - player_size[1]) / 10) * 10,
    }

    food_size = (10, 10)
    food_eaten = 0

    # start loop
    game_end = False
    clock = pygame.time.Clock()

    while not game_end:
        # game loop
        for event in pygame.event.get():
            player_pos["x_change"] = 0
            player_pos["y_change"] = 0
            if event.type == pygame.QUIT:
                game_end = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and player_pos["x_change"] == 0:
                    # move left
                    player_pos["x_change"] = -player_speed
                    player_pos["y_change"] = 0

                elif (event.key == pygame.K_RIGHT or event.key == ord('d')) and player_pos["x_change"] == 0:
                    # move right
                    player_pos["x_change"] = player_speed
                    player_pos["y_change"] = 0

                elif event.key == pygame.K_UP and player_pos["y_change"] == 0:
                    # move up
                    player_pos["x_change"] = 0
                    player_pos["y_change"] = -player_speed

                elif event.key == pygame.K_DOWN and player_pos["y_change"] == 0:
                    # move down
                    player_pos["x_change"] = 0
                    player_pos["y_change"] = player_speed

        # clear screen
        display.fill((0, 0, 0))

        # draw snake
        player_pos["x"] += player_pos["x_change"]
        player_pos["y"] += player_pos["y_change"]

        # teleport snake, if required
        if player_pos["x"] < -player_size[0]:
            player_pos["x"] = width

        elif player_pos["x"] > width:
            player_pos["x"] = 0

        elif player_pos["y"] < -player_size[1]:
            player_pos["y"] = height

        elif player_pos["y"] > height:
            player_pos["y"] = 0

        pygame.draw.rect(display, colors["snake_head"], [
            player_pos["x"],
            player_pos["y"],
            player_size[0],
            player_size[1]])

        # draw food
        pygame.draw.rect(display, colors["apple"], [
            food_pos["x"],
            food_pos["y"],
            food_size[0],
            food_size[1]])

        # detect collision with food
        if (abs(player_pos["x"] - food_pos["x"]) < 10) and (abs(player_pos["y"] - food_pos["y"]) < 10):
            food_eaten += 1

            food_pos = {
                "x": round(random.randrange(0, width - player_size[0]) / 10) * 10,
                "y": round(random.randrange(0, height - player_size[1]) / 10) * 10,
            }

        pygame.display.update()

        # set FPS
        clock.tick(30)

    # close app, if required
    pygame.quit()
    quit()
