
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
PLAYER_VEL=10
color=(255,0,0)

window=pygame.display.set_mode((WIDTH,HEIGHT))

class Player(pygame.sprite.Sprite):
    COLOR=(255,0,0)
    def __init__(self,x,y,width,height):
        self.rect=pygame.Rect(x,y,width,height)
        super().__init__()

        self.x_vel=0
        self.y_vel=float()
        self.mask=None
        self.direction="left"
        self.weight=50

    
    def move(self,dx,dy):
        self.rect.x+=dx
        self.rect.y+=dy
        return
    
    def move_left(self,vel):
        self.x_vel=-vel
        if self.direction!="left":
            self.direction="left"
    
    def move_right(self,vel):
        self.x_vel=vel
        if self.direction!="right":
            self.direction="right"
    
    def move_up(self,vel):
        self.y_vel+=-vel
    def move_down(self,vel):
        self.y_vel+=vel

    def char_loop(self,fps):
        self.move(self.x_vel, self.y_vel)

    def draw(self,window):
        pygame.draw.rect(window,self.COLOR,self.rect)


        

#SCREEN INITIALIZATION
class SCREEN_ON():
    def __init__(self):
        if pygame.display.get_active == True:

            pygame.display.init

#gravity
def grav(player):
    if player.rect.y<HEIGHT-50:
        player.y_vel+=player.weight/10

    else:
  
        player.y_vel=0
        player.rect.y=HEIGHT-50

#movement
def player_move(player):
    key=pygame.key.get_pressed()
    player.x_vel=0

    
    if key[pygame.K_LEFT]:
        player.move_left(PLAYER_VEL)
    if key[pygame.K_RIGHT]:
        player.move_right(PLAYER_VEL)
    if key[pygame.K_UP]:
        player.move_up(PLAYER_VEL)


class Block(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.image = pygame.Surface([20, 15])
        self.image.fill(color)
        self.rect = self.image.get_rect()


#collision


#drawing
def draw(window,player):

    background=pygame.image.load(join("assets","bckgrnd","background_1_example.jpeg"))
    window.blit(background,(0,0))

    player.draw(window)
    pygame.display.update()

#CONTROL OF TIME
def main(window):
    clock=pygame.time.Clock()
    x=50
    y=50
    player = Player(100,100,50,50)
    square=Block(color)
    player_group=pygame.sprite.Group()
    player_group.add(player)
    squares=pygame.sprite.Group()
    squares.add(square)
    player_group.update()
    squares.update()
    if pygame.sprite.groupcollide(player_group,squares,0,0)==True:
        square.fill((18, 0, 255))
    
        


    run=True
    while run==True:
        clock.tick(FPS)
        pygame.display.get_active=True


    
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                break
        player.char_loop(FPS)

        grav(player)
        player_move(player)
        squares.draw(window)
        draw(window,player)
        pygame.display.update()
    pygame.quit()
    quit()




#calling the main function to start as soon, as the run of the code starts
if __name__=="__main__":
    main(window)

