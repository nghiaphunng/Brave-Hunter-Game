import pygame

from random import randint

pygame.init()

WIDTH_SC=1200
HEIGHT_SC=567

screen=pygame.display.set_mode((WIDTH_SC, HEIGHT_SC))  

game_icon=pygame.image.load('assets\hunter_icon.png').convert_alpha()
pygame.display.set_icon(game_icon)
pygame.display.set_caption("Hunter and Zombies")

#score
score=0
max_score=score
font=pygame.font.SysFont('Brush Script MT', 40, True)
font_text=pygame.font.SysFont('Brush Script MT', 60, True)

class Player:
    def __init__(self,x,y):
        #running photos
        self.run_images=[]
        for i in range(0,10):
            run_img=pygame.image.load(f'assets\hunter\Run\Run_{i}.png').convert_alpha()
            self.run_images.append(pygame.transform.scale(run_img,(82,100)))
        
        #jumping photos
        self.jump_images=[]
        for i in range(2,8,5):
            jump_img=pygame.image.load(f'assets\hunter\Jump\Jump_{i}.png').convert_alpha()
            self.jump_images.append(pygame.transform.scale(jump_img,(76,100)))
            
        #sliding photos
        self.slide_images=[]
        for i in range(0,13):
            slide_img=pygame.image.load(f'assets\hunter\Slide\Slide_{i}.png').convert_alpha()
            if 0<=i<=2:
                self.slide_images.append(pygame.transform.scale(slide_img,(76,100)))
            else:
                self.slide_images.append(pygame.transform.scale(slide_img,(90,60)))
                
        #dead photos
        self.dead_images=[]
        for i in range(0,10):
            dead_img=pygame.image.load(f'assets\hunter\Dead\Dead_{i}.png').convert_alpha()
            self.dead_images.append(pygame.transform.scale(dead_img,(98,100)))
        
        #control images that are updated continuously
        self.index=0
        self.image=self.run_images[self.index]
        self.mask=pygame.mask.from_surface(self.image)
        
        self.x=x
        self.y=y
        
        #control states
        self.run=True
        
        self.jump=False
        self.jump_pass=False
        self.GRAVITY=1
        self.jump_velocity=-18
        
        self.slide=False

        self.dead=False
        self.pause=False
        self.dead_pass=False

        self.last_update_time=0
        self.update_time=60

    #function specifies state
    def update(self):
        current_time=pygame.time.get_ticks()
        
        if self.run==True and self.jump==False and self.slide==False:
            if current_time - self.last_update_time > self.update_time:
                self.index+=1
                self.last_update_time=current_time
                if self.index>= len(self.run_images):
                    self.index=0
            self.image=self.run_images[self.index]


        elif self.jump==True:
            if self.jump_velocity < 0:
                self.index=0
            
            elif self.jump_velocity >= 0:
                self.index=1
                    
            self.image=self.jump_images[self.index]

        elif self.slide==True and self.jump==False:
            if current_time - self.last_update_time > self.update_time:
                self.index+=1
                self.last_update_time=current_time
                
                if self.index>=3:
                    self.y=445
                    if self.index>=len(self.slide_images):
                            self.index=12
                        
            self.image=self.slide_images[self.index]

        elif self.dead==True and self.jump==False and self.slide==False and self.run==False and self.dead_pass==True:
            if self.pause==False:
                if current_time - self.last_update_time > 90:
                    self.index+=1
                    self.x+=15
                    if self.y<405: #while jumping, it collided
                        self.y+=15
                        if self.y>=405:
                            self.y=405
                    self.last_update_time=current_time
                
                    if self.index>=len(self.dead_images):
                        self.index=9
                        self.pause=True
            
            else: #self.pause==True
                game_over_txt=font.render("Game Over",True,(255,0,0))
                game_over_txt_rect=game_over_txt.get_rect(center=(WIDTH_SC/2,200))
                screen.blit(game_over_txt,game_over_txt_rect)
                
                play_again_txt=font.render("Press Enter To Play Again",True,(0,0,0))
                play_again_txt_rect=play_again_txt.get_rect(center=(WIDTH_SC/2,300))
                screen.blit(play_again_txt,play_again_txt_rect)
                
            self.image=self.dead_images[self.index]

        self.mask=pygame.mask.from_surface(self.image)
    
class MaleZombie:
    def __init__(self,x,y):
        self.images=[]
        for i in range(1,11):
            img=pygame.image.load(f'assets\zombie_move\male\Walk\Walk_{i}.png').convert_alpha()
            img=pygame.transform.flip(img,True,False)
            self.images.append(pygame.transform.scale(img,(100,100)))
        self.index=0
        self.image=self.images[self.index]
        self.mask=pygame.mask.from_surface(self.image)

        self.x=x
        self.y=y
        
        self.velocity=15
        
        self.last_update_time=0
        self.update_time=30
        
        self.passed_enemy=False
    def update(self):
        current_time=pygame.time.get_ticks()
        if current_time - self.last_update_time > self.update_time:
            self.index+=1
            self.x-=self.velocity
            self.last_update_time=current_time
            if self.index >= len(self.images):
                self.index=0
        self.image=self.images[self.index]
        self.mask=pygame.mask.from_surface(self.image)
               
class FemaleZombie:
    def __init__(self,x,y):
        self.images=[]
        for i in range(1,11):
            img=pygame.image.load(f'assets\zombie_move\girl\Walk\Walk_{i}.png').convert_alpha()
            img=pygame.transform.flip(img,True,False)
            self.images.append(pygame.transform.scale(img,(100,100)))
        self.index=0
        self.image=self.images[self.index]
        self.mask=pygame.mask.from_surface(self.image)

        self.x=x
        self.y=y
        
        self.velocity=15
        
        self.last_update_time=0
        self.update_time=30
        
        self.passed_enemy=False
    def update(self):
        current_time=pygame.time.get_ticks()
        if current_time - self.last_update_time > self.update_time:
            self.index+=1
            self.x-=self.velocity 
            self.last_update_time=current_time
            if self.index>= len(self.images):
                self.index=0
        self.image=self.images[self.index]
        self.mask=pygame.mask.from_surface(self.image)

class Dinosaur:
    def __init__ (self,x,y):
        self.images=[]
        for i in range(1,11):
            img=pygame.image.load(f'assets\dino_move\dino_run\Run_{i}.png').convert_alpha()
            img=pygame.transform.flip(img,True,False)
            self.images.append(pygame.transform.scale(img,(100,100)))
            
        self.index=0
        self.cout_index=0
        self.image=self.images[self.index]
        self.mask=pygame.mask.from_surface(self.image)
        
        self.x=x
        self.y=y
        
        self.velocity=20
        self.run=True
        
        #dinosaur jumping effect
        self.jump_dist_to_player=0
        self.check_jump=False
        self.GRAVITY=1
        self.jump_velocity=-17
        
        self.last_update_time=0
        self.update_time=0
        
        self.passed_enemy=False
    def update(self):
        current_time=pygame.time.get_ticks()
        if self.run==True:
            if current_time - self.last_update_time > self.update_time:
                self.cout_index+=0.25
                if self.cout_index>=1:
                    self.index+=1
                    self.cout_index=0
                self.x-=self.velocity
                self.last_update_time=current_time
            if self.index>= len(self.images)-2:
                self.index=0

        else: #self.run==False
            self.y+=self.jump_velocity
            self.jump_velocity+=self.GRAVITY
            self.x-=self.velocity
            if self.jump_velocity<0:
                self.index=8
            else:
                self.index=9
                if self.y>=405:
                    self.y=405
                    self.run=True
                    self.index=0
                    self.jump_velocity=-17
                    
        self.image=self.images[self.index]
        self.mask=pygame.mask.from_surface(self.image)

class BackGround:
    def __init__(self,x_1):
        bg_img=pygame.image.load('assets\\bg.jpg').convert_alpha()
        self.bg_img=pygame.transform.scale(bg_img,(842,567))

        self.speed_x_bg=5
        self.x_1=x_1
        self.x_2=self.x_1+self.bg_img.get_width()
        self.x_3=self.x_2+self.bg_img.get_width()
        
        self.draw_bg_1=True
        
        self.bone_imgs=[]
        for i in range(1,5):
            bone_img=pygame.image.load(f'assets\png\Tiles\Bone_{i}.png').convert_alpha()
            self.bone_imgs.append(pygame.transform.scale(bone_img,(40,40)))
        skeleton_img=pygame.image.load('assets\png\Tiles\Skeleton.png').convert_alpha()
        self.bone_imgs.append(pygame.transform.scale(skeleton_img,(40,20)))
        
        self.bones_x_y=[]
        for i in range(6):
            x=randint(0,1300)
            y=randint(505,567)
            self.bones_x_y.append([x,y])
            for j in range(len(self.bones_x_y)):
                while ((x-self.bones_x_y[j][0])*(x-self.bones_x_y[j][0]) + (y-self.bones_x_y[j][1])*(y-self.bones_x_y[j][1])) < 20*20:
                    x=randint(0,1300)
                    y=randint(505,567)

    def update(self):
        if self.draw_bg_1==True:
            screen.blit(self.bg_img,(self.x_1,0))
            screen.blit(self.bg_img,(self.x_2,0))
            screen.blit(self.bg_img,(self.x_3,0))
            
            self.x_1-=self.speed_x_bg
            self.x_2-=self.speed_x_bg
            self.x_3-=self.speed_x_bg
            
            if self.x_1<=-self.bg_img.get_width():
                self.x_1=self.x_3+self.bg_img.get_width()
            if self.x_2<=-self.bg_img.get_width():
                self.x_2=self.x_1+self.bg_img.get_width()
            if self.x_3<=-self.bg_img.get_width():
                self.x_3=self.x_2+self.bg_img.get_width()
                
            self.speed_x_bg=round((self.speed_x_bg+0.01),2)

            if self.speed_x_bg>=35:
                self.speed_x_bg=35
                self.alpha=255
                self.draw_bg_1=False
    
        else: #self.draw_bg_1==False
            pygame.draw.rect(screen,(100,95,95),(0,505,1200,62))
            pygame.draw.line(screen,(0,0,0),(0,505),(1200,505),5)
            
            #draw skeletons on the ground
            for i in range(len(self.bones_x_y)):
                screen.blit(self.bone_imgs[i%len(self.bone_imgs)],self.bones_x_y[i])
                self.bones_x_y[i][0]-=self.speed_x_bg*7
                if self.bones_x_y[i][0]<=-self.bone_imgs[i%len(self.bone_imgs)].get_width():
                    self.bones_x_y[i][0]=randint(1000,1300)
                    self.bones_x_y[i][1]=randint(505,567)

#initialize player
player=Player(120,405)

#initialize enemies
zombie_1=MaleZombie(1200,405)

zombie_2=FemaleZombie(1900,405)
zombie_3=MaleZombie(1950,405)

zombie_4=FemaleZombie(2600,405)
zombie_5=MaleZombie(2630,405)
zombie_6=MaleZombie(2660,405)

zombie_7=MaleZombie(3300,405)
zombie_8=FemaleZombie(3350,405)

zombie_9=FemaleZombie(0,405)
zombie_10=MaleZombie(0,405)
zombie_11=FemaleZombie(0,405)
zombie_12=MaleZombie(0,405)

zombie_13=FemaleZombie(0,405)
zombie_14=MaleZombie(0,405)
zombie_15=MaleZombie(0,405)
zombie_16=FemaleZombie(0,405)
zombie_17=MaleZombie(0,405)

zombie_18=FemaleZombie(0,405)
dino_1=Dinosaur(0,405)
dino_2=Dinosaur(0,405)
dino_3=Dinosaur(0,405)
zombie_19=FemaleZombie(0,405)
zombie_20=MaleZombie(0,405)

enemies=[[zombie_1],[zombie_2,zombie_3],[zombie_4,zombie_5,zombie_6],[zombie_7,zombie_8]]
enemies_coordinates=[]
for i in range(len(enemies)):
    enemies_coordinates.append([enemies[i][j].x for j in range(len(enemies[i]))])

is_first_add=False
cout_distance_1=1

is_second_add=False
cout_distance_2=1

is_third_add=False

running=True
clock=pygame.time.Clock()

#tombstone
tombstone_img=pygame.image.load('assets\TombStone.png').convert_alpha()
width_tombstone_img,height_tombstone_img=tombstone_img.get_size()
height_tombstone=0

FPS=60

#collision function
def collision(coordinates1, mask1, coordinates2, mask2):
    x = coordinates2[0] - coordinates1[0]
    y = coordinates2[1] - coordinates1[1]
    if mask1.overlap(mask2, (x, y)) != None:
        return True
    return False

background = BackGround(0)

while running:
    clock.tick(FPS)
    
    screen.fill((255,255,255))
    
    #create dynamic background
    background.update()
    
    #draw the player running on the screen
    screen.blit(player.image,(player.x,player.y))
    player.update()
        
    #drawing enemy and speed
    if player.dead==False:
        if player.update_time>10:
            player.update_time=round((player.update_time-0.03),2)
        else:
            player.update_time=10

        for i in range(len(enemies)):
            # print("enemie.update_time=",enemies[i][0].update_time)
            for j in range(len(enemies[i])):
                screen.blit(enemies[i][j].image,(enemies[i][j].x,enemies[i][j].y))
                enemies[i][j].update()
                
                if enemies[i][j].update_time>0:
                    enemies[i][j].update_time=round((enemies[i][j].update_time-0.03),2)
                else:
                    enemies[i][j].update_time=0
                    enemies[i][j].velocity=20

                if isinstance(enemies[i][j],Dinosaur):
                    if 0<enemies[i][j].x<WIDTH_SC-enemies[i][-1].image.get_width() and enemies[i][j].check_jump==False:
                        enemies[i][j].jump_dist_to_player=600
                        enemies[i][j].check_jump=True
                        # print("jump_dist_to_player",enemies[i][j].jump_dist_to_player)
                        
                    elif enemies[i][j].x <= -enemies[i][-1].image.get_width() or enemies[i][j].x>=WIDTH_SC:
                        enemies[i][j].check_jump=False
                        
                    if abs(player.x-enemies[i][j].x)<=enemies[i][j].jump_dist_to_player:
                        enemies[i][j].run=False

                #check collision 
                if collision([player.x, player.y], player.mask, [enemies[i][j].x, enemies[i][j].y], enemies[i][j].mask):
                    player.dead=True
                    player.run=False
                    player.jump=False
                    player.jump_pass=False
                    if player.slide==True:
                        player.slide=False
                        player.y=405
                    player.index=0
                else: #no collision
                    #overcome enemies
                    if player.x>=enemies[i][j].x+enemies[i][j].image.get_width() and enemies[i][j].passed_enemy==False and 0<enemies[i][j].x<WIDTH_SC:
                        score+=1
                        enemies[i][j].passed_enemy=True
                
                if enemies[i][j].x <= - enemies[i][j].image.get_width():
                    enemies[i][j].passed_enemy=False
                    
            #update new coordinates when zombies reach the end of the screen
            if enemies[i][-1].x <= - enemies[i][-1].image.get_width():
                if background.speed_x_bg==35: #khó
                    distance=randint(500,900)
                    cout_distance_2+=1
                    if cout_distance_2%8==0:
                        distance=randint(800,1200)
                        cout_distance_2=1
                    
                else: #easy
                    distance=randint(600,900)
                    cout_distance_1+=1
                    if cout_distance_1%10==0:
                        distance=randint(800,900)
                        cout_distance_1=1
                        
                for k in range(len(enemies[i])):
                    enemies[i][k].x=enemies[i-1][-1].x+distance+50*k
                
                #first addition: add a group of enemies with a quantity of 4 corresponding to level_1
                if 15<=background.speed_x_bg <=25 and is_first_add==False and i==len(enemies)-1:
                    enemies.append([zombie_9,zombie_10,zombie_11,zombie_12])
                    for k in range(len(enemies[-1])):
                        enemies[-1][k].x=enemies[i][-1].x+distance+50*k
                        enemies[-1][k].update_time=enemies[i][-1].update_time

                    is_first_add=True
                
                #second addition: add a group of enemies with a quantity of 5 corresponding to level_2
                elif 25<background.speed_x_bg <30 and is_second_add==False and i==0:
                    enemies.insert(1,[zombie_13,zombie_14,zombie_15,zombie_16,zombie_17])
                    for k in range(len(enemies[1])):
                        enemies[1][k].x=enemies[i][-1].x+distance+50*k
                        enemies[1][k].update_time=enemies[i][-1].update_time

                    is_second_add=True
                
                #third addition: add set 1 zombie-dino-2 zombies
                elif 30<background.speed_x_bg<=35 and is_third_add==False and i==len(enemies)-1:
                    enemies.append([zombie_18])
                    for k in range(len(enemies[-1])):
                        enemies[-1][k].x=enemies[i][-1].x+distance+50*k
                        enemies[-1][k].update_time=enemies[i][-1].update_time
                    
                    enemies.append([dino_1,dino_2,dino_3])
                    for k in range(len(enemies[-1])):
                        enemies[-1][k].x=enemies[-1-1][-1].x+distance+50*k
                        enemies[-1][k].update_time=enemies[i][-1].update_time
                        
                    enemies.append([zombie_19,zombie_20])
                    for k in range(len(enemies[-1])):
                        enemies[-1][k].x=enemies[-1-1][-1].x+distance+50*k
                        enemies[-1][k].update_time=enemies[i][-1].update_time

                    is_third_add=True

    else: #player.dead==True
        background.speed_x_bg=0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
            
        if event.type == pygame.KEYDOWN:
            #jump
            if  (event.key == pygame.K_UP or event.key == pygame.K_SPACE) and player.jump_pass==False and player.slide==False and player.dead==False:
                player.jump=True
                player.jump_pass=True
                
                player.jump_velocity=-18
                player.GRAVITY=1
            
            #slide
            if (event.key == pygame.K_DOWN) and player.dead==False:
                if player.jump==True:
                    if player.jump_velocity<0:
                        player.jump_velocity=0
                        
                player.GRAVITY=2
                player.slide=True

            #play again
            if (event.key == pygame.K_RETURN) and (player.pause==True):
                #player
                player.pause=False
                player.dead=False
                player.dead_pass=False

                player.run=True
                
                player.last_update_time=0
                player.update_time=60
                
                player.index=0
                
                player.x=120
                player.y=405
                
                #background
                background.draw_bg_1=True
                background.speed_x_bg=5
                
                #score
                score=0
                
                #enemies
                del enemies[:]
                enemies=[[zombie_1],[zombie_2,zombie_3],[zombie_4,zombie_5,zombie_6],[zombie_7,zombie_8]]
                for i in range(len(enemies)):
                    for j in range(len(enemies[i])):
                        enemies[i][j].x=enemies_coordinates[i][j]
                        enemies[i][j].update_time=30
                        enemies[i][j].last_update_time=0
                        enemies[i][j].index=0
                        
                is_first_add=False
                cout_distance_1=1

                is_second_add=False
                cout_distance_2=1

                is_third_add=False
                
                
    key=pygame.key.get_pressed()

    #jump processing
    if player.jump==True:
        player.y+=player.jump_velocity
        player.jump_velocity+=player.GRAVITY

        #when jump
        if player.y>=405:
            player.jump=False
            player.jump_pass=False
            player.index=0

            player.y=405

    #when slide
    if player.slide==True:
        if key[pygame.K_DOWN]:
            player.slide=True
        elif not(key[pygame.K_DOWN]) and player.jump==False:
            player.slide=False
            player.index=0
            player.y=405

    #when lose
    if player.dead==True and player.dead_pass==False:
        player.dead_pass=True
        background.speed_x_bg=0

    #draw score
    if max_score<=score:
        max_score=score
        
    score_txt=font.render("Score:"+str(score),True,(255,0,0))
    screen.blit(score_txt,(5,5))
    
    max_score_txt=font.render("Max Score:"+str(max_score),True,(255,0,0))
    screen.blit(max_score_txt,(5,60))
    
    #update screen
    pygame.display.flip()
    
pygame.quit()