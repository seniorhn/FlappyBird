# HN is all

# Libraries
import pygame
import sys
import random

# start game
pygame.init()


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


# Variables
screen_height = 800
screen_wight = 576
playground_x = 0
gravity = 0.25
bird_movment = 0
pipe_list = []
# ----------------- #
create_pipe = pygame.USEREVENT
pygame.time.set_timer(create_pipe, 1200)
# ----------------- #
background_img = pygame.transform.scale2x(
    pygame.image.load('assets/img/bg1.png'))
playground_img = pygame.transform.scale2x(
    pygame.image.load('assets/img/floor.png'))
bird_img = pygame.transform.scale2x(
    pygame.image.load('assets/img/red_bird_mid_flap.png'))
pipe_img = pygame.transform.scale2x(
    pygame.image.load('assets/img/pipe_red.png'))

# Rectangles
bird_img_rect = bird_img.get_rect(center=(100, 400))

# Display size
main_screen = pygame.display.set_mode((screen_wight, screen_height))

# Refresh time (timer)
time = pygame.time.Clock()

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
        if event.type == create_pipe:
            pipe_list.extend(generate_pipe_rect())

    # Display Background_img (bg1.png)
    main_screen.blit(background_img, (0, 0))

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

    if playground_x <= -576:
        playground_x = 0

    pygame.display.update()

    # Game speed
    time.tick(86)
