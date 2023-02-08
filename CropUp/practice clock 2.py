# -*- coding: utf-8 -*-
"""
Created on Sun May  8 22:32:28 2022

@author: Owner
"""

import datetime as dt
import turtle
import time

def drawClock(trt, x, y, number_color,isFirstClock= False): #interact with specific turtle, center point
    """ Draws circle/numbers
    """
    trt.penup()
    trt.setpos(x + 0, y + 200) #recreating 0 
    trt.left(180)
    trt.pendown()
    #trt.circle(100)