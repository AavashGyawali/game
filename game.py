
import pygame
from sys import exit
from random import randint


def display_score():
    current_time=int(pygame.time.get_ticks()/120)-start_time
    return current_time
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x-=5

            if obstacle_rect.bottom==300:
                screen.blit(snail_surf,obstacle_rect) 

            else:
                screen.blit(fly_surf,obstacle_rect) 


        obstacle_list=[obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list  
    else: return []
def collison(player,obsticles):
    if obsticles:
        for obsticle_rect in obsticles:
            if player.colliderect(obsticle_rect):
                return False
    return True
def player_animation():
    global player_surf,player_index

    if player_rec.bottom<300:
        #jump
        player_surf=player_jump
    else:
        #walk
        player_index+=0.1
        if player_index>=len(player_walk):player_index=0
        player_surf=player_walk[int(player_index)]


#variable declaration
width=800
height= 400
game_active=False
start_time=0
score =0


pygame.init()
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("Alien Run")
clock = pygame.time.Clock()

#creating font
test_font=pygame.font.Font("font\Pixeltype.ttf",50)


#creating surface
sky_surface=pygame.image.load("graphics/Sky.png").convert()
ground_surface=pygame.image.load("graphics/ground.png").convert()

#Title
title_surface=test_font.render("Alien Run",False,(64,64,64))
title_rect=title_surface.get_rect(center=(400,25))

#Result
result_surface=test_font.render(f"Your Score is ",False,(64,64,64))
result_rec=result_surface.get_rect(center=(400,25))

#snail surface
snail_frame_1=pygame.image.load("graphics\snail\snail1.png").convert_alpha()
snail_frame_2=pygame.image.load("graphics\snail\snail2.png").convert_alpha()
snail_frame=[snail_frame_1,snail_frame_2]
snail_frame_index=0
snail_surf=snail_frame[snail_frame_index]

#fly
fly_frame_1=pygame.image.load("graphics\Fly\Fly1.png")
fly_frame_2=pygame.image.load("graphics\Fly\Fly2.png")
fly_frame=[fly_frame_1,fly_frame_2]
fly_frame_index=0
fly_surf=fly_frame[fly_frame_index]

obstacle_rect_list=[]



#player
player_walk_1=pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_walk_2=pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
player_walk=[player_walk_1,player_walk_2]
player_index=0 #to choose among player_walk_1 and 2
player_jump=pygame.image.load("graphics/player/jump.png").convert_alpha()

player_surf=player_walk[player_index]
player_rec=player_surf.get_rect(bottomleft=(80,300))
player_gravity=0


#intro screen
player_stand_surface=pygame.image.load("graphics\Player\player_stand.png").convert_alpha()
player_stand_surface=pygame.transform.rotozoom(player_stand_surface,0,2)
player_stand_rect=player_stand_surface.get_rect(center=(400,200))

#intro Text
intro1_surface=test_font.render("Alien Run",False,(64,64,64))
intro1_rect=intro1_surface.get_rect(center=(400,25))

intro2_surface=test_font.render("Press  Space  to  start",False,(64,64,64))
intro2_rect=intro2_surface.get_rect(center=(400,320))



#Game Over
game_over_surface=test_font.render("Game Over",False,(64,64,64))
game_over_rec=game_over_surface.get_rect(center=(400,150))

to_restart_surface=test_font.render("Press  Space  to  Restart",False,(64,64,64))
to_restart_rec=to_restart_surface.get_rect(center=(400,200))

#Timer
obstacle_timer=pygame.USEREVENT +1  # +1 to avoide confilct with reserved event for pygame 
pygame.time.set_timer(obstacle_timer,1500)#1400 is in ms

snail_animation_timer=pygame.USEREVENT+2
pygame.time.set_timer(snail_animation_timer,500)#500 is in ms

fly_animation_timer=pygame.USEREVENT+3
pygame.time.set_timer(fly_animation_timer,200)#200 is in ms

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            exit()


        if game_active:
#if space key is pressed player will jump
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_SPACE and player_rec.bottom >=300:
                        player_gravity=-20
                        # player_gravity+=1
                
        

        #if mouse key is pressed on the player rectangle than player will jump
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed():
                    if player_rec.collidepoint(event.pos):#instead of event.pos you can write pygame.mouse.get_pos()
                        player_gravity=-20

        else:
            if event.type == pygame.KEYDOWN and event.key==pygame.K_SPACE:
                game_active=True
                
                start_time=int(pygame.time.get_ticks()/120)
        
        if game_active:
            if event.type==obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surf.get_rect(bottomright =(randint(900,1100),300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright =(randint(900,1100),200)))

            if event.type== snail_animation_timer:
                if snail_frame_index==0:snail_frame_index=1
                else:snail_frame_index=0
                snail_surf=snail_frame[snail_frame_index]

            if event.type==fly_animation_timer:
                if fly_frame_index==0:fly_frame_index=1
                else:fly_frame_index=0
                fly_surf=fly_frame[fly_frame_index]

        
 # Before Collison(Gameplay)
    if game_active:
        #showing surface to the screen using coordinate        
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        screen.blit(title_surface,title_rect)
        score=display_score()

        


        #Score Text
        #Score
        score_surface=test_font.render(f'Score: {score}',False,(64,64,64))
        score_rec=score_surface.get_rect(topleft=(10,10))
        screen.blit(score_surface,score_rec)



        #for snail   
        # screen.blit(snail_surface,snail_rec)
        # snail_rec.left-=7 
        # if snail_rec.right<0:snail_rec.left=800

        #Player
        player_gravity+=1
        player_rec.y+=player_gravity
        if player_rec.bottom>=300:player_rec.bottom=300
        player_animation()
        screen.blit(player_surf,player_rec)
        
        if player_rec.left>800:player_rec.right=0

    
        # if player_rec.colliderect(snail_rec):
        #     game_active=False

#obstacle movement
        obstacle_rect_list=obstacle_movement(obstacle_rect_list)
#collison
        game_active=collison(player_rec,obstacle_rect_list)

#After Collision
    else:
            if score ==0:
                screen.fill('white')
                screen.blit(player_stand_surface,player_stand_rect)
                screen.blit(intro1_surface,intro1_rect)
                screen.blit(intro2_surface,intro2_rect)


            else:
                screen.blit(game_over_surface,game_over_rec)
                screen.blit(to_restart_surface,to_restart_rec)
                obstacle_rect_list.clear()
                player_rec.midbottom=(80,300)
                player_gravity=0

            


        
        
        

    pygame.display.update()
    clock.tick(60) # sets max frame to 60fps
    