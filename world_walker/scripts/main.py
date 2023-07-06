import pygame
import random


def main():
    # create variables
    current_frame = 1
    buffing = False
    start_frame_buffing = -250
    ten_secs_in_frames = 250
    speed_buff_rate = 3

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
        'apple': (255, 0, 0),
        'speed_buff': (128, 166, 255)
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

    # speed buffer
    speed_buff_pos = {
        "x": round(random.randrange(0, width - player_size[0]) / 10) * 10,
        "y": round(random.randrange(0, height - player_size[1]) / 10) * 10,
    }

    speed_buff_size = (10, 10)

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
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    # move left
                    player_pos["x_change"] = -player_speed
                    player_pos["y_change"] = 0

                elif event.key == pygame.K_RIGHT or event.key == ord('d'):
                    # move right
                    player_pos["x_change"] = player_speed
                    player_pos["y_change"] = 0

                elif event.key == pygame.K_UP or event.key == ord('w'):
                    # move up
                    player_pos["x_change"] = 0
                    player_pos["y_change"] = -player_speed

                elif event.key == pygame.K_DOWN or event.key == ord('s'):
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

        # draw speed buff
        pygame.draw.rect(display, colors['speed_buff'], [
            speed_buff_pos["x"],
            speed_buff_pos["y"],
            speed_buff_size[0],
            speed_buff_size[1]])

        # detect collision with food
        if (abs(player_pos["x"] - food_pos["x"]) < 10) and (abs(player_pos["y"] - food_pos["y"]) < 10):
            food_eaten += 1

            food_pos = {
                "x": round(random.randrange(0, width - player_size[0]) / 10) * 10,
                "y": round(random.randrange(0, height - player_size[1]) / 10) * 10,
            }

        # detect collision with speed buff and buff player, if required
        if (abs(player_pos["x"] - speed_buff_pos["x"]) < 10) and (abs(player_pos["y"] - speed_buff_pos["y"]) < 10):
            speed_buff_pos = {
                "x": round(random.randrange(0, width - player_size[0]) / 10) * 10,
                "y": round(random.randrange(0, height - player_size[1]) / 10) * 10,
            }

            if not buffing:
                buffing = True
                start_frame_buffing = current_frame
                player_speed *= speed_buff_rate
        if buffing and current_frame - start_frame_buffing > ten_secs_in_frames:
            player_speed /= speed_buff_rate
            buffing = False

        pygame.display.update()

        # set FPS
        clock.tick(25)
        current_frame += 1

    # close app, if required
    pygame.quit()
    quit()
