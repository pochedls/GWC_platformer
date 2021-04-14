# Imports
import pygame
import random
from pygame.locals import *
pygame.init()

# Parameters
vec = pygame.math.Vector2
HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60

# Set up game basics
FramePerSec = pygame.time.Clock()
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fun Game")

# Set up our sprite player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((75, 75, 240))
        self.rect = self.surf.get_rect()
        self.pos = vec((10, 360))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        
    def move(self):
        self.acc = vec(0, 0.5)
        pressed_keys = pygame.key.get_pressed()
  
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
  
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        self.rect.midbottom = self.pos

    def jump(self):
        hits = pygame.sprite.spritecollide(P1, platforms, False)
        if hits:
            self.vel.y = -15

    def update(self):
        hits = pygame.sprite.spritecollide(P1, platforms, False)
        if P1.vel.y > 0:
            if hits:
                self.pos.y = hits[0].rect.top + 1
                self.vel.y = 0

# Set up our sprite platform class
class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        pwidth = random.randint(50, 100)
        pheight = 12
        self.surf = pygame.Surface((pwidth, pheight))
        self.surf.fill((240, 75, 75))
        pcenter_x = random.randint(0, WIDTH-10)
        pcenter_y = random.randint(0, HEIGHT-30)
        self.rect = self.surf.get_rect(center = (pcenter_x, pcenter_y))

# Add our main platform (our floor)
PT1 = platform()
PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((255, 0, 0))
PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT-10))

# Add our player block
P1 = Player()

# Keep track of all the sprites and platforms in groups
all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)
platforms = pygame.sprite.Group()
platforms.add(PT1)

# add random levels
for x in range(6):
    pl = platform()
    platforms.add(pl)
    all_sprites.add(pl)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                P1.jump()
 
    displaysurface.fill((220, 220, 220))
    P1.move()
    P1.update()
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
    pygame.display.update()
    FramePerSec.tick(FPS)
