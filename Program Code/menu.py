import pygame
import sys
import os
from pygame.locals import *
import random

# time
mainClock = pygame.time.Clock()

# init pygame
pygame.init()
font = pygame.font.Font('freesansbold.ttf', 20)
inputFont = pygame.font.Font(None, 32)

# run the game at 60 frames per second
FPS = 100
velocity = 10
person_width = 5
person_height = 5

# direction
choices = ["up", "down", "left", "right"]

# color
alpha = (255, 255, 255)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
red = (255, 0, 0)
COLOR_INACTIVE = pygame.Color('red')
COLOR_ACTIVE = pygame.Color('dodgerblue2')

# sound
pygame.mixer.init(44100, -16, 2, 2048)
game_sound = pygame.mixer.Sound("sound/spooky.mp3")
game_sound.set_volume(0.01)
celebration_sound = pygame.mixer.Sound("sound/auld.mp3")
collision_sound_loader = pygame.mixer.Sound("sound/hitWall.mp3")
game_sound.play()

# SCREEN
screen = pygame.display.set_mode((500, 500))

# write data
def record(filename, data):
    """
    :param filename: filename
    :param data: string
    :return: NONE
    """
    file = open(filename, "a")
    file.write(data)
    print("User Data recorded")

# write data
def recordRandom(data):
    """
    :param data: string
    :return: NONE
    """
    file = open("random.txt", "a")
    file.write(data)
    print("Simulation Data Recorded")

# reporter
def reporter(steps):
    """

    :param steps: a list of how many steps takes
    :return: NONE
    """
    print("Your highest steps:" + str(max(steps)))
    print("Your highest steps:" + str(min(steps)))
    print("Your average steps:" + str(sum(steps) / len(steps)))

def main_menu():
    """
    Main Menu selection the functions
    :return: NONE
    """
    pygame.init()
    pygame.display.set_caption('LOST IN FORREST')
    screen = pygame.display.set_mode((500, 500), 0, 32)
    menuPicture = pygame.image.load(os.path.join('images', "menuImage.jpg"))
    click = False
    while True:
        screen.fill((0, 0, 0))
        screen.blit(menuPicture, (0, 0))
        draw_text('ESC "exit"', font, (255, 255, 255), screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        # rect( x, y, len, width)
        button_1 = pygame.Rect(150, 100, 200, 50)
        button_2 = pygame.Rect(150, 200, 200, 50)
        button_4 = pygame.Rect(150, 300, 200, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                print("Game Menu")
                game_Menu()
        if button_2.collidepoint((mx, my)):
            if click:
                print("Options Menu")
                options()
        if button_4.collidepoint((mx, my)):
            if click:
                print("Simulation Menu")
                randomStimulationMenu()
        pygame.draw.rect(screen, (0, 0, 128), button_1)
        draw_text('Start', font, (255, 255, 255), screen, 220, 100)
        pygame.draw.rect(screen, (0, 0, 128), button_2)
        draw_text('Option', font, (255, 255, 255), screen, 220, 200)
        pygame.draw.rect(screen, (0, 0, 128), button_4)
        draw_text('Simulation', font, (255, 255, 255), screen, 220, 300)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)

# game engine
def draw_text(text, font, color, surface, x, y):
    """
    :param text: text
    :param font: font attribute
    :param color: font color
    :param surface: the field text displayed on
    :param x: x-position
    :param y: y-position
    :return: NONE
    """
    font = pygame.font.Font('freesansbold.ttf', 20)
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def displayGameOverWindow(gameWindow, gameOverImage, stepCounter):
    """
    :param stepCounter:
    :param gameWindow: window to display games
    :param gameOverImage: the image to display after game is over
    :return: NONE

    """
    game_sound.stop()
    pygame.mixer.Sound.play(celebration_sound)
    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render(str(stepCounter) + " steps", True, red, alpha)
    textRect = text.get_rect()
    start_time = pygame.time.get_ticks()
    pygame.display.set_caption("Congrats, You've beat the game")
    while pygame.time.get_ticks() < start_time + 1000:
        gameWindow.fill(white)
        gameWindow.blit(gameOverImage, (0, 0))
        gameWindow.blit(text, textRect)
        pygame.display.update()
    celebration_sound.stop()
    main_menu()


def player_one_movement(key_pressed, player_one_container, stepCounter, width, height):
    """

    :param height: window height
    :param width: window width
    :param stepCounter: counter for steps
    :param key_pressed: when user enter a key
    :param player_one_container: player 1 position
    :return: NONE

    """
    stepCounter += 1
    print(stepCounter)
    # move left
    if key_pressed[pygame.K_a]:
        if player_one_container.x >= 5:
            player_one_container.x -= velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)
    # move right
    if key_pressed[pygame.K_d]:
        if player_one_container.x <= width - 50:
            player_one_container.x += velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)
    # move up
    if key_pressed[pygame.K_w]:
        if player_one_container.y >= 5:
            player_one_container.y -= velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)
    # move down
    if key_pressed[pygame.K_s]:
        if player_one_container.y <= height - 50:
            player_one_container.y += velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)


def player_two_movement(key_pressed, player_two_container, stepCounter, width, height):
    """

    :param height: window height
    :param width: window width
    :param stepCounter: counter for steps
    :param key_pressed: when user enter a key
    :param player_two_container: player 2 position
    :return:NONE

    """
    stepCounter += 1
    print(stepCounter)
    # move left
    if key_pressed[pygame.K_LEFT]:
        if player_two_container.x >= 5:
            player_two_container.x -= velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)
    # move right
    if key_pressed[pygame.K_RIGHT]:
        if player_two_container.x <= width - 50:
            player_two_container.x += velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)
    # move up
    if key_pressed[pygame.K_UP]:
        if player_two_container.y >= 5:
            player_two_container.y -= velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)
    # move down
    if key_pressed[pygame.K_DOWN]:
        if player_two_container.y <= height - 50:
            player_two_container.y += velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)


def player_three_movement(key_pressed, player_three_container, stepCounter, width, height):
    """

    :param height: window height
    :param width: window width
    :param stepCounter: counter for steps
    :param key_pressed: when user enter a key
    :param player_three_container: player 3 position
    :return:NONE

    """
    stepCounter += 1
    print(stepCounter)
    # move left
    if key_pressed[pygame.K_3]:
        if player_three_container.x >= 5:
            player_three_container.x -= velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)
    # move right
    if key_pressed[pygame.K_4]:
        if player_three_container.x <= width - 50:
            player_three_container.x += velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)
    # move up
    if key_pressed[pygame.K_1]:
        if player_three_container.y >= 5:
            player_three_container.y -= velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)
    # move down
    if key_pressed[pygame.K_2]:
        if player_three_container.y <= height - 50:
            player_three_container.y += velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)


def player_four_movement(key_pressed, player_four_container, stepCounter, width, height):
    """

    :param height: window height
    :param width: window width
    :param stepCounter: counter for steps
    :param key_pressed: when user enter a key
    :param player_four_container: player 3 position
    :return:NONE

    """
    stepCounter += 1
    print(stepCounter)
    # move left
    if key_pressed[pygame.K_8]:
        if player_four_container.x >= 5:
            player_four_container.x -= velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)
    # move right
    if key_pressed[pygame.K_9]:
        if player_four_container.x <= width - 50:
            player_four_container.x += velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)
    # move up
    if key_pressed[pygame.K_6]:
        if player_four_container.y >= 5:
            player_four_container.y -= velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)
    # move down
    if key_pressed[pygame.K_7]:
        if player_four_container.y <= height - 50:
            player_four_container.y += velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)


def game_Menu():
    """

    Game Option Panel
    :return: NONE
    """
    pygame.init()
    pygame.display.set_caption('LOST IN FORREST')
    screen = pygame.display.set_mode((500, 500), 0, 32)
    menuPicture = pygame.image.load(os.path.join('images', "menuImage.jpg"))
    gameClick = False
    running = True
    print("Selected Game")
    while running:
        # allow user to pick game mode
        screen.fill((0, 0, 0))
        screen.blit(menuPicture, (0, 0))
        draw_text('ESC "Menu"', font, (255, 255, 255), screen, 20, 20)
        draw_text('Select Game Mode', font, (255, 255, 255), screen, 20, 50)

        # mouse position
        mx, my = pygame.mouse.get_pos()

        # button attribute
        button_1 = pygame.Rect(150, 100, 200, 50)
        button_2 = pygame.Rect(150, 200, 200, 50)
        button_3 = pygame.Rect(150, 300, 200, 50)

        if button_1.collidepoint((mx, my)):
            if gameClick:
                k2_game()
        if button_2.collidepoint((mx, my)):
            if gameClick:
                k_3To5_game()
        if button_3.collidepoint((mx, my)):
            if gameClick:
                multiPlayerGameMenu()

        # draw button
        pygame.draw.rect(screen, (0, 0, 128), button_1)
        draw_text("Basic Map", font, (255, 255, 255), screen, 200, 100)
        pygame.draw.rect(screen, (0, 0, 128), button_2)
        draw_text('Build Your Map', font, (255, 255, 255), screen, 180, 200)
        pygame.draw.rect(screen, (0, 0, 128), button_3)
        draw_text('Multiple Player', font, (255, 255, 255), screen, 180, 300)

        gameClick = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    gameClick = True

        pygame.display.update()
        mainClock.tick(60)


def k2_game():
    """

    Game Option Panel
    :return: NONE
    """
    pygame.init()
    pygame.display.set_caption('LOST IN FORREST')
    screen = pygame.display.set_mode((500, 500), 0, 32)
    menuPicture = pygame.image.load(os.path.join('images', "menuImage.jpg"))
    gameClick = False
    running = True
    print("Selected Game")
    while running:
        # allow user to pick game mode
        screen.fill((0, 0, 0))
        screen.blit(menuPicture, (0, 0))
        draw_text('ESC "Menu"', font, (255, 255, 255), screen, 20, 20)
        draw_text('Select Level Of Difficulty', font, (255, 255, 255), screen, 20, 50)

        mx, my = pygame.mouse.get_pos()

        # button attribute
        button_1 = pygame.Rect(150, 100, 200, 50)
        button_2 = pygame.Rect(150, 200, 200, 50)
        button_3 = pygame.Rect(150, 300, 200, 50)
        button_4 = pygame.Rect(150, 400, 200, 50)

        if button_1.collidepoint((mx, my)):
            if gameClick:
                easyMode()
        if button_2.collidepoint((mx, my)):
            if gameClick:
                mediumMode()
        if button_3.collidepoint((mx, my)):
            if gameClick:
                hardMode()
        if button_4.collidepoint((mx, my)):
            if gameClick:
                hellMode()

        # draw button
        pygame.draw.rect(screen, (0, 0, 128), button_1)
        draw_text('Easy', font, (255, 255, 255), screen, 220, 100)
        pygame.draw.rect(screen, (0, 0, 128), button_2)
        draw_text('Medium', font, (255, 255, 255), screen, 220, 200)
        pygame.draw.rect(screen, (0, 0, 128), button_3)
        draw_text('Hard', font, (255, 255, 255), screen, 220, 300)
        pygame.draw.rect(screen, (0, 0, 128), button_4)
        draw_text('Hell', font, (255, 255, 255), screen, 220, 400)

        gameClick = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    gameClick = True

        pygame.display.update()
        mainClock.tick(60)


def displayGameWindow(gameWindow, forrestImage, player_one_container, player_two_container, person_One_Image,
                      person_Two_Image, ):
    """
    Display and update 2 players on the map
    :param forrestImage: forrest image
    :param person_Two_Image: display person one image
    :param person_One_Image: display person two image
    :param gameWindow: game window
    :param player_one_container: player_one position
    :param player_two_container: player_two position
    :return: NONE

    """
    gameWindow.fill(white)
    gameWindow.blit(forrestImage, (0, 0))
    gameWindow.blit(person_One_Image, (player_one_container.x, player_one_container.y))
    gameWindow.blit(person_Two_Image, (player_two_container.x, player_two_container.y))
    pygame.display.update()


def displayGameWindow_player3(gameWindow, forrestImage, player_one_container, player_two_container,
                              player_three_container, person_One_Image,
                              person_Two_Image, person_Three_Image):
    """
    Display and update 3 players on the map
    :param gameWindow: game window
    :param forrestImage: forrest image
    :param person_One_Image: display person one image
    :param person_Two_Image: display person two image
    :param person_Three_Image: display person three image
    :param player_one_container: player_one position
    :param player_two_container: player_two position
    :param player_three_container: player_three position
    :return: NONE

    """
    gameWindow.fill(white)
    gameWindow.blit(forrestImage, (0, 0))
    gameWindow.blit(person_One_Image, (player_one_container.x, player_one_container.y))
    gameWindow.blit(person_Two_Image, (player_two_container.x, player_two_container.y))
    gameWindow.blit(person_Three_Image, (player_three_container.x, player_three_container.y))
    pygame.display.update()


def displayGameWindow_player4(gameWindow, forrestImage, player_one_container, player_two_container,
                              player_three_container, player_four_container, person_One_Image,
                              person_Two_Image, person_Three_Image, person_Four_Image):
    """
    Display and update 4 players on the map
    :param gameWindow: game window
    :param forrestImage: forrest image
    :param person_One_Image: display person one image
    :param person_Two_Image: display person two image
    :param person_Three_Image: display person three image
    :param person_Four_Image: display person four image
    :param player_one_container: player_one position
    :param player_two_container: player_two position
    :param player_three_container: player_three position
    :param player_four_container: player_four position
    :return: NONE

    """
    gameWindow.fill(white)
    gameWindow.blit(forrestImage, (0, 0))
    gameWindow.blit(person_One_Image, (player_one_container.x, player_one_container.y))
    gameWindow.blit(person_Two_Image, (player_two_container.x, player_two_container.y))
    gameWindow.blit(person_Three_Image, (player_three_container.x, player_three_container.y))
    gameWindow.blit(person_Four_Image, (player_four_container.x, player_four_container.y))
    pygame.display.update()


def easyMode():
    """

    :return: easy mode active
    """

    print("Easy Mode Selected")
    map300_manuelStimulation()


def map300_manuelStimulation():
    """

    stimulate the k_2 student lost in forrest game
    :return: NONE

    """
    pygame.init()
    pygame.mixer.init()

    # map data
    width, height = 300, 300
    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "300map.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "tom.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "jerry.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # init position and draw player
    gameOverImage = pygame.image.load(os.path.join('images', "300gameover.jpg"))
    player_one_container = pygame.Rect(0, 0, person_width, person_height)
    player_two_container = pygame.Rect(width - 70, height - 70, person_width, person_height)

    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(player_one_container.x - player_two_container.x) <= 50 and abs(
                    player_one_container.y - player_two_container.y) <= 50:
                filename = "results/300results.txt"
                Data = str(stepCounter) + "  two players " + "\n"
                record(filename, Data)
                is_GameOver = False
                displayGameOverWindow(gameWindow, gameOverImage=gameOverImage, stepCounter=stepCounter)

        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        player_one_movement(key_pressed, player_one_container, stepCounter, width, height)
        player_two_movement(key_pressed, player_two_container, stepCounter, width, height)
        displayGameWindow(gameWindow,
                          player_one_container=player_one_container,
                          forrestImage=forrestImage,
                          player_two_container=player_two_container,
                          person_One_Image=person_One_Image,
                          person_Two_Image=person_Two_Image)


def mediumMode():
    """

    :return: easy mode active
    """
    print("Medium Mode Selected")
    map500_manuelStimulation()


def map500_manuelStimulation():
    """

    stimulate the k_2 student lost in forrest game
    :return: NONE

    """
    pygame.init()
    pygame.mixer.init()

    # map data
    width, height = 500, 500
    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "500map.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "tom.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "jerry.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # game over image
    gameOverImage = pygame.image.load(os.path.join('images', "500gameover.jpg"))

    # init position and draw player
    player_one_container = pygame.Rect(0, 0, person_width, person_height)
    player_two_container = pygame.Rect(width - 70, height - 70, person_width, person_height)

    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(player_one_container.x - player_two_container.x) <= 50 and abs(
                    player_one_container.y - player_two_container.y) <= 50:
                filename = "results/500results.txt"
                Data = str(stepCounter) + "  two players " + "\n"
                record(filename, Data)
                is_GameOver = False
                displayGameOverWindow(gameWindow, gameOverImage=gameOverImage, stepCounter=stepCounter)

        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        player_one_movement(key_pressed, player_one_container, stepCounter, width, height)
        player_two_movement(key_pressed, player_two_container, stepCounter, width, height)
        displayGameWindow(gameWindow,
                          player_one_container=player_one_container,
                          forrestImage=forrestImage,
                          player_two_container=player_two_container,
                          person_One_Image=person_One_Image,
                          person_Two_Image=person_Two_Image)


def hardMode():
    """

    :return: hard mode active
    """
    print("Hard Mode Selected")
    vanGogh_Map_manuelStimulation()


def vanGogh_Map_manuelStimulation():
    """

    stimulate the k_2 student lost in forrest game
    :return: NONE

    """

    # map data
    width, height = 1200, 800
    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "vanmap.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "tom.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "jerry.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # game over image
    gameOverImage = pygame.image.load(os.path.join('images', "forrestgameover.jpg"))

    # init position and draw player
    player_one_container = pygame.Rect(0, 0, person_width, person_height)
    player_two_container = pygame.Rect(width - 70, height - 70, person_width, person_height)

    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(player_one_container.x - player_two_container.x) <= 50 and abs(
                    player_one_container.y - player_two_container.y) <= 50:
                filename = "results/hardresults.txt"
                Data = str(stepCounter) + "  two players " + "\n"
                record(filename, Data)
                is_GameOver = False
                displayGameOverWindow(gameWindow, gameOverImage=gameOverImage, stepCounter=stepCounter)

        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        player_one_movement(key_pressed, player_one_container, stepCounter, width, height)
        player_two_movement(key_pressed, player_two_container, stepCounter, width, height)
        displayGameWindow(gameWindow,
                          player_one_container=player_one_container,
                          forrestImage=forrestImage,
                          player_two_container=player_two_container,
                          person_One_Image=person_One_Image,
                          person_Two_Image=person_Two_Image)


def hellMode():
    """

    :return: hell mode active
    """
    print("Hell Mode Selected")
    Map2560_manuelStimulation()


def Map2560_manuelStimulation():
    """

    stimulate the k_2 student lost in forrest game
    :return: NONE

    """
    # map data
    width, height = 2560, 1600
    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "2560map.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "tom.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "jerry.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # game over image
    gameOverImage = pygame.image.load(os.path.join('images', "2560gameover.jpg"))

    # init position and draw player
    player_one_container = pygame.Rect(0, 0, person_width, person_height)
    player_two_container = pygame.Rect(width - 70, height - 70, person_width, person_height)
    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(player_one_container.x - player_two_container.x) <= 50 and abs(
                    player_one_container.y - player_two_container.y) <= 50:
                filename = "results/hellresults.txt"
                Data = str(stepCounter) + "  two players " + "\n"
                record(filename, Data)
                is_GameOver = False
                displayGameOverWindow(gameWindow, gameOverImage=gameOverImage, stepCounter=stepCounter)

        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        player_one_movement(key_pressed, player_one_container, stepCounter, width, height)
        player_two_movement(key_pressed, player_two_container, stepCounter, width, height)
        displayGameWindow(gameWindow,
                          player_one_container=player_one_container,
                          forrestImage=forrestImage,
                          player_two_container=player_two_container,
                          person_One_Image=person_One_Image,
                          person_Two_Image=person_Two_Image)


def k_3To5_game():
    """

    stimulate the k3-5 student lost in forrest game
    :return: NONE

    """
    # map data
    while True:
        try:
            width = int(input('Enter your width(0-1000):'))
            if width in range(0, 1000):
                break
            else:
                print("Out of range")
        except:
            print("That's not a valid option!")

    while True:
        try:
            height = int(input('Enter your height(0-1000): '))
            if height in range(0, 1000):
                break
            else:
                print("Out of range")
        except:
            print("That's not a valid option!")

    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "forrest.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "tom.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "jerry.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # game over image
    gameOverImage = pygame.image.load(os.path.join('images', "300gameover.jpg"))

    # init position and draw player
    player_one_container = pygame.Rect(0, 0, person_width, person_height)
    player_two_container = pygame.Rect(width - 70, height - 70, person_width, person_height)
    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(player_one_container.x - player_two_container.x) <= 50 and abs(
                    player_one_container.y - player_two_container.y) <= 50:
                Data = str(width) + " * " + str(height) + ":          " + str(stepCounter) + "   two player\n"
                filename = "results/randomMap.txt"
                record(filename, Data)
                is_GameOver = False
                displayGameOverWindow(gameWindow, gameOverImage=gameOverImage, stepCounter=stepCounter)

        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        player_one_movement(key_pressed, player_one_container, stepCounter, width, height)
        player_two_movement(key_pressed, player_two_container, stepCounter, width, height)
        displayGameWindow(gameWindow,
                          player_one_container=player_one_container,
                          forrestImage=forrestImage,
                          player_two_container=player_two_container,
                          person_One_Image=person_One_Image,
                          person_Two_Image=person_Two_Image)


def multiPlayerGameMenu():
    """

        Game Option Panel
        :return: NONE
    """
    pygame.init()
    pygame.display.set_caption('LOST IN FORREST')
    screen = pygame.display.set_mode((500, 500), 0, 32)
    menuPicture = pygame.image.load(os.path.join('images', "menuImage.jpg"))
    gameClick = False
    running = True
    print("Selected Game")
    while running:
        # allow user to pick game mode
        screen.fill((0, 0, 0))
        screen.blit(menuPicture, (0, 0))
        draw_text('ESC "Menu"', font, (255, 255, 255), screen, 20, 20)
        draw_text('Select number of players', font, (255, 255, 255), screen, 20, 50)

        mx, my = pygame.mouse.get_pos()

        # button attribute
        button_1 = pygame.Rect(150, 100, 200, 50)
        button_2 = pygame.Rect(150, 200, 200, 50)
        button_3 = pygame.Rect(150, 300, 200, 50)

        if button_1.collidepoint((mx, my)):
            if gameClick:
                print("2 players")
                map300_manuelStimulation()
        if button_2.collidepoint((mx, my)):
            if gameClick:
                print("3 players")
                map300_manuelStimulation_3players()
        if button_3.collidepoint((mx, my)):
            if gameClick:
                print("4 players")
                map300_manuelStimulation_4players()

        # draw button
        pygame.draw.rect(screen, (0, 0, 128), button_1)
        draw_text('Dual Player', font, (255, 255, 255), screen, 200, 100)
        pygame.draw.rect(screen, (0, 0, 128), button_2)
        draw_text('Three Player', font, (255, 255, 255), screen, 200, 200)
        pygame.draw.rect(screen, (0, 0, 128), button_3)
        draw_text('Four Player', font, (255, 255, 255), screen, 200, 300)

        gameClick = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    gameClick = True

        pygame.display.update()
        mainClock.tick(60)


def map300_manuelStimulation_3players():
    """

    stimulate the k_2 student lost in forrest game
    :return: NONE

    """
    pygame.init()
    pygame.mixer.init()

    # map data
    width, height = 300, 300
    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "300map.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "tom.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "jerry.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # person three image
    person_Three_Image = pygame.image.load(os.path.join('images', "sandy.png"))
    person_Three_Image.convert_alpha()
    person_Three_Image.set_colorkey(alpha)

    # init position and draw player
    gameOverImage = pygame.image.load(os.path.join('images', "300gameover.jpg"))
    player_one_container = pygame.Rect(0, 0, person_width, person_height)
    player_two_container = pygame.Rect(width - 70, height - 70, person_width, person_height)
    player_three_container = pygame.Rect(0, height - 70, person_width, person_height)

    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(player_one_container.x - player_two_container.x) <= 50 and abs(
                    player_one_container.x - player_three_container.x) <= 50 and abs(
                player_one_container.y - player_two_container.y) <= 50 and abs(
                player_one_container.y - player_three_container.y) <= 50:
                filename = "results/300results.txt"
                Data = str(stepCounter) + "  three players " + "\n"
                record(filename, Data)
                is_GameOver = False
                displayGameOverWindow(gameWindow, gameOverImage=gameOverImage, stepCounter=stepCounter)

        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        player_one_movement(key_pressed, player_one_container, stepCounter, width, height)
        player_two_movement(key_pressed, player_two_container, stepCounter, width, height)
        player_three_movement(key_pressed, player_three_container, stepCounter, width, height)
        displayGameWindow_player3(gameWindow,
                                  forrestImage=forrestImage,
                                  player_one_container=player_one_container,
                                  player_two_container=player_two_container,
                                  player_three_container=player_three_container,
                                  person_One_Image=person_One_Image,
                                  person_Two_Image=person_Two_Image,
                                  person_Three_Image=person_Three_Image)


def map300_manuelStimulation_4players():
    """

    stimulate the k_2 student lost in forrest game
    :return: NONE

    """
    pygame.init()
    pygame.mixer.init()

    # map data
    width, height = 300, 300
    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "300map.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "tom.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "jerry.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # person three image
    person_Three_Image = pygame.image.load(os.path.join('images', "sandy.png"))
    person_Three_Image.convert_alpha()
    person_Three_Image.set_colorkey(alpha)

    # person four image
    person_Four_Image = pygame.image.load(os.path.join('images', "squid.jpg"))
    person_Four_Image.convert_alpha()
    person_Four_Image.set_colorkey(alpha)

    # init position and draw player
    gameOverImage = pygame.image.load(os.path.join('images', "300gameover.jpg"))
    player_one_container = pygame.Rect(0, 0, person_width, person_height)
    player_two_container = pygame.Rect(width - 70, height - 70, person_width, person_height)
    player_three_container = pygame.Rect(0, height - 70, person_width, person_height)
    player_four_container = pygame.Rect(width - 70, 0, person_width, person_height)

    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(player_one_container.x - player_two_container.x) <= 50 and abs(
                    player_one_container.x - player_three_container.x) <= 50 and abs(
                player_one_container.x - player_four_container.x) <= 50 and abs(
                player_one_container.y - player_two_container.y) <= 50 and abs(
                player_one_container.y - player_three_container.y) <= 50 and abs(
                player_one_container.y - player_four_container.y) <= 50:
                filename = "results/300results.txt"
                Data = str(stepCounter) + "  four players " + "\n"
                record(filename, Data)
                is_GameOver = False
                displayGameOverWindow(gameWindow, gameOverImage=gameOverImage, stepCounter=stepCounter)

        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        player_one_movement(key_pressed, player_one_container, stepCounter, width, height)
        player_two_movement(key_pressed, player_two_container, stepCounter, width, height)
        player_three_movement(key_pressed, player_three_container, stepCounter, width, height)
        player_four_movement(key_pressed, player_four_container, stepCounter, width, height)
        displayGameWindow_player4(gameWindow,
                                  forrestImage=forrestImage,
                                  player_one_container=player_one_container,
                                  player_two_container=player_two_container,
                                  player_three_container=player_three_container,
                                  player_four_container=player_four_container,
                                  person_One_Image=person_One_Image,
                                  person_Two_Image=person_Two_Image,
                                  person_Three_Image=person_Three_Image,
                                  person_Four_Image=person_Four_Image, )


# option
def options():
    """

    :return: option page
    """
    pygame.init()
    pygame.display.set_caption('LOST IN FORREST')
    screen = pygame.display.set_mode((500, 500), 0, 32)
    menuPicture = pygame.image.load(os.path.join('images', "menuImage.jpg"))
    optionClick = False
    running = True
    while running:
        # allow user to pick game mode
        screen.fill((0, 0, 0))
        screen.blit(menuPicture, (0, 0))
        draw_text('ESC "Menu"', font, (255, 255, 255), screen, 20, 20)
        draw_text('Select Sound Volume', font, (255, 255, 255), screen, 20, 50)

        mx, my = pygame.mouse.get_pos()

        # button attribute
        button_1 = pygame.Rect(150, 100, 200, 50)
        button_2 = pygame.Rect(150, 200, 200, 50)
        button_3 = pygame.Rect(150, 300, 200, 50)

        if button_1.collidepoint((mx, my)):
            if optionClick:
                set_Volume_Low()
        if button_2.collidepoint((mx, my)):
            if optionClick:
                set_Volume_Medium()
        if button_3.collidepoint((mx, my)):
            if optionClick:
                set_Volume_High()

        pygame.draw.rect(screen, (0, 0, 128), button_1)
        draw_text('Volume Low', font, (255, 255, 255), screen, 180, 100)
        pygame.draw.rect(screen, (0, 0, 128), button_2)
        draw_text('Volume Medium', font, (255, 255, 255), screen, 180, 200)
        pygame.draw.rect(screen, (0, 0, 128), button_3)
        draw_text('Volume High', font, (255, 255, 255), screen, 180, 300)

        optionClick = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    optionClick = True

        pygame.display.update()
        mainClock.tick(60)


def set_Volume_Low():
    """
    change volume to Low
    :return: NONE
    """
    game_sound.set_volume(0.01)


def set_Volume_Medium():
    """
    change volume to Medium
    :return: NONE
    """
    game_sound.set_volume(0.1)


def set_Volume_High():
    """
    change volume to High
    :return: NONE
    """
    game_sound.set_volume(0.5)


def credit():
    """
    Display credit page
    :return: NONE
    """
    pygame.init()
    pygame.display.set_caption('LOST IN FORREST')
    screen = pygame.display.set_mode((500, 500), 0, 32)
    menuPicture = pygame.image.load(os.path.join('images', "menuImage.jpg"))
    while True:
        draw_text('ESC "Menu"', font, (255, 255, 255), screen, 20, 20)
        screen.fill((0, 0, 0))
        screen.blit(menuPicture, (0, 0))
        draw_text('Credit:', font, (255, 255, 255), screen, 20, 20)
        draw_text('CPSC 60500', font, (255, 255, 255), screen, 20, 50)
        draw_text('Dr. Fadi Wedyan', font, (255, 255, 255), screen, 20, 80)
        draw_text('Wandering in the Woods', font, (255, 255, 255), screen, 20, 110)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()

        pygame.display.update()
        mainClock.tick(60)


# random stimulation engine
def randomStimulationMenu():
    """
    Display random Stimulation Menu
    :return: NONE
    """
    pygame.init()
    pygame.display.set_caption('LOST IN FORREST')
    game_sound.set_volume(0.01)
    screen = pygame.display.set_mode((500, 500), 0, 32)
    menuPicture = pygame.image.load(os.path.join('images', "menuImage.jpg"))
    click = False
    while True:
        screen.fill((0, 0, 0))
        screen.blit(menuPicture, (0, 0))
        draw_text('ESC "exit"', font, (255, 255, 255), screen, 20, 20)
        draw_text('Random Simulation'
                  ' Mode', font, (255, 255, 255), screen, 20, 50)
        mx, my = pygame.mouse.get_pos()

        # rect( x, y, len, width)
        button_1 = pygame.Rect(150, 100, 200, 50)
        button_2 = pygame.Rect(150, 200, 200, 50)
        button_3 = pygame.Rect(150, 300, 200, 50)
        button_4 = pygame.Rect(150, 400, 200, 50)
        if button_1.collidepoint((mx, my)):
            if click:
                print("300*300 Simulation")
                stimulation_300_300_MultiPlayerGameMenu()
        if button_2.collidepoint((mx, my)):
            if click:
                print("500*500 Simulation")
                stimulation_500_500_MultiPlayerGameMenu()
        if button_3.collidepoint((mx, my)):
            if click:
                print("1000*1000 Simulation")
                stimulation_1000_1000_MultiPlayerGameMenu()
        if button_4.collidepoint((mx, my)):
            if click:
                print("Build Your Map")
                stimulation_customizedMap_MultiPlayerGameMenu()
        pygame.draw.rect(screen, (0, 0, 128), button_1)
        draw_text('300*300', font, (255, 255, 255), screen, 220, 100)
        pygame.draw.rect(screen, (0, 0, 128), button_2)
        draw_text('500*500', font, (255, 255, 255), screen, 220, 200)
        pygame.draw.rect(screen, (0, 0, 128), button_3)
        draw_text('1000*1000', font, (255, 255, 255), screen, 210, 300)
        pygame.draw.rect(screen, (0, 0, 128), button_4)
        draw_text('Customize Map', font, (255, 255, 255), screen, 170, 400)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


def player_one_random_movement(player_one_Container, width, height):
    """

    :param height: window height
    :param width: window width
    :param player_one_Container: player 1 location update after move a step
    :return: NONE
    """
    choice = random.choice(choices)

    if choice == "left":
        if player_one_Container.x >= 50:
            player_one_Container.x -= velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)

    if choice == "right" and player_one_Container.x <= width:
        if player_one_Container.x <= width - 50:
            player_one_Container.x += velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)

    if choice == "up":
        if player_one_Container.y >= 50:
            player_one_Container.x -= velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)
        player_one_Container.y -= velocity

    if choice == "down":
        if player_one_Container.y <= height - 50:
            player_one_Container.y += velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)


def player_two_random_movement(player_two_Container, width, height):
    """

    :param player_two_Container:  player two container
    :param height: window height
    :param width: window width
    :return: NONE

    """
    choice = random.choice(choices)
    if choice == "left":
        if player_two_Container.x >= 50:
            player_two_Container.x -= velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)

    if choice == "right" and player_two_Container.x <= width - 50:
        if player_two_Container.x <= width - 50:
            player_two_Container.x += velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)

    if choice == "up":
        if player_two_Container.y >= 50:
            player_two_Container.x -= velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)
        player_two_Container.y -= velocity

    if choice == "down":
        if player_two_Container.y <= height - 50:
            player_two_Container.y += velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)


def player_three_random_movement(player_three_Container, width, height):
    """

    :param player_three_Container:  player three container
    :param height: window height
    :param width: window width
    :return: NONE

    """
    choice = random.choice(choices)
    if choice == "left":
        if player_three_Container.x >= 50:
            player_three_Container.x -= velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)

    if choice == "right" and player_three_Container.x <= width - 50:
        if player_three_Container.x <= width - 50:
            player_three_Container.x += velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)

    if choice == "up":
        if player_three_Container.y >= 50:
            player_three_Container.x -= velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)
        player_three_Container.y -= velocity

    if choice == "down":
        if player_three_Container.y <= height - 50:
            player_three_Container.y += velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)


def player_four_random_movement(player_four_Container, width, height):
    """

    :param player_four_Container:  player three container
    :param height: window height
    :param width: window width
    :return: NONE

    """
    choice = random.choice(choices)
    if choice == "left":
        if player_four_Container.x >= 50:
            player_four_Container.x -= velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)

    if choice == "right" and player_four_Container.x <= width - 50:
        if player_four_Container.x <= width - 50:
            player_four_Container.x += velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)

    if choice == "up":
        if player_four_Container.y >= 50:
            player_four_Container.x -= velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)
        player_four_Container.y -= velocity

    if choice == "down":
        if player_four_Container.y <= height - 50:
            player_four_Container.y += velocity
        else:
            pygame.mixer.Channel(0).play(collision_sound_loader, maxtime=600)


def stimulation_300_300_MultiPlayerGameMenu():
    """

        Game Option Panel
        :return: NONE
    """
    pygame.init()
    pygame.display.set_caption('LOST IN FORREST')
    screen = pygame.display.set_mode((500, 500), 0, 32)
    menuPicture = pygame.image.load(os.path.join('images', "menuImage.jpg"))
    gameClick = False
    running = True
    print("Selected Game")
    while running:
        # allow user to pick game mode
        screen.fill((0, 0, 0))
        screen.blit(menuPicture, (0, 0))
        draw_text('ESC "Menu"', font, (255, 255, 255), screen, 20, 20)
        draw_text('Select number of players', font, (255, 255, 255), screen, 20, 50)

        mx, my = pygame.mouse.get_pos()

        # button attribute
        button_1 = pygame.Rect(150, 100, 200, 50)
        button_2 = pygame.Rect(150, 200, 200, 50)
        button_3 = pygame.Rect(150, 300, 200, 50)

        if button_1.collidepoint((mx, my)):
            if gameClick:
                print("2 players")
                random_stimulation_300()
        if button_2.collidepoint((mx, my)):
            if gameClick:
                print("3 players")
                random_stimulation_300_3player()
        if button_3.collidepoint((mx, my)):
            if gameClick:
                print("4 players")
                random_stimulation_300_4player()

        # draw button
        pygame.draw.rect(screen, (0, 0, 128), button_1)
        draw_text('Dual Player', font, (255, 255, 255), screen, 200, 100)
        pygame.draw.rect(screen, (0, 0, 128), button_2)
        draw_text('Three Player', font, (255, 255, 255), screen, 200, 200)
        pygame.draw.rect(screen, (0, 0, 128), button_3)
        draw_text('Four Player', font, (255, 255, 255), screen, 200, 300)

        gameClick = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    gameClick = True

        pygame.display.update()
        mainClock.tick(60)


def random_stimulation_300():
    """
    Random Stimulate map size of 300 * 300
    :return: NONE
    """
    pygame.init()
    pygame.mixer.init()

    # map data
    width, height = 300, 300
    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "300map.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "tom.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "jerry.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    player_one_container = pygame.Rect(0, 0, person_width, person_height)
    player_two_container = pygame.Rect(width - 70, height - 70, person_width, person_height)
    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(player_one_container.x - player_two_container.x) <= 100 and abs(
                    player_one_container.y - player_two_container.y) <= 100:
                Data = "300 " + str(stepCounter) + " 2players\n"
                recordRandom(Data)
                is_GameOver = False
                randomStimulationMenu()
        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        player_one_random_movement(player_one_container, width, height)
        player_two_random_movement(player_two_container, width, height)
        displayGameWindow(gameWindow,
                          player_one_container=player_one_container,
                          forrestImage=forrestImage,
                          player_two_container=player_two_container,
                          person_One_Image=person_One_Image,
                          person_Two_Image=person_Two_Image)


def random_stimulation_300_3player():
    """
    Random Stimulate map size of 300 * 300 for 3 players
    :return: NONE
    """
    pygame.init()
    pygame.mixer.init()

    # map data
    width, height = 300, 300
    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "300map.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "tom.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "jerry.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # person three image
    person_Three_Image = pygame.image.load(os.path.join('images', "sandy.png"))
    person_Three_Image.convert_alpha()
    person_Three_Image.set_colorkey(alpha)

    # init position and draw player
    player_one_container = pygame.Rect(0, 0, person_width, person_height)
    player_two_container = pygame.Rect(width - 70, height - 70, person_width, person_height)
    player_three_container = pygame.Rect(0, height - 70, person_width, person_height)

    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(player_one_container.x - player_two_container.x) <= 50 and abs(
                    player_one_container.x - player_three_container.x) <= 50 and abs(
                    player_one_container.y - player_two_container.y) <= 50 and abs(
                    player_one_container.y - player_three_container.y) <= 50:
                Data = "300 " + str(stepCounter) + " 3players\n"
                recordRandom(Data)
                is_GameOver = False
                randomStimulationMenu()
        print(player_one_container.x)
        print(player_one_container.y)
        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        player_one_random_movement(player_one_container, width, height)
        player_two_random_movement(player_two_container, width, height)
        player_three_random_movement(player_three_container, width, height)
        displayGameWindow_player3(gameWindow,
                                  forrestImage=forrestImage,
                                  player_one_container=player_one_container,
                                  player_two_container=player_two_container,
                                  player_three_container=player_three_container,
                                  person_One_Image=person_One_Image,
                                  person_Two_Image=person_Two_Image,
                                  person_Three_Image=person_Three_Image)


def random_stimulation_300_4player():
    """
    Random Stimulate map size of 300 * 300 for 4 players
    :return: NONE
    """
    pygame.init()
    pygame.mixer.init()

    # map data
    width, height = 300, 300
    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "300map.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "tom.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "jerry.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # person three image
    person_Three_Image = pygame.image.load(os.path.join('images', "sandy.png"))
    person_Three_Image.convert_alpha()
    person_Three_Image.set_colorkey(alpha)

    # person four image
    person_Four_Image = pygame.image.load(os.path.join('images', "squid.jpg"))
    person_Four_Image.convert_alpha()
    person_Four_Image.set_colorkey(alpha)

    # init position and draw player
    player_one_container = pygame.Rect(0, 0, person_width, person_height)
    player_two_container = pygame.Rect(width - 70, height - 70, person_width, person_height)
    player_three_container = pygame.Rect(0, height - 70, person_width, person_height)
    player_four_container = pygame.Rect(width - 70, 0, person_width, person_height)

    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(player_one_container.x - player_two_container.x) <= 50 and abs(
                    player_one_container.x - player_three_container.x) <= 50 and abs(
                    player_one_container.x - player_four_container.x) <= 50 and abs(
                    player_one_container.y - player_two_container.y) <= 50 and abs(
                    player_one_container.y - player_three_container.y) <= 50 and abs(
                    player_one_container.y - player_four_container.y) <= 50:
                Data = "300 " + str(stepCounter) + " 4players\n"
                recordRandom(Data)
                is_GameOver = False
                randomStimulationMenu()
        print(player_one_container.x)
        print(player_one_container.y)
        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        player_one_random_movement(player_one_container, width, height)
        player_two_random_movement(player_two_container, width, height)
        player_three_random_movement(player_three_container, width, height)
        player_four_random_movement(player_four_container, width, height)
        displayGameWindow_player4(gameWindow,
                                  forrestImage=forrestImage,
                                  player_one_container=player_one_container,
                                  player_two_container=player_two_container,
                                  player_three_container=player_three_container,
                                  player_four_container=player_four_container,
                                  person_One_Image=person_One_Image,
                                  person_Two_Image=person_Two_Image,
                                  person_Three_Image=person_Three_Image,
                                  person_Four_Image=person_Four_Image, )


def stimulation_500_500_MultiPlayerGameMenu():
    """

        Game Option Panel
        :return: NONE
    """
    pygame.init()
    pygame.display.set_caption('LOST IN FORREST')
    screen = pygame.display.set_mode((500, 500), 0, 32)
    menuPicture = pygame.image.load(os.path.join('images', "menuImage.jpg"))
    gameClick = False
    running = True
    print("Selected Game")
    while running:
        # allow user to pick game mode
        screen.fill((0, 0, 0))
        screen.blit(menuPicture, (0, 0))
        draw_text('ESC "Menu"', font, (255, 255, 255), screen, 20, 20)
        draw_text('Select number of players', font, (255, 255, 255), screen, 20, 50)

        mx, my = pygame.mouse.get_pos()

        # button attribute
        button_1 = pygame.Rect(150, 100, 200, 50)
        button_2 = pygame.Rect(150, 200, 200, 50)
        button_3 = pygame.Rect(150, 300, 200, 50)

        if button_1.collidepoint((mx, my)):
            if gameClick:
                print("2 players")
                random_stimulation_500()
        if button_2.collidepoint((mx, my)):
            if gameClick:
                print("3 players")
                random_stimulation_500_3player()
        if button_3.collidepoint((mx, my)):
            if gameClick:
                print("4 players")
                random_stimulation_500_4player()

        # draw button
        pygame.draw.rect(screen, (0, 0, 128), button_1)
        draw_text('Dual Player', font, (255, 255, 255), screen, 200, 100)
        pygame.draw.rect(screen, (0, 0, 128), button_2)
        draw_text('Three Player', font, (255, 255, 255), screen, 200, 200)
        pygame.draw.rect(screen, (0, 0, 128), button_3)
        draw_text('Four Player', font, (255, 255, 255), screen, 200, 300)

        gameClick = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    gameClick = True

        pygame.display.update()
        mainClock.tick(60)


def random_stimulation_500():
    """
    Random Stimulate map size of 500 * 500
    :return: NONE
    """
    pygame.init()
    pygame.mixer.init()

    # map data
    width, height = 500, 500
    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "500map.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "tom.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "jerry.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # init player position and draw them
    player_one_container = pygame.Rect(0, 0, person_width, person_height)
    player_two_container = pygame.Rect(width - 70, height - 70, person_width, person_height)
    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(player_one_container.x - player_two_container.x) <= 100 and abs(
                    player_one_container.y - player_two_container.y) <= 100:
                Data = "500 " + str(stepCounter) + " 2players\n"
                recordRandom(Data)
                is_GameOver = False
                randomStimulationMenu()

        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        player_one_random_movement(player_one_container, width, height)
        player_two_random_movement(player_two_container, width, height)
        displayGameWindow(gameWindow,
                          player_one_container=player_one_container,
                          forrestImage=forrestImage,
                          player_two_container=player_two_container,
                          person_One_Image=person_One_Image,
                          person_Two_Image=person_Two_Image)


def random_stimulation_500_3player():
    """
    Random Stimulate map size of 500 * 500 for 3 players
    :return: NONE
    """
    pygame.init()
    pygame.mixer.init()

    # map data
    width, height = 500, 500
    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "500map.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "tom.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "jerry.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # person three image
    person_Three_Image = pygame.image.load(os.path.join('images', "sandy.png"))
    person_Three_Image.convert_alpha()
    person_Three_Image.set_colorkey(alpha)

    # init position and draw player
    player_one_container = pygame.Rect(0, 0, person_width, person_height)
    player_two_container = pygame.Rect(width - 70, height - 70, person_width, person_height)
    player_three_container = pygame.Rect(0, height - 70, person_width, person_height)

    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(player_one_container.x - player_two_container.x) <= 50 and abs(
                    player_one_container.x - player_three_container.x) <= 50 and abs(
                    player_one_container.y - player_two_container.y) <= 50 and abs(
                    player_one_container.y - player_three_container.y) <= 50:
                Data = "500 " + str(stepCounter) + " 3players\n"
                recordRandom(Data)
                is_GameOver = False
                randomStimulationMenu()
        print(player_one_container.x)
        print(player_one_container.y)
        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        player_one_random_movement(player_one_container, width, height)
        player_two_random_movement(player_two_container, width, height)
        player_three_random_movement(player_three_container, width, height)
        displayGameWindow_player3(gameWindow,
                                  forrestImage=forrestImage,
                                  player_one_container=player_one_container,
                                  player_two_container=player_two_container,
                                  player_three_container=player_three_container,
                                  person_One_Image=person_One_Image,
                                  person_Two_Image=person_Two_Image,
                                  person_Three_Image=person_Three_Image)


def random_stimulation_500_4player():
    """
    Random Stimulate map size of 500 * 500 for 4 players
    :return: NONE
    """
    pygame.init()
    pygame.mixer.init()

    # map data
    width, height = 500, 500
    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "500map.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "tom.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "jerry.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # person three image
    person_Three_Image = pygame.image.load(os.path.join('images', "sandy.png"))
    person_Three_Image.convert_alpha()
    person_Three_Image.set_colorkey(alpha)

    # person four image
    person_Four_Image = pygame.image.load(os.path.join('images', "squid.jpg"))
    person_Four_Image.convert_alpha()
    person_Four_Image.set_colorkey(alpha)

    # init position and draw player
    player_one_container = pygame.Rect(0, 0, person_width, person_height)
    player_two_container = pygame.Rect(width - 70, height - 70, person_width, person_height)
    player_three_container = pygame.Rect(0, height - 70, person_width, person_height)
    player_four_container = pygame.Rect(width - 70, 0, person_width, person_height)

    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(player_one_container.x - player_two_container.x) <= 50 and abs(
                    player_one_container.x - player_three_container.x) <= 50 and abs(
                    player_one_container.x - player_four_container.x) <= 50 and abs(
                    player_one_container.y - player_two_container.y) <= 50 and abs(
                    player_one_container.y - player_three_container.y) <= 50 and abs(
                    player_one_container.y - player_four_container.y) <= 50:
                Data = "500         " + str(stepCounter) + "   4players\n"
                recordRandom(Data)
                is_GameOver = False
                randomStimulationMenu()
        print(player_one_container.x)
        print(player_one_container.y)
        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        player_one_random_movement(player_one_container, width, height)
        player_two_random_movement(player_two_container, width, height)
        player_three_random_movement(player_three_container, width, height)
        player_four_random_movement(player_four_container, width, height)
        displayGameWindow_player4(gameWindow,
                                  forrestImage=forrestImage,
                                  player_one_container=player_one_container,
                                  player_two_container=player_two_container,
                                  player_three_container=player_three_container,
                                  player_four_container=player_four_container,
                                  person_One_Image=person_One_Image,
                                  person_Two_Image=person_Two_Image,
                                  person_Three_Image=person_Three_Image,
                                  person_Four_Image=person_Four_Image, )


def stimulation_1000_1000_MultiPlayerGameMenu():
    """

        Game Option Panel
        :return: NONE
    """
    pygame.init()
    pygame.display.set_caption('LOST IN FORREST')
    screen = pygame.display.set_mode((500, 500), 0, 32)
    menuPicture = pygame.image.load(os.path.join('images', "menuImage.jpg"))
    gameClick = False
    running = True
    print("Selected Game")
    while running:
        # allow user to pick game mode
        screen.fill((0, 0, 0))
        screen.blit(menuPicture, (0, 0))
        draw_text('ESC "Menu"', font, (255, 255, 255), screen, 20, 20)
        draw_text('Select number of players', font, (255, 255, 255), screen, 20, 50)

        mx, my = pygame.mouse.get_pos()

        # button attribute
        button_1 = pygame.Rect(150, 100, 200, 50)
        button_2 = pygame.Rect(150, 200, 200, 50)
        button_3 = pygame.Rect(150, 300, 200, 50)

        if button_1.collidepoint((mx, my)):
            if gameClick:
                print("2 players")
                random_stimulation_1000()
        if button_2.collidepoint((mx, my)):
            if gameClick:
                print("3 players")
                random_stimulation_1000_3player()
        if button_3.collidepoint((mx, my)):
            if gameClick:
                print("4 players")
                random_stimulation_1000_4player()

        # draw button
        pygame.draw.rect(screen, (0, 0, 128), button_1)
        draw_text('Dual Player', font, (255, 255, 255), screen, 200, 100)
        pygame.draw.rect(screen, (0, 0, 128), button_2)
        draw_text('Three Player', font, (255, 255, 255), screen, 200, 200)
        pygame.draw.rect(screen, (0, 0, 128), button_3)
        draw_text('Four Player', font, (255, 255, 255), screen, 200, 300)

        gameClick = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    gameClick = True

        pygame.display.update()
        mainClock.tick(60)


def random_stimulation_1000():
    """
    Random Stimulate map size of 1000 * 1000
    :return: NONE
    """
    pygame.init()
    pygame.mixer.init()

    # map data
    width, height = 1000, 1000
    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "forrest.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "tom.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "jerry.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # init player position and draw them
    player_one_container = pygame.Rect(0, 0, person_width, person_height)
    player_two_container = pygame.Rect(width - 70, height - 70, person_width, person_height)
    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(player_one_container.x - player_two_container.x) <= 100 and abs(
                    player_one_container.y - player_two_container.y) <= 100:
                Data = "1000 " + str(stepCounter) + " 2players\n"
                recordRandom(Data)
                is_GameOver = False
                randomStimulationMenu()

        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        player_one_random_movement(player_one_container, width, height)
        player_two_random_movement(player_two_container, width, height)
        displayGameWindow(gameWindow,
                          player_one_container=player_one_container,
                          forrestImage=forrestImage,
                          player_two_container=player_two_container,
                          person_One_Image=person_One_Image,
                          person_Two_Image=person_Two_Image)


def random_stimulation_1000_3player():
    """
    Random Stimulate map size of 1000*1000 for 3 players
    :return: NONE
    """
    pygame.init()
    pygame.mixer.init()

    # map data
    width, height = 1000, 1000
    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "forrest.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "tom.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "jerry.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # person three image
    person_Three_Image = pygame.image.load(os.path.join('images', "sandy.png"))
    person_Three_Image.convert_alpha()
    person_Three_Image.set_colorkey(alpha)

    # init position and draw player
    player_one_container = pygame.Rect(0, 0, person_width, person_height)
    player_two_container = pygame.Rect(width - 70, height - 70, person_width, person_height)
    player_three_container = pygame.Rect(0, height - 70, person_width, person_height)

    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(player_one_container.x - player_two_container.x) <= 50 and abs(
                    player_one_container.x - player_three_container.x) <= 50 and abs(
                    player_one_container.y - player_two_container.y) <= 50 and abs(
                    player_one_container.y - player_three_container.y) <= 50:
                Data = "1000 " + str(stepCounter) + " 3players\n"
                recordRandom(Data)
                is_GameOver = False
                randomStimulationMenu()
        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        player_one_random_movement(player_one_container, width, height)
        player_two_random_movement(player_two_container, width, height)
        player_three_random_movement(player_three_container, width, height)
        displayGameWindow_player3(gameWindow,
                                  forrestImage=forrestImage,
                                  player_one_container=player_one_container,
                                  player_two_container=player_two_container,
                                  player_three_container=player_three_container,
                                  person_One_Image=person_One_Image,
                                  person_Two_Image=person_Two_Image,
                                  person_Three_Image=person_Three_Image)


def random_stimulation_1000_4player():
    """
    Random Stimulate map size of 1000*1000 for 4 players
    :return: NONE
    """
    pygame.init()
    pygame.mixer.init()

    # map data
    width, height = 500, 500
    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "forrest.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "tom.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "jerry.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # person three image
    person_Three_Image = pygame.image.load(os.path.join('images', "sandy.png"))
    person_Three_Image.convert_alpha()
    person_Three_Image.set_colorkey(alpha)

    # person four image
    person_Four_Image = pygame.image.load(os.path.join('images', "squid.jpg"))
    person_Four_Image.convert_alpha()
    person_Four_Image.set_colorkey(alpha)

    # init position and draw player
    player_one_container = pygame.Rect(0, 0, person_width, person_height)
    player_two_container = pygame.Rect(width - 70, height - 70, person_width, person_height)
    player_three_container = pygame.Rect(0, height - 70, person_width, person_height)
    player_four_container = pygame.Rect(width - 70, 0, person_width, person_height)

    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(player_one_container.x - player_two_container.x) <= 50 and abs(
                    player_one_container.x - player_three_container.x) <= 50 and abs(
                    player_one_container.x - player_four_container.x) <= 50 and abs(
                    player_one_container.y - player_two_container.y) <= 50 and abs(
                    player_one_container.y - player_three_container.y) <= 50 and abs(
                    player_one_container.y - player_four_container.y) <= 50:
                Data = "1000 " + str(stepCounter) + " 4players\n"
                recordRandom(Data)
                is_GameOver = False
                randomStimulationMenu()
        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        player_one_random_movement(player_one_container, width, height)
        player_two_random_movement(player_two_container, width, height)
        player_three_random_movement(player_three_container, width, height)
        player_four_random_movement(player_four_container, width, height)
        displayGameWindow_player4(gameWindow,
                                  forrestImage=forrestImage,
                                  player_one_container=player_one_container,
                                  player_two_container=player_two_container,
                                  player_three_container=player_three_container,
                                  player_four_container=player_four_container,
                                  person_One_Image=person_One_Image,
                                  person_Two_Image=person_Two_Image,
                                  person_Three_Image=person_Three_Image,
                                  person_Four_Image=person_Four_Image, )


def stimulation_customizedMap_MultiPlayerGameMenu():
    """

        Game Option Panel
        :return: NONE
    """
    pygame.init()
    pygame.display.set_caption('LOST IN FORREST')
    screen = pygame.display.set_mode((500, 500), 0, 32)
    menuPicture = pygame.image.load(os.path.join('images', "menuImage.jpg"))
    gameClick = False
    running = True
    print("Selected Game")
    while running:
        # allow user to pick game mode
        screen.fill((0, 0, 0))
        screen.blit(menuPicture, (0, 0))
        draw_text('ESC "Menu"', font, (255, 255, 255), screen, 20, 20)
        draw_text('Select number of players', font, (255, 255, 255), screen, 20, 50)

        mx, my = pygame.mouse.get_pos()

        # button attribute
        button_1 = pygame.Rect(150, 100, 200, 50)
        button_2 = pygame.Rect(150, 200, 200, 50)
        button_3 = pygame.Rect(150, 300, 200, 50)

        if button_1.collidepoint((mx, my)):
            if gameClick:
                print("2 players")
                random_stimulation_CustomizeMap()
        if button_2.collidepoint((mx, my)):
            if gameClick:
                print("3 players")
                random_stimulation_CustomizeMap_3player()
        if button_3.collidepoint((mx, my)):
            if gameClick:
                print("4 players")
                random_stimulation_CustomizeMap_4player()

        # draw button
        pygame.draw.rect(screen, (0, 0, 128), button_1)
        draw_text('Dual Player', font, (255, 255, 255), screen, 200, 100)
        pygame.draw.rect(screen, (0, 0, 128), button_2)
        draw_text('Three Player', font, (255, 255, 255), screen, 200, 200)
        pygame.draw.rect(screen, (0, 0, 128), button_3)
        draw_text('Four Player', font, (255, 255, 255), screen, 200, 300)

        gameClick = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    main_menu()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    gameClick = True

        pygame.display.update()
        mainClock.tick(60)


def random_stimulation_CustomizeMap():
    """
    Random Stimulate map with customized size
    :return: NONE
    """
    pygame.init()
    pygame.mixer.init()

    # map data
    while True:
        try:
            width = int(input('Enter your width(200-1000):'))
            if width in range(200, 1000):
                break
            else:
                print("Out of range")
        except:
            print("That's not a valid option!")

    while True:
        try:
            height = int(input('Enter your height(200-1000): '))
            if height in range(200, 1000):
                break
            else:
                print("Out of range")
        except:
            print("That's not a valid option!")

    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "forrest.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "tom.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "jerry.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # init player position and draw them
    player_one_container = pygame.Rect(0, 0, person_width, person_height)
    player_two_container = pygame.Rect(width - 70, height - 70, person_width, person_height)
    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(player_one_container.x - player_two_container.x) <= 100 and abs(
                    player_one_container.y - player_two_container.y) <= 100:
                Data = str(width)+"*"+str(height) + "          " + str(stepCounter) + " 2player\n"
                recordRandom(Data)
                is_GameOver = False
                randomStimulationMenu()

        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        player_one_random_movement(player_one_container, width, height)
        player_two_random_movement(player_two_container, width, height)
        displayGameWindow(gameWindow,
                          player_one_container=player_one_container,
                          forrestImage=forrestImage,
                          player_two_container=player_two_container,
                          person_One_Image=person_One_Image,
                          person_Two_Image=person_Two_Image)


def random_stimulation_CustomizeMap_3player():
    """
    Random Stimulate map with customized size for 3 players
    :return: NONE
    """
    pygame.init()
    pygame.mixer.init()

    # map data
    while True:
        try:
            width = int(input('Enter your width(200-1000):'))
            if width in range(200, 1000):
                break
            else:
                print("Out of range")
        except:
            print("That's not a valid option!")

    while True:
        try:
            height = int(input('Enter your height(200-1000): '))
            if height in range(200, 1000):
                break
            else:
                print("Out of range")
        except:
            print("That's not a valid option!")

    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "forrest.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "tom.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "jerry.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # person three image
    person_Three_Image = pygame.image.load(os.path.join('images', "sandy.png"))
    person_Three_Image.convert_alpha()
    person_Three_Image.set_colorkey(alpha)

    # init position and draw player
    player_one_container = pygame.Rect(0, 0, person_width, person_height)
    player_two_container = pygame.Rect(width - 70, height - 70, person_width, person_height)
    player_three_container = pygame.Rect(0, height - 70, person_width, person_height)

    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(player_one_container.x - player_two_container.x) <= 50 and abs(
                    player_one_container.x - player_three_container.x) <= 50 and abs(
                    player_one_container.y - player_two_container.y) <= 50 and abs(
                    player_one_container.y - player_three_container.y) <= 50:
                Data = str(width)+"*"+str(height) + "          " + str(stepCounter) + " 3player\n"
                recordRandom(Data)
                is_GameOver = False
                randomStimulationMenu()
        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        player_one_random_movement(player_one_container, width, height)
        player_two_random_movement(player_two_container, width, height)
        player_three_random_movement(player_three_container, width, height)
        displayGameWindow_player3(gameWindow,
                                  forrestImage=forrestImage,
                                  player_one_container=player_one_container,
                                  player_two_container=player_two_container,
                                  player_three_container=player_three_container,
                                  person_One_Image=person_One_Image,
                                  person_Two_Image=person_Two_Image,
                                  person_Three_Image=person_Three_Image)


def random_stimulation_CustomizeMap_4player():
    """
    Random Stimulate map with customized size for 4 players
    :return: NONE
    """
    pygame.init()
    pygame.mixer.init()

    """
        Random Stimulate map with customized size
        :return: NONE
        """
    pygame.init()
    pygame.mixer.init()

    # map data
    while True:
        try:
            width = int(input('Enter your width(200-1000):'))
            if width in range(200, 1000):
                break
            else:
                print("Out of range")
        except:
            print("That's not a valid option!")

    while True:
        try:
            height = int(input('Enter your height(200-1000): '))
            if height in range(200, 1000):
                break
            else:
                print("Out of range")
        except:
            print("That's not a valid option!")

    gameWindow = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Lost in the Wood")

    # forrest image
    forrestImage = pygame.image.load(os.path.join('images', "forrest.jpg"))

    # person one image
    person_One_Image = pygame.image.load(os.path.join('images', "tom.png"))
    person_One_Image.convert_alpha()
    person_One_Image.set_colorkey(alpha)

    # person two image
    person_Two_Image = pygame.image.load(os.path.join('images', "jerry.png"))
    person_Two_Image.convert_alpha()
    person_Two_Image.set_colorkey(alpha)

    # person three image
    person_Three_Image = pygame.image.load(os.path.join('images', "sandy.png"))
    person_Three_Image.convert_alpha()
    person_Three_Image.set_colorkey(alpha)

    # person four image
    person_Four_Image = pygame.image.load(os.path.join('images', "squid.jpg"))
    person_Four_Image.convert_alpha()
    person_Four_Image.set_colorkey(alpha)

    # init position and draw player
    player_one_container = pygame.Rect(0, 0, person_width, person_height)
    player_two_container = pygame.Rect(width - 70, height - 70, person_width, person_height)
    player_three_container = pygame.Rect(0, height - 70, person_width, person_height)
    player_four_container = pygame.Rect(width - 70, 0, person_width, person_height)

    clock = pygame.time.Clock()
    is_GameOver = False
    stepCounter = 0
    while not is_GameOver:
        game_sound.play(-1)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # if they meet game over
            if abs(player_one_container.x - player_two_container.x) <= 50 and abs(
                    player_one_container.x - player_three_container.x) <= 50 and abs(
                    player_one_container.x - player_four_container.x) <= 50 and abs(
                    player_one_container.y - player_two_container.y) <= 50 and abs(
                    player_one_container.y - player_three_container.y) <= 50 and abs(
                    player_one_container.y - player_four_container.y) <= 50:
                Data = str(width) + "*" + str(height) + "          " + str(stepCounter) + " 4player\n"
                recordRandom(Data)
                is_GameOver = False
                randomStimulationMenu()
        key_pressed = pygame.key.get_pressed()
        if key_pressed:
            stepCounter += 1
        player_one_random_movement(player_one_container, width, height)
        player_two_random_movement(player_two_container, width, height)
        player_three_random_movement(player_three_container, width, height)
        player_four_random_movement(player_four_container, width, height)
        displayGameWindow_player4(gameWindow,
                                  forrestImage=forrestImage,
                                  player_one_container=player_one_container,
                                  player_two_container=player_two_container,
                                  player_three_container=player_three_container,
                                  player_four_container=player_four_container,
                                  person_One_Image=person_One_Image,
                                  person_Two_Image=person_Two_Image,
                                  person_Three_Image=person_Three_Image,
                                  person_Four_Image=person_Four_Image, )

main_menu()
