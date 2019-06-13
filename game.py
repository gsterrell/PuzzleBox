import pygame
import sys

from pygame.locals import *

def game():
    pygame.init()

    path = "./characters/Jill/"

    size = width, height = 1280, 720
    black = 0, 0, 0
    white = 255, 255, 255

    jump_height = 75
    jumping = False
    falling = False
    jump_distance = 0
    face_direction = 1
    # 0: Left  1: Right

    screen = pygame.display.set_mode(size)

    pygame.mixer.music.load("BGM.wav")
    # Patakas World
    # www.dl-sounds.com
    pygame.mixer.music.play(-1)

    pygame.display.set_caption("Puzzle Box")

    character = pygame.image.load(path + "Right.gif")
    # Source: opengameart.org
    # Name from source: Sara and Star
    # Artist: Mandi Paugh

    sprite_coordinates = [0, 670]

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()

                elif event.key == K_c:
                    if path == "./characters/Jill/":
                        path = "./characters/Jack/"
                    elif path == "./characters/Jack/":
                        path = "./characters/Jill/"

                    if face_direction == 0:
                        character = pygame.image.load(path + "Left.gif")
                    elif face_direction == 1:
                        character = pygame.image.load(path + "Right.gif")

        screen.fill(black)
        keys = pygame.key.get_pressed()
        if keys[K_a] == True:
            sprite_coordinates[0] -= 5
            face_direction = 0
            character = pygame.image.load(path + "Left.gif")
            if sprite_coordinates[0] < 0:
                sprite_coordinates[0] = 0

        elif keys[K_d] == True:
            sprite_coordinates[0] += 5
            face_direction = 1
            character = pygame.image.load(path + "Right.gif")
            if sprite_coordinates[0] > 1247:
                sprite_coordinates[0] = 1247

        if keys[K_j] == True and jumping == False and falling == False:
            jumping = True

        if jumping == True:
            sprite_coordinates[1] -= 3
            jump_distance += 3
        elif falling == True:
            sprite_coordinates[1] += 3
            jump_distance -= 3

        if jump_distance == jump_height:
            jumping = False
            falling = True
        if jump_distance == 0 and falling == True:
            falling = False
        fps = pygame.time.Clock()
        fps.tick(60)
        pygame.draw.line(screen, white, (0, 720), (1280, 720), 5)
        screen.blit(character, sprite_coordinates)
        pygame.display.flip()