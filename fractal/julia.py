# julia

import sys,math,time
import pygame
from pygame.locals import *

pygame.init()
surface = pygame.display.set_mode((900, 900))

w= WIDTH = 900
h = HEIGHT = 900
zoom = 1

def julia(i):
    maxIter = 255
 
    for x in range(0,w,res):
        for y in range(0,h,res):
            zx =  (x - w/2) / w * 3 * zoom
            zy =   (y - h/2) / h * 2 * zoom
            i = maxIter
            while zx*zx + zy*zy < 4 and i > 1:
                tmp = zx*zx - zy*zy + cx
                zy = 2.0 * zx * zy + cy
                zx =  tmp              
                i -= 1
                
            colorpixel(x,y,i)
                          
def colorpixel(x,y,c):
    if invertcolors == 1: c = 255 - c
    pen = clr[c]
    pygame.draw.rect(surface,pen,(x,y,res,res))
    
scale = 1./384
cx = -0.45
cy = 0.56

clr= [int(i**3) for i in range(255,-1,-1)]

invertcolors = 1

res = 1
for r in range(70):
    julia(1)
    pygame.display.flip()
    cy += 0.001
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            sys.exit(0)
            break
          
