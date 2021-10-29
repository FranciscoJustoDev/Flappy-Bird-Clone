import pygame
import random
import os

WIDTH = 800
HEIGHT = 400
FPS = 30
STD_SIZE = (50, 50)

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FlappyBiwwwaaaard!")
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.direction = pygame.math.Vector2(0, 0)
        self.player_speed = 2.2
        self.gravity = 0.8

    def player_movement(self):
        # initial movement
        self.direction.y += self.gravity
        self.direction.x = self.player_speed
        if self.rect.left > WIDTH - (WIDTH / 2.5):
            self.player_speed = 0
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.direction.y = -10

    def update(self):
        self.player_movement()
        self.rect.x += self.direction.x * self.player_speed
        self.rect.y += self.direction.y * self.gravity


class Level(pygame.sprite.Sprite):
    def __init__(self):
        self.last = pygame.time.get_ticks()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(
            (50, random.randrange(100, int(HEIGHT - (HEIGHT / 3)))))
        self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.top = 0
        self.x = random.randrange(WIDTH, int(WIDTH + (WIDTH / 4)))
        self.rect.x = self.x
        self.image_dwn = pygame.Surface((50, HEIGHT))
        self.image_dwn.fill((255, 0, 0))
        self.rect_dwn = self.image_dwn.get_rect()
        self.rect_dwn.top = random.randrange(
            int(HEIGHT / 2), int(HEIGHT - (HEIGHT / 8)))
        self.rect_dwn.x = self.x
        self.flag = True

    def spawn(self):
        # if enough time passed, spawn another wall
        now = pygame.time.get_ticks()
        if now - self.last >= 3000:
            self.last = now
            level = Level()
            all_sprites.add(level)
            return False
        else:
            return True

    def update(self):
        if player.player_speed <= 0:
            self.rect.x -= 2.2
            self.rect_dwn.x -= 2.2
        if self.flag is True:
            self.flag = self.spawn()
        if self.rect.right < 0:
            self.kill()
            print("super dead sprite!")


all_sprites = pygame.sprite.Group()
player = Player()
level = Level()
all_sprites.add(player)
all_sprites.add(level)

while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    all_sprites.update()

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()
