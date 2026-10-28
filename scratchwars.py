import pygame
import os
import random
import math
from os import listdir
from os.path import isfile, join
pygame.init()

pygame.display.set_caption("Scratch Wars")

Background_color = (255, 255, 255)
WIDTH, HEIGHT = 1000, 600
FPS = 60

window = pygame.display.set_mode((WIDTH, HEIGHT))

def make_background():
    image = pygame.image.load("assets/space_background.png").convert()

    image = pygame.transform.scale(image, (WIDTH, HEIGHT))
    flipped_image = pygame.transform.flip(image, True, False)

    tiles = []

    for i in range(2):
        pos = (WIDTH * i, 0)

        if i % 2 == 0:
            tiles.append((pos, image))
        else:
            tiles.append((pos, flipped_image))

    return tiles

def draw(window, background):
    for pos, image in background:
        window.blit(image, pos)

    pygame.display.update()

def main(window):
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        background = make_background()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        draw(window, background)

    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)