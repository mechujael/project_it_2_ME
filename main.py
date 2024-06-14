
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
        
        super(Player,self).__init__()
        self.rect=pygame.Rect(x,y,width,height)
        path = join("assets", "player","player_test1.png")
        self.image = pygame.image.load(path).convert()
        self.surface = pygame.Surface((width, height),pygame.SRCALPHA, 32)
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
        self.y_vel=-vel*2

    def bottom(self):
        self.y_vel*=-1
    def top(self):
        self.y_vel=0

    def char_loop(self,fps):
        self.move(self.x_vel, self.y_vel)

    def update(self):
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self,window,offset_x):
        window.blit(self.image,(self.rect.x -offset_x,self.rect.y))


        

#SCREEN INITIALIZATION
class SCREEN_ON():
    def __init__(self):
        if pygame.display.get_active == True:

            pygame.display.init

#gravity
def grav(player):
    if player.rect.y<HEIGHT-50:
        player.y_vel+=player.weight/50

    else:
  
        player.y_vel=0
        player.rect.y=HEIGHT-50

#movement
def player_move(player,objects,dy):
    key=pygame.key.get_pressed()
    player.update()
    player.x_vel=0
    map_bottom_coll=False
    map_top_coll=False
    for obj in objects:
        if pygame.sprite.collide_mask(player,obj):
            if dy>0:
                player.rect.bottom=obj.rect.top
                map_top_coll=True
            if dy<0:
             player.rect.top=obj.rect.bottom
             map_bottom_coll=True



    if key[pygame.K_LEFT]:# and not map_left_coll:
        player.move_left(PLAYER_VEL)
    else:
        map_left_coll=False
    if key[pygame.K_RIGHT]:
        player.move_right(PLAYER_VEL) #and not map_right_coll:
    if key[pygame.K_UP] and not map_top_coll:
        player.move_up(PLAYER_VEL)
    if map_top_coll==True:
        player.top()
        
    if map_bottom_coll==True:
        player.bottom()
        map_bottom_coll=False





#objects in the game

def get_block(size,FileBlock):
    path = join("assets", "Terrain",FileBlock)
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size),pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0,0), rect)
    return pygame.transform.scale2x(surface)


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height),pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x -offset_x, self.rect.y))
        


class Block(Object):
    def __init__(self, x, y, size,FileBlock):
        super().__init__(x, y, size,size)
        block = get_block(size,FileBlock)
        self.image.blit(block, (0,0))
        self.mask = pygame.mask.from_surface(self.image)


#objects to bounce
class Bouncer(pygame.sprite.Sprite):
    COLOR=(255,0,0)
    def __init__(self,x,y,width,height):
        
        super(Player,self).__init__()
        self.rect=pygame.Rect(x,y,width,height)
        path = join("assets", "player","player_test1.png")
        self.image = pygame.image.load(path).convert()
        self.surface = pygame.Surface((width, height),pygame.SRCALPHA, 32)
        self.x_vel=0
        self.y_vel=float()
        self.mask = pygame.mask.from_surface(self.image)
        self.weight=50



#collision



background=pygame.image.load(join("assets","bckgrnd","background_1_example.jpeg"))
#drawing
def draw(window,player,objects,offset_x):

    window.blit(background,(0,0))

    player.draw(window,0)

    for obj in objects:
        obj.draw(window,offset_x)
    
    pygame.display.update()




#CONTROL OF TIME
def main(window):
    clock=pygame.time.Clock()
    x=50
    y=50
    player = Player(100,100,65,65)

    block_size=96
    floor = [Block(i * block_size, HEIGHT - block_size, block_size,"block_1.png")
             for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]
  

    offset_x=0
    scroll_area_width=500

    main_objects=[]


    objects = [*floor,Block(0, HEIGHT - block_size * 2, block_size,"block_1.png")]
    run=True
    while run==True:
        clock.tick(FPS)
        print(pygame.time.Clock.get_fps(clock))
        pygame.display.get_active=True


    
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                break
        player.char_loop(FPS)

        grav(player)
        player_move(player,objects,player.y_vel)
        #squares.draw(window)
        draw(window,player,objects,offset_x)
        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel
 
    pygame.quit()
    quit()




#calling the main function to start as soon, as the run of the code starts
if __name__=="__main__":
    main(window)

