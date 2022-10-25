import pygame, random, time, math, sys
from pygame.locals import *

FPS = 30
WINWIDTH = 640
WINHEIGHT = 480
HALF_WINWIDTH = int(WINWIDTH/2)
HALF_WINHEIGHT = int(WINHEIGHT/2)

GRASSCOLOR = (24 ,255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
CAMERASLACK = 90 #koliko se veverica pomeri pre nego se pomeri kamera
MOVERATE = 9 #kolko brzo se lik pomera
BOUNCERATE = 6 #kolko brzo lik skace
BOUNCEHEIGHT = 30 #kolko visoko lik skace
STARTSIZE = 25 #pocetna velicina lika
WINSIZE = 300 #velicina potrebna za kraj igre
INVULTIME = 2 #koliko sekundi je lik imun na stetu nakon sto ga udare
GAMEOVERTIME = 4 #kolko dugo game over screen ostaje nakon sto se igra zavrsi
MAXHEALTH = 3 #kolko HP lik ima na pocetku
NUMGRASS = 80 #broj travnatih povrsina
NUMSQUIRRELS = 30 #broj veverica u aktivnom prostoru
SQUIRRELMINSPEED = 3 #najsporija veverica
SQUIRRELMAXSPEED = 7 #najbrza veverica
DIRCHANGEFREQ = 2 #% sanse promene smera po frejmu
LEFT = 'left'
RIGHT = 'right'

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, L_SQUIR_IMG, R_SQUIR_IMG, GRASSIMAGES
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_icon(pygame.image.load('gameicon.png'))
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    pygame.display.set_caption('Squirrel eat squirrel')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 32)
    #ucitaj slike
    L_SQUIR_IMG = pygame.image.load('squirrel.py')
    R_SQUIR_IMG = pygame.transform.flip(L_SQUIR_IMG,True,False)
    GRASSIMAGES = []
    for i in range(5):
        GRASSIMAGES.append(pygame.image.load('grass%s.png' %i))
    while True:
        runGame()

def runGame():
    #podesi promenljive za pocetak
    invulnerableMode = False #da li je lik neranjiv
    invulnerableStartTime = 0 #trenutak kada je postao neranjiv
    gameOverMode = False #da li je igrac izgubio
    gameOverStartTime = 0 #trenutak kada je igrac izgubio
    winMode = False #da li je igrac pobedio

    gameOverSurf = BASICFONT.render('Game Over', True, WHITE)
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.center = (HALF_WINWIDTH, HALF_WINHEIGHT)

    winSurf = BASICFONT.render('YOU WON!!', True, WHITE)
    winRect = winSurf.get_rect()
    winRect.center = (HALF_WINWIDTH, HALF_WINHEIGHT)

    winSurf2 = BASICFONT.render('Press "r" to restart', True, WHITE)
    winRect2 = winSurf2.get_rect()
    winRect2.center = (HALF_WINWIDTH, HALF_WINHEIGHT)

    #camerax i cameray su koordinate sredine kamere
    camerax = 0
    cameray = 0

    grassObjs = [] #svi trava objekti
    squirrelObjs = [] #svi ne-lik veverica objekti
    #lik objekat
    playerObj = {'surface': pygame.transform.scale(L_SQUIR_IMG,(STARTSIZE, STARTSIZE)),
                 'facing': LEFT,
                 'size': STARTSIZE,
                 'x': HALF_WINWIDTH,
                 'y': HALF_WINHEIGHT,
                 'bounce': 0,
                 'health': MAXHEALTH}
    moveLeft = False
    moveRight = False
    moveUp = False
    moveDown = False

    #random trava za pocetak
    for i in range(10):
        grassObjs.append(makeNewGrass(camerax, cameray))
        grassObjs[i]['x'] = random.randint(0,WINWIDTH)
        grassObjs[i]['y'] = random.randint(0, WINHEIGHT)

    while True:
        #proveri dal treba da se iskljuci neranjivost
        if invulnerableMode and time.Time() - invulnerableStartTime > INVULTIME:
            invulnerableMode = False
        
        #pomeri veverice
        for sObjs in squirrelObjs:
            #pomeraj veverice i podesi bounce
            sObjs['x'] += sObjs['movex']
            sObjs['y'] += sObjs['movey']
            sObjs['bounce'] += 1
            if sObjs['bounce'] > sObjs['bouncerate']:
                sObjs['bounce'] = 0 #resetuj bounce
            # random sansa da promene smer
            if random.randint(0,99) < DIRCHANGEFREQ:
                sObjs['movex'] = getRandomVelocity()
                sObjs['movey'] = getRandomVelocity()
                if sObjs['movex'] > 0: # okrenut desno
                    sObjs['surface'] = pygame.transform.scale(R_SQUIR_IMG, (sObjs['width'], sObjs['height']))
                else: #okrenut levo
                    sObjs['surface'] = pygame.transform.scale(L_SQUIR_IMG, (sObjs['width'], sObjs['height']))
        
        #prodji keoz sve objekte i vidi dal neki treba da se obrise
        for i in range(len(grassObjs)-1,-1,-1):
            if isOutsideActiveArea(camerax, cameray, grassObjs[i]):
                del grassObjs[i]
        for i in range(len(squirrelObjs)-1,-1,-1):
            if isOutsideActiveArea(camerax, cameray, squirrelObjs[i]):
                del squirrelObjs[i]
        
        #dodaj jos trave i veverica ako ih nema dovoljno
        while len(grassObjs) < NUMGRASS:
            grassObjs.append(makeNewGrass(camerax, cameray))
        while len(squirrelObjs) < NUMSQUIRRELS:
            squirrelObjs.append(makeNewSquirrel(camerax, cameray))
        
        #podesi camerax i cameray ako si izvan camera slack granica
        playerCenterx = playerObj['x'] + int(playerObj['size'] / 2)
        playerCentery = playerObj['y'] + int(playerObj['size'] / 2)
        if (camerax + HALF_WINWIDTH) - playerCenterx > CAMERASLACK:
            camerax = playerCenterx + CAMERASLACK - HALF_WINWIDTH
        elif playerCenterx - (camerax + HALF_WINWIDTH) > CAMERASLACK:
            camerax = playerCenterx - CAMERASLACK - HALF_WINWIDTH
        
        if (cameray + HALF_WINHEIGHT) - playerCentery > CAMERASLACK:
            cameray = playerCentery + CAMERASLACK - HALF_WINHEIGHT
        elif playerCentery - (cameray + HALF_WINHEIGHT) > CAMERASLACK:
            cameray = playerCentery - CAMERASLACK - HALF_WINHEIGHT

        # ofarbaj pozadinu zeleno
        DISPLAYSURF.fill(GRASSCOLOR)

        # nacrtaj trava objekte
        for gObj in grassObjs:
            gRect = pygame.Rect((gObj['x'] - camerax,
                                 gObj['y'] - cameray,
                                 gObj['width'],
                                 gObj['height']))
            DISPLAYSURF.blit(GRASSIMAGES[gObj['grassImage']], gRect)
        
        # nacrtaj ostale veverice
        for sObj in squirrelObjs:
            sRect = pygame.Rect((sObj['x'] - camerax,
                                 sObj['y'] - cameray - getBounceAmount(sObj['bounce'], sObj['bouncerate'], sObj['bounceheight']),
                                 sObj['width'],
                                 sObj['height']))
            DISPLAYSURF.blit(sObj['surface'], sObj['rect'])
        
        #nacrtaj lika
        flashIsOn = round(time.time(), 1) * 10 % 2 == 1
        if not gameOverMode and not (invulnerableMode and flashIsOn):
            playerObj['rect'] = pygame.Rect((playerObj['x'] - camerax,
            playerObj['y'] - cameray - getBounceAmount(playerObj['bounce'], BOUNCERATE, BOUNCEHEIGHT),
            playerObj['size'],
            playerObj['size']))
            DISPLAYSURF.blit(playerObj['surface'], playerObj['rect'])

        # nacrtaj health bar
        drawHealthMeter(playerObj['health'])

        
