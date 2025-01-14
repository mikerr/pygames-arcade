# jetpac
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

class spriteobj:
    x = y = 0
    xdir = ydir = 0.5
    time = grabbed = 0
    img = [0,0]
    w = h = 16
    def __init__(self, img):
        self.img = img

def collide (obj,sprite,xdistance):
    ydistance = 10
    if (abs(sprite.x - obj.x) < xdistance  and abs(sprite.y - obj.y) < ydistance) : return True
    else : return False

def hitplatform (platforms,sprite):
    for p in platforms:
            px,py,width = p
            if ( (sprite.x > px and (sprite.x-px) < width) and (abs(py - sprite.y - 4) < 4)) : return True
    return False

def getsprite(spritesheet,x,y,w,h):
    sprite = pygame.Surface([w,h])
    sprite.blit(spritesheet,(0,0),(x,y,w,h))
    return sprite

def blitsprite (spritesheet,sprite,mirror = 0):
     offset = 0
     if sprite.h > 8 : offset = 8  - sprite.h
     image = getsprite(spritesheet,sprite.img[0],sprite.img[1],sprite.w,sprite.h)
     screen.blit(pygame.transform.flip(image,mirror,False),(int(sprite.x),int(sprite.y) + offset),(0,0,sprite.w,sprite.h))
         
# initialize
# setup gpio
GPIO.setmode(GPIO.BCM)         
for btn in buttons:
    GPIO.setup(buttons[btn], GPIO.IN)
def pressed(btn) :
    return ( GPIO.input(buttons[btn]) != True) 

screen = pygame.display.set_mode()
pygame.mouse.set_visible(False) 
spritebuffer = pygame.image.load("jetpac.png")

screensize = WIDTH
ground = HEIGHT - 10

jetman = spriteobj([36,26])
jetman.h = 24

rocket = spriteobj([40,64])
rocket.h = 64
rocket.x = 140

splat = spriteobj([70,0])

fuel = spriteobj([106,100])
fuel.x = 50
fuel.w = 22

gem = spriteobj([106,0])
gem.w = 20

fuelled = takeoff = firing = 0

platforms = [(11,93,55), (80,122,43), (190,64,50), (0,233,240)]

aliens = [spriteobj([0,50]) for i in range(4)]
for alien in aliens :
    alien.x = random.randrange(screensize)
    alien.y = random.randrange(screensize)
    
def update () :
    global firing,takeoff,fuelled
    
    if (pressed("A")) : firing  = 1
    else : firing = 0
        
    if (pressed("LEFT")):  jetman.xdir -= 1
    if (pressed("RIGHT")): jetman.xdir += 1
    if (pressed("B") or pressed("UP")): jetman.ydir -= 1   
    
     # not too fast
    if (abs(jetman.xdir) > 5): jetman.xdir *= 0.5
    if (abs(jetman.ydir) > 5): jetman.ydir *= 0.9
    jetman.xdir *= 0.8
    # keep on screen / wrap left/right
    jetman.y = min(ground,jetman.y)
    jetman.y = max(30,jetman.y)
    if (jetman.x < 0 or jetman.x > screensize) : jetman.x = screensize - jetman.x
     
    jetman.x += jetman.xdir 
    jetman.y += jetman.ydir
        
    # gravity
    jetman.ydir += 0.4
    
    if (hitplatform(platforms,jetman)):
                if (jetman.ydir > 0) :
                    jetman.y -= 1
                    jetman.ydir = 0
                else :
                    jetman.ydir = - jetman.ydir #bounce underneath
                jetman.img = [16* (int(jetman.x) % 4),0] #walking
    if (abs(jetman.ydir) > 1) : jetman.img = [36,26]  # flying
        
    if collide(gem,jetman,10):
            gem.img[1] = 20 * random.randrange(4) # gems at 0,10,20,30,40
            gem.x = random.randrange(screensize)
            gem.y = -100
            gem.ydir = 2
    gem.y += gem.ydir        
    fuel.y += fuel.ydir
    if (fuel.ydir > 0) : fuel.ydir += 0.02
    if (hitplatform(platforms,gem)) : gem.ydir = 0
    if (hitplatform(platforms,fuel)) : fuel.ydir = 0    

    # fuel grabbing and dropping
    dropzone = 140
    if (not fuel.grabbed and collide(fuel,jetman,10)) : fuel.grabbed = 1
    if (fuel.grabbed) :
                fuel.x = jetman.x
                fuel.y = jetman.y + 8
                fuel.ydir = 1
                if (abs(fuel.x - dropzone) < 5) :
                    fuel.grabbed = 0
                    fuel.x = dropzone
    if (fuel.x == dropzone and fuel.y > ground - 10) :
            fuelled += 1
            fuel.x = random.randrange(screensize)
            fuel.y = -50
            fuel.ydir = 1
    # rocket
    rocket.y = ground - takeoff + 6
    if (fuelled >= 3) :
                takeoff += 1
                if (takeoff > 100) :
                    takeoff = fuelled = 0
                    rocket.img[0] += 16
                    if (rocket.img[0] > 90): rocket.img[0] = 40
    #aliens
    for alien in aliens :
            alien.x += alien.xdir
            alien.y += alien.ydir
            dead = 0
            if (alien.x > screensize or alien.x < -25) : dead = 1
            if (hitplatform(platforms,alien)) : dead = 1
            if (firing and collide(alien,jetman,100)) : dead = 1
            # player collides with alien
            if (collide(alien,jetman,10)) :
                jetman.xdir = alien.xdir * 2
                jetman.ydir = -1
                dead = 1
            if (dead) :
                    splat.x = alien.x
                    splat.y = alien.y
                    splat.time = 5
                    
                    alien.xdir = 1 + random.randrange(2)
                    alien.y = random.randrange(screensize)
                    if (random.randrange(5) > 1) :
                        alien.x = -10
                    else :
                        alien.x = WIDTH
                        alien.xdir = alien.xdir * -1
                    
def draw () :
        global fuelled,takeoff

        screen.fill((0,0,0))
        blitsprite(spritebuffer,gem)    
        #laser
        if firing:
            for laser in range(5,100):
                if (jetman.xdir > 0) : laser *= -1;
                if (random.random() > 0.3) : screen.fill((255,255,255),( (int(jetman.x) - laser,int(jetman.y)),(1,1)))

        for alien in aliens :
            if (alien.xdir < 0) : mirror = 1
            else : mirror = 0
            blitsprite(spritebuffer,alien,mirror)
        #explosions stay on screen for 5 frames    
        if (splat.time  > 0) :
            splat.time -= 1
            blitsprite(spritebuffer,splat) 
        # rocket
        blitsprite(spritebuffer,rocket)
        #if (fuelled < 3) :    
            #for f in range(fuelled) :
            #    blit(spritebuffer,54,50,12,8,70,ground - (f * 8))
        blitsprite(spritebuffer,fuel)     
        # jetman
        if (jetman.xdir > 0) : mirror = 1
        else : mirror = 0
        blitsprite(spritebuffer,jetman,mirror)
        # platforms    
        for p in platforms:
            px,py,width = p
            pygame.draw.line(screen,(0,128,0),(px, py), (px + width,py),5)
while True:
    update()
    draw()
    pygame.display.update()
    pygame.time.wait(20)
