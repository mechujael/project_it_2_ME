import physics_engine as phys
import pygame
import random as rand
import os
import math
from os import listdir
from os.path import isfile, join


pygame.display.set_caption("Platformer")


#BASIC SETTINGS
BG_COLOR=(255,255,255)
WIDTH=1280
HEIGHT=720
FPS=60
PLAYER_VEL=5

window=pygame.display.set_mode(WIDTH,HEIGHT)


#SCREEN SETTINGS
class SCREEN_ON():
    def __init__(self):
        if pygame.display.get_active == "True":
            pygame.init()
            pygame.display.init
        else:
            pygame.display.quit


#CONTROL OF TIME
class TIME_RUN():

    i=0
    while i<1:
        if pygame.display.get_init =="True":
            pass
        else:
            pygame.time.wait
    

#FPS INFO
i=0
while i<1:
    print(pygame.time.Clock.get_fps)







