import pygame
import os
import random
import math
from os import listdir
from os.path import isfile, join
pygame.init()

pygame.display.set_caption("Scratch Wars")

WIDTH, HEIGHT = 1000, 600
FPS = 60

window = pygame.display.set_mode((WIDTH, HEIGHT))

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, height, width):
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.x_speed = 0
        self.y_speed = 0

    def draw_player(self):
        player_sprite = pygame.image.load("assets/player_ship.png")
        player_sprite = pygame.transform.rotate(player_sprite, 90.0)
        player_sprite = pygame.transform.scale(player_sprite, (self.width, self.height))
        window.blit(player_sprite, (self.x, self.y))


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

def main(window):
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        background = make_background()

        player = Player(100, 100, 100, 100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        draw(window, background)
        player.draw_player()

        pygame.display.update()

    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)