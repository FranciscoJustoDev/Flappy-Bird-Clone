import pygame
import random
import os

WIDTH = 800
HEIGHT = 400
FPS = 30
STD_SIZE = (64, 64)
JUMP_FORCE = -10
JUMP_DELAY = 3
OBSTACLE_GAP = STD_SIZE[0] + 100
OBSTACLE_SPEED = 2.2

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FlappyBiwwwaaaard!")
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(STD_SIZE)
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.direction = pygame.math.Vector2(0, 0)
        self.player_speed = 2.2
        self.gravity = 0.8

    def player_movement(self):
        # initial movement
        self.direction.x = self.player_speed
        if self.rect.left > WIDTH - (WIDTH / 2.5):
            self.player_speed = 0
        
    def jump(self):
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.direction.y = JUMP_FORCE
        
    def update(self):
        self.direction.y += self.gravity
        self.player_movement()
        if self.direction.y >= JUMP_DELAY:
            self.jump()
        self.rect.x += self.direction.x * self.player_speed
        self.rect.y += self.direction.y * self.gravity

class Level_Manager(object):
    def __init__(self):
        self.flag = True

    def update(self):
        now = pygame.time.get_ticks()
        self.y_size = random.randrange(100, int(HEIGHT - (HEIGHT / 3)))
        if self.flag is True:
            obstacle1 = Obstacle(self.y_size, 0)
            obstacle_sprites.add(obstacle1)
            all_sprites.add(obstacle1)
            obstacle2 = Obstacle(HEIGHT, self.y_size + OBSTACLE_GAP)
            obstacle_sprites.add(obstacle2)
            all_sprites.add(obstacle2)
            self.last = pygame.time.get_ticks()
            self.flag = False
        if now - self.last >= 3000:
            self.last = now
            self.flag = True

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, size, y):
        pygame.sprite.Sprite.__init__(self)
        self.last = pygame.time.get_ticks()
        self.image = pygame.Surface(
            (STD_SIZE[0], size))
        self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.x = WIDTH

    def update(self):
        if player.player_speed <= 0:
            self.rect.x -= OBSTACLE_SPEED
        if self.rect.right < 0:
            self.kill()
            print("super dead sprite -top!")   

all_sprites = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
obstacle_sprites = pygame.sprite.Group()
manager = Level_Manager()
player = Player()
player_sprite.add(player)
all_sprites.add(player)

while True:
    clock.tick(FPS)
    # input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    # update
    manager.update()
    all_sprites.update()

    #draw
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
