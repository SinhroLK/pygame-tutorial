from logging import BASIC_FORMAT
import random, sys, copy, os, pygame
from tkinter.tix import IMAGE
from pygame.locals import *

FPS = 30
WINWIDTH = 800
WINHEIGHT = 600
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)

#sirina i visina svakog polja u pikselima
TILEWIDTH = 50
TILEHEIGHT = 85
TILEFLOORHEIGHT = 45

CAM_MOVE_SPEED = 5 # koliko piksela po frejmu se pomera kamera

#procenat spoljanjih polja koja imaju dekoraciju
OUTSIDE_DECORATION_PCT = 20

BRIGHTBLUE = (0,170,255)
WHITE = (255,255,255)
BGCOLOR = BRIGHTBLUE
TEXTCOLOR = WHITE

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

def main():
    global FPSCLOCK, DISPLAYSURF, IMAGEDICT, TILEMAPPING, OUTSIDEDECOMAPPING, BASICFONT, PLAYERIMAGES, currentImage

    #Pygame inicijalizaija i podesavanje globalnih promenljivih
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    pygame.display.set_caption('Star Pusher')
    BASICFONT = pygame.font.Font("freesansbold.ttf", 18)
    # sve slike koje se koriste 
    IMAGESDICT = {'uncovered goal': pygame.image.load('RedSelector.png'),
                  'covered goal': pygame.image.load('Selector.png'),
                  'star': pygame.image.load('Star.png'),
                  'corner': pygame.image.load('Wall Block Tall.png'),
                  'wall': pygame.image.load('Wood Block Tall.png'),
                  'inside floor': pygame.image.load('Plain Block.png'),
                  'outside floor': pygame.image.load('Grass Block.png'),
                  'title': pygame.image.load('star_title.png'),
                  'solved': pygame.image.load('star_solved.png'),
                  'princess': pygame.image.load('princess.png'),
                  'boy': pygame.image.load('boy.png'),
                  'catgirl': pygame.image.load('catgirl.png'),
                  'horngirl': pygame.image.load('horngirl.png'),
                  'pinkgirl': pygame.image.load('pinkgirl.png'),
                  'rock': pygame.image.load('Rock.png'),
                  'short tree': pygame.image.load('Tree_Short.png'),
                  'tall tree': pygame.image.load('Tree_Tall.png'),
                  'ugly tree': pygame.image.load('Tree_Ugly.png')}
    #globalne vrednosti iz tekstualnog fajla za nivoe
    TILEMAPPING = {'x': IMAGESDICT['corner'],
                   '#': IMAGESDICT['wall'],
                   'o': IMAGESDICT['inside floor'],
                   ' ': IMAGESDICT['outside floor']}
    OUTSIDEDECOMAPPING = {'1': IMAGESDICT['rock'],
                          '2': IMAGESDICT['short tree'],
                          '3': IMAGESDICT['tall tree'],
                          '4': IMAGESDICT['ugly tree']}
    #PLAYERIMAGES je lista svih likova koje igrac moze da bude
    #currentImages je je index trenutne slike koju igrac koristi
    currentImages = 0
    PLAYERIMAGES = [IMAGESDICT['princess'],
                    IMAGESDICT['boy'],
                    IMAGESDICT['catgirl'],
                    IMAGESDICT['horngirl'],
                    IMAGESDICT['pinkgirl']]

    startScreen() #prikazuj sve dok igrac ne klikne A

    #procitaj tekstualni fajl sa nivoima
    levels = readLevelsFile('starPusherLevels.txt')
    currentLevelIndex = 0

    #glavna petlja
    while True:
        #pokreni nivo kako bi zapoceo igru
        result = runLevel(levels, currentLevelIndex)
        if result in ('solved', 'next'):
            #idi na sledeci nivo
            currentLevelIndex += 1
            if currentLevelIndex >= len(levels):
                currentLevelIndex = 0
        elif result == 'back':
            currentLevelIndex -= 1
            if currentLevelIndex < 0:
                currentLevelIndex = len(levels) - 1
        elif result == 'reset':
            pass # petlja sama okrene runLevel() da resetuje

