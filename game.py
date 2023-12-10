import pygame
from pygame.locals import *
import random

pygame.init()

# create the window
game_width: int = 800
game_height: int = 500
screen_size: int= (game_width, game_height)
game_window: pygame.Surface = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Side Scroller')
padding_y: int = 100
padding_x: int = 50

# colors
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)

# number of milliseconds before you can fire another bullet
bullet_cooldown: int= 500
last_bullet_time: int= pygame.time.get_ticks()
next_enemy: int = pygame.time.get_ticks()

# function for resizing an image
def scale_image(image: pygame.Surface, new_width: int) -> pygame.Surface:
    image_scale = new_width / image.get_rect().width
    new_height = image.get_rect().height * image_scale
    scaled_size = (new_width, new_height)
    return pygame.transform.scale(image, scaled_size)

# background image
bg = pygame.image.load('images/bg.png').convert_alpha()
bg = scale_image(bg, game_width)
bg_scroll = 0

character_images = []
for i in range(2):
   character_image = pygame.image.load(f'images/player/fly{i}.png').convert_alpha()
   character_image = scale_image(character_image, 70)
   character_images.append(character_image)

heart_images = []
heart_image_index = 0
for i in range(8):
    heart_image = pygame.image.load(f'images/hearts/heart{i}.png').convert_alpha()
    heart_image = scale_image(heart_image, 30)
    heart_images.append(heart_image)

enemy_colors = ['blue', 'grey', 'red', 'yellow']
enemy_images = {}
for enemy_color in enemy_colors:
    enemy_images[enemy_color] = []
    for i in range(4):
        enemy_image: pygame.Surface = scale_image(pygame.image.load(f'images/birds/{enemy_color}{i}.png').convert_alpha(), 50)
        enemy_image = pygame.transform.flip(enemy_image, True, False)
        enemy_images[enemy_color].append(enemy_image)

class Player(pygame.sprite.Sprite):
    
    def __init__(self, x, y):

        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.jump = False
        self.jumpState = 0

        self.lives = 3
        self.score = 0

        # index of the image to be displayed
        self.image_index: int = 0

        # angle of the image
        self.image_angle: int = 0

    def update(self):

        # determine next image to display
        self.image_index += 1
        if self.image_index >= len(character_images):
            self.image_index = 0

        if self.jump == True:
            self.jumpState += 1
            if self.jumpState < 40:
                self.y -= 3
            elif self.jumpState > 40 and self.jumpState < 64:
                self.y += 5
            elif self.jumpState > 64:
                self.jump = False
                self.jumpState = 0



        # assign next image
        self.image =character_images[self.image_index]
        self.rect = self.image.get_rect()

        # update the angle of image
        self.image = pygame.transform.rotate(self.image, self.image_angle)

        self.rect.x = self.x
        self.rect.y = self.y

        # check if player collides with a enemy
        if pygame.sprite.spritecollide(self, enemy_group, True):
            self.lives -= 1

class Bullet(pygame.sprite.Sprite):
    
    def __init__(self, x, y):

        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.radius = 5

        self.rect = Rect(x, y, 10, 10)

    def draw(self):
        pygame.draw.circle(game_window, yellow, (self.x, self.y), self.radius)

    def update(self):

        # move the bullet to the right
        self.x += 2

        self.rect.x = self.x
        self.rect.y = self.y

        # remove bullet from sprite group when it goes off screen
        if self.x > game_width:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        # start on the right side of the game window
        self.x = game_width

        # select a random y coordinate
        self.y = random.randint(padding_y, game_height - padding_y * 2)

        # select a random color
        self.color = random.choice(enemy_colors)

        # index of the image to be displayed
        self.image_index = 0

        self.image = enemy_images[self.color][self.image_index]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):

        # move left
        self.x -= 2

        # determine next image to display
        self.image_index += 0.25
        if self.image_index >= len(enemy_images[self.color]):
            self.image_index = 0

        # assign next image
        self.image = enemy_images[self.color][int(self.image_index)]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # check if enemy collides with bullet
        if pygame.sprite.spritecollide(self, bullet_group, True):
            self.kill()
            player.score += 1

        # remove enemy from sprite group when it goes off screen
        if self.x < 0:
            self.kill()

# create the sprite groups
player_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

# create the player
player_x = 30
player_y = game_height - padding_y
player = Player(player_x, player_y)
player_group.add(player)

# game loop
clock = pygame.time.Clock()
fps = 60
running = True
while running:

    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # move thecharacter using the up/down arrow keys
    if keys[K_UP] and player.rect.top > padding_y:
        if player.jump == False:
            player.jump = True
    elif keys[K_LEFT] and player.rect.left > padding_x:
        player.x -= 2
    elif keys[K_RIGHT] and player.rect.right < game_width - padding_x:
        player.x += 2
    if player.y > game_height - padding_y:
        player.y = game_height - padding_y

    # shoot bullet with space bar
    if keys[K_SPACE] and last_bullet_time + bullet_cooldown < pygame.time.get_ticks():
        bullet_x = player.x + player.image.get_width()
        bullet_y = player.y + player.image.get_height() // 2
        bullet = Bullet(bullet_x, bullet_y)
        bullet_group.add(bullet)
        last_bullet_time = pygame.time.get_ticks()

    # spawn a new enemy
    if next_enemy < pygame.time.get_ticks():
        enemy = Enemy()
        enemy_group.add(enemy)

        # randomly pick between 0 to 3 seconds when the next enemy will spawn
        next_enemy = random.randint(pygame.time.get_ticks(), pygame.time.get_ticks() + 3000)

    # draw the background
    game_window.blit(bg, (0 - bg_scroll, 0))
    game_window.blit(bg, (game_width - bg_scroll, 0))
    bg_scroll += 1
    if bg_scroll == game_width:
        bg_scroll = 0

    # draw the player
    player_group.update()
    player_group.draw(game_window)

    # draw the bullets
    bullet_group.update()
    for bullet in bullet_group:
        bullet.draw()

    # draw the enemys
    enemy_group.update()
    enemy_group.draw(game_window)

    # display remaining lives
    for i in range(player.lives):
        heart_image = heart_images[int(heart_image_index)]
        heart_x = 10 + i * (heart_image.get_width() + 10)
        heart_y = 10
        game_window.blit(heart_image, (heart_x, heart_y))
    heart_image_index += 0.1
    if heart_image_index >= len(heart_images):
        heart_image_index = 0

    # display score
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render(f'Score: {player.score}', True, black)
    text_rect = text.get_rect()
    text_rect.center = (200, 20)
    game_window.blit(text, text_rect)
    pygame.display.update()

    # check if game is over
    while player.lives == 0:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

        gameover_str = f'Game over. Play again (y or n)?'
        font = pygame.font.Font(pygame.font.get_default_font(), 24)
        text = font.render(gameover_str, True, red)
        text_rect = text.get_rect()
        text_rect.center = (game_width / 2, game_height / 2)
        game_window.blit(text, text_rect)

        keys = pygame.key.get_pressed()
        if keys[K_y]:
            player_group.empty()
            bullet_group.empty()
            enemy_group.empty()
            player = Player(player_x, player_y)
            player_group.add(player)
        elif keys[K_n]:
            running = False
            break
        pygame.display.update()
pygame.quit()
