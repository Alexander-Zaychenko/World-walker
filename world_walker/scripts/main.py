import pygame
import random


def change_pos_ent(x, y):
    new_ent_pos = {
        "x": round(random.randrange(0, x - 10) / 10) * 10,
        "y": round(random.randrange(0, y - 10) / 10) * 10,
    }
    return new_ent_pos


def add_ent(display, color, player_pos, player_size):
    pygame.draw.rect(display, color, [
        player_pos["x"],
        player_pos["y"],
        player_size[0],
        player_size[1]])


def check_collision(player_x, player_y, second_x, second_y, player_size):
    x_collision = (abs(player_x - second_x) < player_size[0])
    y_collision = (abs(player_y - second_y) < player_size[1])
    return x_collision and y_collision


def main():
    # create variables
    fps = 25
    current_frame = 1
    buffing = False
    start_frame_buffing = -250
    ten_secs_in_frames = fps * 10
    speed_buff_rate = 3

    # initialize game
    pygame.init()

    # create display & run update
    width = 1080
    height = 720

    display = pygame.display.set_mode((width, height))

    pygame.display.update()
    pygame.display.set_caption("World walker BETA")

    # define colors
    colors = {
        "player": (0, 255, 0),
        'food': (255, 0, 0),
        'speed_buff': (128, 166, 255),
        'mine': (255, 255, 0)
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
    food_pos = change_pos_ent(width, height)

    food_size = (10, 10)
    food_eaten = 0

    # speed buffer
    speed_buff_pos = change_pos_ent(width, height)

    # mine
    mine_pos = change_pos_ent(width, height)
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
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    # move left
                    player_pos["x_change"] = -player_speed
                    player_pos["y_change"] = 0

                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    # move right
                    player_pos["x_change"] = player_speed
                    player_pos["y_change"] = 0

                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    # move up
                    player_pos["x_change"] = 0
                    player_pos["y_change"] = -player_speed

                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
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

        # draw player
        add_ent(display, colors['player'], player_pos, player_size)

        # draw food
        add_ent(display, colors['food'], food_pos, player_size)

        # draw speed buff
        add_ent(display, colors['speed_buff'], speed_buff_pos, player_size)

        # draw mine
        add_ent(display, colors['mine'], mine_pos, player_size)

        # detect collision with food
        if check_collision(player_pos['x'], player_pos['y'], food_pos['x'], food_pos['y'], player_size):
            food_eaten += 1

            food_pos = change_pos_ent(width, height)

            print(f"Очков: {food_eaten}")

        # detect collision with speed buff
        if check_collision(player_pos['x'], player_pos['y'], speed_buff_pos['x'], speed_buff_pos['y'], player_size):
            if not buffing:
                buffing = True
                start_frame_buffing = current_frame
                player_speed *= speed_buff_rate

                speed_buff_pos = change_pos_ent(width, height)

        if buffing and current_frame - start_frame_buffing > ten_secs_in_frames:
            player_speed /= speed_buff_rate
            buffing = False

        # detect collision with mine
        if check_collision(player_pos['x'], player_pos['y'], mine_pos['x'], mine_pos['y'], player_size):
            print('Очки сброшены!')
            food_eaten = 0
            mine_pos = change_pos_ent(width, height)

        pygame.display.update()

        # set FPS
        clock.tick(fps)
        current_frame += 1

    # close app, if required
    pygame.quit()
    quit()
