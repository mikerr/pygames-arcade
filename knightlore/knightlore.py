# knightlore - isometric game
import pygame
import random
#import RPi.GPIO as GPIO         

buttons = { "A":5, "B":6, "UP":17, "DOWN":22, "LEFT":27, "RIGHT":23, "CENTER":4 }
# zx spectrum colors
BLACK = (0,0,0)
BLUE = (0,0,255)
RED = (255,0,0)
MAGENTA = (255,0,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)
CYAN = (0,255,255)
WHITE = (255,255,255)
colors = [BLACK,BLUE,RED,MAGENTA,GREEN,CYAN,YELLOW,WHITE]

class spriteobj:
    color = WHITE
    name = ""
    flip = 0
    x = y = height = 0
    img = [0,0]
    w = h = 32
#class player:
    jumping = 0
    xdir = ydir = 1
    speed = 0
    facing  = 0
    time = grabbed = 0
    def __init__(self,newimg):
        self.img = newimg
        
def iso2screen (x,y):
    # convert to isometric 
    isox = 120 + int ( 11 * (x - y))
    isoy = 20 + int ( 7 * (x + y ))
    return (isox,isoy)

def getsprite(spritesheet,x,y,w,h):
    sprite = pygame.Surface([w,h],flags = pygame.SRCALPHA)
    sprite.blit(spritesheet,(0,0),(x,y,w,h))
    return sprite

def blitsprite (spritesheet,sprite):
    sprite.color = roomcolor
    r,g,b = sprite.color

    isox, isoy = iso2screen(sprite.x,sprite.y)
    isoy -= sprite.height
    image = getsprite(spritesheet,sprite.img[0],sprite.img[1],sprite.w,sprite.h)
    image.fill((r,g,b,255), special_flags=pygame.BLEND_RGBA_MIN)
    screen.blit(pygame.transform.flip(image,sprite.flip,False),(isox,isoy),(0,0,sprite.w,sprite.h))
        
def depth(spr):
    isox,isoy = iso2screen(spr.x,spr.y)
    return isoy
   
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

def newroom():
    global sprites,roomcolor,roompic
    sprites = []
    for i in range(5):
        newblock = spriteobj(block.img)
        newblock.x = 2 * random.randrange(0,5)
        newblock.y = 2 * random.randrange(0,5)
        sprites.append(newblock)
        
    mine.x = random.randrange(3,8)
    mine.y = random.randrange(3,8)
    sprites.append(mine)
    
    chest.x = random.randrange(3,8)
    chest.y = random.randrange(3,8)
    sprites.append(chest)
    
    table.x = random.randrange(3,8)
    table.y = random.randrange(3,8)
    sprites.append(table)
    
    sprites.append(sabreman)
    
    roomcolor = colors[random.randrange(2,7)]
    r,g,b = roomcolor
    roompic = backdrop.copy()
    roompic.fill((r,g,b,255), special_flags=pygame.BLEND_RGBA_MIN)
    
def update () :
    global hours,moon
    run = 0.1
    if (pressed("B") and sabreman.jumping == 0 ):
        sabreman.jumping = 30
        sabreman.speed = run
    # change to a wolf
    wolf = 64
    if (moon) : man = wolf
    else : man = 0
    
    if (pressed("DOWN")):
        sabreman.xdir = 0; sabreman.ydir = 1
        sabreman.flip  = 1; sabreman.facing = 32
        sabreman.speed = run
    if (pressed("RIGHT")):
        sabreman.xdir = 1; sabreman.ydir = 0
        sabreman.flip  = 0; sabreman.facing = 32
        sabreman.speed = run
    if (pressed("UP")):
        sabreman.xdir = 0; sabreman.ydir = -1
        sabreman.flip  = 1; sabreman.facing = 0
        sabreman.speed = run
    if (pressed("LEFT")):
        sabreman.xdir = -1; sabreman.ydir = 0
        sabreman.flip  = 0; sabreman.facing = 0
        sabreman.speed = run
        
    man += sabreman.facing
    sabreman.img[1] = man
 
    # keep on 8x8 grid
    if (sabreman.x < 0) : sabreman.x = 0 ; sabreman.speed = 0
    if (sabreman.x > 10) : sabreman.x = 10 ; sabreman.speed = 0
    if (sabreman.y < 0) : sabreman.y = 0 ; sabreman.speed = 0
    if (sabreman.y > 10) : sabreman.y = 10 ; sabreman.speed = 0

    sabreman.x += sabreman.xdir * sabreman.speed
    sabreman.y += sabreman.ydir * sabreman.speed

    if (sabreman.jumping > 0 and sabreman.speed  > 0) :
        sabreman.jumping -= 1
        if (sabreman.jumping > 15):  sabreman.height = 30 - sabreman.jumping  
        if (sabreman.jumping < 15): sabreman.height = sabreman.jumping
        
    if (sabreman.speed > 0) : ## walking
        sabreman.img[0] += 24
        if sabreman.img[0] > 100 : sabreman.img[0] = 0
    #doors
    xy = [round(sabreman.x),round(sabreman.y)]    
    if xy == [5,10] and sabreman.ydir > 0 :
        sabreman.y = 0; newroom()
    if xy == [5,0] and sabreman.ydir < 0 :
        sabreman.y = 10; newroom()
    if xy == [10,4] and sabreman.xdir > 0 :
        sabreman.x = 0; newroom()
    if xy == [0,4] and sabreman.xdir < 0 :
        sabreman.x = 10; newroom()
    
    for obj in sprites:
        if obj.name == "sabreman": continue # don't collide with yourself!
        objxy = [round(obj.x),round(obj.y)] 
        if xy == objxy and not sabreman.jumping:
            sabreman.x -= sabreman.xdir * sabreman.speed
            sabreman.y -= sabreman.ydir * sabreman.speed

    if not sabreman.jumping : sabreman.speed *= 0.97
    if sabreman.speed < 0.1 :sabreman.speed = 0
    hours += 0.01
    if hours > 12 : 
        hours = 0
        moon = 1 - moon
        
def draw () :
    screen.blit(roompic,(0,0))
    #screen.fill((50,50,50))
    if (moon) : color = WHITE
    else : color = YELLOW
    pygame.draw.circle(screen,color,(180 + int(hours * 2) ,170), 5)
      
    sprites.sort(key = depth)
    for sprite in sprites:
        if (sprite.name == "sabreman"): blitsprite(mansprites,sabreman)
        else : blitsprite(objectsprites,sprite)
        
    blitsprite(objectsprites,door1)
    blitsprite(objectsprites,door2)
# initialize
# setup gpio
#GPIO.setmode(GPIO.BCM)         
#for btn in buttons:
    #GPIO.setup(buttons[btn], GPIO.IN)

window = pygame.display.set_mode((480,480))
screen = pygame.Surface((240, 240))
pygame.mouse.set_visible(False) 

mansprites = pygame.image.load("sabreman.png")
roompic = backdrop = pygame.image.load("backdrop.png")
objectsprites = pygame.image.load("objects.png")
charsprites = pygame.image.load("charsprites.png")

sabreman = spriteobj([0,32])
sabreman.w = 23
sabreman.x = sabreman.y  = 7
sabreman.facing = 32
sabreman.name = "sabreman"

table = spriteobj([80,299])
block = spriteobj([80,9])
spike = spriteobj([80,215])
mine = spriteobj([127,9])
themoon = spriteobj([240,0])
chest = spriteobj([80,258])
door = spriteobj([19,5])

door1 = spriteobj(door.img)
door1.w = 40; door1.h = 50
door1.x = 4; door1.y = 10
door2 = spriteobj(door.img)
door2.w = 40; door2.h = 50
door2.x = 9; door2.y = 3
door2.flip = 1
    
hours = moon = 0

newroom()    
    
while True:
    update()
    draw()
    
    pygame.transform.scale2x(screen, window)
    pygame.display.flip()
    pygame.time.wait(10)
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
