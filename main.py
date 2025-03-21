'''
'''

#--------------IMPORTS----------------
import sys
import time
import pygame

from pygame.locals import(
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

pygame.init()

#------------CONSTANTS---------------

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

#move somewhere else
screen = display.set_mode((1000, 800))
display.set_caption("Piggy Roundup")

#------------FUNCTIONS---------------

def createPlayer(sham):
    '''
    '''
    

    sham.image = pygame.image.load("insert image file").convert()
    sham.image.set_colorkey((255, 255, 255), RLEACCEL)
    sham.rect = sham.image.get_rect()












#Main loop
running = True
while running:
    for event inpygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
    
    blit(bg, screen)
    shamSprite.draw(screen)
    
    pygame.display.update()



pygame.quit()
