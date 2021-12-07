#Liftoff
#Ben Stephenson 2021

import pygame
import random
import os
from pygame.locals import *
from settings import *

#Initialize pygame
pygame.init()
pygame.mixer.init()

#Define Colors
BLACK = (0,0,0)	
WHITE = (255,255,255)		
RED = (255,0,0)		
GREEN = (0,255,0)		
BLUE = (0,0,255)		
YELLOW = (255,255,0)

#Define fonts
font_name = "lucidafax"
font_small = pygame.font.SysFont(font_name, 20)
font_big = pygame.font.SysFont(font_name, 24)

#Create game window and set window title
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(("Liftoff!"))

#Create clock object
clock = pygame.time.Clock()

#Load music and sounds
coin_fx = pygame.mixer.Sound('assets/coin.wav')
coin_fx.set_volume(0.5)

#Game variables
SCROLL_THRESH = 350 #pixels (y = 400)
GRAVITY = 1 #pixel
MAX_COINS = 20
COIN_JUMP_HEIGHT = 70
scroll = 0
bg_scroll = 0
score = 0
game_over = False
fade_counter = 0
coin_count = 0

#Read high score if it exists
if os.path.exists("score.txt"):
    with open("score.txt", 'r') as file:
        high_score = int(file.read())
else:
    high_score = 0
    
#Load images
start_screen_dir = "assets/backgroundSpace_01.1.png"
start_screen_image = pygame.image.load(start_screen_dir)\
    .convert_alpha()
background_image_dir = "assets/backgroundSpace_01.1.png"
background_image = pygame.transform.scale(pygame.image.load(background_image_dir)\
    .convert_alpha(), (SCREEN_WIDTH, SCREEN_HEIGHT))
player_image = pygame.image.load("assets/playerShip2_orange.png")\
    .convert_alpha()
coin_image = pygame.image.load("assets/pieniąszka 1 1.png")\
    .convert_alpha()

#Function for outputting text onto the screen
def draw_text(text, font, text_color, x, y):
    #Render the font
    #Arguments:
    #   The words to render,
    #   a Boolean for antialiasing (True for smooth curves),
    #   and the text color
    img = font.render(text, True, text_color)
    #Draw the words onto the screen at specified coordinates
    SCREEN.blit(img, (x, y))
    
#Function for the start screen
def start_screen():
    pass
    
#Function for drawing info panel
def draw_panel(coin_count):
    pygame.draw.line(SCREEN, WHITE, (0, 60), (SCREEN_WIDTH, 60), 2)
    draw_text("SCORE: " + str(score), font_small, WHITE, 0, 0)
    draw_text("Coins: " + str(coin_count), font_small, WHITE, \
        0, 30)
    
#Function for drawing the background
def draw_background(bg_scroll):
    SCREEN.blit(background_image, (0, 0 + bg_scroll))
    SCREEN.blit(background_image, (0, -SCREEN_HEIGHT + bg_scroll))

#Create Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        #Call the constructor method of the super class
        super().__init__()
        #Scale player sprite to 60 x 60 pixels and store in self.image
        self.image = pygame.transform.scale(player_image, (60, 60))
        #Create a rect from self.image
        self.rect = self.image.get_rect()
        #Position the sprite onto the screen at the specified location
        self.rect.centerx = (SCREEN_WIDTH / 2)
        self.rect.bottom = (SCREEN_HEIGHT - 100)
        #Set vertical velocity to 0
        self.vel_y = 0

    def update(self):
        #Reset variables (delta x, delta y)
        dx = 0
        dy = 0
        horizontal_speed = 10
        scroll = 0
        coin_bool = False
        
        #Process keypresses
        key = pygame.key.get_pressed()
        if key[K_a] or key[K_LEFT]:
            dx += -horizontal_speed
        if key[K_d] or key[K_RIGHT]:
            dx += horizontal_speed
        
        #Gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        #Allow player to wrap around the screen
        if self.rect.right + dx < 10:
            dx = SCREEN_WIDTH + 10
        if self.rect.left + dx > SCREEN_WIDTH - 10:
            dx = -SCREEN_WIDTH - 10
        
        #Check collision with coins
        for coin in coin_group:
            #Collision with player's rect
            if coin.rect.colliderect(self.rect):
                dy = -COIN_JUMP_HEIGHT
                self.vel_y = -25
                #Remove the coin from the screen
                coin_fx.play()
                coin.kill()
                coin_bool = True
            
        #Check if the player has made it to the scroll threshold
        if self.rect.top <= SCROLL_THRESH:
            #ALSO if 
            if self.vel_y < 0:
                scroll = -dy
            
        #Update player's x and y position
        self.rect.x += dx
        self.rect.y += dy + scroll
        
        return scroll, coin_bool
        
    def draw(self):
        #Draw the player image onto the screen with the coordinates
        #at the location of self.rect
        SCREEN.blit(self.image, self.rect)
        #Draw a red rectangle around player's rectangle (self.rect)
        # pygame.draw.rect(SCREEN, RED, self.rect, 2)

#Create Coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        #Load coin_image scaled to 30 x 30 pixels
        self.image = pygame.transform.scale(coin_image, (60, 60))
        #Get rectangle of the coin image
        self.rect = self.image.get_rect()
        #Set x and y values of the rect
        self.rect.x = x
        self.rect.y = y
        
    def update(self, scroll):
        #Update coin's vertical position when scrolling
        self.rect.y += scroll
        
        #Check if coin has gone off screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
        
#Create player instance
player = Player()

#Create sprite groups
coin_group = pygame.sprite.Group()

#Create initial coin 
coin = Coin(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
coin_group.add(coin)

#Game loop
run = True
while run:
    
    #While player is still alive:
    if game_over == False:
        
        #Update player sprite (move around)
        scroll, coin_bool = player.update()
        
        #Draw background
        bg_scroll += scroll / 4
        if bg_scroll >= SCREEN_HEIGHT:
            bg_scroll = 0
        draw_background(bg_scroll)
        
        #Generate coins
        if len(coin_group) < MAX_COINS:
            #Get random x coordinate for coin
            coin_x = random.randint(100, SCREEN_WIDTH - 100)
            #Get y coordinate of last coin rect and subtract by 80-120
            #pixels so they are always within range
            coin_y = coin.rect.y - 160
            #Create coin instance and add to coin group
            coin = Coin(coin_x, coin_y)
            coin_group.add(coin)
            
        #Update coins (scrolling)
        coin_group.update(scroll)
            
        #Check to see if player got a coin
        if coin_bool:
            coin_count += 1
            
        #Update score
        if scroll > 0:
            score += scroll
            if coin_bool:
                score += 100
            
        #Draw sprites
        coin_group.draw(SCREEN)
        player.draw()
        
        #Draw info panel
        draw_panel(coin_count)
        
        #Draw line at previous high score
        pygame.draw.line(SCREEN, WHITE, (0, score - high_score \
            + SCROLL_THRESH), (SCREEN_WIDTH, score - high_score \
            + SCROLL_THRESH), 3)
        draw_text("HIGH SCORE: " + str(high_score), \
            font_small, WHITE, SCREEN_WIDTH - 275, 
            score - high_score + SCROLL_THRESH)
        
        #Check game over
        if player.rect.top > SCREEN_HEIGHT + 10:
            game_over = True
        
    else:
        #Game over fade
        if fade_counter < SCREEN_WIDTH:
            fade_counter += 20
            for y in range(0, 6, 2):
                pygame.draw.rect(SCREEN, BLACK, (0, y * 100, \
                    fade_counter, SCREEN_HEIGHT / 6))
                pygame.draw.rect(SCREEN, BLACK, \
                    (SCREEN_WIDTH - fade_counter, (y + 1) * 100, \
                        SCREEN_WIDTH, SCREEN_HEIGHT / 6))
        
        #This else fixes making game over text appear after fade effect
        else:   
            draw_text("GAME OVER!", font_big, WHITE, 130, 200)
            draw_text("SCORE: " + str(score), font_big, WHITE, \
                130, 250)
            draw_text("COINS: " + str(coin_count), font_big, \
                WHITE, 130, 300)
            draw_text("PRESS SPACE TO PLAY AGAIN", font_big, WHITE, \
                20, 350)
    
            #Update high score
            if score > high_score:
                high_score = score
                with open("score.txt", 'w') as file:
                    file.write(str(high_score))
                    
            key = pygame.key.get_pressed()
            if key[K_SPACE]:
                #Reset variables
                game_over = False
                score = 0
                scroll = 0
                fade_counter = 0
                coin_count = 0
                #Reposition player
                player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
                #Reset coins
                coin_group.empty()
                #Create initial coin 
                coin = Coin(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
                coin_group.add(coin)
                
    #Event handler
    for event in pygame.event.get():
        if event.type == QUIT:
            #Update high score
            if score > high_score:
                high_score = score
                with open("score.txt", 'w') as file:
                    file.write(str(high_score))
            run = False 
            
    #Update display window
    pygame.display.flip()
    clock.tick(FPS)
    
pygame.quit()