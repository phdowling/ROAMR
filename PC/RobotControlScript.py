""" Simplified control script for the robot, allows only for rudimentary control"""
import serial
import pygame
import time
import sys
pygame.init()
forward=False
left=False
right=False
back=False
q=False
speed=220
screen = pygame.display.set_mode((100,100))

#ser=serial.Serial("/dev/ttyUSB0")
ser=serial.Serial("COM12")

while True:
    pygame.event.pump()
    key=pygame.key.get_pressed()

    forward=key[pygame.K_UP]
    left=key[pygame.K_LEFT]
    right=key[pygame.K_RIGHT]
    back=key[pygame.K_DOWN]
    q=key[pygame.K_q]
    
    if forward and not ((left or right) or back):
        LDirection="+"
        RDirection="+"
        LSpeed=chr(254)
        RSpeed=chr(254)
    elif back and not ((left or right) or forward):
        LDirection="-"
        RDirection="-"
        LSpeed=chr(254)
        RSpeed=chr(254)
    elif left and not ((forward or right) or back):
        LDirection="-"
        RDirection="+"
        LSpeed=chr(254)
        RSpeed=chr(254)
    elif right and not ((forward or left) or back):
        LDirection="+"
        RDirection="-"
        LSpeed=chr(254)
        RSpeed=chr(254)
    elif (forward and left) and not (right or back):
        LDirection="+"
        RDirection="+"
        LSpeed=chr(200)
        RSpeed=chr(254)
    elif (forward and right) and not (left or back):
        LDirection="+"
        RDirection="+"
        LSpeed=chr(254)
        RSpeed=chr(200)
    elif (back and right) and not (left or forward):
        LDirection="-"
        RDirection="-"
        LSpeed=chr(254)
        RSpeed=chr(200)
    elif (back and left) and not (right or forward):
        LDirection="-"
        RDirection="-"
        LSpeed=chr(200)
        RSpeed=chr(254)
    else:
        LDirection="-"
        RDirection="-"
        LSpeed=chr(0)
        RSpeed=chr(0)
    #checksum=ord(LDirection)+ord(LSpeed)+ord(RDirection)+ord(RSpeed)
    string="s"+LDirection+LSpeed+RDirection+RSpeed+"0"+"e"
    ser.write(string)
    print string
    if q:
        pygame.quit()
        sys.exit()
        ser.close()
    time.sleep(0.05)

    
