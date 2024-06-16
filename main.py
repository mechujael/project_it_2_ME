
import pygame
import os
import math
import random
from os import listdir
from os.path import isfile, join

pygame.init()
pygame.display.set_caption("calm birds")


#BASIC SETTINGS
WIDTH,HEIGHT=1280,720
FPS=60
PLAYER_VEL=5
color=(255,0,0)

window=pygame.display.set_mode((WIDTH,HEIGHT))

def flip_sprites(sprites):
    return[pygame.transform.flip(sprite,True,False) for sprite in sprites]
def load_spritesheets(width,height,dir1,dir2,direction):
    path=join("assets",dir1,dir2)
    images=[f for f in listdir(path) if isfile(join(path,f))]
    all_sprites={}
    for image in images:
        sprite_sheet=pygame.image.load(join(path,image)).convert_alpha()

        sprites=[]
        for i in range(sprite_sheet.get_width()//width):
            surface=pygame.Surface((width,height),pygame.SRCALPHA,32)
            rect=pygame.Rect(i*width,0,width,height)
            surface.blit(sprite_sheet,(0,0),rect)
            sprites.append(surface)
        
        if direction:
            all_sprites[image.replace(".png", "") +"_right"]=sprites
            all_sprites[image.replace(".png", "") +"_left"]=flip_sprites(sprites)
        else:
            all_sprites[image.replace(".png", "")]=sprites
    return all_sprites


class Player(pygame.sprite.Sprite):
    COLOR=(255,0,0)
    SPRITES = load_spritesheets( 65, 65,"player", "hog", True)
    ANIMATION_DELAY=7
    def __init__(self,x,y,width,height):
        
        super(Player,self).__init__()
        self.rect=pygame.Rect(x,y,width,height)
        path = join("assets","player", "hog","hog1.png")
        self.image = pygame.image.load(path).convert_alpha()
        self.surface = pygame.Surface((width, height),pygame.SRCALPHA, 32)
        self.animation_count=0
        self.x_vel=0
        self.landed=bool()
        self.y_vel=float()
        self.jump=0
        self.mask=None
        self.direction="left"
        self.weight=50
        self.boost=0
        self.hit=0

    def sprite_animation(self):
        sprite_sheet = "hog_idle5"
        if self.x_vel != 0:
            sprite_sheet = "hog_walking"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

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
        self.weight=50
        if self.jump==0:
            self.weight=25
        elif self.jump==1:
            self.weight=35
        self.jump+=1

    def hearts(self):
        sprite_sheet="hearts"
        if self.hit==0:
            sprite_sheet_name = sprite_sheet + "_" + self.direction
            sprites = self.SPRITES[sprite_sheet_name]
            sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
            self.sprite = sprites[sprite_index]
            self.animation_count += 1
            self.update()           

    def bottom(self):
        self.y_vel=0
    def top(self):
        self.y_vel=0
        self.jump=0

    def char_loop(self,fps):
        self.move(self.x_vel, self.y_vel)
        self.sprite_animation()

    def update(self):
        #self.rect=self.sprite.get_rect(topleft=(self.rect.x,self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)


    def draw(self,window,offset_x):
        window.blit(self.sprite,(self.rect.x -offset_x,self.rect.y))


        

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
def player_move(player,objects,dy,dx):
    key=pygame.key.get_pressed()
    player.update()
    player.x_vel=0
    map_bottom_coll=False
    map_top_coll=False
    map_left_coll=False
    map_right_coll=False
    for obj in objects:

        if pygame.sprite.collide_mask(player,obj):
            if player.rect.y>=obj.rect.y-player.rect.height and player.rect.y<=obj.rect.y-player.rect.height/3:
                player.rect.y=obj.rect.y-player.rect.height
                map_top_coll=True
            if dy<0:
                if player.rect.y<=obj.rect.y+obj.rect.height and player.rect.y>=obj.rect.y+obj.rect.height/3:
                    player.rect.top=obj.rect.bottom
                    map_bottom_coll=True
        
        for i in range(-1,2,2):
            player.move(PLAYER_VEL*i/4,0)
            if pygame.sprite.collide_mask(player, obj):
                if i==-1:
                    map_left_coll=True
                else:
                    map_right_coll=True
            player.move(-PLAYER_VEL*i,0)
            player.update      


    if key[pygame.K_LEFT] and not map_left_coll:
        player.move_left(PLAYER_VEL)

    if key[pygame.K_RIGHT] and not map_right_coll:
        player.move_right(PLAYER_VEL)

 #   if key[pygame.K_UP] and not map_top_coll and not map_bottom_coll:
#      if pygame.KEYDOWN and pressed==0:
#            player.move_up(PLAYER_VEL)
#            pressed=1

    if map_top_coll==True:
        player.top()
    if map_bottom_coll==True:
        player.y_vel*=-1




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
class Carrot(pygame.sprite.Sprite):
    COLOR=(255,0,0)
    SPRITES = load_spritesheets( 65, 65,"carrot", "carrot_animation", True)

    ANIMATION_DELAY=15
    def __init__(self,x,y,width,height):
        
        super(Carrot,self).__init__()
        self.rect=pygame.Rect(x,y,width,height)
        path = join("assets","carrot","Carrot.png")
        self.image = pygame.image.load(path).convert_alpha()
        self.surface = pygame.Surface((width, height),pygame.SRCALPHA, 32)
        self.direction="right"
        self.animation_count=0
        self.digging=0
        self.mask=None
        self.wait=0
        self.boost_player=0

    def sprite_animation(self):
        sprite_sheet = "Carrot"
        if self.digging != 0:
            sprite_sheet = "carrot_digging"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        if sprite_sheet=="carrot_digging" and sprite_index==4:
            pygame.sprite.Sprite.kill(self)
            self.boost_player+=1
        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0           

        self.animation_count += 1
        self.update()

    def update(self):
        #self.rect=self.sprite.get_rect(topleft=(self.rect.x,self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)


    def draw(self,window,offset_x):
        self.sprite_animation()
        window.blit(self.sprite,(self.rect.x -offset_x,self.rect.y))

def carrot_interaction(player,carrot_group):
    key=pygame.key.get_pressed()
    for carrot in carrot_group:
        if pygame.sprite.collide_mask(player,carrot) and key[pygame.K_e]:
            carrot.digging=1
        if carrot.boost_player==1:
            player.boost+=1
            carrot.boost_player=0


background=pygame.image.load(join("assets","bckgrnd","background_1_example.jpeg"))
#drawing
def draw(window,player,objects,offset_x,carrots):

    window.blit(background,(0,0))

    player.draw(window,offset_x)

    for obj in objects:
        obj.draw(window,offset_x)
    
    for carrot in carrots:
        carrot.draw(window,offset_x)
    
    
    pygame.display.update()


block_size=96
carrot_group=pygame.sprite.Group()
for i in range(1,20,1):
    carrot=Carrot(i*random.randint(i*100,i*200),HEIGHT-block_size*1.5,65,65)
    if carrot_group.has()==False:
        carrot_group.add(carrot)        
    for carrot in carrot_group:
        if pygame.sprite.spritecollideany(carrot,carrot_group,None)==None:
            carrot_group.add(carrot)        

   
#CONTROL OF TIME
def main(window):
    clock=pygame.time.Clock()
    player = Player(100,100,65,65)
    offset_x=0
    scroll_area_width=500


    block_size=96
    floor = [Block(i * block_size, HEIGHT - block_size, block_size,"block_1.png")
             for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]
    platforms= [Block(i * block_size, HEIGHT - block_size, block_size,"block_1.png")
             for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]
  

    objects = [*floor,Block(200, HEIGHT - block_size * 2, block_size,"block_1.png"),Block(500, HEIGHT - block_size * 4, block_size,"block_1.png"),]
    run=True
    while run==True:
        clock.tick(FPS)
        print(pygame.time.Clock.get_fps(clock))
        pygame.display.get_active=True


    
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player.jump < 2:
                    player.move_up(PLAYER_VEL)
        player.char_loop(FPS)
        grav(player)
        player_move(player,objects,player.y_vel,player.x_vel)
        draw(window,player,objects,offset_x,carrot_group)
        carrot_interaction(player,carrot_group)
        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel
 
    pygame.quit()
    quit()




#calling the main function to start as soon, as the run of the code starts
if __name__=="__main__":
    main(window)

