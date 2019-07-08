import pygame
import random

width = 480
height = 360
FPS = 30

# Initializing the Game

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Hello People")
clock = pygame.time.Clock()

# sprites are anything that moves around in the screen

all_sprites = pygame.sprite.Group()


run_game = True
while run_game:
    # keep the loop running at the right speed:
    clock.tick(FPS)

    # the game Loop
    for event in pygame.event.get():
        # checking for a closed window
        if event.type == pygame.QUIT:
            run_game = False
    # Update
    # Updating all of the moving objects that we have in the game
    all_sprites.update()


    # Draw

    screen.fil(0, 255, 0)
    all_sprites.draw(screen)
    # after drawing everything, flip
    pygame.display.flip()

pygame.quit()
