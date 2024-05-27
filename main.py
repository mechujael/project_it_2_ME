
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

class Player(pygame.sprite.Sprite):
    COLOR=(255,0,0)
    def __init__(self,x,y,width,height):
        self.rect=pygame.Rect(x,y,width,height)
        self.x_vel=0
        self.y_vel=0
        self.mask=None
        self.direction="left"
    
    def move(self,dx,dy):
        self.rect.x+=dx
        self.rect.y+=dy
    
    def move_left(self,vel):
        self.x_vel=-vel
        if self.direction!="left":
            self.direction="left"
    
    def move_right(self,vel):
        self.x_vel=vel
        if self.direction!="right":
            self.direction="right"

    def char_loop(self,fps):
        self.move(self.x_vel, self.y_vel)



    def draw(self,window):
        pygame.draw.rect(window,self.COLOR,self.rect)
        

#SCREEN INITIALIZATION
class SCREEN_ON():
    def __init__(self):
        if pygame.display.get_active == True:

            pygame.display.init



#movement
def player_move(player):
    key=pygame.key.get_pressed()
    player.x_vel=0
    if key[pygame.K_LEFT]:
        player.move_left(PLAYER_VEL)
    if key[pygame.K_RIGHT]:
        player.move_right(PLAYER_VEL)


#drawing
def draw(window,player):
    player.draw(window)
    pygame.display.update()

#CONTROL OF TIME
def main(window):
    clock=pygame.time.Clock()

    player = Player(100,100,50,50)
    
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
        player.char_loop(FPS)
        player_move(player)
        draw(window,player)
    pygame.quit()
    quit()




#calling the main function to start as soon, as the run of the code starts
if __name__=="__main__":
    main(window)

