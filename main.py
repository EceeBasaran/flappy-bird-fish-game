import pygame
import sys
import random

# Pygame başla
pygame.init()

pygame.mixer.music.load('assets/Fun Adventure.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.6)

game_over_sound = pygame.mixer.Sound('assets/game_over_bad_chest.wav')
game_over_sound.set_volume(0.4)

flap_sound = pygame.mixer.Sound('assets/sd_0.wav')
flap_sound.set_volume(0.6)

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

# Arka plan
background = pygame.image.load('assets/tree.png')
background = pygame.transform.scale(background, (screen_width, screen_height))
bg_x1 = 0
bg_x2 = screen_width
bg_speed = 2

# Sualtı tema görselleri
underwater_bg = pygame.transform.scale(pygame.image.load('assets/sea_background.png'), (screen_width, screen_height))
underwater_image = pygame.transform.scale(pygame.image.load('assets/purple_fish.png'), (50, 35))

# Font
font = pygame.font.Font(None, 40)

# Skor
score = 0
pass_pipe = False

# Tema durumu
current_theme = 'normal'
next_theme_score = 50  # ilk değişim 50'de olacak

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Kuş
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
        self.single_image_mode = False  # sualtı temasında True olacak

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
                flap_sound.play()

            if keys[pygame.K_SPACE] and not self.clicked:
                self.clicked = True
                self.vel = -10
                flap_sound.play()

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
            self.vel = 0
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
            if not game_over:
                game_over = True
                game_over_sound.play()
                self.hit_counter = 0
                self.hit_index = 0

# Borular
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        super().__init__()
        self.image = pygame.image.load('assets/pipe_alt.png')
        self.image = pygame.transform.scale(self.image, (40, 320))
        self.rect = self.image.get_rect()
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - pipe_gap // 2]
        else:
            self.rect.topleft = [x, y + pipe_gap // 2]

    def update(self):
        self.rect.x -= bg_speed
        if self.rect.right < 0:
            self.kill()

# Gruplar
bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, screen_height // 2)
bird_group.add(flappy)

# Oyun değişkenleri
pipe_gap = 180
pipe_frequency = 1500
last_pipe = pygame.time.get_ticks() - pipe_frequency
flying = False
game_over = False

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

# Game Over butonu
button = Button(screen_width // 2 - 50, screen_height // 2 - 25, button_img)

# Skor sıfırlama işlevi
def reset_game():
    global score
    global current_theme, next_theme_score, background
    score = 0
    current_theme = 'normal'
    next_theme_score = 50
    background = pygame.transform.scale(pygame.image.load('assets/tree.png'), (screen_width, screen_height))
    bird_group.empty()
    flappy = Bird(100, screen_height // 2)
    bird_group.add(flappy)
    pipe_group.empty()
    return flappy

# Ana döngü
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
            # Sualtı temasına geç
            background = underwater_bg
            flappy.images = [underwater_image]  
            flappy.hit_images = [underwater_image]
            flappy.single_image_mode = True
            current_theme = 'underwater'
        else:
            # Normal temaya dön
            background = pygame.transform.scale(pygame.image.load('assets/tree.png'), (screen_width, screen_height))
            flappy.images = [
                pygame.transform.scale(pygame.image.load('assets/flying1.png'), (50, 35)),
                pygame.transform.scale(pygame.image.load('assets/flying2.png'), (50, 35))
            ]
            flappy.hit_images = [
                pygame.transform.scale(pygame.image.load('assets/hit1.png'), (50, 35)),
                pygame.transform.scale(pygame.image.load('assets/hit2.png'), (50, 35))
            ]
            flappy.single_image_mode = False
            current_theme = 'normal'
        next_theme_score += 50

    # Arka planı çiz
    screen.blit(background, (bg_x1, 0))
    screen.blit(background, (bg_x2, 0))
    bird_group.draw(screen)
    bird_group.update()
    pipe_group.draw(screen)

    # Skor güncelleme (boru ortasına bakalım)
    if flying and not game_over:
        for pipe in pipe_group:
            if flappy.rect.centerx > pipe.rect.centerx - 5 and flappy.rect.centerx < pipe.rect.centerx + 5:
                if not pass_pipe:
                    score += 10
                    pass_pipe = True
            if flappy.rect.centerx > pipe.rect.centerx + 5:
                pass_pipe = False

    draw_text(str(score), font, BLACK, screen_width // 2 - 10, 20)

    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False):
        if not game_over:
            game_over = True
            game_over_sound.play()

    if flying and not game_over:
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe(screen_width, screen_height // 2 + pipe_height, -1)
            top_pipe = Pipe(screen_width, screen_height // 2 + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now
        pipe_group.update()

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