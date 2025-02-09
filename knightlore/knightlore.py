# knightlore - isometric game
import pygame
import random
#import RPi.GPIO as GPIO         

buttons = { "A":5, "B":6, "UP":17, "DOWN":22, "LEFT":27, "RIGHT":23, "CENTER":4 }
# zx spectrum colors
BLACK = (0,0,0); BLUE = (0,0,255); RED = (255,0,0); MAGENTA = (255,0,255); GREEN = (0,255,0); YELLOW = (255,255,0); CYAN = (0,255,255); WHITE = (255,255,255)
colors = [BLACK,BLUE,RED,MAGENTA,GREEN,CYAN,YELLOW,WHITE]

rooms = [
    #"r444b400b410b420b430b401b411b421b431b402b412b422b432",
   # "r444b130b140b210b310b221b321b251b260b351b360b430b440s431s441",
   # "r444b330b350b530b550b331b341b351b431b441b451b531b541b551b442",
   # "r444b330b331s332b630b631s632",
   # "r444b330b331b332b333b430b530b540b550",
   # "r444b210b250s211s251s410s450",
    "r400b000b010b020b031b040b050b060b070"]

class spriteobj:
    color = WHITE
    name = ""
    flip = 0
    x = y = height = 0
    img = [0,0]
    w = h = 32
    moveable = 0
#class player:
    jumping = 0
    xdir = ydir = 0
    speed = 0
    facing  = 0
    def __init__(self,newimg):
        self.img = newimg[:] # make a copy, not a reference
        
def iso2screen (x,y):
    # convert to isometric 
    isox = 115 + int ( 12 * (x - y))
    isoy = 30 + int ( 6 * (x + y ))
    return (isox,isoy)

def getsprite(spritesheet,x,y,w,h):
    # grab a portion of spritesheet as a new sprite
    sprite = pygame.Surface([w,h],flags = pygame.SRCALPHA)
    sprite.blit(spritesheet,(0,0),(x,y,w,h))
    return sprite

def blitsprite2d (spritesheet,sprite,xy):
    #blit a sprite, recolored 
    r,g,b = sprite.color
    
    image = getsprite(spritesheet,sprite.img[0],sprite.img[1],sprite.w,sprite.h)
    image.fill((r,g,b,255), special_flags=pygame.BLEND_RGBA_MIN)
    screen.blit(image,xy,(0,0,sprite.w,sprite.h))
    
def blitsprite (spritesheet,sprite):
    #blit a sprite, recolored and projected o isometric
    r,g,b = sprite.color
    #2d
    #isox = 50 + sprite.x * 10
    #isoy = 50 + sprite.y * 10
    isox, isoy = iso2screen(sprite.x,sprite.y)
    isoy -= sprite.height * 12
    image = getsprite(spritesheet,sprite.img[0],sprite.img[1],sprite.w,sprite.h)
    image.fill((r,g,b,255), special_flags=pygame.BLEND_RGBA_MIN)
    screen.blit(pygame.transform.flip(image,sprite.flip,False),(isox,isoy),(0,0,sprite.w,sprite.h))
    #pygame.draw.rect(screen,WHITE,(isox,isoy,10,10))
    
def depth(spr):
    # get depth of sprite for sorting
    isox,isoy = iso2screen(spr.x,spr.y)
    return isoy

def collide(a,b):
    return (b.x - 0.5 <= a.x <= b.x + 0.5) and (b.y - 0.5 <= a.y <= b.y + 0.5)
def pressed(btn) :
    #check button presses
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
    # generate new room
    global sprites,roomcolor,roompic
    
    roomcolor = colors[random.randrange(2,7)]
    
    sprites = []
    roomdesc = rooms[random.randrange(len(rooms))]
    for i in range(4,len(roomdesc),4):
        newblock = spriteobj(block.img)
        newblock.y = int(roomdesc[i+1]) + 2
        newblock.x = int(roomdesc[i+2]) + 1
        newblock.height = int(roomdesc[i+3])
        newblock.color = roomcolor
        sprites.append(newblock)
        
    chest.x = random.randrange(3,8)
    chest.y = random.randrange(3,8)
    chest.color = YELLOW
    chest.moveable = 1
    sprites.append(chest)
    
    table.x = random.randrange(3,8)
    table.y = random.randrange(3,8)
    table.color = YELLOW
    table.moveable = 1
    sprites.append(table)
    
    sprites.append(guard)
    
    sprites.append(sabreman)
    
    door1.color  = door2.color = roomcolor
    r,g,b = roomcolor
    roompic = backdrop.copy()
    roompic.fill((r,g,b,255), special_flags=pygame.BLEND_RGBA_MIN)

frames = 0
def update () :
    # all game code, but no rendering
    global hours,moon,frames
    run = 0.1
    guardspeed = run  / 5
    
    if (pressed("B") and sabreman.jumping == 0 ):
        sabreman.jumping = 30
        sabreman.speed = run
    # change to a wolf
    wolf = 65
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
    if (sabreman.x < 0 ) : sabreman.x = 0 
    if (sabreman.x > 10) : sabreman.x = 10 
    if (sabreman.y < 0 ) : sabreman.y = 0 
    if (sabreman.y > 10) : sabreman.y = 10

    sabreman.x += sabreman.xdir * sabreman.speed
    sabreman.y += sabreman.ydir * sabreman.speed

    if (sabreman.jumping > 0 and sabreman.speed  > 0) :
        sabreman.jumping -= 1
        if (sabreman.jumping > 15): sabreman.height += 0.1 
        if (sabreman.jumping < 15): sabreman.height -= 0.1
    if sabreman.height  < 0 : sabreman.height  = 0
    
    if (sabreman.speed > 0 and frames % 3  == 0) : ## walking
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
    
    #collisions
    for obj in sprites:
        if obj.name == "sabreman": continue # don't collide with yourself !
        
        colliding  =  collide(sabreman,obj)
        if colliding and obj.moveable:
                # moveable objects
                if obj.x > 0 and obj.x < 10 : obj.x += sabreman.xdir * run
                if obj.y > 0 and obj.y < 10 : obj.y += sabreman.ydir * run
                continue
            
        #stop if hit an object at same height
        if colliding and sabreman.height == obj.height * 1.5:
                sabreman.x -= sabreman.xdir * sabreman.speed
                sabreman.y -= sabreman.ydir * sabreman.speed    
        #land on top of object
        if sabreman.jumping > 25 and colliding and (sabreman.height) > obj.height:
                sabreman.height = obj.height + 1.5
                sabreman.jumping = 0
                sabreman.speed = 0
                break
    colliding = 0
    for obj in sprites:
        if obj.name == "sabreman": continue # don't collide with yourself !
        
        colliding  =  collide(sabreman,obj)
        if colliding : break
        
        #fall off end if not coliided with anything
    if sabreman.height >= 1.5 and not colliding:
            sabreman.jumping = 15
    
    if not sabreman.jumping : sabreman.speed *= 0.97
    if sabreman.speed < 0.07 :sabreman.speed = 0
    
    #guard
    guard.x += guard.xdir
    guard.y += guard.ydir
    if guard.x <= 0 :
        guard.xdir = 0
        guard.ydir = guardspeed
    if guard.x > 10:
        guard.x = 10
        guard.xdir = 0
        guard.ydir = -guardspeed
    if guard.y > 10:
        guard.y = 10
        guard.ydir = 0
        guard.xdir = guardspeed
    if guard.y < 0:
        guard.y = 0
        guard.ydir = 0
        guard.xdir = -guardspeed
        
    #day / night
    hours += 0.005
    if hours > 12 : 
        hours = 0
        moon = 1 - moon
    frames += 1
    
def draw () :
    # all screen rendering here
    screen.blit(roompic,(0,0))
    #screen.fill((0,0,0))
    
    if (moon) : sky = themoon
    else : sky = thesun
    blitsprite2d(objectsprites,sky,(180 + int(hours * 3),175))
    blitsprite2d(objectsprites,picframe,(175,172))
                
    # blit sprites in depth order
    sprites.sort(key = depth)
    for sprite in sprites:
        if (sprite.name == "sabreman" or sprite.name == "guard"):
            blitsprite(mansprites,sprite)
        else : blitsprite(objectsprites,sprite)
    
    #doors always in front    
    blitsprite(objectsprites,door1)
    blitsprite(objectsprites,door2)
    
    #collected gems
    for i in range(0,3):
        gem = gems[i]
        blitsprite2d(objectsprites,gem,(20 + i * 20 ,180))
    #lives
    life = gems[7]
    blitsprite2d(objectsprites,life,(20,145))
    
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

sabreman = spriteobj([0,32])
sabreman.w = 24
sabreman.x = sabreman.y  = 3
sabreman.name = "sabreman"

guard = spriteobj([0,132])
guard.w = 24
guard.name = "guard"

block = spriteobj([80,2])
spike = spriteobj([80,215])
mine = spriteobj([130,9])
table = spriteobj([80,299])
chest = spriteobj([80,258])
door = spriteobj([19,5])
diamond = spriteobj([167,54])
themoon = spriteobj([341,10])
thesun = spriteobj([322,10])
thesun.color = YELLOW
thesun.w = 16
picframe = spriteobj([160,85])
picframe.w = 56

gems = []
for i in range(0,8):
    gem = spriteobj(diamond.img)
    gem.w = gem.h = 24
    gem.img[0] += i * 24
    gems.append(gem)

door1 = spriteobj(door.img)
door1.w = 40; door1.h = 50
door1.x = 4; door1.y = 9
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