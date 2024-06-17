
import pygame
import random
import sys
from os import listdir
from os.path import isfile, join
#import utilities

pygame.init()
pygame.display.set_caption("calm birds")


#BASIC SETTINGS
WIDTH,HEIGHT=1280,720
FPS=60
PLAYER_VEL=5
color=(255,0,0)
bigfont = pygame.font.Font(None, 80)
smallfont = pygame.font.Font(None, 45)

background=pygame.image.load(join("assets","bckgrnd","bg1.png"))

window=pygame.display.set_mode((WIDTH,HEIGHT))

def flip_sprites(sprites):
    return[pygame.transform.flip(sprite,True,False) for sprite in sprites]
def load_spritesheets(width,height,dir1,dir2,direction):
    print(1)
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
        self.hit=0
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
        if self.rect.y>=HEIGHT:
            self.game=0

        if self.hit_chill!=0 and self.damageWait==0:
            sound=pygame.mixer.Sound(join("assets","music","Minecraft_Damage_-_Sound_Effect.mp3"))
            sound.play()
            self.hit+=self.hit_chill
            self.damageWait=100
        if self.damageWait!=0:
            self.damageWait-=1
        if self.boost!=0 and self.wait==0:
            if self.boost<=self.hit:
                self.hit=self.hit-self.boost
                self.boost=0
                self.wait=50
        else:
            self.boost=0
        if self.wait!=0:
            self.wait-=1
            text = bigfont.render(str(self.wait*10), 13, (255, 0, 0))
            dist = self.heart.get_rect()
            textx_size = text.get_width()
            pygame.draw.rect(window, (255, 255, 255), ((dist.x+dist.width, 0),(textx_size, 50)))

            window.blit(text, (WIDTH / 2 - text.get_width() / 2,
                       HEIGHT / 2 - text.get_height() / 2))
        self.hearts()


    def update(self):
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
    def __init__(self,x,y,width,height,distance,dir1):
        
        super(ChillEnemy,self).__init__()
        self.rect=pygame.Rect(x,y,width,height)
        path = join("assets","Enemy", "chilling.png")
        self.image = pygame.image.load(path).convert_alpha()
        self.surface = pygame.Surface((width, height),pygame.SRCALPHA, 32)
        self.rand=random.randint(1,3)
        self.animation_count=0
        self.x_vel=self.rand
        self.y_vel=float()
        self.mask=None
        self.direction="left"
        self.weight=70
        self.boost=0
        self.hit=0
        self.game=1
        self.wait=0
        self.cooldown=0
        self.distance=(distance-1)*block_size+(block_size-self.rect.width)
        self.travel=0.1
        self.dir=dir1

    def sprite_animation(self):
        sprite_sheet = self.dir

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
        if self.hit==1 and self.wait==0 and self.cooldown==0:
            self.x_vel=0
            self.hit=0
            self.wait=150
            self.cooldown=1
        elif self.hit==0 and self.wait!=0 or self.hit==1 and self.wait!=0:
            self.hit=0
            self.wait-=1
            self.x_vel=0
        elif self.hit==0 and self.wait==0 and self.cooldown==1 or self.hit==1 and self.wait==0 and self.cooldown==1:
            self.x_vel=self.rand
            self.cooldown=0

        self.sprite_animation()



    def update(self):
        self.mask = pygame.mask.from_surface(self.sprite)



    def draw(self,window,offset_x):
        window.blit(self.sprite,(self.rect.x -offset_x,self.rect.y))

class FallingEnemy(pygame.sprite.Sprite):
    COLOR=(255,0,0)
    SPRITES = load_spritesheets( 65, 65,"Enemy", "fallingEnemy", True)
    ANIMATION_DELAY=7
    def __init__(self,x,y,width,height):
        
        super(FallingEnemy,self).__init__()
        self.rect=pygame.Rect(x,y,width,height)
        path = join("assets","Enemy","fallingEnemy","bird3walking.png")
        self.image = pygame.image.load(path).convert_alpha()
        self.surface = pygame.Surface((width, height),pygame.SRCALPHA, 32)

        self.animation_count=0
        self.x_vel=random.randint(-2,2)
        self.y_vel=random.randint(2,6)
        self.mask=None
        self.direction="left"
        self.weight=70
        self.hit=2
        self.counter=0

    def sprite_animation(self):
        sprite_sheet = "bird3walking"
        if self.x_vel != 0:
            sprite_sheet = "bird3walking"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        if self.counter==1:
            pygame.sprite.Sprite.kill(self)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def move(self,dx,dy):
        self.rect.x+=dx
        self.rect.y+=dy
        return

    def char_loop(self):
        self.move(self.x_vel, self.y_vel)
        if self.x_vel>0:
            if self.direction!="right":
                self.direction="right"      
        if self.x_vel<0:
            if self.direction!="left":
                self.direction="left"
        self.sprite_animation()



    def update(self):
        #self.rect=self.sprite.get_rect(topleft=(self.rect.x,self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)



    def draw(self,window,offset_x):
        window.blit(self.sprite,(self.rect.x-offset_x,self.rect.y))
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
        self.b=0

    def sprite_animation(self):
        sprite_sheet = "Carrot"
        if self.digging != 0:
            sprite_sheet = "carrot_digging"      

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        if sprite_sheet=="carrot_digging" and sprite_index==0 and self.b==0 or sprite_sheet=="carrot_digging" and sprite_index==1 and self.b==0:
            sound1=pygame.mixer.Sound(join("assets","carrot","eating.mp3"))
            sound1.play()
            self.b=1
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

#player taking damage from enemies
def chilling_enemy_movement(chillEnemy_group,player,objects,fallingEnemy_group):
    for falling in fallingEnemy_group:
        if pygame.sprite.collide_mask(falling,player):
            player.hit_chill=1
            player.char_loop(FPS)
        else:
            player.hit_chill=0
    for chill in chillEnemy_group:
        if pygame.sprite.collide_mask(chill,player):
            if player.rect.bottom>=chill.rect.bottom-20:
                player.hit_chill=1
                break
            else:
                player.y_vel*=-1
                chill.hit=1
                player.hit_chill=0
            
            player.update()
        else:
            player.hit_chill=0
    for object in objects:
        for falling in fallingEnemy_group:

            if pygame.sprite.collide_mask(object,falling):
                falling.counter=1
    





#drawing
def draw(window,player,objects,offset_x,carrots,chillEnemy,progress,fallingEnemy_group):

    window.blit(background,(0,0))

    for obj in objects:
        obj.draw(window,offset_x)
    
    for carrot in carrots:
        carrot.draw(window,offset_x)
    
    player.draw(window,offset_x)
    for chill in chillEnemy:
        chill.draw(window,offset_x)
    for falling in fallingEnemy_group:
        falling.draw(window,offset_x)


    maxwidth=350
    pygame.draw.rect(window, (0,0,0), pygame.Rect(WIDTH/2-maxwidth/2-3,0,maxwidth+6,41))  
    pygame.draw.rect(window, (255,0,0), pygame.Rect(WIDTH/2-maxwidth/2,3,maxwidth,35))        
    pygame.draw.rect(window, (127,255,0), pygame.Rect(WIDTH/2-maxwidth/2,3,maxwidth*progress,35)) 
    text = smallfont.render(("PROGRESS "), 13, (0, 0, 0))
    window.blit(text, (WIDTH / 2 - text.get_width() / 2,39))        
    pygame.display.update()



FallingEnemy_group=pygame.sprite.Group() 
ChillEnemy_group=pygame.sprite.Group()    
block_size=96
class Level1():
    def __init__(self):
        self.block_size=96
        self.x_distribution=self.block_size*5
        pygame.mixer.music.load(join("assets","music","bad_piggies_drip.mp3"))
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.4)
        self.delay=int(0)


    def enemies(self,player,difficulty):

        if difficulty==1:
            chance=1
        if difficulty==2:
            chance=4
        if difficulty==3:
            chance=7
        k=random.randint(int(player.rect.x),int(player.rect.x+WIDTH))    
        fallingEnemy=FallingEnemy(k,0,65,65)
        guess=random.randint(1,100)
        if guess<=chance:  
            FallingEnemy_group.add(fallingEnemy)  
        return

    def objects(self,difficulty):
        floor = [Block(i * self.block_size, HEIGHT - self.block_size, self.block_size,"block_1.png")
             for i in range(0, (WIDTH * 5) // self.block_size)]
        


        steps=[Block(self.block_size*25+i*self.block_size, HEIGHT - self.block_size * 2, self.block_size,"block_1.png")
               for i in range(0,5)]
        for k in range(45,47,1):
            steps.append(Block(k * self.block_size, HEIGHT - self.block_size * 4, self.block_size,"wall_1.png"))
            steps.append(Block(k * self.block_size, HEIGHT - self.block_size * 3, self.block_size,"wall_1.png")) 
        for k in range(4,8,1):
            steps.append(Block(49 * self.block_size, HEIGHT - self.block_size * k, self.block_size,"wall_1.png"))
               
        for i in range(0,3):
            steps.append(Block(self.block_size*35+i*self.block_size, HEIGHT - self.block_size * 2, self.block_size,"block_1.png"))




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
        for k in range(37,42,1):
            platforms.append(Block(k * self.block_size, HEIGHT - self.block_size * 3, self.block_size,"block_1.png"))
            for obj in floor:
                if obj.rect.x==k*self.block_size:
                    floor.remove(obj)
                  
        for k in range(40,44,1):
            platforms.append(Block(k * self.block_size, HEIGHT - self.block_size * 5, self.block_size,"block_1.png"))
            for obj in floor:
                if obj.rect.x==k*self.block_size:
                    floor.remove(obj)
           
        for k in range(45,47,1):
            platforms.append(Block(k * self.block_size, HEIGHT - self.block_size * 5, self.block_size,"block_1.png"))
            for obj in floor:
                if obj.rect.x==45*self.block_size:
                    floor.remove(obj)       
        platforms.append(Block(49 * self.block_size, HEIGHT - self.block_size * 8, self.block_size,"block_1.png"))
        for i in range(49,51,1):
            for obj in floor:
                if obj.rect.x==i*self.block_size:
                    floor.remove(obj)          
        for k in range(51,53,1):
            platforms.append(Block(k * self.block_size, HEIGHT - self.block_size * 2, self.block_size,"block_1.png"))
            platforms.append(Block(k * self.block_size, HEIGHT - self.block_size * 6, self.block_size,"block_1.png"))           
            for obj in floor:
                if obj.rect.x==k*self.block_size:
                    floor.remove(obj)                  
        platforms.append(Block(50 * self.block_size, HEIGHT - self.block_size * 4, self.block_size,"block_1.png"))
        for k in range(53,58):
            platforms.append(Block(k * self.block_size, HEIGHT - self.block_size * 5, self.block_size,"block_1.png"))           
            for obj in floor:
                if obj.rect.x==k*self.block_size:
                    floor.remove(obj)              

        walls=[]
        for k in range(0,HEIGHT//self.block_size+1):
            for i in range(-6,0,1):
                walls.append(Block(i * self.block_size, k*self.block_size, self.block_size,"wall_1.png"))
        for k in range(0,HEIGHT//self.block_size+1):
            for i in range((WIDTH*5)//self.block_size,((WIDTH*5)//self.block_size)+6,1):
                walls.append(Block(i * self.block_size, k*self.block_size, self.block_size,"wall_1.png"))
        objects = [*floor,*walls,*steps,*platforms,Block(200, HEIGHT - self.block_size * 2, self.block_size,"block_1.png"),Block(500, HEIGHT - self.block_size * 4, self.block_size,"block_1.png")]

        #carrot distribution system
        if difficulty==1:
            chance=5
        if difficulty==2:
            chance=3
        if difficulty==3:
            chance=1      
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
                guess=random.randint(1,50)
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
        
        #stationary enemies
        dir=["bird1walking","bird2walking"]
        ChillEnemy_group.add(ChillEnemy(12*block_size,HEIGHT-block_size*3-65,65,65,5,dir[random.randint(0,1)]))
        ChillEnemy_group.add(ChillEnemy(18*block_size,HEIGHT-block_size*5-65,65,65,2,dir[random.randint(0,1)]))
        ChillEnemy_group.add(ChillEnemy(40*block_size,HEIGHT-block_size*5-65,65,65,4,dir[random.randint(0,1)]))
        ChillEnemy_group.add(ChillEnemy(45*block_size,HEIGHT-block_size*5-65,65,65,2,dir[random.randint(0,1)]))
        ChillEnemy_group.add(ChillEnemy(51*block_size,HEIGHT-block_size*2-65,65,65,2,dir[random.randint(0,1)]))
        ChillEnemy_group.add(ChillEnemy(53*block_size,HEIGHT-block_size*5-65,65,65,5,dir[random.randint(0,1)]))
        ChillEnemy_group.add(ChillEnemy(27*block_size,HEIGHT-block_size*3-65,65,65,3,dir[random.randint(0,1)]))
        ChillEnemy_group.add(ChillEnemy(20*block_size,HEIGHT-block_size*1-65,65,65,5,dir[random.randint(0,1)]))
        ChillEnemy_group.add(ChillEnemy(3*block_size,HEIGHT-block_size*1-65,65,65,8,dir[random.randint(0,1)]))
        return objects
    
    def length(self):
        length=WIDTH*5
        return length


class Back():
    def __init__(self):
        self.backing=0



back=Back()
#CONTROL OF TIME
def main(window,difficulty):
    clock=pygame.time.Clock()
    player = Player(50,150,65,65)
    offset_x=0
    scroll_area_width=500
    progress=0
    level1= Level1()
    objects=level1.objects(difficulty)
    run=True
    while run==True:
        clock.tick(FPS)
        #print(pygame.time.Clock.get_fps(clock))
        pygame.display.get_active=True

                 
    
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player.jump < 2:
                    player.move_up(PLAYER_VEL)

        if player.game==0:
            objects.clear()
            for chill in ChillEnemy_group:
                chill.kill()
            player.kill()
            carrot_group.empty()
            run=False

        progr=(player.rect.x/(level1.length()-65*2))
        if progress<=progr:
            progress=progr
        else:
            pass

        player.char_loop(FPS)
        level1.enemies(player,difficulty)

        grav(player)
        player_move(player,objects,player.y_vel)
        for falling in FallingEnemy_group:
            falling.char_loop()
        for chill in ChillEnemy_group:
            chill.char_loop()
        chilling_enemy_movement(ChillEnemy_group,player,objects,FallingEnemy_group)
        draw(window,player,objects,offset_x,carrot_group,ChillEnemy_group,progress,FallingEnemy_group)
        carrot_interaction(player,carrot_group)
        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            
            offset_x += player.x_vel
    window.blit(background,(0,0))
    pygame.mixer.music.fadeout(1000)
    run=play_again(difficulty)

SCREEN = pygame.display.set_mode((1280, 720))

class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/mainmenu/font.ttf", size)

def play_again(difficulty):

    run=True
    while run:
        PLAY_AGAIN_POS = pygame.mouse.get_pos()

        #Options button is DIFFICULTY in this case!!!!!!!!!!!
        PLAY_AGAIN_BUTTON = Button(image=pygame.image.load("assets/mainmenu/Play Rect.png"), pos=(640, 350), 
                            text_input="Play Again", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        MAINMENU_BUTTON = Button(image=pygame.image.load("assets/mainmenu/Options Rect.png"), pos=(640, 500), 
                            text_input="Main Menu", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        #When mouse is over button (Najechanie na przycisk)
        for button in [PLAY_AGAIN_BUTTON, MAINMENU_BUTTON]:
            button.changeColor(PLAY_AGAIN_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #clicked buttons
                if PLAY_AGAIN_BUTTON.checkForInput(PLAY_AGAIN_POS):
                    main(window,difficulty)
                    break
                if MAINMENU_BUTTON.checkForInput(PLAY_AGAIN_POS):
                    Back.backing=1
                    run=False
                    break

        pygame.display.update()





#calling the main function to start as soon, as the run of the code starts
while __name__=="__main__":
    main(window)

