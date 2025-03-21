import sys
import pygame
import random

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Piggy Roundup")

# Load background image
bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
bg.fill((173, 216, 230))  # Light blue background as a placeholder

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png").convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def update(self, keys):
        if keys[K_UP]:
            self.rect.move_ip(0, -5)
        if keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep the player within screen bounds
        self.rect.clamp_ip(screen.get_rect())

# Pig class
class Pig(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("pig.png").convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect()
        self.rect.topleft = (random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50))

# Create player and pigs
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

pigs = pygame.sprite.Group()
for _ in range(5):  # Add 5 pigs
    pig = Pig()
    pigs.add(pig)
    all_sprites.add(pig)

# Main loop
running = True
while running:
    screen.blit(bg, (0, 0))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            running = False
    
    keys = pygame.key.get_pressed()
    player.update(keys)
    
    # Check for collision between player and pigs
    caught_pigs = pygame.sprite.spritecollide(player, pigs, True)
    if caught_pigs:
        print(f"Caught {len(caught_pigs)} pig(s)!")
    
    all_sprites.draw(screen)
    pygame.display.update()

pygame.quit()
