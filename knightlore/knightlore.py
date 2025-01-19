# knightlore - isometric game

import pygame
import random
#import RPi.GPIO as GPIO         

buttons = { "A":5, "B":6, "UP":17, "DOWN":22, "LEFT":27, "RIGHT":23, "CENTER":4 }
WIDTH = HEIGHT = 240
# zx spectrum colors
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
    height = 0
    jumping = 0
    xdir = ydir = 1
    speed = 0
    facing  = 0
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
    isoy -= sprite.height
    image = getsprite(spritesheet,sprite.img[0],sprite.img[1],sprite.w,sprite.h)
    image.fill((r,g,b,255), special_flags=pygame.BLEND_RGBA_MIN)
    screen.blit(pygame.transform.flip(image,mirror,False),(isox,isoy),(0,0,sprite.w,sprite.h))
    
def pressed(btn) :
    #return ( GPIO.input(buttons[btn]) != True)
    key = ""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: key = "LEFT"
    if keys[pygame.K_RIGHT]: key = "RIGHT"
    if keys[pygame.K_UP]: key = "UP"
    if keys[pygame.K_DOWN]: key = "DOWN"
    if keys[pygame.K_SPACE]: key = "B"
    return (key == btn)
        
# initialize
# setup gpio
#GPIO.setmode(GPIO.BCM)         
#for btn in buttons:
    #GPIO.setup(buttons[btn], GPIO.IN)

screen = pygame.display.set_mode((240,240))
pygame.mouse.set_visible(False) 

sprites = pygame.image.load("sabreman.bmp")
backdrop = pygame.image.load("backdrop.png")
objects = pygame.image.load("sprites.gif")

sabreman = spriteobj()
sabreman.img = [0,32]
sabreman.w = 23

themoon = spriteobj()
themoon.img = [240,0]

blocks = []
for i in range(5):
    block = spriteobj()
    block.img = [290,36]
    block.x = 2 * random.randrange(0,4)
    block.y = 2 * random.randrange(0,4) 
    blocks.append(block)
    
hours = 0
moon = 0
def update () :
    global hours,moon
    if (pressed("B") and sabreman.jumping == 0 ):
        sabreman.jumping = 30
    # change to a wolf
    wolf = 64
    if (moon) : man = wolf
    else : man = 0
    
    run = 0.1
    if (pressed("DOWN")):
        sabreman.xdir = 0
        sabreman.ydir = 1
        sabreman.flip  = 1
        sabreman.facing = 32
        sabreman.speed = run
    if (pressed("RIGHT")):
        sabreman.xdir = 1
        sabreman.ydir = 0
        sabreman.flip  = 0
        sabreman.facing = 32
        sabreman.speed = run
    if (pressed("UP")):
        sabreman.xdir = 0
        sabreman.ydir = -1
        sabreman.flip  = 1
        sabreman.facing = 0
        sabreman.speed = run
    if (pressed("LEFT")):
        sabreman.xdir = -1
        sabreman.ydir = 0
        sabreman.flip  = 0
        sabreman.facing = 0
        sabreman.speed = run
        
    man += sabreman.facing
    sabreman.img[1] = man
 
    # keep on 8x8 grid
    if (sabreman.x < 0) : sabreman.x = 0 ; sabreman.speed = 0
    if (sabreman.x > 9) : sabreman.x = 9 ; sabreman.speed = 0
    if (sabreman.y < 0) : sabreman.y = 0 ; sabreman.speed = 0
    if (sabreman.y > 9) : sabreman.y = 9 ; sabreman.speed = 0


    sabreman.x += sabreman.xdir * sabreman.speed
    sabreman.y += sabreman.ydir * sabreman.speed

    if (sabreman.jumping > 0 and sabreman.speed  > 0) :
        sabreman.jumping -= 1
        if (sabreman.jumping > 15):  sabreman.height = 30 - sabreman.jumping  
        if (sabreman.jumping < 15): sabreman.height = sabreman.jumping
        
    if (sabreman.speed > 0) : ## walking
        frame = sabreman.img[0]
        if frame < 100 : frame += 24
        else : frame = 0
        sabreman.img[0] = frame
    #doors
    doors = [[5,8],[5,0],[8,4],[0,4]]
    
    if round(sabreman.x) == 5 and round(sabreman.y) == 9:
        if sabreman.ydir > 0 : sabreman.y = 0     
    if round(sabreman.x) == 5 and round(sabreman.y) == 0: 
        if sabreman.ydir < 0 : sabreman.y = 9
    if round(sabreman.x) == 9 and round(sabreman.y) == 4:
        if sabreman.xdir > 0 : sabreman.x = 0
    if round(sabreman.x) == 0 and round(sabreman.y) == 4:
        if sabreman.xdir < 0 : sabreman.x = 9
    
    sabreman.speed = 0
    hours += 0.01
    if hours > 12 : 
        hours = 0
        moon = 1 - moon

def draw () :
    global hours,moon
    screen.blit(backdrop,(0,0))
    
    if (moon) : color = WHITE
    else : color = YELLOW
    pygame.draw.circle(screen,color,(180 + int(hours * 2) ,170), 5)
    
    for block in blocks:
        blitsprite(objects,block)
    
    blitsprite(sprites,sabreman,sabreman.flip)
        
while True:
    update()
    draw()
    pygame.display.flip()
    pygame.time.wait(10)
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
