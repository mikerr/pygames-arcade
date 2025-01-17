# knightlore - isometric game

import pygame
import time,random

import RPi.GPIO as GPIO         

buttons = {
           "A":5,
           "B":6,
           "UP":17,
           "DOWN":22,
           "LEFT":27,
           "RIGHT":23,
           "CENTER":4
}
WIDTH = HEIGHT = 240

BLACK = (0,0,0)
BLUE = (0,0,255)
RED = (255,0,0)
MAGENTA = (255,0,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)
CYAN = (0,255,255)
WHITE = (255,255,255)
colors = (BLACK,BLUE,RED,MAGENTA,CYAN,YELLOW,WHITE)


class spriteobj:
    color = WHITE
    flip = 0
    x = y = 0
    xdir = ydir = 0.5
    time = grabbed = 0
    img = [0,0]
    w = h = 32

def iso2screen (x,y):
     # convert to isometric 
     isox = 100 + int ( 11 * (x - y))
     isoy = 20 + int ( 6 * (x + y ))
     return (isox,isoy)

def getsprite(spritesheet,x,y,w,h):
    sprite = pygame.Surface([w,h])
    sprite.blit(spritesheet,(0,0),(x,y,w,h))
    return sprite

def blitsprite (spritesheet,sprite,mirror = 0):
     r,g,b = sprite.color

     isox, isoy = iso2screen(sprite.x,sprite.y)
     image = getsprite(spritesheet,sprite.img[0],sprite.img[1],sprite.w,sprite.h)
     image.fill((r,g,b,255), special_flags=pygame.BLEND_RGBA_MIN)
     screen.blit(pygame.transform.flip(image,mirror,False),(isox,isoy),(0,0,sprite.w,sprite.h))
    
# initialize
# setup gpio
GPIO.setmode(GPIO.BCM)         
for btn in buttons:
    GPIO.setup(buttons[btn], GPIO.IN)
def pressed(btn) :
    return ( GPIO.input(buttons[btn]) != True) 

screen = pygame.display.set_mode()
pygame.mouse.set_visible(False) 

spritesheet = pygame.image.load("sabreman.bmp")
backdrop = pygame.image.load("backdrop.png")

sabreman = spriteobj()
sabreman.img = [0,32]
sabreman.w = 23

man = 0
def update () :
    global firing,wolf,man
    
    if (pressed("A")) : firing  = 1
    else : firing = 0
    
    if (pressed("A")) : man = 65 - man
    
    wolfimg = 64
    
    speed = 0.05
    if (pressed("DOWN")):
        sabreman.img[1] = man + 32 #facing front
        sabreman.ydir += speed
        sabreman.flip  = 1
    if (pressed("RIGHT")):
        sabreman.img[1] = man + 32  # facing front
        sabreman.xdir += speed
        sabreman.flip  = 0
        
    if (pressed("UP")):
        sabreman.img[1] = man # facing away
        sabreman.ydir -= speed
        sabreman.flip  = 1
    if (pressed("LEFT")):
        sabreman.img[1] = man # facing away
        sabreman.xdir -= speed
  
    # keep on screen / wrap left/right
    if (sabreman.x < 0) : sabreman.x = 0 ; sabreman.xdir = 0
    if (sabreman.x > 8) : sabreman.x = 8 ; sabreman.xdir = 0
    if (sabreman.y < 0) : sabreman.y = 0 ; sabreman.ydir = 0
    if (sabreman.y > 8) : sabreman.y = 8 ; sabreman.ydir = 0

    sabreman.x += sabreman.xdir 
    sabreman.y += sabreman.ydir

    sabreman.xdir *= 0.7
    sabreman.ydir *= 0.7

    stopped =  speed  / 2 
    if (abs(sabreman.xdir) > stopped or abs(sabreman.ydir) > stopped) : ## walking
        frame = sabreman.img[0]
        if frame < 100 : frame += 24
        else : frame = 0
        sabreman.img[0] = frame

def draw () :
        screen.blit(backdrop,(0,0))
        # sabreman
        blitsprite(spritesheet,sabreman,sabreman.flip)
        
while True:
    update()
    draw()
    pygame.display.flip()
    pygame.time.wait(10)
