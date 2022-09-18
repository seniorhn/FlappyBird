# HN is all

# Libraries
import pygame
import sys

# Variables
screen_height = 800
screen_wight = 576
playground_x = 0
background_img = pygame.transform.scale2x(
    pygame.image.load('assets/img/bg1.png'))
playground_img = pygame.transform.scale2x(
    pygame.image.load('assets/img/floor.png'))

# Display size
main_screen = pygame.display.set_mode((screen_wight, screen_height))

# start game
pygame.init()

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
    # Display Background_img (bg1.png)
    main_screen.blit(background_img, (0, 0))
    # Display Playground_img (floor.png)
    playground_x -= 1
    main_screen.blit(playground_img, (playground_x, 760))
    main_screen.blit(playground_img, (playground_x + 576, 760))

    if playground_x <= -576:
        playground_x = 0

    pygame.display.update()
    # Game speed
    time.tick(86)
