import random, pygame, sys
from turtle import window_width
from pygame.locals import *
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