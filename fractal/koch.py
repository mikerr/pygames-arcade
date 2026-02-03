# koch snowflake fractal

import pygame
from pygame.locals import *
import math,random,time

pygame.init()

surface = pygame.display.set_mode((640, 480))
WHITE = 65535
 
def drawangle(linestart,angle,length):
    
    ax = math.sin(math.radians(angle) )* length
    ay = math.cos(math.radians(angle )) * length
    
    x,y = linestart
    lineend = (x + ax,y + ay)
    
    return lineend

kochangles = [0,60,-120,60]
 
def koch (linestart,angle,length,order):
    
    points = [linestart]
    line = linestart
    length= length / 3
    
    for a in kochangles:  	
        angle = angle + a
        line = drawangle(line,angle, length)
        points.append (line)
        
        if order > 0: 
              koch(points[-2],angle,length,order - 1)
        else:
              pygame.draw.lines(surface,WHITE,0,points)         
    return line
    
recursion  = 0

angle = 0
linestart = (700,400)

while True:
    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.quit()
     # surface.fill(0)
    
    linestart = koch(linestart,angle,700,recursion)
    
    pygame.display.flip()
    
    # triangle
    angle = angle - 120
    
    time.sleep(0)
    if angle  % 360 == 0:
    	time.sleep(1)
    	recursion = recursion + 1
    	surface.fill(0)
