import pygame
import sys

from pygame.locals import *

pygame.init()

size = width, height = 1600, 900
black = 0, 0, 0
white = 255, 255, 255

screen = pygame.display.set_mode(size)

girl = pygame.image.load("Girl_Right.gif")
# Source: opengameart.org
# Author: Mandi Paugh

sprite_coordinates = [0, 850]
pygame.key.set_repeat(1, 1)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
            elif event.key == K_a:
                sprite_coordinates[0] = sprite_coordinates[0] - 1
                girl = pygame.image.load("Girl_Left.gif")
                if sprite_coordinates[0] == -1:
                    sprite_coordinates[0] = 0
            elif event.key == K_d:
                sprite_coordinates[0] = sprite_coordinates[0] + 1
                girl = pygame.image.load("Girl_Right.gif")
                if sprite_coordinates[0] == 1568:
                    sprite_coordinates[0] = 1567
    screen.fill(black)
    pygame.draw.line(screen, (255, 255, 255), (1, 899), (1599, 899), 5)
    screen.blit(girl, sprite_coordinates)
    pygame.display.flip()
