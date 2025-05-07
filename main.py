import pygame
import sys
import random

#Pygame başlat
pygame.init()

pygame.mixer.music.load('assets/Fun Adventure.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.6)

game_over_sound = pygame.mixer.Sound('assets/game_over_bad_chest.wav')
game_over_sound.set_volume(0.4)

flap_sound = pygame.mixer.Sound('assets/sd_0.wav')
flap_sound.set_volume(0.6)

bubble_sound = pygame.mixer.Sound('assets/bubbles-single2.wav')
bubble_sound.set_volume(0.6)

# Ekran boyutları
screen_width = 600
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Saat
clock = pygame.time.Clock()
fps = 60

# Arka planlar
normal_bg = pygame.image.load('assets/tree.png')
normal_bg = pygame.transform.scale(normal_bg, (screen_width, screen_height))
underwater_bg = pygame.transform.scale(pygame.image.load('assets/sea_background.png'), (screen_width, screen_height))

bg_x1 = 0
bg_x2 = screen_width
bg_speed = 2

# Temaya özel görseller
underwater_image = pygame.transform.scale(pygame.image.load('assets/purple_fish.png'), (50, 35))
swordish_image = pygame.transform.scale(pygame.image.load('assets/Swordfish.png'), (90, 45))  # daha büyük

# Font
font = pygame.font.Font(None, 40)

# Skor
score = 0

# Tema durumu
current_theme = 'normal'
next_theme_score = 50
background = normal_bg

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Kuş sınıfı
class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = [
            pygame.transform.scale(pygame.image.load('assets/flying1.png'), (50, 35)),
            pygame.transform.scale(pygame.image.load('assets/flying2.png'), (50, 35))
        ]
        self.hit_images = [
            pygame.transform.scale(pygame.image.load('assets/hit1.png'), (50, 35)),
            pygame.transform.scale(pygame.image.load('assets/hit2.png'), (50, 35))
        ]
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False
        self.counter = 0
        self.hit_counter = 0
        self.hit_index = 0
        self.single_image_mode = False

    def update(self):
        global game_over

        if flying:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            self.rect.y += int(self.vel)

        if not game_over:
            keys = pygame.key.get_pressed()
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
              self.clicked = True
              self.vel = -10
              sound_to_play = flap_sound if current_theme == 'normal' else bubble_sound
              sound_to_play.play()

            if keys[pygame.K_SPACE] and not self.clicked:
              self.clicked = True
              self.vel = -10
              sound_to_play = flap_sound if current_theme == 'normal' else bubble_sound
              sound_to_play.play()

            if not pygame.mouse.get_pressed()[0] and not keys[pygame.K_SPACE]:
                self.clicked = False

            if not self.single_image_mode:
                self.counter += 1
                if self.counter > 10:
                    self.counter = 0
                    self.index = (self.index + 1) % len(self.images)
                self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
            else:
                self.image = pygame.transform.rotate(self.images[0], self.vel * -2)
        else:
            if not self.single_image_mode:
                self.hit_counter += 1
                if self.hit_counter > 5:
                    self.hit_counter = 0
                    self.hit_index = (self.hit_index + 1) % len(self.hit_images)
                self.image = self.hit_images[self.hit_index]
            else:
                self.image = self.images[0]
            self.rect.y += 2

        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
            if not game_over:
                game_over = True
                game_over_sound.play()
                self.hit_counter = 0
                self.hit_index = 0

# Boru sınıfı
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position, is_scoring_pipe=False):
        super().__init__()
        self.image = pygame.image.load('assets/pipe_alt.png')
        self.image = pygame.transform.scale(self.image, (40, 320))
        self.rect = self.image.get_rect()
        self.is_scoring_pipe = is_scoring_pipe
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - pipe_gap // 2]
        else:
            self.rect.topleft = [x, y + pipe_gap // 2]
        self.scored = False

    def update(self):
        self.rect.x -= bg_speed
        if self.rect.right < 0:
            self.kill()

# Swordfish sınıfı
class EnemyFish(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = swordish_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.scored = False

    def update(self):
        self.rect.x -= 5  
        if self.rect.right < 0:
            self.kill()

# Gruplar
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()
enemy_fish_group = pygame.sprite.Group()

flappy = Bird(100, screen_height // 2)
bird_group.add(flappy)

# Oyun değişkenleri
pipe_gap = 180
pipe_frequency = 1500
last_pipe = pygame.time.get_ticks() - pipe_frequency
flying = False
game_over = False
enemy_spawn_frequency = 1000  
last_enemy = pygame.time.get_ticks() - enemy_spawn_frequency

# Butonlar
button_img = pygame.image.load('assets/restart.png')
button_img = pygame.transform.scale(button_img, (100, 50))

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action

button = Button(screen_width // 2 - 50, screen_height // 2 - 25, button_img)

def reset_game():
    global score, current_theme, next_theme_score, background, flappy
    score = 0
    current_theme = 'normal'
    next_theme_score = 50
    background = normal_bg
    bird_group.empty()
    flappy = Bird(100, screen_height // 2)
    bird_group.add(flappy)
    pipe_group.empty()
    enemy_fish_group.empty()
    return flappy

while True:
    clock.tick(fps)
    # Arka plan kaydır
    bg_x1 -= bg_speed
    bg_x2 -= bg_speed
    if bg_x1 <= -screen_width:
        bg_x1 = screen_width
    if bg_x2 <= -screen_width:
        bg_x2 = screen_width
    # Tema kontrolü
    if score >= next_theme_score:
        if current_theme == 'normal':
            background = underwater_bg
            flappy.images = [underwater_image]
            flappy.hit_images = [underwater_image]
            flappy.single_image_mode = True
            pipe_group.empty()
            current_theme = 'underwater'
        else:
            background = normal_bg
            flappy.images = [
                pygame.transform.scale(pygame.image.load('assets/flying1.png'), (50, 35)),
                pygame.transform.scale(pygame.image.load('assets/flying2.png'), (50, 35))
            ]
            flappy.hit_images = [
                pygame.transform.scale(pygame.image.load('assets/hit1.png'), (50, 35)),
                pygame.transform.scale(pygame.image.load('assets/hit2.png'), (50, 35))
            ]
            flappy.single_image_mode = False
            enemy_fish_group.empty()
            current_theme = 'normal'
        next_theme_score += 50

    # Arka plan çiz
    screen.blit(background, (bg_x1, 0))
    screen.blit(background, (bg_x2, 0))

    bird_group.update()
    
    # Swordfish üretimi sadece underwater modda
    if flying and not game_over:
        if current_theme == 'underwater':
            time_now = pygame.time.get_ticks()
            if time_now - last_enemy > enemy_spawn_frequency:
                enemy_y = random.randint(100, screen_height - 100)
                enemy_fish = EnemyFish(screen_width, enemy_y)
                enemy_fish_group.add(enemy_fish)
                last_enemy = time_now
            enemy_fish_group.update()
        
        # Boru üretimi sadece normal modda
        if current_theme == 'normal':
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > pipe_frequency:
                pipe_height = random.randint(-100, 100)
                btm_pipe = Pipe(screen_width, screen_height // 2 + pipe_height, -1, is_scoring_pipe=True)
                top_pipe = Pipe(screen_width, screen_height // 2 + pipe_height, 1)
                pipe_group.add(btm_pipe)
                pipe_group.add(top_pipe)
                last_pipe = time_now
            pipe_group.update()
    # Çarpışmalar
    bird_hit_pipe = pygame.sprite.groupcollide(bird_group, pipe_group, False, False)
    bird_hit_fish = pygame.sprite.groupcollide(bird_group, enemy_fish_group, False, False)
    if (bird_hit_pipe or bird_hit_fish) and not game_over:
        game_over = True
        game_over_sound.play()
    # Skor güncelle
    if flying and not game_over:
        for pipe in pipe_group:
            if pipe.is_scoring_pipe and flappy.rect.centerx > pipe.rect.centerx and not pipe.scored:
                score += 10
                pipe.scored = True
        for fish in enemy_fish_group:
            if flappy.rect.centerx > fish.rect.centerx and not fish.scored:
                score += 10
                fish.scored = True
   # Çizimler
    pipe_group.draw(screen)
    enemy_fish_group.draw(screen)
    bird_group.draw(screen)
    draw_text(str(score), font, BLACK, screen_width // 2 - 10, 20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and not flying and not game_over:
            if event.key == pygame.K_SPACE:
                flying = True
        if event.type == pygame.MOUSEBUTTONDOWN and not flying and not game_over:
            flying = True

    if game_over:
        if button.draw():
            game_over = False
            flappy = reset_game()

    pygame.display.update()