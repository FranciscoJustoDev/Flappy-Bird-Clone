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
GAME_SPEED = 2.2
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FlappyBiwwwaaaard!")
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(STD_SIZE)
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.direction = pygame.math.Vector2(0, 0)
        self.player_speed = GAME_SPEED
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
        if self.player_speed == 0:
            self.direction.y += self.gravity
        self.player_movement()
        if self.direction.y >= JUMP_DELAY:
            self.jump()
        self.rect.x += self.direction.x * self.player_speed
        self.rect.y += self.direction.y * self.gravity

class Level_Manager(object):
    def __init__(self):
        self.flag = True

    def spawn(self, y_size):
        obstacle1 = Obstacle(y_size, 0)
        obstacle_sprites.add(obstacle1)
        obstacle2 = Obstacle(HEIGHT, y_size + OBSTACLE_GAP)
        obstacle_sprites.add(obstacle2)
    
    def game_over(self):
        player.rect.center = (WIDTH / 2, HEIGHT / 2)
        player.player_speed = GAME_SPEED
        player.direction.y = 0
        obstacle_sprites.empty()


    def collision(self):
        if pygame.sprite.groupcollide(player_sprite, obstacle_sprites, False, False):
            self.game_over()
            print("Collision! - Dead!")
        if player.rect.top >= HEIGHT:
            self.game_over()
            print("Out of bounds! - Dead!")
        if player.rect.bottom <= 0:
            self.game_over()
            print("Out of bounds! - Dead!")

    def update(self):
        self.collision()
        now = pygame.time.get_ticks()
        self.y_size = random.randrange(100, int(HEIGHT - (HEIGHT / 3)))
        if self.flag is True:
            self.spawn(self.y_size)
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
            self.rect.x -= GAME_SPEED
        if self.rect.right < 0:
            self.kill()
            print("super dead sprite -top!")   


player_sprite = pygame.sprite.Group()
obstacle_sprites = pygame.sprite.Group()
manager = Level_Manager()
player = Player()
player_sprite.add(player)


while True:
    clock.tick(FPS)
    # input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    # update
    manager.update()
    player_sprite.update()
    obstacle_sprites.update()

    #draw
    screen.fill(BLACK)
    player_sprite.draw(screen)
    obstacle_sprites.draw(screen)
    pygame.display.flip()
