import pygame
import sys
import time

from pygame.locals import *

pygame.init()
width = 1272
height = 720
black = 0, 0, 0
white = 255, 255, 255
red = 200,0,0
green = 0,200,0
blue = 0, 0, 100
bright_red = (255,0,0)
bright_green = (0,255,0)
bright_blue = (0, 0, 255)
grey = 102,102,102
backgroundIntro = 56,142,142
icon = pygame.image.load("./sprites/icon.jpg")
pygame.display.set_icon(icon)
gameDisplay = pygame.display.set_mode((width, height))
pygame.display.set_caption('Puzzle Game')
clock = pygame.time.Clock()
continued = False
current_level = "level1.lvl"
next_level = "level2.lvl"

def pause():
    paused = True
    pygame.draw.rect(gameDisplay, grey, (440, 200, 400, 80))
    largeText = pygame.font.Font('freesansbold.ttf', 50)
    TextSurf, TextRect = text_objects("Game Paused!", largeText, white)
    TextRect.center = ((width / 2), (height / 3))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.draw.rect(gameDisplay, grey, (340, 320, 590, 70))
    mediumText = pygame.font.Font('freesansbold.ttf', 30)
    TextSurf, TextRect = text_objects("Press 'C' to Continue or 'Q' to Quit", mediumText, white)
    TextRect.center = ((width / 2), (height / 2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_c:
                    paused = False
                #ullupdate = True
                elif event.key == K_q:
                    pygame.quit()
                    quit()


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
    textSurf, textRect = text_objects(msg, smallText, black)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)


def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
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
        TextSurf, TextRect = text_objects("Puzzle Game", largeText, black)
        TextRect.center = ((width/2),(height/2))
        gameDisplay.blit(TextSurf, TextRect)
        button("Start", 600, 450, 100, 50, green, bright_green, game)
        button("Continue", 600, 550, 100, 50, blue, bright_blue, continue_game)
        button("Quit", 600, 650, 100, 50, red, bright_red, quitgame)
        pygame.display.update()
        clock.tick(80)


def quitgame():
    quit()


def load_settings():
    global current_level, next_level
    try:
        file = open("settings.ini")
        current_level = file.readline()
        file.close()
        level = open("./levels/" + current_level)
        for i, line in enumerate(level):
            if i == 30:
                next_level = line
        level.close()
    except IOError:
        current_level = "level1.lvl"
        next_level = "level2.lvl"


def save_settings(saved_level):
    global current_level
    file = open("settings.ini", 'w')
    file.write(saved_level)
    file.close()


def continue_game():
    global continued
    try:
        if open("settings.ini") is False:
            continued = False
        else:
            continued = True
    except IOError:
        continued = False
    game()


def game():
    pygame.init()

    characterpath = "./characters/Jill/"
    objectpath = "./sprites/"

    size = width, height = 1272, 720
    black = 0, 0, 0
    gameObjs = []
    barrier_objects = []
    movebox_objects = []
    switch_objects = []
    plate_objects = []
    wall_objects = []

    global current_level, next_level, continued

    if continued is False:
        current_level = "level1.lvl"
        next_level = "level1.lv2"
    else:
        load_settings()

    unit_size = 24
    fullupdate = True
    green = (0, 255, 0)
    blue = (0, 0, 128)

    #jumping = False
    face_direction = 1
    # 0: Left  1: Right

    screen = pygame.display.set_mode(size)

    pygame.mixer.music.load("./sounds/BGM.wav")
    # Patakas World
    # www.dl-sounds.com
    pygame.mixer.music.play(-1)

    # Credit to Michael Baradari
    # Release under CC-BY 3.0
    barrier_sound = pygame.mixer.Sound('./sounds/doorsound.wav')

    # Credit to Jesús Lastra
    # Public Domain CC0
    jump_sound = pygame.mixer.Sound('./sounds/jump.wav')

    # Credit to  Dan Knoflicek
    # Release under CC-BY 3.0
    box_sound = pygame.mixer.Sound('./sounds/box_drop.wav')

    pygame.display.set_caption("Puzzle Box")

    class Player(pygame.sprite.Sprite):

        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            starting_position = 500, 500
            self.img = pygame.image.load(characterpath + "Right.gif")
            self.overwrite = pygame.image.load(characterpath + "Right_Overwrite.gif")
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
            self.carrying = [False]

        def check_collision(self, game_obj):
            collided = pygame.sprite.collide_rect(self, game_obj)
            if collided:
                if game_obj.get_type() in ['floor', 'wall', 'ClosedBarrier']:
                    if (self.rect.y + 45 <= game_obj.rect.y) and self.falling:
                        # using this as there is no other instance where both should be true at the same time
                        self.update_position(0, -3)
                        if self.carrying[0]:
                            self.carrying[1].update_position(0,-3)
                        self.jumping = False
                        self.falling = False
                        self.jump_distance = 0
                    elif (self.rect.x <= game_obj.rect.x) and (self.rect.y > (game_obj.rect.y - 47)):
                        self.update_position(-4, 0)
                        if self.carrying[0]:
                            self.carrying[1].update_position(-4, 0)
                    elif (self.rect.x >= game_obj.rect.x) and (self.rect.y > (game_obj.rect.y - 47)):
                        self.update_position(4, 0)
                        if self.carrying[0]:
                            self.carrying[1].update_position(4 ,0)
                    if (pygame.sprite.collide_rect(self, game_obj)) and (self.rect.y > game_obj.rect.y):
                        self.update_position(0, 3)
                        if self.carrying[0]:
                            self.carrying[1].update_position(0,3)
                        self.jumping = False
                        self.falling = True

                elif game_obj.get_type() == "goal":
                    for x in range(-3, 3):
                        for y in range(-3, 3):
                            if (self.rect.x + x == game_obj.rect.x) and (self.rect.y + y == game_obj.rect.y):
                                game_obj.collided = True
                                return "GOAL"
                elif game_obj.get_type() == 'redswitch':
                    for maybe_goal in barrier_objects:
                        if maybe_goal.get_type() in ['ClosedBarrier'] and game_obj.obj_num == maybe_goal.obj_num:
                            maybe_goal.set_type("OpenBarrier")
                            game_obj.collided = True
                            game_obj.set_type('greenswitch')
                            barrier_sound.play()
                            return "SWITCH"
                elif game_obj.get_type() == 'movebox':
                    if (self.rect.y + 45 <= game_obj.rect.y) and self.falling:
                        # using this as there is no other instance where both should be true at the same time
                        self.update_position(0, -3)
                        if self.carrying[0]:
                            self.carrying[1].update_position(0, -3)
                        self.jumping = False
                        self.falling = False
                        self.jump_distance = 0
                    game_obj.collided = True
                    return "MOVEBOX"
                elif game_obj.get_type() == 'helpbox' and game_obj.collided == False:
                    game_obj.collided = True
                    return ["helpbox", int(game_obj.obj_num)]
                game_obj.collided = True
                return True
            elif self.carrying[0] and (pygame.sprite.collide_rect(self.carrying[1], game_obj)):
                game_obj.collided = True
                if game_obj.get_type() in ['floor', 'wall', 'ClosedBarrier']:
                    if (self.carrying[1].rect.x <= game_obj.rect.x) and (self.carrying[1].rect.y > (game_obj.rect.y - 47)):
                        self.update_position(-4, 0)
                        self.carrying[1].update_position(-4, 0)
                    elif (self.carrying[1].rect.x >= game_obj.rect.x) and (self.carrying[1].rect.y > (game_obj.rect.y - 47)):
                        self.update_position(4, 0)
                        self.carrying[1].update_position(4, 0)
                    if (pygame.sprite.collide_rect(self.carrying[1], game_obj)) and (self.carrying[1].rect.y > game_obj.rect.y):
                        self.update_position(0, 3)
                        self.carrying[1].update_position(0, 3)
                        self.jumping = False
                        self.falling = True
                return True
            elif game_obj.collided:
                game_obj.collided = False
                if game_obj.get_type() == 'helpbox':
                    pygame.draw.rect(screen, black, pygame.Rect(280, 685, 700, 30))
                    updates.append(pygame.Rect(280, 685, 700, 30))
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
                jump_sound.play()
                self.jumping = True
            if self.jumping and not self.falling:
                self.update_position(0, -3)
                if self.carrying[0]:
                    self.carrying[1].update_position(0,-3)
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
                    if self.carrying[0]:
                        self.carrying[1].update_position(0,3)
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
            self.collided = False

        def update_position(self, offset_x, offset_y):
            self.rect.x += offset_x
            self.rect.y += offset_y
            self.coordinates = self.rect.x, self.rect.y

        def set_type(self, the_type):
            self.img = pygame.image.load(objectpath + the_type + ".png")
            self.type = str(the_type)

        def get_type(self):
            return str(self.type)

        def check_collision(self, game_obj):
            return pygame.sprite.collide_rect(self, game_obj)

    def load_level(the_level):
        gameObjs.clear()
        level = open("./levels/" + the_level)
        helptext = []
        for i, line in enumerate(level):
            if i == 0:
                starting_position = line
            elif i == 1:
                Levelname = line.strip()
            elif i == 30:
                nextlevel = line.strip()
            elif i > 30:
                helptext.append(line.strip()[:])
            else:
                for j, word in enumerate(line.split()):
                    if word != 'empty':
                        if not word.isalpha():
                            words = word.split(':')
                            if words[0] == 'plateup':
                                new_object = GameObj("./sprites/" + str(words[0]) + ".png", str(word[0]), unit_size * j,
                                                     unit_size * (i - 2)-4)
                            else:
                                new_object = GameObj("./sprites/" + str(words[0]) + ".png", str(word[0]), unit_size * j, unit_size * (i - 2))
                            new_object.obj_num = str(words[1])
                            new_object.type = str(words[0])
                        else:
                            new_object = GameObj("./sprites/" + word + ".png", word, unit_size*j, unit_size*(i-2))

                        gameObjs.append(new_object)

                        if new_object.type == 'plateup':
                            plate_objects.append(new_object)
                        if new_object.type == 'ClosedBarrier':
                            barrier_objects.append(new_object)
                        if new_object.type == 'movebox':
                            movebox_objects.append(new_object)
                        if new_object.type == 'greenswitch':
                            switch_objects.append(new_object)
                        if new_object.type == 'wall':
                            wall_objects.append(new_object)
        level.close()
        return nextlevel, starting_position, helptext, Levelname

    # Source: opengameart.org
    # Name from source: Sara and Star
    # Artist: Mandi Paugh

    player = Player()

    # load the level information
    next_level, player.coordinates, helptext, levelname = load_level(current_level)

    player.rect.x = int(player.coordinates.strip().split(", ")[0])
    player.rect.y = int(player.coordinates.strip().split(", ")[1])
    player.coordinates = player.rect.x, player.rect.y

    starttime = pygame.time.get_ticks()
    frames = 0
    while 1:
        updates = [pygame.Rect(100, 100, 500, 100)]
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
                
                elif event.key == K_k:
                    if player.carrying[0] and not player.jumping and not player.falling:
                        box_sound.play()
                        player.carrying[0] = False
                        pygame.draw.rect(screen, black, player.carrying[1].rect)
                        updates.append(player.carrying[1].rect[:])
                        player.carrying[1].update_position(0,48)
                        gameObjs.append(player.carrying[1])
                    else:
                        for level_object in gameObjs:
                            collided = player.check_collision(level_object)
                            if (collided == "MOVEBOX") and (player.carrying[0] == False):
                                player.carrying = [True, level_object]
                                fullupdate = True
                                gameObjs.remove(level_object)
                                player.carrying[1].rect.x = player.rect.x + 3
                                player.carrying[1].rect.y = player.rect.y - 24
                                player.carrying[1].coordinates = player.carrying[1].rect.x, player.carrying[1].rect.y

                elif event.key == K_r:
                    fullupdate = True

                elif event.key == K_s:
                    save_settings(current_level)

                elif event.key == K_p:
                    pause()
                    fullupdate = True

        screen.blit(player.overwrite, player.coordinates)
        updates.append(player.rect[:])
        if player.carrying[0]:
            pygame.draw.rect(screen, black, player.carrying[1].rect)
            updates.append(player.carrying[1].rect[:])
        keys = pygame.key.get_pressed()
        if keys[K_a]:
            player.update_position(-4, 0)
            if player.carrying[0]:
                player.carrying[1].update_position(-4,0)
            face_direction = 0
            player.img = pygame.image.load(characterpath + "Left.gif")
            player.overwrite = pygame.image.load(characterpath + "Left_Overwrite.gif")
            if player.coordinates[0] <= 0:
                player.update_position(4, 0)
                if player.carrying[0]:
                    player.carrying[1].update_position(4, 0)

        elif keys[K_d]:
            player.update_position(4, 0)
            if player.carrying[0]:
                player.carrying[1].update_position(4, 0)
            face_direction = 1
            player.img = pygame.image.load(characterpath + "Right.gif")
            player.overwrite = pygame.image.load(characterpath + "Right_Overwrite.gif")
            if player.coordinates[0] >= width - 32:
                player.update_position(-4, 0)
                if player.carrying[0]:
                    player.carrying[1].update_position(-4, 0)

        if keys[K_j]:
            player.jump()
        elif not keys[K_j]:
            player.fall()

        for obj in plate_objects:
            collision = False
            for objb in movebox_objects:
                if obj.check_collision(objb):
                    collision = True
            if obj.check_collision(player):
                collision = True
            if collision and obj.type == "plateup":
                if barrier_objects[int(obj.obj_num) - 1].get_type() == "ClosedBarrier":
                    barrier_objects[int(obj.obj_num) - 1].set_type("OpenBarrier")
                    obj.set_type('platedown')
                    obj.update_position(0, 3)
                    barrier_sound.play()
                    fullupdate = True
            if collision == False and obj.type == "platedown":
                if barrier_objects[int(obj.obj_num) - 1].get_type() == "OpenBarrier":
                    barrier_objects[int(obj.obj_num) - 1].set_type("ClosedBarrier")
                    obj.set_type('plateup')
                    obj.update_position(0,-3)
                    barrier_sound.play()
                    fullupdate = True

        for level_object in gameObjs:
            collided = player.check_collision(level_object)
            if collided == "GOAL":
                current_level = next_level
                next_level, player.coordinates, helptext, levelname = load_level(next_level)
                player.rect.x = int(player.coordinates.strip().split(", ")[0])
                player.rect.y = int(player.coordinates.strip().split(", ")[1])
                player.coordinates = player.rect.x, player.rect.y
                starttime = pygame.time.get_ticks()
                frames = 0
                player.carrying[0] = False
                fullupdate = True
            elif collided == "SWITCH" or collided == "PLATEDOWN":
                fullupdate = True
            elif isinstance(collided, list):
                if collided[0] == 'helpbox':
                    font = pygame.font.Font('freesansbold.ttf', 24)
                    text = font.render(helptext[collided[1] - 1], True, bright_red, black)
                    screen.blit(text, (280, 685))
                    updates.append(pygame.Rect(280, 685, 700, 30))
                    screen.blit(level_object.img, level_object.coordinates)
                    updates.append(level_object.rect)
            elif collided:
                screen.blit(level_object.img, level_object.coordinates)
                updates.append(level_object.rect)





        fps = pygame.time.Clock()
        fps.tick(80)

        #FPS PRINT START
        font = pygame.font.Font('freesansbold.ttf', 32)
        currtime = pygame.time.get_ticks()
        frames += 1
        text = font.render(str(frames / ((currtime-starttime) / 1000)), True, green, blue)
        screen.blit(text, (100, 100))
        #FPS PRINT STOP

        seconds = (currtime - starttime) // 1000
        if seconds < 60:
            text = font.render("Time: " + str(seconds) + "s", True, green, black)
        else:
            minutes = seconds // 60
            seconds = seconds - (minutes * 60)
            text = font.render("Time: " + str(minutes) + "m " + str(seconds) + "s", True, green, black)
        pygame.draw.rect(screen, black, pygame.Rect(10,680,250,30))
        screen.blit(text, (10, 680))
        updates.append(pygame.Rect(10, 680, 250, 30))

        if fullupdate == True:
            screen.fill(black)
            screen.blit(player.img, player.coordinates)

            for thing in gameObjs:
                screen.blit(thing.img, thing.coordinates)
                if thing.type == "helpbox":
                    thing.collided = False
                    collided = player.check_collision(thing)
                    if collided:
                        font = pygame.font.Font('freesansbold.ttf', 24)
                        text = font.render(helptext[collided[1] - 1], True, bright_red, black)
                        screen.blit(text, (280, 685))
                        updates.append(pygame.Rect(280, 685, 700, 30))
                        screen.blit(level_object.img, level_object.coordinates)

            font = pygame.font.Font('freesansbold.ttf', 32)
            currtime = pygame.time.get_ticks()
            frames += 1
            text = font.render(str(frames / ((currtime - starttime) / 1000)), True, green, blue)
            screen.blit(text, (100, 100))

            if seconds < 60:
                text = font.render("Time: " + str(seconds) + "s", True, green, black)
            else:
                minutes = seconds // 60
                seconds = seconds - (minutes * 60)
                text = font.render("Time: " + str(minutes) + "m " + str(seconds) + "s", True, green, black)
            screen.blit(text, (10, 680))

            text = font.render("Level: " + levelname, True, green, black)
            screen.blit(text, (1000, 680))

            if player.carrying[0]:
                screen.blit(player.carrying[1].img, player.carrying[1].coordinates)

            screen.blit(player.img, player.coordinates)
            pygame.display.flip()
            fullupdate = False

        else:
            screen.blit(player.img, player.coordinates)
            updates.append(player.rect)
            if player.carrying[0]:
                screen.blit(player.carrying[1].img, player.carrying[1].coordinates)
                updates.append(player.carrying[1].rect)
            pygame.display.update(updates)
