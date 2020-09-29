# Space shooter game by SHR
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder>
# licensed under CC-BY-3 <http://creativecommons.org/licenses/by/3.0/>
# Art and other graphics are taken from Kenny.nl


import pygame
import random
from os import path

#nafis DUm dum 

img_dir = path.join(path.dirname(__file__))

snd_dir = img_dir

width = 500
height = 600
FPS = 60
POWERUP_TIME = 5000

# Basic Colors:
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
# Initializing the Game

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Shooter By SHR ")
clock = pygame.time.Clock()

# sprites are anything that moves around in the screen

all_sprites = pygame.sprite.Group()
# Drawing the Scores and stuff
font_name = pygame.font.match_font("arial")


def draw_shield_bar(x, y, pct, isboss):
    if pct < 0:
        pct = 0

    bar_length = 100
    bar_height = 10
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    pygame.draw.rect(screen, WHITE, outline_rect, 2)
    if isboss:
        percentage = (pct / 500) * 100
    else:
        percentage = pct
    fill_rect = pygame.Rect(x, y, percentage, bar_height)
    if percentage >= 70:
        color = GREEN
    if 70 > percentage >= 36:
        color = YELLOW
    if 36 > percentage:
        color = RED

    pygame.draw.rect(screen, color, fill_rect)


def show_go_screen():
    draw_text(screen, "WELCOME TO", 42, width / 2, height / 4 - 50)
    draw_text(screen, "SPACE SHOOTER BY SHR", 50, width / 2, height / 4)
    draw_text(screen, "Arrow keys to move and space to shoot", 22, width / 2, height / 2)
    draw_text(screen, "OR", 22, width / 2, height / 2 + 30)
    draw_text(screen, "A and D keys to move and space to shoot", 22, width / 2, height / 2 + 50)
    draw_text(screen, "Press a key to start", 18, width / 2, height * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


def show_end_screen(player_score, boss_dead):
    score_display = f"Your Score : {player_score}"
    draw_text(screen, "Thank you for playing!", 64, width / 2, height / 4)
    if boss_dead:
        draw_text(screen, "CONGRATULATIONS!", 64, width / 2, height / 4)
        draw_text(screen, "YOU WIN!", 64, width / 2, height / 4)

    draw_text(screen, score_display, 22, width / 2, height / 2)
    draw_text(screen, "Press a key to Quit", 18, width / 2, height * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
                return True


def draw_lives(surf, x, y, lives, img):
    for z in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * z
        img_rect.y = y
        surf.blit(img, img_rect)


def new_mob(score_player):
    m = Mob(score_player)
    all_sprites.add(m)
    mobs.add(m)


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(boss_img, (120, 90))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = width / 2
        self.rect.bottom = 200
        self.speedx = 0
        self.shield = 500
        self.last_shot = pygame.time.get_ticks()
        self.speedx = 2

    def update(self):

        self.rect.x += self.speedx
        if self.rect.right >= width:
            self.speedx = -2
        elif self.rect.left <= 0:
            self.speedx = 2

    def shoot(self):
        bullet = Bullet(self.rect.left, self.rect.bottom + 30, True)
        bullet2 = Bullet(self.rect.right, self.rect.bottom + 30, True)
        all_sprites.add(bullet)
        all_sprites.add(bullet2)
        bullets.add(bullet2)
        bullets.add(bullet)
        shoot_sound.play()
        shoot_sound.play()


# The space Ship

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (55, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = width / 2
        self.rect.bottom = height - 10
        self.speedx = 0
        self.shield = 100
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_timer = pygame.time.get_ticks()

    def update(self):
        # Timeout of Powerups
        if self.power > 1:
            if pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
                self.power -= 1
                self.power_time = pygame.time.get_ticks()

        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = width / 2
            self.rect.bottom = height - 10

        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedx = 5
        self.rect.x += self.speedx
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def shoot(self):
        if self.power == 1:
            bullet = Bullet(self.rect.centerx, self.rect.top, False)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()
        if self.power > 1:
            bullet1 = Bullet(self.rect.left, self.rect.centery, False)
            bullet2 = Bullet(self.rect.right, self.rect.centery, False)
            all_sprites.add(bullet1)
            bullets.add(bullet1)
            all_sprites.add(bullet2)
            bullets.add(bullet2)
            shoot_sound.play()

    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (width / 2, height + 200)


# **************************===================*************=======================********************========***********==============**********
class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.num = random.random()
        if self.num > 0.5:
            # self.image = powerup_img["shield"]
            self.type = "gun"
            self.image = pygame.image.load(path.join(img_dir, "laser.png")).convert()
        else:
            self.type = "shield"
            self.image = pygame.image.load(path.join(img_dir, "shield.png")).convert()

        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        # kill it if it moves off the screen
        if self.rect.top > height:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, isboss):
        pygame.sprite.Sprite.__init__(self)
        self.isboss = isboss
        if not self.isboss:
            self.image = pygame.transform.scale(bullet1_img, (10, 30))
        else:
            self.image = pygame.transform.scale(bullet2_img, (10, 30))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        if isboss:
            self.speedy = 15
        else:
            self.speedy = -10
        if isboss:
            self.speedx = random.randrange(-4, 4)

    def update(self):
        if self.isboss:
            self.rect.y += self.speedy
            self.rect.x += self.speedx
        else:
            self.rect.y += self.speedy

        # kill it if it moves off the screen
        if self.rect.bottom < 0:
            self.kill()


# pygame.transform.scale(enemy_img, (70, 45))
class Mob(pygame.sprite.Sprite):
    def __init__(self, player_score):
        pygame.sprite.Sprite.__init__(self)
        self.ennum = random.randrange(1, 3)
        if self.ennum // 2 == 0:
            self.image = pygame.transform.scale(enemy_img, (70, 45))
        else:
            self.image = pygame.transform.scale(enemy2_img, (70, 45))

        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, width - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedx = random.randrange(-3, 3)
        if 0 < player_score < 1000:
            self.speedy = random.randrange(1, 8)
        elif 1000 <= player_score < 2500:
            self.speedy = random.randrange(3, 9)
        elif 2500 <= player_score < 3000:
            self.speedy = random.randrange(4, 10)
        elif 3000 <= player_score < 10000:
            self.speedy = random.randrange(4, 12)
        elif 10000 <= player_score < 15000:
            self.speedy = random.randrange(5, 13)
        elif 15000 <= player_score < 20000:
            self.speedy = random.randrange(6, 13)
        elif 20000 <= player_score < 30000:
            self.speedy = random.randrange(7, 14)
        elif 30000 <= player_score < 37000:
            self.speedy = random.randrange(8, 14)
        elif 370000 <= player_score < 43000:
            self.speedy = random.randrange(8, 15)
        elif 430000 <= player_score:
            self.speedy = random.randrange(9, 15)
        else:
            self.speedy = random.randrange(1, 8)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > height + 20 or self.rect.left <= -60 or self.rect.right > width + 60:
            self.rect.x = random.randrange(0, width - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)


class explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


player_img = pygame.image.load(path.join(img_dir, "player.png")).convert()
boss_img = pygame.image.load(path.join(img_dir, "boss.png")).convert()
mini_player = pygame.transform.scale(player_img, (25, 19))
mini_player.set_colorkey(BLACK)

enemy_img = pygame.image.load(path.join(img_dir, "enemyShip.png")).convert()
enemy2_img = pygame.image.load(path.join(img_dir, "enemyUFO.png")).convert()

bullet1_img = pygame.image.load(path.join(img_dir, "laserRed.png")).convert()
bullet2_img = pygame.image.load(path.join(img_dir, "laserGreen.png")).convert()


bullets = pygame.sprite.Group()
mobs = pygame.sprite.Group()

# initalizing scores
score = 0
powerups = pygame.sprite.Group()

for i in range(8):
    new_mob(score)

player = Player()
boss_lvl = Boss()
all_sprites.add(player)

# Explosions
explosion_anim = {}
explosion_anim["lg"] = []
explosion_anim["sm"] = []

for i in range(1, 5):
    filename = f"exp{i}.jpg"

    if i == 1:
        img = pygame.image.load(f"C:/Users/User/PycharmProjects/GameDevlopment/exp{i}.png").convert()
        img.set_colorkey(BLACK)
    else:
        img = pygame.image.load(f"C:/Users/User/PycharmProjects/GameDevlopment/exp{i}.jpg").convert()
        img.set_colorkey(BLACK)

    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim["lg"].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim["sm"].append(img_sm)


# Load all graphics ==============================================================================================
powerup_img = {}
powerup_img["gun"] = pygame.image.load(path.join(img_dir, "laser.png")).convert()
powerup_img["shield"] = pygame.image.load(path.join(img_dir, "shield.png")).convert()

background = pygame.image.load(path.join(img_dir, "backgrnd.png")).convert()
background_rect = background.get_rect()

# Load all of the game sounds

shield_sound = pygame.mixer.Sound(path.join(snd_dir, "shield.wav"))
gun_sound = pygame.mixer.Sound(path.join(snd_dir, "gun.wav"))

shoot_sound = pygame.mixer.Sound(path.join(snd_dir, "FireLaser.wav"))
expl_sounds = []
for snd in ["Explosion.wav", "Explosion2.wav"]:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))

pygame.mixer.music.load(path.join(snd_dir, "backgndsnd.ogg"))
pygame.mixer.music.set_volume(0.4)

game_start = True
boss_start = False
run_game = True
pygame.mixer.music.play(loops=-1)
while run_game:
    # keep the loop running at the right speed:
    clock.tick(FPS)
    if game_start:
        show_go_screen()
        game_start = False
    # the game Loop
    for event in pygame.event.get():
        # checking for a closed window
        if event.type == pygame.QUIT:
            run_game = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    # Update
    # Updating all of the moving objects that we have in the game
    all_sprites.update()

    # Checking if a bullet hits a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    current_time = pygame.time.get_ticks()
    for hit in hits:
        # Scoring System

        if score < 500:
            score += 25
        elif 500 <= score < 1000:
            score += 50
        elif 1000 <= score < 2000:
            score += 75
        elif 2000 <= score < 6000:
            score += 125
        elif 6000 <= score < 11000:
            score += 150
        elif 11000 <= score < 20000:
            score += 175
        elif 20000 <= score < 35000:
            score += 200
        elif 35000 <= score < 45000:
            score += 250
        elif 45000 <= score < 60000:
            score += 300

        random.choice(expl_sounds).play()
        if score < 19700:
            new_mob(score)
        expl = explosion(hit.rect.center, "lg")
        all_sprites.add(expl)
        if random.random() > 0.96:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)

    # ############################################################
    if score >= 20000:
        all_sprites.add(boss_lvl)
        boss_start = True

    if boss_start:
        if current_time - boss_lvl.last_shot > 1000:
            boss_lvl.last_shot = pygame.time.get_ticks()
            boss_lvl.shoot()

    # checking if boss bullet hit the player:
    if boss_start:
        hits = pygame.sprite.spritecollide(player, bullets, True)
        for hit in hits:
            random.choice(expl_sounds).play()
            player.shield -= 33
            if player.shield > 33:
                player_expl = explosion(hit.rect.center, "sm")
            else:
                player_expl = explosion(hit.rect.center, "lg")

            all_sprites.add(player_expl)
            if player.shield <= 2:
                player.hide()
                player.lives -= 1
                player.shield = 100

        # checking if player bullet hit boss
        hits = pygame.sprite.spritecollide(boss_lvl, bullets, True)
        for hit in hits:
            random.choice(expl_sounds).play()
            boss_lvl.shield -= 20
            if boss_lvl.shield > 33:
                player_expl = explosion(hit.rect.center, "sm")
            else:
                player_expl = explosion(hit.rect.center, "lg")

            all_sprites.add(player_expl)
            if boss_lvl.shield < 0:
                run_game = show_end_screen(score, True)
                pygame.quit()

    # Checking if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, True)
    for hit in hits:
        player.shield -= 33
        if score < 19700:
            new_mob(score)
        random.choice(expl_sounds).play()
        if player.shield > 33:
            player_expl = explosion(hit.rect.center, "sm")
        else:
            player_expl = explosion(hit.rect.center, "lg")

        all_sprites.add(player_expl)
        if player.shield <= 0:
            player.hide()
            player.lives -= 1
            player.shield = 100

    # checking if  the player took a powerup: ** This is getting frustrating!!!
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == "shield":
            if not player.shield + 33 > 100:
                player.shield += 33
            else:
                player.shield = 100

            shield_sound.play()
        if hit.type == "gun":
            player.powerup()
            gun_sound.play()

    if player.lives == 0:
        run_game = show_end_screen(score, False)
        pygame.quit()
    # Draw
    score_string = "Score: " + str(score)
    health_string = "Health: " + str(player.shield) + "%"
    boss_health_string = "Health: " + str(boss_lvl.shield) + "%"

    screen.fill(BLACK)
    screen.blit(background, background_rect)

    all_sprites.draw(screen)
    draw_text(screen, score_string, 22, width/2, 13)

    current_shield = player.shield
    draw_shield_bar(5, 5, current_shield, False)

    # Drawing the boss's health bar
    if boss_start:
        draw_shield_bar(14, 20, boss_lvl.shield, True)
        draw_text(screen, boss_health_string, 15, 150, 20)

    draw_text(screen, "LIVES: ", 18, width - 125, 10)
    draw_lives(screen, width - 100, 10, player.lives, mini_player)
    draw_text(screen, health_string, 15, 150, 2)
    # after drawing everything, flip
    pygame.display.flip()
pygame.quit()
