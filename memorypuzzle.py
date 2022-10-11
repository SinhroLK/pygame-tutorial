import random, pygame, sys
from turtle import window_width
from pygame.locals import *

from catanimation import DISPLAYSURF
FPS = 30 #fps jelte
WINDOWWIDTH = 640 #sirina prozora u pikselima
WINDOWHEIGHT = 480 #visina prozora u pikselima
REVEALSPEED = 8 #brzina kojom se okrece kartica
BOXSIZE = 40 #sirina i visina kutije u pikselima
GAPSIZE = 10 #razmak izmedju kutija

BOARDWIDTH = 10 #broj kolona 
BOARDHEIGHT = 7 #broj redova
assert(BOARDWIDTH * BOARDHEIGHT) % 2 == 0, "Tabla mora da ima paran broj kutija"
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)
#boje
GRAY = (100,100,100)
NAVYBLUE = (60,60,100)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
ORANGE = (255,128,0)
PURPLE = (255,0,255)
CYAN = (0,255,255)
BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE
#oblici
DONUT = "donut"
SQUARE = "square"
DIAMOND = "diamond"
LINES = "lines"
OVAL = "oval"

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, "Tabla je previse velika za ovaj broj oblika/boja"

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    mousex = 0 #x koordinata kursora
    mousey = 0 #y koordinata kursora
    pygame.display.set_caption("Memory game")

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealBoxesData(False)
    
    firstSelection = None
    
    DISPLAYSURF.fill(BGCOLOR)
    startGameAnimation(mainBoard)

    while True:
        mouseClicked = False
        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(mainBoard, revealedBoxes)

        for event in pygame.event.get():
            if event.type==QUIT or (event.type == KEYUP and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex,mousey = event.pos
                mouseClicked = True
        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx != None and boxy != None:
            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx, boxy)
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                revealBoxesAnimation(mainBoard, [(boxx, boxy)])
                revealedBoxes[boxx][boxy] = True #namesta kutiju na otkriveno
                if firstSelection == None: #trenutna kutija je prva odabrana
                    firstSelection = (boxx,boxy)
                else:#trenutna kutija je druga odabrana
                    icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                    icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)
                    if icon1shape != icon2shape or icon1color!= icon2color:#nisu isti oblik ili boja
                        pygame.time.wait(1000)#sacekaj 100 milisekundi iliti 1 sekundu
                        coverBoxesAnimation(mainBoard,[(firstSelection[0], firstSelection[1]), (boxx,boxy)])
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxx][boxy] = False
                    elif hasWon(revealedBoxes):#proveri da nisi pobedio
                        gameWonAnimation(mainBoard)
                        pygame.time.wait(2000)
                        #resetuje tablu
                        mainBoard = getRandomizedBoard()
                        revealedBoxes = generateRevealBoxesData(False)
                        #pokazi tablu
                        drawBoard(mainBoard, revealedBoxes)
                        pygame.display.update()
                        pygame.time.wait(1000)
                        #ponovo pokreni patriju
                        startGameAnimation(mainBoard)
                    firstSelection = None #resetuj prvi odabrani  
        pygame.display.update()
        FPSCLOCK.tick(FPS)  
def generateRevealBoxesData(val):
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT)
    return revealedBoxes

def getRandomizedBoard():
    #napravi listu svih mogucih kombinacija
    icons = []
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append((shape,color))
    random.shuffle(icons) #randomizuje raspored ikonica
    numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT / 2) # kolko ikonica nam treba
    icons = icons[:numIconsUsed] * 2 # napravi dve od svaku
    random.shuffle(icons)
    #napravi tablu sa nasumicno postavljene ikonice
    board = []
    for x in range (BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(icons[0])
            del icons[0] #izbacuje ikonicu kad je iskoristimo
        board.append(column)
    return board
def splitIntoGroupsOf(groupSize, theList):
    result=[]
    for i in range(0,len(theList), groupSize):
        result.append(theList[i:i+groupSize])
    return result
def leftTopCoordsOfBox(boxx,boxy):
    #konvertuje koordinate table u piksele
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)
def getBoxAtPixel(x,y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top=leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x,y):
                return(boxx,boxy)
    return(None, None)
def drawIcon(shape, color, boxx, boxy):
    quarter = int(BOXSIZE * 0.25)
    half = int(BOXSIZE * 0.5)
    left, top = leftTopCoordsOfBox(boxx,boxy) # nadji koordinate 
    #nacrtaj oblik
    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top+ half), half-5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half),quarter-5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top+ quarter, BOXSIZE - half, BOXSIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left+ BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1), (left, top +half)))
    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left +i, top))
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE- 1), (left + BOXSIZE - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter,BOXSIZE, half))
def getShapeAndColor(board, boxx, boxy):
    return board[boxx][boxy][0], board[boxx][boxy][1]
def drawBoxCovers(board, boxes, coverage):
    #crta kutije koje su pokrivene/oktrivene
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage>0:
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
    pygame.display.upadate()
    FPSCLOCK.tick(FPS)
def revealBoxesAnimation(board, boxesToReveal):
    #otkriva kutije
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
        drawBoxCovers(board, boxesToReveal, coverage)
def coverBoxesAnimation(board, boxesToCover):
    for coverage in range(0,BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesToCover, coverage)
def drawBoard(board, revealed):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)
def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left-5, top-5, BOXSIZE+10, BOXSIZE+10), 4)
def startGameAnimation(board):
    coveredBoxes = generateRevealBoxesData(False)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append((x,y))
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8, boxes)
    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)
def gameWonAnimation(board):
    coveredBoxes = generateRevealBoxesData(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR
    for i in range (13):
        color1, color2 = color2, color1
        DISPLAYSURF.fill(color1)
        drawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)
def hasWon(revealedBoxes):
    for i in revealedBoxes:
        if False in i:
            return False
    return True

if __name__ == "__main__":
    main()