import pygame
import os
import random
import math
from os.path import join
pygame.init()

pygame.display.set_caption("Scratch Wars")

WIDTH, HEIGHT = 1000, 600
FPS = 60

window = pygame.display.set_mode((WIDTH, HEIGHT))

class Enemyships(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed, name, player):
        super().__init__()
        self.rect = pygame.Rect(x, y, height, width)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.player = player
        self.name = name

    def move_eship(self):
        if self.player.x - self.x < 0:
            self.x -= self.speed
        elif self.player.x - self.x > 0:
            self.x += self.speed

        if self.player.y - self.y < 0:
            self.y -= self.speed
        elif self.player.y - self.y > 0:
            self.y += self.speed

    def draw_eship(self, scroll_x):
        Hship_sprite = pygame.image.load(join("assets", self.name))
        Hship_sprite = pygame.transform.scale(Hship_sprite, (self.width, self.height))
        Hship_sprite = pygame.transform.rotate(Hship_sprite, -90.0)
        window.blit(Hship_sprite, (self.x - scroll_x, self.y))

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.time_limit = 20000
        self.start_time = None
        self.approach_planet = False

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
        if self.x > 500: 
            current_time = pygame.time.get_ticks()

            if self.x_speed != 0 and self.start_time is None:
                self.start_time = current_time
            
            if self.start_time is not None:
                if current_time - self.start_time >= self.time_limit and self.x_speed > 0:
                    self.approach_planet = True

    def draw_player(self, scroll_x):
        keys = pygame.key.get_pressed()
        player_sprite = pygame.image.load("assets/player_ship.png")
        player_sprite = pygame.transform.scale(player_sprite, (self.width, self.height))
        player_sprite = pygame.transform.rotate(player_sprite, 90.0)
        if keys[pygame.K_w]:
            player_sprite = pygame.transform.rotate(player_sprite, 90.0)
        elif keys[pygame.K_a]:
            player_sprite = pygame.transform.rotate(player_sprite, 180.0)
        elif keys[pygame.K_d]:
            player_sprite = pygame.transform.rotate(player_sprite, 0.0)
        elif keys[pygame.K_s]:
            player_sprite = pygame.transform.rotate(player_sprite, 270.0)

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

        for i in range(50):
            frame = self.planet_sprite.subsurface((i * self.frame_width, 0, self.frame_width, self.frame_height))
            frame = pygame.transform.scale(frame, (self.width, self.height))
            self.frames.append(frame)

    def update_planet(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_frame_time >= self.animation_speed:
            self.current_frame = (self.current_frame + 1) % 50
            self.last_frame_time = current_time

    def draw_planet(self):
        window.blit(self.frames[self.current_frame], (self.x, self.y))

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y, x2, y2, width, height, player, trigger_point):
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
        self.trigger_point = trigger_point

        self.ast_speed = 5
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
        if self.player.x > self.trigger_point:
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

    def draw_ast(self):
        window.blit(self.frames[self.current_frame], (self.x, self.y))


def make_background():
    image = pygame.image.load("assets/space_background.png").convert()

    image = pygame.transform.scale(image, (WIDTH, HEIGHT))
    flipped_image = pygame.transform.flip(image, True, False)

    return image, flipped_image

def draw(window, background, scroll_x):
    image, flipped_image = background
    image_set = int(scroll_x // WIDTH)

    for i in range(image_set, image_set + 3):
        pos_x = (i * WIDTH - scroll_x)

        if i % 2 == 0:
            window.blit(image, (pos_x, 0))
        elif i % 2 != 0:
            window.blit(flipped_image, (pos_x, 0))

def main(window):
    clock = pygame.time.Clock()
    background = make_background()
    player = Player(70, 250, 50, 50)
    asteroid1 = Asteroid(800, -100, 0, 600, 100, 100, player, 500)
    asteroid2 = Asteroid(200, 680, 900, -100, 100, 100, player, 700)
    asteroid3 = Asteroid(-100, 500, 1200, -100, 100, 100, player, 1000)
    planet = Planet(800, 200, 150, 150, player)
    enemyship1 = Enemyships(900, 700, 60, 60, 2, "enemyBlack1.png", player)
    scroll_x = 0

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        player.move_player()
        enemyship1.move_eship()
        if not player.approach_planet:
            scroll_x = max(0, player.x - 500)

        draw(window, background, scroll_x)
        player.draw_player(scroll_x)
        enemyship1.draw_eship(scroll_x)
        asteroid1.draw_ast()
        asteroid2.draw_ast()
        asteroid3.draw_ast()
        planet.draw_planet()
        

        planet.update_planet()
        asteroid1.update_ast()
        asteroid2.update_ast()
        asteroid3.update_ast()
        pygame.display.update()

    pygame.quit()
    quit()

if __name__ == "__main__":
    main(window)