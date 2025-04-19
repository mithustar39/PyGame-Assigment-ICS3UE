"""

"""

# ============== Useful notes about Pygame ==============
"""
"""

# ============== Image Sources ==============
"""

"""

# ======================== IMPORTS & SETUP ========================
import sys
import time # just for the end win/lose screen
import random

# allows access to the pygame library
import pygame

# These allow you to just write K_UP instead of having to write pygame.K_UP. Not necessary, but handy as shortforms.
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_RETURN,
    KEYDOWN,
    QUIT,
)

# Initialize pygame - this is required.
pygame.init()

# ================== CONSTANTS =============

#  Define constants for the screen width and height
infoObject = pygame.display.Info()
SCREEN_WIDTH = infoObject.current_w
SCREEN_HEIGHT = infoObject.current_h

# Level thresholds and settings
LEVEL_TARGETS = {1:10, 2:15, 3:20, 4:25, 5:30}
MAX_LEVEL = 5
level = 1
hungerStatus = LEVEL_TARGETS[level]

# Player speed and states
pSpeed = 8       # base movement speed
powered = False  # power-up state
powerEnd = 0     # time when power-up ends
stunned = False  # stun state from zombie
stunEnd = 0      # time when stun ends

# Timers & custom events
ADDFOOD   = pygame.USEREVENT + 1
ADDMUD    = pygame.USEREVENT + 2
ADDZOMBIE = pygame.USEREVENT + 3
pygame.time.set_timer(ADDFOOD, 3000)      # spawn pigs every second
pygame.time.set_timer(ADDMUD, 15000)      # spawn mud every 15 seconds
# ADDZOMBIE timer set at level-ups


# ================== FUNCTIONS =============

def createPlayer():
    """
    Initializes Player surface and rectangle.
    newPlayer.image (Surface): player image
    newPlayer.rect (Rectangle): rectangle placed at bottom centre of screen
    
    Returns:
        newPlayer (Sprite)
    """
    player = pygame.sprite.Sprite()
    img = pygame.image.load("player.png").convert()
    img.set_colorkey((0,0,0), RLEACCEL)
    img = pygame.transform.scale(img, (SCREEN_WIDTH//6, SCREEN_HEIGHT//5))
    player.image = img
    player.rect = img.get_rect(midbottom=(SCREEN_WIDTH/2, SCREEN_HEIGHT-10))
    return player

def playerUpdate(player, pressed_keys, speed):
    """
    Move the Player sprites based on user keypresses
    Args:
    player (Sprite)
    pressed_keys: dictionary containing the pressed keys 
    """
    #Controles of player
    if pressed_keys[K_UP]:    
        player.rect.y -= speed
    if pressed_keys[K_DOWN]:  
        player.rect.y += speed
    if pressed_keys[K_LEFT]:  
        player.rect.x -= speed
    if pressed_keys[K_RIGHT]: 
        player.rect.x += speed
    # keep on screen
    if player.rect.left < 0: player.rect.left = 0
    if player.rect.right > SCREEN_WIDTH: player.rect.right = SCREEN_WIDTH
    if player.rect.top < 0: player.rect.top = 0
    if player.rect.bottom > SCREEN_HEIGHT: player.rect.bottom = SCREEN_HEIGHT

def createFood():
    """
    Returns a sprite object called food (pig).
    Adds an image, rectangle, and speed to the food object
    food.image (Surface): pig image
    food.rect (Rectangle): initial position is randomly placed
    food.speed (int): Random integer between -5 and 5
    
    Returns:
        food (Sprite)

    """
    food = pygame.sprite.Sprite()
    img = pygame.image.load("pig.png").convert()
    img.set_colorkey((0,0,0), RLEACCEL)
    img = pygame.transform.scale(img, (SCREEN_WIDTH//16, SCREEN_HEIGHT//16))
    food.image = img
    food.rect = img.get_rect(center=(
        random.randint(0,SCREEN_WIDTH), random.randint(0,SCREEN_HEIGHT)
    ))
    food.speedx = random.randint(-5,5)
    food.speedy = random.randint(-5,5)
    return food

def foodUpdate(food):
    """
    Updates the position of the food sprite, destorying it if in contact with player
    Will bounce on contact with screen edge
    """
    food.rect.move_ip(food.speedx, food.speedy)
    
    #if off screen, bounce object
    if food.rect.left < 0 or food.rect.right > SCREEN_WIDTH:
        food.speedx *= -1
    if food.rect.top < 0 or food.rect.bottom > SCREEN_HEIGHT:
        food.speedy *= -1

def createMud():
    """
    Returns a sprite object called mud.
    Adds an image, rectangle, and speed to the mud object
    mud.image (Surface): mud image
    mud.rect (Rectangle): initial position is randomly placed just to the right of the screen
    """
    mud = pygame.sprite.Sprite()
    img = pygame.image.load("mud.png").convert()
    img.set_colorkey((0,0,0), RLEACCEL)
    img = pygame.transform.scale(img, (SCREEN_WIDTH//12, SCREEN_HEIGHT//12))
    mud.image = img
    mud.rect = img.get_rect(center=(
        random.randint(0,SCREEN_WIDTH),
        random.randint(0,SCREEN_HEIGHT)
    ))
    return mud

def createPowerUp():
    """
    Provides the player with a speed boost when collected
    """
    pu = pygame.sprite.Sprite()
    # load & transparent‑key the image
    img = pygame.image.load("powerup.png").convert()
    img.set_colorkey((0,0,0), RLEACCEL)
    # scale to desired size
    img = pygame.transform.scale(img, (SCREEN_WIDTH//20, SCREEN_HEIGHT//20))
    pu.image = img
    # place it at a random spot on screen
    pu.rect = img.get_rect(
        center=(
            random.randint(50, SCREEN_WIDTH - 50),
            random.randint(50, SCREEN_HEIGHT - 50)
        )
    )
    return pu

def createZombie():
    """
    On contact with player, will stun player for a set amount of time
    """
    zb = pygame.sprite.Sprite()
    # load & set transparency
    img = pygame.image.load("zombie.png").convert()
    img.set_colorkey((0,0,0), RLEACCEL)
    img = pygame.transform.scale(img, (SCREEN_WIDTH//16, SCREEN_HEIGHT//16))
    zb.image = img
    # place randomly on screen
    zb.rect = img.get_rect(
        center=(
            random.randint(0, SCREEN_WIDTH),
            random.randint(0, SCREEN_HEIGHT)
        )
    )
    # give it a simple bouncing movement
    zb.speedx = random.choice([-3, 3])
    zb.speedy = random.choice([-3, 3])
    return zb

def start(screen):
    """
    Instruction screen shown at the start of the game
    Args:
        screen (Surface)
    """
    # Set screen as black with white text. 
    screen.fill((0,0,0))
    font = pygame.font.Font('freesansbold.ttf', 32)

    # Create text object, with associated rectangle in centre of screen
    text1 = font.render('OH NO, Ellies pigs have broken out of the barn!', True, (255,255,255))
    textRect1 = text1.get_rect()
    textRect1.center = SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 45

    # Create text object, with associated rectangle below the other text
    text2 = font.render('Use the arrow keys to move.', True, (255,255,255))
    textRect2 = text2.get_rect()
    textRect2.center = SCREEN_WIDTH/2, SCREEN_HEIGHT/2 
    text3 = font.render('There are 5 levels and you must catch the needed number of pigs.', True, (255,255,255))
    textRect3 = text3.get_rect()
    textRect3.center = SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 45
    text4 = font.render('Press Enter to Begin.', True, (255,255,255))
    textRect4 = text4.get_rect()
    textRect4.center = SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 90

    # blit needed for it to be placed on the surface, then display updated for it to show up.
    screen.blit(text1, textRect1)
    screen.blit(text2, textRect2)
    screen.blit(text3, textRect3)
    screen.blit(text4, textRect4)
  
  
def end(screen, duration):
    """
    Win screen shown at the end of the game
    Args:
        screen (Surface)
    """
    # Set screen as black with white text. 
    screen.fill((0,0,0))
    font = pygame.font.Font('freesansbold.ttf', 32)

    # Create text object, with associated rectangle in centre of screen
    text = font.render('YOU CAUGHT ALL OF THE PIGS!', True, (255,255,255))
    textRect = text.get_rect()
    textRect.center = SCREEN_WIDTH/2, SCREEN_HEIGHT/2

    # blit needed for it to be placed on the surface, then display updated for it to show up.
    screen.blit(text, textRect)

    # score
    # calculate time taken to win in seconds
    time = duration/1000
    time = round(time, 2)
    scoreText = font.render(f'Time: {time} seconds', True, (255,255,255))
    scoreRect = scoreText.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2+30))
    screen.blit(scoreText, scoreRect)

# ======================== MAIN ========================

#  Set up the drawing window
# Returns a Surface, which represents the inside dimensions of drawing window --> the OS controls the borders & title bar, etc.
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT]) 
imgbg = pygame.image.load("BG.png").convert()
imgbg = pygame.transform.scale(imgbg, (SCREEN_WIDTH, SCREEN_HEIGHT))

# =====SPRITE GROUPS
#  Create groups to hold food sprites and all sprites
#  - foodGrp is used for collision detection and position updates
#  - all_sprites is used for rendering
player = createPlayer()
all_sprites = pygame.sprite.Group(player)
foodGrp = pygame.sprite.Group()
mudGrp = pygame.sprite.Group()
powerGrp = pygame.sprite.Group()
zombieGrp = pygame.sprite.Group()

#  Adjust the timing so the framerate isn't so high (adjusted in the game loop)
clock = pygame.time.Clock()

status = 'instructions'
startTimer = 0
endTimer = 0
running = True

#  Main loop - this is where the game runs. It will run until the user closes the window or presses Esc.
#  The loop will run until the user closes the window or presses Esc.
while running:

    for event in pygame.event.get(): # every user input --> an event. This gets each of the events in a list.
        if event.type == KEYDOWN:
            # Check if the user clicked the escape key
            if event.key == K_ESCAPE:
                running = False
            # Start game if user is seeing the instructions and presses enter
            if event.key == K_RETURN and status == 'instructions':
                status = 'game'
        #  Did the user click the window close button?
        elif event.type == QUIT:
            running = False
          
        #  Add a new food if it's time
        elif event.type == ADDFOOD and status == 'game':
            for _ in range(2):
                f = createFood(); 
                foodGrp.add(f); 
                all_sprites.add(f)
        elif status == 'game' and event.type == ADDMUD:
            m = createMud(); 
            mudGrp.add(m); 
        elif status == 'game' and event.type == ADDZOMBIE:
            # spawn one zombie per event
            z = createZombie(); 
            zombieGrp.add(z); 
            all_sprites.add(z)
      
    # gets a dictionary of the keys pressed 
    pressed_keys = pygame.key.get_pressed()
      
    # Show instructions
    if status == 'instructions':
        start(screen)
    
    
    elif status == 'game':
        now = pygame.time.get_ticks()
        # recover stun/power
        if stunned and now > stunEnd:
            stunned = False
        if powered and now > powerEnd:
            powered = False; pSpeed = 8
        
        # check mud
        if pygame.sprite.spritecollideany(player, mudGrp) and not stunned:
            speedNow = max(2, 8//2)
        else:
            speedNow = pSpeed if not stunned else 0

        # check power-up
        pu = pygame.sprite.spritecollideany(player, powerGrp)
        if pu:
            pu.kill(); 
            powered = True; 
            pSpeed = 16; 
            powerEnd = now + 5000

        # check zombie
        zb = pygame.sprite.spritecollideany(player, zombieGrp)
        if zb:
            zb.kill(); 
            stunned = True; 
            stunEnd = now + 3000

        # update player position based on key presses
        playerUpdate(player, pressed_keys, speedNow)
      
        # Update food position
        for food in foodGrp:
            foodUpdate(food)
        for zb in zombieGrp: 
            foodUpdate(zb)  # reuse bounce logic    
        
        #  Check if any of the foodGrp have collided with the player
        col = pygame.sprite.spritecollideany(player, foodGrp)
        if col is not None:
            col.kill() # kill the food it ate
            hungerStatus -= 1

        # Check if any of the zombies have collided with the player
        col = pygame.sprite.spritecollideany(player, zombieGrp)
        if col is not None:
            col.kill()
            if not powered:
                hungerStatus -= 1
                stunned = True; 
                stunEnd = now + 3000

        # level up
        if hungerStatus <= 0:
            if level < MAX_LEVEL:
                level += 1
                hungerStatus = LEVEL_TARGETS[level]
                # increase spawn speed & speed
                pSpeed += 1
                for grp in (foodGrp, mudGrp, powerGrp, zombieGrp, all_sprites):
                    for spr in list(grp):
                        #so we do not kill the player
                        if spr is not player:
                            spr.kill()

                # schedule zombies
                if level == 4:
                    pygame.time.set_timer(ADDZOMBIE, 10000)
                    pu = createPowerUp()
                if level == 5:
                    pygame.time.set_timer(ADDZOMBIE, 8000)
                    # add an extra power-up
                    pu = createPowerUp()
                    pu = createPowerUp()
                    powerGrp.add(pu) 
                    all_sprites.add(pu)
            else:
                status = 'win'
                endTimer = pygame.time.get_ticks()

        #  Draw the background
        #screen.fill((0,0,0)) # solid colour option
        screen.blit(imgbg, (0,0))

        # Draw all sprites
        # draw is a built in method. We pass the display screen, and it will draw the sprites within the group
        # In order to draw the sprites, they must have an image attribute (.image -- this is a Surface) and a rect attribute (.rect)
        mudGrp.draw(screen)       # draw mud beneath
        all_sprites.draw(screen)  # draw player, food, powerups, zombies on top



        # Display the hunger level
        font = pygame.font.Font('freesansbold.ttf', 25)
        text = font.render('Catch pigs: '+ str(hungerStatus), True, (255,255,255))
        textRect = text.get_rect()
        textRect.center = SCREEN_WIDTH/2, 50
        screen.blit(text, textRect)
        txt1 = font.render(f'Level: {level}', True, (255,255,255))
        screen.blit(txt1, (30,30))
        
    elif status == 'win':
        end(screen, endTimer)
        # User is able to close the screen if they press Esc or the x on the end screen
        # Window automatically closes after 5 seconds
        if pygame.time.get_ticks()  - endTimer > 5000:
            running = False
        
        

    pygame.display.update()

    #  Set framerate to 30 frames per second
    clock.tick(30)



# Quit
pygame.quit()
