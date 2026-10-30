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

class Chasingships(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, height, width):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.x_speed = 0
        self.y_speed = 0
        self.accleration = 0.2
        self.max_speed = 5
        self.friction = 0.2

    def move_player(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.x_speed -= self.accleration
        if keys[pygame.K_d]:
            self.x_speed += self.accleration
        if keys[pygame.K_w]:
            self.y_speed -= self.accleration
        if keys[pygame.K_s]:
            self.y_speed += self.accleration

        if not keys[pygame.K_a] and not keys[pygame.K_d]:
            if self.x_speed > 0:
                self.x_speed = max(0, self.x_speed - self.friction)
            elif self.x_speed < 0:
                self.x_speed = min(0, self.x_speed + self.friction)

        if not keys[pygame.K_w] and not keys[pygame.K_s]:
            if self.y_speed > 0:
                self.y_speed = max(0, self.y_speed - self.friction)
            elif self.y_speed < 0:
                self.y_speed = min(0, self.y_speed + self.friction)

        self.x_speed = max(-self.max_speed, min(self.x_speed, self.max_speed))
        self.y_speed = max(-self.max_speed, min(self.y_speed, self.max_speed))

        self.x += self.x_speed
        self.y += self.y_speed

        self.rect.topleft = round(self.x), round(self.y)

    def draw_player(self, scroll_x):
        player_sprite = pygame.image.load("assets/player_ship.png")
        player_sprite = pygame.transform.rotate(player_sprite, 90.0)
        player_sprite = pygame.transform.scale(player_sprite, (self.width, self.height))
        self.move_player()
        window.blit(player_sprite, (self.x - scroll_x, self.y))

class Planet(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, player):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.player = player

        self.planet_sprite = pygame.image.load("assets/planet.png").convert_alpha()
        self.frame_width = 100
        self.frame_height = 100
        self.frames = []

        self.current_frame = 0
        self.last_frame_time = pygame.time.get_ticks()
        self.animation_speed = 100

        self.time_limit = 5000
        self.start_time = None

        for i in range(50):
            frame = self.planet_sprite.subsurface((i * self.frame_width, 0, self.frame_width, self.frame_height))
            frame = pygame.transform.scale(frame, (self.width, self.height))
            self.frames.append(frame)

    def update_planet(self):
        current_time = pygame.time.get_ticks()

        if self.player.x_speed != 0 and self.start_time is None:
            self.start_time = current_time

        if self.start_time is not None:
            if current_time - self.start_time >= self.time_limit and self.player.x_speed != 0:
                self.x -= 2

        if current_time - self.last_frame_time >= self.animation_speed:
            self.current_frame = (self.current_frame + 1) % 50
            self.last_frame_time = current_time

    def draw_planet(self):
        window.blit(self.frames[self.current_frame], (self.x, self.y))

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y, x2, y2, width, height, player):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2
        self.width = width
        self.height = height
        self.player = player
        self.passed = False

        self.ast_speed = 4
        self.ast_sprite = pygame.image.load("assets/asteroid.png").convert_alpha()
        self.frame_width = 100
        self.frame_height = 100
        self.frames = []

        self.current_frame = 0
        self.last_frame_time = pygame.time.get_ticks()
        self.animation_speed = 100

        for i in range(50):
            frame = self.ast_sprite.subsurface((i * self.frame_width, 0, self.frame_width, self.frame_height))
            frame = pygame.transform.scale(frame, (self.width, self.height))
            self.frames.append(frame)

    def update_ast(self):
        current_time = pygame.time.get_ticks()
        if self.player.x > 500:
            self.passed = True

        if self.passed:
            if self.x2 - self.x < 0:
                self.x -= self.ast_speed
            elif self.x2 - self.x > 0:
                self.x += self.ast_speed
            
            if self.y2 - self.y < 0:
                self.y -= self.ast_speed
            elif self.y2 - self.y > 0:
                self.y += self.ast_speed
            
            
            if current_time - self.last_frame_time >= self.animation_speed:
                self.current_frame = (self.current_frame + 1) % 50
                self.last_frame_time = current_time

    def draw_ast(self, scroll_x):
        window.blit(self.frames[self.current_frame], (self.x - scroll_x, self.y))


def make_background():
    image = pygame.image.load("assets/space_background.png").convert()

    image = pygame.transform.scale(image, (WIDTH, HEIGHT))
    flipped_image = pygame.transform.flip(image, True, False)
    number_of_bg = 5

    tiles = []

    for i in range(number_of_bg):
        pos = [WIDTH * i, 0]

        if i % 2 == 0:
            tiles.append((pos, image))
        else:
            tiles.append((pos, flipped_image))

    return tiles

def draw(window, background, scroll_x):
    for pos, image in background:
        window.blit(image, (pos[0] - scroll_x, pos[1]))

def main(window):
    clock = pygame.time.Clock()
    background = make_background()
    player = Player(70, 250, 50, 50)
    asteroid = Asteroid(800, -80, 0, 600, 100, 100, player)
    planet = Planet(800, 200, 150, 150, player)
    scroll_x = 0

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        draw(window, background, scroll_x)
        player.draw_player(scroll_x)
        asteroid.draw_ast(scroll_x)
        planet.draw_planet()

        planet.update_planet()
        asteroid.update_ast()
        pygame.display.update()

        if player.x > 500:
            scroll_x += player.x_speed

    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)