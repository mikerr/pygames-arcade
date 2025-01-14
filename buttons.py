
from time import sleep           
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

# setup gpio
GPIO.setmode(GPIO.BCM)         
for btn in buttons:
    GPIO.setup(buttons[btn], GPIO.IN)

def pressed(btn) :
    return ( GPIO.input(buttons[btn]) != True) 

while True: 
           if pressed("A"): print('A')
           if pressed("B"): print('B')
           if pressed("LEFT"): print('LEFT')
           if pressed("RIGHT"): print('RIGHT')
           if pressed("UP"): print('UP')
           if pressed("DOWN"): print('DOWN')
           if pressed("CENTER"): print('CENTER')
           sleep(0.1);           
