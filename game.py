import pygame
import sys
import time

from pygame.locals import *

pygame.init()
width = 1280
height = 720
black = 0, 0, 0
white = 255, 255, 255
red = 200,0,0
green = 0,200,0
bright_red = (255,0,0)
bright_green = (0,255,0)
backgroundIntro = 56,142,142
gameDisplay = pygame.display.set_mode((width,height))
pygame.display.set_caption('Puzzle Game')
clock = pygame.time.Clock()
gameObjs = []

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = text_objects("Puzzle Game", largeText)
    TextRect.center = ((width / 2), (height / 2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    time.sleep(2)
    game()


def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(backgroundIntro)
        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects("Puzzle Game", largeText)
        TextRect.center = ((width/2),(height/2))
        gameDisplay.blit(TextSurf, TextRect)
        button("Start", 600, 450, 100, 50, green, bright_green, game)
        button("Quit", 600, 550, 100, 50, red, bright_red, quitgame)
        pygame.display.update()
        clock.tick(15)


def quitgame():
    quit()

def load_level(filename):
    f = open(filename)
    player_location = f.readline()
    for i in range(1, 50):
        for j in range(1, 30):
            gameObjs.append()


from pygame.locals import *


def game():
    pygame.init()

    path = "./characters/Jill/"

    size = width, height = 1280, 720
    black = 0, 0, 0
    white = 255, 255, 255

    #jumping = False
    face_direction = 1
    # 0: Left  1: Right

    screen = pygame.display.set_mode(size)

    pygame.mixer.music.load("BGM.wav")
    # Patakas World
    # www.dl-sounds.com
    pygame.mixer.music.play(-1)

    pygame.display.set_caption("Puzzle Box")

    block_coordinates = [200, height - 48]

    class Player(pygame.sprite.Sprite):

        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.img = pygame.image.load(path + "Right.gif")
            # Source: opengameart.org
            # Name from source: Sara and Star
            # Artist: Mandi Paugh
            self.rect = self.img.get_rect()
            self.coordinates = 0, 0
            self.rect.x, self.rect.y = self.coordinates
            self.jumping = False
            self.falling = False
            self.jump_distance = 0
            self.jump_height = 75
            self.speedX = 0
            self.speedY = 0
            self.accelY = 0
            self.max_accel = 30
            self.max_speed = 5

        def check_collision(self, sprite1, sprite2):
            collided = pygame.sprite.collide_rect(sprite1, sprite2)
            if collided and self.rect.y < sprite2.rect.y and self.falling:
                # using this as there is no other instance where both should be true at the same time
                self.jumping = False
                self.falling = False
                self.jump_distance = 0

            elif collided and self.rect.x <= sprite2.rect.x and not (self.rect.y <= sprite2.rect.y):
                self.update_position(-5, 0)
            elif collided and self.rect.x >= sprite2.rect.x and not (self.rect.y <= sprite2.rect.y):
                self.update_position(5, 0)

        def update_position(self, offset_x, offset_y):
            self.rect.x += offset_x
            self.rect.y += offset_y
            self.coordinates = self.rect.x, self.rect.y

        def jump(self):
            if self.falling == True:
                self.fall()
            elif self.jump_distance > self.jump_height:
                self.jumping = False
                self.falling = True
                self.fall()
            elif not self.jumping:
                self.jumping = True
            if self.jumping and not self.falling:
                self.update_position(0, -3)
                self.jump_distance += 3
                return True

        def fall(self):
            if pygame.sprite.collide_rect(self, block) and self.rect.y < block.rect.y - 40:
                self.falling = False
                self.jump_distance = 0
            elif self.rect.y > height - 48:
                self.rect.y = height - 48
                self.jump_distance = 0
                self.falling = False
            else:
                self.update_position(0,3)
                self.falling = True
                return

    class GameObj(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.img = pygame.image.load("./sprites/block24x.png")
            self.rect = self.img.get_rect()
            self.coordinates = 0, 0
            self.rect.x, self.rect.y = self.coordinates

        def update_position(self, offset_x, offset_y):
            self.rect.x += offset_x
            self.rect.y += offset_y
            self.coordinates = self.rect.x, self.rect.y

    # Source: opengameart.org
    # Name from source: Sara and Star
    # Artist: Mandi Paugh

    player = Player()
    player.update_position(0, height - 48)

    #changed block class to GameObj class
    block = GameObj()
    block.update_position(200, height - 48)

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
                        player.img = pygame.image.load(path + "Left.gif")
                    elif face_direction == 1:
                        player.img = pygame.image.load(path + "Right.gif")

                elif event.key == K_j:
                    jumping = True

        screen.fill(black)
        keys = pygame.key.get_pressed()
        if keys[K_a]:
            player.update_position(-5, 0)
            face_direction = 0
            player.img = pygame.image.load(path + "Left.gif")
            if player.coordinates[0] <= 0:
                player.update_position(5, 0)

        elif keys[K_d]:
            player.update_position(5, 0)
            face_direction = 1
            player.img = pygame.image.load(path + "Right.gif")
            if player.coordinates[0] >= width - 32:
                player.update_position(-5, 0)

        if keys[K_j]:
            player.jump()
        elif not keys[K_j]:
            player.fall()

        player.check_collision(player, block)

        fps = pygame.time.Clock()
        fps.tick(60)
        pygame.draw.line(screen, white, (0, 720), (1280, 720), 5)
        screen.blit(player.img, player.coordinates)
        screen.blit(block.img, block_coordinates)
        pygame.display.flip()
