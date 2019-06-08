import pygame
import sys

from pygame.locals import *

pygame.init()

size = width, height = 1600, 900
black = 0, 0, 0
white = 255, 255, 255

jump_height = 75
jumping = False
falling = False
jump_distance = 0

screen = pygame.display.set_mode(size)
pygame.mixer.music.load("BGM.wav")
#Patakas World
#www.dl-sounds.com

pygame.mixer.music.play(-1)

pygame.display.set_caption("Puzzle Box")
girl = pygame.image.load("Girl_Right.gif")

# Source: opengameart.org
# Author: Mandi Paugh

sprite_coordinates = [0, 850]

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
    screen.fill(black)
    keys = pygame.key.get_pressed()
    if keys[K_a] == True:
        sprite_coordinates[0] -= 1
        girl = pygame.image.load("Girl_Left.gif")
        if sprite_coordinates[0] == -1:
            sprite_coordinates[0] = 0

    elif keys[K_d] == True:
        sprite_coordinates[0] += 1
        girl = pygame.image.load("Girl_Right.gif")
        if sprite_coordinates[0] == 1568:
            sprite_coordinates[0] = 1567

    if keys[K_j] == True and jumping == False and falling == False:
        jumping = True

    if jumping == True:
        sprite_coordinates[1] -= 1
        jump_distance += 1
    elif falling == True:
        sprite_coordinates[1] += 1
        jump_distance -= 1

    if jump_distance == jump_height:
        jumping = False
        falling = True
    if jump_distance == 0 and falling == True:
        falling = False

    pygame.draw.line(screen, white, (1, 899), (1599, 899), 5)
    screen.blit(girl, sprite_coordinates)
    pygame.display.flip()
