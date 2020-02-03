import pygame
import time
from random import random, randint

pygame.init()

clock = pygame.time.Clock()
slowFactor = 0.97
gravity = 0.15

swags = []
displayWidth = 1300
displayHeight = 500

gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption('[hey]')

backgroundColor = (0, 0, 255)
background = pygame.image.load('map.png')

flower = pygame.image.load('flower.png')
bee = pygame.image.load('bee.png')
goat = pygame.image.load('goat.png')
lava = pygame.image.load('lava.png')
octo = pygame.image.load('octo.png')
bike = pygame.image.load('bike.png')
beer = pygame.image.load('beer.png')
heart = pygame.image.load('heart.png')


ashSL = pygame.image.load('ashstandleft.png')
ashLL = pygame.image.load('ashliftleft.png')
ashWL = pygame.image.load('ashwalkleft.png')
ashSR = pygame.image.load('ashstandright.png')
ashLR = pygame.image.load('ashliftright.png')
ashWR = pygame.image.load('ashwalkright.png')

ashSize = (24,65)
ashleyRight = True
ashleyWalk = 0



def draw_background():
    gameDisplay.fill(backgroundColor)
    gameDisplay.blit(pygame.transform.scale(background, (displayWidth, displayHeight)), (0, 0))


def draw_ash(directionright, walkstate, x, y):
    if directionright == True:
        if walkstate == 0:
            gameDisplay.blit(ashSR, (x, y))
        elif walkstate == 1:
            gameDisplay.blit(ashLR, (x, y))
        elif walkstate == 2:
            gameDisplay.blit(ashWR, (x, y))
        else:
            print "wrong walkstate!"
    elif directionright == False:
        if walkstate == 0:
            gameDisplay.blit(ashSL, (x, y))
        elif walkstate == 1:
            gameDisplay.blit(ashLL, (x, y))
        elif walkstate == 2:
            gameDisplay.blit(ashWL, (x, y))
        else:
            print "wrong walkstate!"


def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()


def message_display(text):
    largeText = pygame.font.Font('wedgie.ttf',20)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((displayWidth/8),(displayHeight/20))
    gameDisplay.blit(TextSurf, TextRect)


def game_loop(directionright, walkstate):
    x = (displayWidth * 0.16)
    y = (displayHeight * 0.3)
    x_change = 0
    y_change = 0
    moving = False

    while True:

        for event in pygame.event.get():  # and event is not quit, which literally just means hitting the upper right x
            if event.type == pygame.QUIT:
                print ";-P"
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:  # move the car a little if keys are being presed
                if event.key == pygame.K_LEFT:
                    x_change = -5
                    directionright = False
                    moving = True
                elif event.key == pygame.K_RIGHT:
                    x_change = 5
                    directionright = True
                    moving = True
                elif event.key == pygame.K_UP:
                    y_change = -5
                    moving = True
                elif event.key == pygame.K_DOWN:
                    y_change = 5
                    moving = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    x_change, y_change, walkstate = 0, 0, 0
                    moving = False

        if moving == True:
            walkstate = (walkstate + 1) % 3

        x = max(0, min(displayWidth - ashSize[0], x + x_change))
        y = max(0, min(displayHeight - ashSize[1], y + y_change))

        splash = 25

        if x-splash < displayWidth * 0.16 < x+splash and y-splash < displayHeight * 0.3 < y+splash and randint(0,19) < 1:
            swags.append(Swag((x, y), flower))
        if x-splash < displayWidth * 0.05 < x+splash and y-splash < displayHeight * 0.1 < y+splash and randint(0,9) < 1:
            swags.append(Swag((x, y), bee))
        if x-splash < displayWidth * 0.93 < x+splash and y-splash < displayHeight * 0.2 < y+splash and randint(0,19) < 1:
            swags.append(Swag((x, y), goat))
        if x-splash < displayWidth * 0.93 < x+splash and y-splash < displayHeight * 0.2 < y+splash and randint(0,19) < 1:
            swags.append(Swag((x, y), lava))
        if x-splash < displayWidth * 0.9 < x+splash and y-splash < displayHeight * 0.08 < y+splash and randint(0,9) < 1:
            swags.append(Swag((x, y), bike))
        if x-splash < displayWidth * 0.125 < x+splash and y-splash < displayHeight * 0.12 < y+splash and randint(0,9) < 1:
            swags.append(Swag((x, y), octo))
        if x-splash < displayWidth * 0.27 < x+splash and y-splash < displayHeight * 0.65 < y+splash and randint(0,19) < 1:
            swags.append(Swag((x, y), beer))
        if x-splash < displayWidth * 0.27 < x+splash and y-splash < displayHeight * 0.65 < y+splash and randint(0,19) < 1:
            swags.append(Swag((x, y), heart))

        draw_background()
        draw_ash(directionright, walkstate, x, y)  # update location
        for swag in swags:
            swag.move()
            gameDisplay.blit(swag.image, (swag.x_coord, swag.y_coord))
        message_display('Good times: %d' % len(swags))
        pygame.display.update()  # redraw everything

        clock.tick(1680)  # allow 0.12 seconds to pass



class Swag(object):

    def move(self):
        self.x_coord += self.x_speed
        self.x_speed *= slowFactor
        if self.y_coord > self.origin[1]:
            self.y_speed *= -1
        self.y_speed *= slowFactor
        if abs(self.y_speed) < 0.01:
            self.y_speed = 0
        else:
            self.y_speed += gravity
        self.y_coord += self.y_speed


    def __init__(self, origin, image):
        self.x_speed = randint(0,4) - 2
        self.y_speed = randint(0,10) * -1
        self.origin = origin
        self.x_coord = origin[0]
        self.y_coord = origin[1]
        self.image = image


game_loop(ashleyRight, ashleyWalk)  # run the game until the user hits the x
pygame.quit()  # if by some miracle you get here without that happening, quit immediately omg
quit()

