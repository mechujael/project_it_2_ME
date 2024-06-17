
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
PLAYER_VEL=15
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
        path_heart=join("assets","player","hearts")
        self.image = pygame.image.load(path).convert_alpha()
        self.surface = pygame.Surface((width, height),pygame.SRCALPHA, 32)

        self.heart1=pygame.image.load(join(path_heart,"1heart.png"))
        self.heart2=pygame.image.load(join(path_heart,"2heart.png"))
        self.heart3=pygame.image.load(join(path_heart,"3heart.png"))
        self.heart4=pygame.image.load(join(path_heart,"4heart.png"))
        self.heart5=pygame.image.load(join(path_heart,"5heart.png"))      
        self.heart=self.heart5


        self.animation_count=0
        self.x_vel=0
        self.landed=bool()
        self.y_vel=float()
        self.jump=0
        self.mask=None
        self.direction="left"
        self.weight=50

        self.boost=0
        self.hit=2
        self.hit_chill=0

        self.game=1
        self.wait=0
        self.damageWait=0

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
        if self.hit==0:
            self.heart=self.heart5
        elif self.hit==1:
            self.heart=self.heart4
        elif self.hit==2:
            self.heart=self.heart3
        elif self.hit==3:
            self.heart=self.heart2
        elif self.hit==4:            
            self.heart=self.heart1            
        else:
            self.game=0
       

    def bottom(self):
        self.y_vel=0
    def top(self):
        self.y_vel=0
        self.jump=0

    def char_loop(self,fps):
        self.move(self.x_vel, self.y_vel)
        self.sprite_animation()

        if self.hit_chill!=0 and self.damageWait==0:
            self.hit+=self.hit_chill
            self.damageWait=100
        if self.damageWait!=0:
            self.damageWait-=1
        if self.boost!=0 and self.wait==0:
            if self.boost<=self.hit:
                self.hit=self.hit-self.boost
                self.boost=0
                self.wait=100
        else:
            self.boost=0
        if self.wait!=0:
            self.wait-=1
        self.hearts()


    def update(self):
        #self.rect=self.sprite.get_rect(topleft=(self.rect.x,self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)



    def draw(self,window,offset_x):
        window.blit(self.sprite,(self.rect.x -offset_x,self.rect.y))
        window.blit(self.heart,(0,0))


        

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


def handle_move(player,objects,dy):
    wait=0

               
#movement
def player_move(player,objects,dy):
    key=pygame.key.get_pressed()
    player.update()
    player.x_vel=0
    map_bottom_coll=False
    map_top_coll=False
    map_left_coll=False
    map_right_coll=False
    if player.rect.x<=0:
        player.rect.x=0
    if player.rect.x<=0:
        player.rect.x=0
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



#enemies
class ChillEnemy(pygame.sprite.Sprite):
    COLOR=(255,0,0)
    SPRITES = load_spritesheets( 65, 65,"Enemy", "chill_enemy", True)
    ANIMATION_DELAY=7
    def __init__(self,x,y,width,height,distance):
        
        super(ChillEnemy,self).__init__()
        self.rect=pygame.Rect(x,y,width,height)
        path = join("assets","Enemy", "chilling.png")
        self.image = pygame.image.load(path).convert_alpha()
        self.surface = pygame.Surface((width, height),pygame.SRCALPHA, 32)

        self.animation_count=0
        self.x_vel=1
        self.y_vel=float()
        self.mask=None
        self.direction="left"
        self.weight=70
        self.boost=0
        self.hit=2
        self.game=1
        self.wait=0
        self.distance=(distance-1)*block_size+(block_size-self.rect.width)
        self.travel=0.1

    def sprite_animation(self):
        sprite_sheet = "idling"
        if self.x_vel != 0:
            sprite_sheet = "walking"

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
        self.travel+=dx
        return

    def bottom(self):
        self.y_vel=0
    def top(self):
        self.y_vel=0
        self.jump=0

    def char_loop(self):
        self.move(self.x_vel, self.y_vel)
        if self.x_vel>0:
            if self.direction!="right":
                self.direction="right"      
        if self.x_vel<0:
            if self.direction!="left":
                self.direction="left"
        if self.travel>=self.distance:
            self.x_vel*=-1
        if self.travel<=0:
            self.x_vel*=-1
        self.sprite_animation()



    def update(self):
        #self.rect=self.sprite.get_rect(topleft=(self.rect.x,self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)



    def draw(self,window,offset_x):
        window.blit(self.sprite,(self.rect.x -offset_x,self.rect.y))


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

carrot_group=pygame.sprite.Group()

def carrot_interaction(player,carrot_group):
    boost_player=0
    key=pygame.key.get_pressed()
    for carrot in carrot_group:
        if pygame.sprite.collide_mask(player,carrot) and key[pygame.K_e] and pygame.KEYDOWN:      
            carrot.digging=1
            boost_player=1

    if boost_player==1 and pygame.KEYUP:

        player.boost=1
        boost_player=0

def chilling_enemy_movement(chillEnemy,player):
    if pygame.sprite.collide_mask(chillEnemy,player):
        player.hit_chill=1
        player.char_loop(FPS)
    else:
        player.hit_chill=0




background=pygame.image.load(join("assets","bckgrnd","background_1_example.jpeg"))
#drawing
def draw(window,player,objects,offset_x,carrots,chillEnemy):

    window.blit(background,(0,0))

    for obj in objects:
        obj.draw(window,offset_x)
    
    for carrot in carrots:
        carrot.draw(window,offset_x)
    
    player.draw(window,offset_x)
    chillEnemy.draw(window,offset_x)
    pygame.display.update()


block_size=96
class Level1():
    def __init__(self):
        self.block_size=96
        self.x_distribution=self.block_size*5

        pygame.mixer.music.load(join("assets","music","AngryBirdsThemeSongDubstepRemix_TerenceJayMusic.mp3"))
        pygame.mixer.music.play()
  
    def objects(self):
        floor = [Block(i * self.block_size, HEIGHT - self.block_size, self.block_size,"block_1.png")
             for i in range(0, (WIDTH * 5) // self.block_size)]
        steps=[Block(self.block_size*25+i*self.block_size, HEIGHT - self.block_size * 2, self.block_size,"block_1.png")
               for i in range(0,5)]
        for i in range(0,3):
            steps.append(Block(self.block_size*35+i*self.block_size, HEIGHT - self.block_size * 2, self.block_size,"block_1.png"))
        walls=[]
        platforms= []
        for k in range(12,17,1):
            platforms.append(Block(k * self.block_size, HEIGHT - self.block_size * 3, self.block_size,"block_1.png"))
            for obj in floor:
                if obj.rect.x==k*self.block_size:
                    floor.remove(obj)
        for k in range(27,30):
           platforms.append(Block(k * self.block_size, HEIGHT - self.block_size * 3, self.block_size,"block_1.png"))  
        for k in range(32,34):
           platforms.append(Block(k * self.block_size, HEIGHT - self.block_size * 5, self.block_size,"block_1.png"))
           for obj in floor:
                if obj.rect.x==k*self.block_size:
                    floor.remove(obj)        
        for k in range(18,20,1):
            platforms.append(Block(k * self.block_size, HEIGHT - self.block_size * 5, self.block_size,"block_1.png"))
            for obj in floor:
                if obj.rect.x==k*self.block_size:
                    floor.remove(obj)
        

        for k in range(0,HEIGHT//self.block_size+1):
            for i in range(-6,0,1):
                walls.append(Block(i * self.block_size, k*self.block_size, self.block_size,"wall_1.png"))
        for k in range(0,HEIGHT//self.block_size+1):
            for i in range((WIDTH*5)//self.block_size,((WIDTH*5)//self.block_size)+6,1):
                walls.append(Block(i * self.block_size, k*self.block_size, self.block_size,"wall_1.png"))
        objects = [*floor,*walls,*steps,*platforms,Block(200, HEIGHT - self.block_size * 2, self.block_size,"block_1.png"),Block(500, HEIGHT - self.block_size * 4, self.block_size,"block_1.png")]

        #carrot distribution system
        chance=2
        for obj in floor:
            if obj.rect.x>=self.x_distribution:
                for step in steps:
                    if obj.rect.x!=step.rect.x:
                        height=obj.rect.y 
                    else:
                        for plat in platforms:
                            if step.rect.x!=plat.rect.x:
                                height=step.rect.y
                            else:
                                height=plat.rect.y
                                break
                        break   
                carrot=Carrot(obj.rect.x+random.randint(0,self.block_size//3),height-32,65,65)
                guess=random.randint(1,10)
                if guess<=chance:  
                    carrot_group.add(carrot)  
        for obj in platforms:
            for step in steps:
                if step.rect.x!=obj.rect.x:
                    chance1=chance
                else:
                    chance1=0
                    break
            carrot=Carrot(obj.rect.x+random.randint(0,self.block_size//3),obj.rect.y-32,65,65)
            guess=random.randint(1,10)
            if guess<=chance1:  
                carrot_group.add(carrot)  
        return objects

     

#CONTROL OF TIME
def main(window):
    clock=pygame.time.Clock()
    player = Player(100,100,65,65)
    offset_x=0
    scroll_area_width=500

    chillEnemy=ChillEnemy(5,HEIGHT-block_size-65,65,65,2)
    level1= Level1()
    objects=level1.objects()
    run=True
    while run==True:
        clock.tick(FPS)
        #print(pygame.time.Clock.get_fps(clock))
        pygame.display.get_active=True

        if player.game==0:
            pygame.sprite.Sprite.kill(player)
            font=pygame.font.Font("Times New Roman",15)
            gameover = pygame.font.Font.render(font,"Press R to Respawn", False, (255, 255, 255))
            rect = gameover.get_rect()
            rect.center = window.get_rect().center
            window.blit(gameover, rect)
        key=pygame.key.get_pressed()
        if player.game==0 and key[pygame.K_r]:
            main(window)
                      
    
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player.jump < 2:
                    player.move_up(PLAYER_VEL)
            
        player.char_loop(FPS)
        chillEnemy.char_loop()
        grav(player)
        player_move(player,objects,player.y_vel)
        chilling_enemy_movement(chillEnemy,player)
        draw(window,player,objects,offset_x,carrot_group,chillEnemy)
        carrot_interaction(player,carrot_group)
        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel
 
    pygame.quit()
    quit()




#calling the main function to start as soon, as the run of the code starts
if __name__=="__main__":
    main(window)

