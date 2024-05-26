
import pygame
import os
import math
from os import listdir
from os.path import isfile, join

pygame.init()
pygame.display.set_caption("calm birds")


#BASIC SETTINGS
WIDTH,HEIGHT=1280,720
FPS=60
PLAYER_VEL=5

window=pygame.display.set_mode((WIDTH,HEIGHT))



#SCREEN INITIALIZATION
class SCREEN_ON():
    def __init__(self):
        if pygame.display.get_active == True:

            pygame.display.init

def foreground(window):
    sad=True

#CONTROL OF TIME
def main(window):
    clock=pygame.time.Clock()

    
    background=pygame.image.load(join("assets","bckgrnd","background_1_example.jpeg"))
    window.blit(background,(0,0))
    pygame.display.flip()


    run=True
    while run==True:
        clock.tick(FPS)
        pygame.display.get_active=True

    
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                break
    pygame.quit()
    quit()


#calling the main function to start as soon, as the run of the code starts
if __name__=="__main__":
    main(window)



