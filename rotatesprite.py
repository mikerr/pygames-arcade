import os, math, time
import pygame


buttons = {
           "A":5,
           "B":6,
           "UP":17,
           "DOWN":22,
           "LEFT":27,
           "RIGHT":23,
           "CENTER":4
}


def pressed(btn) :
    return 0

def rotatesprite (image,rot,q=2):
    width = image.get_width()
    height = image.get_height()
    xpos = int (width / 1.4)
    ypos = int (height / 1.4)
    rotatedsprite = pygame.Surface([int(width * 1.4) ,int (height * 1.4)])
    sinangle = math.sin(rot)
    cosangle = math.cos(rot)
    w2 = width / 2
    h2 = height / 2
    for x in range(0,width,q):
        for y in range(0,height,q):
            x1 = x - w2
            y1 = y - h2
            rotx = x1 * sinangle + y1 * cosangle
            roty = y1 * sinangle - x1 * cosangle
            
            rotatedsprite.blit(image,(int(rotx)+xpos,int(roty)+ypos),(x,y,q,q))
    return rotatedsprite

def update() :
        global x,y,angle
        
        if (pressed("LEFT")) : x -= 1
        if (pressed("RIGHT")) : x += 1
        
        if (pressed("UP")) : y -= 1
        if (pressed("DOWN")) : y += 1
        
        if (pressed("A")) : y += 1
        if (pressed("B")) : y += 1
        angle += 0.05

angle = 0
def draw() :
    
        global angle,x,y,rot
        screen.fill((0,0,0))
    
        # create a new rotated sprite then blit it to screen
        sprite = rotatesprite(image,angle,2) 
        screen.blit(sprite,(50 + x,50 +y))
     
        pygame.display.flip()

screen = pygame.display.set_mode()
pygame.mouse.set_visible(False)
x = y = rot = 50
texWidth = 64

image = pygame.image.load("crate.bmp")

while True:
   update()
   draw()
   time.sleep(0.1)
