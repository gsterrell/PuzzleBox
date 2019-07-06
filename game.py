import pygame
import sys
import time
import re

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
icon = pygame.image.load("./sprites/icon.jpg")
pygame.display.set_icon(icon)
gameDisplay = pygame.display.set_mode((width,height))
pygame.display.set_caption('Puzzle Game')
clock = pygame.time.Clock()

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

def game():
    pygame.init()

    characterpath = "./characters/Jill/"
    objectpath = "./sprites/"

    size = width, height = 1280, 720
    black = 0, 0, 0
    gameObjs = []
    current_level = "level1.lvl"
    unit_size = 24
    fullupdate = True
    green = (0, 255, 0)
    blue = (0, 0, 128)

    #jumping = False
    face_direction = 1
    # 0: Left  1: Right

    screen = pygame.display.set_mode(size)

    pygame.mixer.music.load("BGM.wav")
    # Patakas World
    # www.dl-sounds.com
    pygame.mixer.music.play(-1)

    pygame.display.set_caption("Puzzle Box")

    class Player(pygame.sprite.Sprite):

        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            starting_position = 500, 500
            self.img = pygame.image.load(characterpath + "Right.gif")
            # Source: opengameart.org
            # Name from source: Sara and Star
            # Artist: Mandi Paugh
            self.rect = self.img.get_rect()
            self.coordinates = starting_position
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

        def check_collision(self, game_obj):
            collided = pygame.sprite.collide_rect(self, game_obj)
            if collided:
                if game_obj.get_type() in ['floor', 'wall', 'ClosedBarrier']:
                    if (self.rect.y + 45 <= game_obj.rect.y) and self.falling:
                        # using this as there is no other instance where both should be true at the same time
                        self.update_position(0, -3)
                        self.jumping = False
                        self.falling = False
                        self.jump_distance = 0
                    elif (self.rect.x <= game_obj.rect.x) and (self.rect.y > (game_obj.rect.y - 47)):
                        self.update_position(-4, 0)
                    elif (self.rect.x >= game_obj.rect.x) and (self.rect.y > (game_obj.rect.y - 47)):
                        self.update_position(4, 0)
                    if (pygame.sprite.collide_rect(self, game_obj)) and (self.rect.y > game_obj.rect.y):
                        self.update_position(0, 3)
                        self.jumping = False
                        self.falling = True

                elif game_obj.get_type() == "goal":
                    for x in range(-3, 3):
                        for y in range(-3, 3):
                            if (self.rect.x + x == game_obj.rect.x) and (self.rect.y + y == game_obj.rect.y):
                                return "GOAL"
                elif game_obj.get_type() == 'switch':
                    for maybe_goal in gameObjs:
                        if maybe_goal.get_type() in ['ClosedBarrier'] and game_obj.obj_num == maybe_goal.obj_num:
                            maybe_goal.set_type("OpenBarrier")
                            return "SWITCH"

                return True
            return False

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
            for each in gameObjs:
                if self.rect.y < each.rect.y - unit_size:
                    self.falling = False
                    self.jump_distance = 0
                if self.rect.y > height - 48:
                    self.rect.y = height - 48
                    self.jump_distance = 0
                    self.falling = False
                else:
                    self.update_position(0,3)
                    self.falling = True
                    return

    class GameObj(pygame.sprite.Sprite):
        def __init__(self, image_path, the_type, posx, posy):
            pygame.sprite.Sprite.__init__(self)
            self.img = pygame.image.load(image_path)
            self.rect = self.img.get_rect()
            self.coordinates = posx, posy
            self.rect.x, self.rect.y = self.coordinates
            self.type = str(the_type)
            self.obj_num = '0'

        def update_position(self, offset_x, offset_y):
            self.rect.x += offset_x
            self.rect.y += offset_y
            self.coordinates = self.rect.x, self.rect.y

        def set_type(self, the_type):
            self.img = pygame.image.load(objectpath + the_type + ".png")
            self.type = str(the_type)

        def get_type(self):
            return str(self.type)

    def load_level(the_level):
        gameObjs.clear()
        level = open("./levels/" + the_level)
        for i, line in enumerate(level):
            if i == 0:
                starting_position = line
            elif i == 31:
                return line, starting_position
            else:
                for j, word in enumerate(line.split()):
                    if word != 'empty':
                        if not word.isalpha():
                            words = word.split(':')
                            new_object = GameObj("./sprites/" + str(words[0]) + ".png", str(word[0]), unit_size * j, unit_size * (i - 1))
                            new_object.obj_num = str(words[1])
                            new_object.type = str(words[0])
                        else:
                            new_object = GameObj("./sprites/" + word + ".png", word, unit_size*j, unit_size*(i-1))

                        gameObjs.append(new_object)

    # Source: opengameart.org
    # Name from source: Sara and Star
    # Artist: Mandi Paugh

    player = Player()

    # load the level information
    current_level, player.coordinates = load_level(current_level)
    player.rect.x = int(player.coordinates.strip().split(", ")[0])
    player.rect.y = int(player.coordinates.strip().split(", ")[1])
    player.coordinates = player.rect.x, player.rect.y

    starttime = pygame.time.get_ticks()
    frames = 0
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()

                elif event.key == K_c:
                    if characterpath == "./characters/Jill/":
                        characterpath = "./characters/Jack/"
                    elif characterpath == "./characters/Jack/":
                        characterpath = "./characters/Jill/"

                    if face_direction == 0:
                        player.img = pygame.image.load(characterpath + "Left.gif")
                    elif face_direction == 1:
                        player.img = pygame.image.load(characterpath + "Right.gif")
                elif event.key == K_r:
                    fullupdate = True

        pygame.draw.rect(screen, black, player.rect)
        keys = pygame.key.get_pressed()
        if keys[K_a]:
            player.update_position(-4, 0)
            face_direction = 0
            player.img = pygame.image.load(characterpath + "Left.gif")
            if player.coordinates[0] <= 0:
                player.update_position(4, 0)

        elif keys[K_d]:
            player.update_position(4, 0)
            face_direction = 1
            player.img = pygame.image.load(characterpath + "Right.gif")
            if player.coordinates[0] >= width - 32:
                player.update_position(-4, 0)

        if keys[K_j]:
            player.jump()
        elif not keys[K_j]:
            player.fall()

        updates = [pygame.Rect(player.rect.x - 10, player.rect.y - 6, 52, 60), pygame.Rect(100, 100, 500, 100)]

        for level_object in gameObjs:
            collided = player.check_collision(level_object)
            if collided == "GOAL":
                current_level, player.coordinates = load_level(current_level)
                player.rect.x = int(player.coordinates.strip().split(", ")[0])
                player.rect.y = int(player.coordinates.strip().split(", ")[1])
                player.coordinates = player.rect.x, player.rect.y
                fullupdate = True
            elif collided == "SWITCH":
                fullupdate = True
            elif collided:
                screen.blit(level_object.img, level_object.coordinates)
                updates.append(level_object.rect)

        fps = pygame.time.Clock()
        fps.tick(80)

        font = pygame.font.Font('freesansbold.ttf', 32)

        currtime = pygame.time.get_ticks()
        frames += 1
        text = font.render(str(frames / ((currtime-starttime) / 1000)), True, green, blue)
        screen.blit(text, (100, 100))

        if fullupdate == True:
            screen.fill(black)
            screen.blit(player.img, player.coordinates)

            for thing in gameObjs:
                screen.blit(thing.img, thing.coordinates)

            pygame.display.flip()
            fullupdate = False

        else:
            screen.blit(player.img, player.coordinates)
            pygame.display.update(updates)