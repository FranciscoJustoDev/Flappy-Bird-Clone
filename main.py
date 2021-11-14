# Birds
from numpy.core.fromnumeric import size
import pygame
import random
from os import path
from pygame import mouse

from pygame.constants import MOUSEBUTTONDOWN

assets_dir = path.join(path.dirname(__file__), "assets/")
textures_dir = path.join(path.dirname(assets_dir), "textures")
audio_dir = path.join(path.dirname(assets_dir), "audio")

WIDTH = 800
HEIGHT = 400
FPS = 30
STD_SIZE = (64, 64)
JUMP_FORCE = -10
JUMP_DELAY = 3
DEATH_JUMP = -5
OBSTACLE_GAP = STD_SIZE[0] + 100
GAME_SPEED = 2.2
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

in_menu = True
score = 0
high_score = 0

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("FlappyBiwwwaaaard!")
clock = pygame.time.Clock()

def text(surf, x, y, size, text, color):
    font = pygame.font.Font(pygame.font.match_font('arial'), size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surf.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_idle
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.direction = pygame.math.Vector2(0, 0)
        self.player_speed = GAME_SPEED
        self.gravity = 0.8
        self.alive = True

    def player_movement(self):
        # initial movement
        self.direction.x = self.player_speed
        if self.rect.left > WIDTH - (WIDTH / 2.5):
            self.player_speed = 0
        
    def jump(self):
        if pygame.key.get_pressed()[pygame.K_SPACE] and self.alive:
            self.direction.y = JUMP_FORCE
            sound_jump.play()
        
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
        player.alive = False
        player.image = player_dead
        player.direction.y = 0
        player.direction.y += JUMP_FORCE + DEATH_JUMP
        sound_die.play()

    def collision(self):
        if player.alive:
            if pygame.sprite.groupcollide(player_sprite, obstacle_sprites, False, False):
                self.game_over()
                print("Collision! - Dead!")
            if player.rect.top >= HEIGHT:
                self.game_over()
                print("Out of bounds! - Dead!")
            if player.rect.bottom <= 0:
                self.game_over()
                print("Out of bounds! - Dead!")
        if player.rect.top >= HEIGHT + STD_SIZE[1] and player.alive == False:
            player.rect.center = (WIDTH / 2, HEIGHT / 2)
            player.player_speed = GAME_SPEED
            player.direction.y = 0
            obstacle_sprites.empty()
            player.image = player_idle
            player.alive = True
            return 1

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
        if player.alive:
            if player.direction.y < JUMP_FORCE / 4:
                player.image = player_jump
            else:
                player.image = player_idle

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
        self.counts = True

    def update(self):
        if player.player_speed <= 0:
            self.rect.x -= GAME_SPEED
        if self.rect.right < 0:
            self.kill()
            print("super dead sprite -top!")   

class Start_button(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((90, 45))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT - (HEIGHT / 8) * 4)
        self.l = self.rect.left
        self.r = self.rect.right
        self.t = self.rect.top
        self.b = self.rect.bottom

    def select(self):
        mp = pygame.mouse.get_pos()
        if ((mp[0] >= self.l and mp[0] <= self.r) and (mp[1] >= self.t and mp[1] <= self.b)):
            self.image.fill(BLACK)
            if pygame.mouse.get_pressed(3) == (True, False, False):
                print("Pressed")
                return 1
        else:
            self.image.fill(GREEN)

    def update(self):
        self.select()

class Settings_button(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((80, 45))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT - ((HEIGHT / 8) * 3))
        self.l = self.rect.left
        self.r = self.rect.right
        self.t = self.rect.top
        self.b = self.rect.bottom

    def select(self):
        mp = pygame.mouse.get_pos()
        if ((mp[0] >= self.l and mp[0] <= self.r) and (mp[1] >= self.t and mp[1] <= self.b)):
            self.image.fill(BLACK)
            if pygame.mouse.get_pressed(3) == (True, False, False):
                print("Pressed")
                return 1
        else:
            self.image.fill(BLUE)

    def update(self):
        self.select()

class Quit_button(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((80, 45))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT - ((HEIGHT / 8) * 2))
        self.l = self.rect.left
        self.r = self.rect.right
        self.t = self.rect.top
        self.b = self.rect.bottom

    def select(self):
        mp = pygame.mouse.get_pos()
        if ((mp[0] >= self.l and mp[0] <= self.r) and (mp[1] >= self.t and mp[1] <= self.b)):
            self.image.fill(BLACK)
            if pygame.mouse.get_pressed(3) == (True, False, False):
                print("Pressed")
                pygame.quit()
        else:
            self.image.fill(RED)

    def update(self):
        self.select()


player_idle = pygame.image.load(path.join(textures_dir, "player_idle.png")).convert()
player_jump = pygame.image.load(path.join(textures_dir, "player_jump.png")).convert()
player_dead = pygame.image.load(path.join(textures_dir, "player_dead.png")).convert()

sound_jump = pygame.mixer.Sound(path.join(audio_dir, "jump.wav"))
sound_die = pygame.mixer.Sound(path.join(audio_dir, "die.wav"))
sound_highscore = pygame.mixer.Sound(path.join(audio_dir, "highscore-surpass.wav"))
sound_curs_move = pygame.mixer.Sound(path.join(audio_dir, "cursor-move.wav"))
sound_curs_select = pygame.mixer.Sound(path.join(audio_dir, "cursor-select.wav"))


# Groups
player_sprite = pygame.sprite.Group()
obstacle_sprites = pygame.sprite.Group()
menu_sprites = pygame.sprite.Group()
manager = Level_Manager()
player = Player()
start_button = Start_button()
settings_button = Settings_button()
quit_button = Quit_button()
menu_sprites.add(start_button)
menu_sprites.add(settings_button)
menu_sprites.add(quit_button)
player_sprite.add(player)


# Game Loop
while True:
    clock.tick(FPS)

    if in_menu is True:
        # input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        if start_button.select():
            in_menu = False

        # update
        menu_sprites.update()
        print(high_score)

        # draw
        screen.fill(WHITE)
        menu_sprites.draw(screen)
        text(screen, start_button.rect.centerx, start_button.rect.centery, 10, "START", BLACK)
        text(screen, settings_button.rect.centerx, settings_button.rect.centery, 10, "OPTIONS", BLACK)
        text(screen, quit_button.rect.centerx, quit_button.rect.centery, 10, "QUIT", BLACK)
        text(screen, 50, 50, 35, str(high_score), BLACK)
        pygame.display.flip()
    elif in_menu is False:
        # input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        # update
        manager.update()
        player_sprite.update()
        obstacle_sprites.update()
        if manager.collision():
            if score > high_score:
                high_score = score
            score = 0
            in_menu = True
        for obstacle in obstacle_sprites:
            if ((obstacle.rect.x < player.rect.x) and obstacle.counts) and player.alive:
                score += 1 
                obstacle.counts = False

        # draw
        screen.fill(BLACK)
        player_sprite.draw(screen)
        obstacle_sprites.draw(screen)
        text(screen, 50, 50, 35, str(score), WHITE)
        pygame.display.flip()
