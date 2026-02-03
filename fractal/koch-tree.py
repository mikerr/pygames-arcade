
import pygame
from pygame.locals import *
import math,random,time

pygame.init()
# Resolution is ignored on Android
surface = pygame.display.set_mode((640, 480))
    
def drawangle(linestart,angle,length):
    
    ax = math.sin(math.radians(angle) )* length
    ay = math.cos(math.radians(angle )) * length
    
    x,y = linestart
    lineend = (x + ax,y + ay)
    
    return lineend
    
def koch (linestart,angle,length,order):
    kochangles = [60,-120,60,0]
    
    points = [linestart]
    line = linestart
    length= length / 3
    if order > 0:
      for a in kochangles:  	
        angle = angle + a
        line = drawangle(line,angle, length)
        points.append (line)
  
        pygame.draw.lines(surface, 53335,0,points)     
        koch(line,angle,length,order - 1)
        
    return line
    
linestart = (300,0)

angle = 0

while True:
    for ev in pygame.event.get():
        if ev.type == QUIT:
            pygame.quit()
             
    linestart = koch(linestart,angle,150,6)
    
    pygame.display.flip()
    
    angle = angle - random.randrange(-45,45)
    
    time.sleep(1)
