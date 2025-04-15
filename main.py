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
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

# ================== FUNCTIONS =============

def createPlayer():
    """
    Initializes Player surface and rectangle.
    newPlayer.image (Surface): otter image
    newPlayer.rect (Rectangle): rectangle placed at bottom centre of screen
    
    Returns:
        newPlayer (Sprite)
    """
    # Create a player sprite. This allows adding a surface, rectangle, etc.. durectly to the player so all the data is kept with that sprite.
    # It also allows adding the player to a sprite group, which will come in handy later
    newPlayer = pygame.sprite.Sprite()
    # load the image, which returns a surface. Convert makes it faster to blit
    newPlayer.image = pygame.image.load("player.png").convert()
    #Make a specific colour on the image transparent (black, here).
    newPlayer.image.set_colorkey((0,0,0), RLEACCEL)
    #setting size of image
    playerSize = (250,300)
    newPlayer.image = pygame.transform.scale(newPlayer.image, playerSize)
    # the rectangle is used for the location of an object (where to place it), but also for collisions, etc..
    # this creates with the size of the surf. Without parameters, the rect is located wherever the surf was created
    newPlayer.rect = newPlayer.image.get_rect()
    # Return the newly created player sprite
    return newPlayer

def playerUpdate(player, pressed_keys):
    """
    Move the Player sprites based on user keypresses
    Args:
    player (Sprite)
    pressed_keys: dictionary containing the pressed keys 
    """
    # Move the Player's rectangle based on the keys pressed by the user
    if pressed_keys[K_UP]: # checks if the value for the K_UP key is True in the dictionary (i.e. the user pressed the up key)
        player.rect.y -= 8
    if pressed_keys[K_DOWN]: # notice if not elif, so more than one can be pressed
        player.rect.y+= 8
    if pressed_keys[K_LEFT]:
        player.rect.x -= 8 
    if pressed_keys[K_RIGHT]:
        player.rect.x += 8

    #  Keep player on the screen
    if player.rect.left < 0:
        player.rect.left = 0
    elif player.rect.right > SCREEN_WIDTH:
        player.rect.right = SCREEN_WIDTH
    if player.rect.top <= 0:
        player.rect.top = 0
    elif player.rect.bottom >= SCREEN_HEIGHT:
        player.rect.bottom = SCREEN_HEIGHT

def createFood():
    """
    Returns a sprite object called food.
    Adds an image, rectangle, and speed to the food object
    food.image (Surface): abalone image
    food.rect (Rectangle): initial position is randomly placed just to the right of the screen
    food.speed (int): Random integer between 5 and 20
    
    Returns:
        food (Sprite)

    """
    #  Create the new food
    food = pygame.sprite.Sprite()
    food.image = pygame.image.load("pig.png").convert() # load the image, which returns a surface. Convert makes it faster to blit
    food.image.set_colorkey((0,0,0), RLEACCEL) # This can be used to make a specific colour on your image transparent (white, here).

    #changing size of image
    foodSize = (200,100)
    food.image = pygame.transform.scale(food.image, foodSize)

    # Place the abalone randomly on the screen, starting between 20-100 pixels beyond the right hand side of the screen
    food.rect = food.image.get_rect(
        center=(
          random.randint(0, SCREEN_WIDTH ),
          random.randint(0, SCREEN_HEIGHT),
        )
    )
    # Select a random speed
    food.speed = random.randint(1, 5)
    return food

def foodUpdate(food):
    """
    Updates the position of the abalone sprite, destorying it if it off screen
    Args:
    food
    """

    food.rect.move_ip(-food.speed, 0)

    # if off screen, kill/destroy the object
    if food.rect.right < 0: 
        food.kill()

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
    text1 = font.render('Ollie the Otter is hungry', True, (255,255,255))
    textRect1 = text1.get_rect()
    textRect1.center = SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 45

    # Create text object, with associated rectangle below the other text
    text2 = font.render('Use the arrow keys to move.', True, (255,255,255))
    textRect2 = text2.get_rect()
    textRect2.center = SCREEN_WIDTH/2, SCREEN_HEIGHT/2 
    text3 = font.render('Catch 10 Abalone to win.', True, (255,255,255))
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
  
  
def end(screen):
    """
    Win screen shown at the end of the game
    Args:
        screen (Surface)
    """
    # Set screen as black with white text. 
    screen.fill((0,0,0))
    font = pygame.font.Font('freesansbold.ttf', 32)

    # Create text object, with associated rectangle in centre of screen
    text = font.render('YOU WIN', True, (255,255,255))
    textRect = text.get_rect()
    textRect.center = SCREEN_WIDTH/2, SCREEN_HEIGHT/2

    # blit needed for it to be placed on the surface, then display updated for it to show up.
    screen.blit(text, textRect)

# ======================== MAIN ========================

#  Set up the drawing window
# Returns a Surface, which represents the inside dimensions of your drawing window --> the OS controls the borders & title bar, etc.
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT]) 


#  Create a custom event for adding a new food
ADDFOOD = pygame.USEREVENT + 1 # USEREVENT is the last kind of event that pygame reserves, so by adding 1 to this number, ADDFOOD becomes a new event with its own individual # 
pygame.time.set_timer(ADDFOOD, 1000) # this makes the ADDFOOD event happen every 250ms (4/s). We call this once, but it fires throughout the game.

# Initialize hunger status
hungerStatus = 10

# ====PLAYER SPRITE
# Create a player sprite.
player = createPlayer()

# =====SPRITE GROUPS
#  Create groups to hold food sprites and all sprites
#  - foodGrp is used for collision detection and position updates
#  - all_sprites is used for rendering
foodGrp = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

#  Adjust the timing so the framerate isn't so high (adjusted in the game loop)
clock = pygame.time.Clock()

status = 'instructions' # Used to determine whether the user quit (default setting), lost, or won

# Used to show end screen for a short time period
endTimer = 0

#  Run until the user asks to quit or game ends
running = True

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
            #  Create the new food
            new_food = createFood()
            # Add new food to the food group and to the all sprites group
            foodGrp.add(new_food)
            all_sprites.add(new_food)
      
    # gets a dictionary of the keys pressed 
    pressed_keys = pygame.key.get_pressed()
      
    # Show instructions
    if status == 'instructions':
        start(screen)
        
    elif status == 'game':
        # update player position based on key presses
        playerUpdate(player, pressed_keys)
      
        # Update food position
        for food in foodGrp:
            foodUpdate(food)
            
        #  Check if any of the foodGrp have collided with the player
        col = pygame.sprite.spritecollideany(player, foodGrp)
        if col is not None:
            col.kill() # kill the food it ate
            hungerStatus -= 1

        # if hunger gets to zero, user wins
        if hungerStatus == 0:
            status = 'win'
            # get the time since beginning of the program
            endTimer = pygame.time.get_ticks()

        #  Draw the background
        screen.fill((0,0,0)) # solid colour option


        # Draw all sprites
        # draw is a built in method. We pass the display screen, and it will draw the sprites within the group
        # In order to draw the sprites, they must have an image attribute (.image -- this is a Surface) and a rect attribute (.rect)
        all_sprites.draw(screen)



        # Display the hunger level
        font = pygame.font.Font('freesansbold.ttf', 25)
        text = font.render('Hunger: '+ str(hungerStatus), True, (255,255,255))
        textRect = text.get_rect()
        textRect.center = SCREEN_WIDTH/2, 50
        screen.blit(text, textRect)
        
    elif status == 'win':
        end(screen)
        # User is able to close the screen if they press Esc or the x on the end screen
        # Window automatically closes after 5 seconds
        if pygame.time.get_ticks()  - endTimer > 5000:
            running = False
        
        

    pygame.display.update()

    #  Set framerate to 30 frames per second
    clock.tick(30)



# Quit
pygame.quit()
