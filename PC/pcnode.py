#!/usr/bin/env python

#Advanced control script, uses ROS to communicate with the Android node

import roslib; roslib.load_manifest('androidcontrol')
import rospy
from std_msgs.msg import String
import math
import pygame
import time
import sys
import serial


pygame.init()
forward=False
left=False
right=False
back=False
q=False
speed=220
azimuth = 0
screen = pygame.display.set_mode((100,100))



ser=serial.Serial("/dev/ttyUSB0")
#ser=serial.Serial("COM12")
azimuth=0

def callback(data):
    #rospy.loginfo(rospy.get_name()+"Mag values: %s", data.data)
    global azimuth
    azimuth = float(data.data)

def listener():
    rospy.init_node('pc', anonymous=True)
    rospy.Subscriber("/mobile/acceleration", String, callback)

    
def main():
    global azimuth
    while not rospy.is_shutdown():
        pygame.event.pump()
        key=pygame.key.get_pressed()

        forward=key[pygame.K_UP]
        left=key[pygame.K_LEFT]
        right=key[pygame.K_RIGHT]
        back=key[pygame.K_DOWN]
        q=key[pygame.K_q]
        n=key[pygame.K_n]
        if n:
            rotateto(0)
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
            rospy.signal_shutdown("shutting down")
            ser.close()
            pygame.quit()
            sys.exit()
        time.sleep(0.05)

def rotateto(x):
    global azimuth
    x = float(x)
    x = x - (math.pi/2.0)
    az = azimuth
    az = az - x
    if az > math.pi:
        az = -2*math.pi + az
    if az < 0.0 -math.pi:
        az = 2*math.pi + az
        
    while abs(az)>(0.05) and not rospy.is_shutdown():
        
        az = azimuth - x
        if az > math.pi:
            az = -2*math.pi + az
        if az < 0.0 -math.pi:
            az = 2*math.pi + az
        
        pygame.event.pump()
        key=pygame.key.get_pressed()
        q=key[pygame.K_q]
        #print az
        #print""
        if az<0:
            #rotate right
            ser.write("s+"+chr(254)+"-"+chr(254)+"0"+"e")
            print "right"
        else:
            #rotate left
            ser.write("s-"+chr(254)+"+"+chr(254)+"0"+"e")
            print "left"
        if q:
            rospy.signal_shutdown("shutting down")
            ser.close()
            pygame.quit()
            sys.exit()
        #print ""
        time.sleep(0.01)
    print "azimuth is ", az, ", done."
    print ""
    time.sleep(1)
    
    
if __name__ == '__main__':
    listener()
    main()
    
