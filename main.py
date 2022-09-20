# HN is all

# Libraries
import pygame
import sys
import random
import time

# start game
pygame.init()

# Variables
screen_height = 800
screen_wight = 576
playground_x = 0
gravity = 0.25
bird_movment = 0
pipe_list = []
game_status = True
active_score = True
bird_list_index = 0
score = 0
high_score = 0
game_font = pygame.font.Font('assets/font/Flappy.TTF', 40)

# ----------------- #
point_sound = pygame.mixer.Sound('assets/sounds/point.mp3')
game_over_sound = pygame.mixer.Sound('assets/sounds/hd.mp3')
# ----------------- #
create_pipe = pygame.USEREVENT
pygame.time.set_timer(create_pipe, 1100)
create_flap = pygame.USEREVENT + 1
pygame.time.set_timer(create_flap, 100)
# ----------------- #
background_img = pygame.transform.scale2x(
    pygame.image.load('assets/img/bg1.png'))

playground_img = pygame.transform.scale2x(
    pygame.image.load('assets/img/floor.png'))

bird_img1 = pygame.transform.scale2x(
    pygame.image.load('assets/img/red_bird_mid_flap.png'))
bird_img2 = pygame.transform.scale2x(
    pygame.image.load('assets/img/red_bird_down_flap.png'))
bird_img3 = pygame.transform.scale2x(
    pygame.image.load('assets/img/red_bird_up_flap.png'))

bird_list = [bird_img1, bird_img2, bird_img3]

bird_img = bird_list[bird_list_index]

pipe_img = pygame.transform.scale2x(
    pygame.image.load('assets/img/pipe_red.png'))

game_over_img = pygame.transform.scale2x(
    pygame.image.load('assets/img/message.png'))

game_over_img_rect = game_over_img.get_rect(center=(280, 500))

# Rectangles
bird_img_rect = bird_img.get_rect(center=(100, 400))

# Display size
main_screen = pygame.display.set_mode((screen_wight, screen_height))

# Refresh time (timer)
time = pygame.time.Clock()

# defs


def generate_pipe_rect():
    random_pipes = random.randrange(300, 500)
    pipe_rect_top = pipe_img.get_rect(midbottom=(700, random_pipes - 250))
    pipe_rect_bottom = pipe_img.get_rect(midtop=(700, random_pipes))
    return pipe_rect_bottom, pipe_rect_top


def move_pipe_rect(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    inside_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return inside_pipes


def display_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 800:
            main_screen.blit(pipe_img, pipe)
        else:
            reversed_pipes = pygame.transform.flip(pipe_img, False, True)
            main_screen.blit(reversed_pipes, pipe)


def check_collision(pipes):
    global active_score
    for pipe in pipes:
        if bird_img_rect.colliderect(pipe):
            game_over_sound.play()
            time.sleep(1)
            active_score = True
            return False
        if bird_img_rect.top <= -50 or bird_img_rect.bottom >= 576:
            game_over_sound.play()
            time.sleep(1)
            active_score = True
            return False
    return True


def bird_animation():
    new_bird = bird_list[bird_list_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_img_rect.centery))
    return new_bird, new_bird_rect


def display_score(status):
    if status == 'active':
        text1 = game_font.render(str(score), True, (255, 255, 255))
        text1_rect = text1.get_rect(center=(298, 30))
        main_screen.blit(text1, text1_rect)

    if status == 'game_over':
        # Score
        text1 = game_font.render(f'Score: {score}', True, (255, 255, 255))
        text1_rect = text1.get_rect(center=(298, 30))
        main_screen.blit(text1, text1_rect)

        # High Score
        text2 = game_font.render(
            f'High Score: {high_score}', True, (255, 255, 255))
        text2_rect = text2.get_rect(center=(295, 100))
        main_screen.blit(text2, text2_rect)


def update_score():
    global score, high_score, active_score
    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and active_score:
                point_sound.play()
                score += 1
                active_score = False
            if pipe.centerx < 0:
                active_score = True

    if score > high_score:
        high_score = score

    return high_score


# Game logic
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # stop(end)game
            pygame.quit()
            # Terminate program
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movment = 0
                bird_movment -= 8
            if event.key == pygame.K_SPACE and game_status == False:
                game_status = True
                pipe_list.clear()
                bird_img_rect.center = (100, 400)
                bird_movment = 0

        if event.type == create_pipe:
            pipe_list.extend(generate_pipe_rect())
        if event.type == create_flap:
            if bird_list_index < 2:
                bird_list_index += 1
            else:
                bird_list_index = 0
            bird_img, bird_img_rect = bird_animation()

    # Display Background_img (bg1.png)
    main_screen.blit(background_img, (0, 0))

    if game_status:
        # Display Playground_img (floor.png)
        playground_x -= 1
        main_screen.blit(playground_img, (playground_x, 760))
        main_screen.blit(playground_img, (playground_x + 576, 760))

        # Display Bird_img
        main_screen.blit(bird_img, bird_img_rect)

        # Move pipes
        pipe_list = move_pipe_rect(pipe_list)
        display_pipes(pipe_list)

        # Floor gravity and Bird movement
        bird_movment += gravity
        bird_img_rect.centery += bird_movment

        # Check for Collisions
        game_status = check_collision(pipe_list)

        # Show Score
        update_score()
        display_score('active')
    else:
        main_screen.blit(game_over_img, game_over_img_rect)
        display_score('game_over')

    if playground_x <= -576:
        playground_x = 0

    # Check collision
    check_collision(pipe_list)

    pygame.display.update()

    # Game speed
    time.tick(90)
