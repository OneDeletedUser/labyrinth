import pygame

pygame.init()

# Размеры экрана
WIDTH = 700
HEIGHT = 500
# Цвета
GREEN = (155, 200, 50)
BLACK = (0,0,0)

# Окно
window = pygame.display.set_mode((WIDTH, HEIGHT))
# Загрузка фона
BG = pygame.image.load('background.jpg')
# Масштабирование изображения фона
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))

# Игровые часы
clock = pygame.time.Clock()

class Sprite(pygame.sprite.Sprite):
    def init(self, image, x, y):
        super().init()
        # Загрузка и масштабирование изображения
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (55, 55))
        # Получение хитбокса
        self.rect = self.image.get_rect()
        # Указание координат
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(Sprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= 3
        if keys[pygame.K_d]:
            self.rect.x += 3
        if keys[pygame.K_w]:
            self.rect.y -= 3
        if keys[pygame.K_s]:
            self.rect.y += 3

class Enemy(Sprite):
    def update(self):
        self.rect.x += self.dx
        if self.rect.x <= 470 or self.rect.x >= 620:
            self.dx = -self.dx

class Wall(pygame.sprite.Sprite):
    def init(self, x, y, width, height):
        super().init()
        # Создание поверхности
        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)
        # Хитбокс стены
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Стены
walls = pygame.sprite.Group()
walls.add(Wall(100, 20, 450, 10))
walls.add(Wall(100, 480, 350, 10))
walls.add(Wall(100, 20, 10, 380))
walls.add(Wall(200, 130, 10, 350))
walls.add(Wall(450, 130, 10, 360))
walls.add(Wall(300, 20, 10, 350))
walls.add(Wall(390, 120, 130, 10))

player = Player('hero.png', 5, 100)
bot = Enemy('cyborg.png', 600, 280)
bot.dx = 3
goal = Sprite('tresure.png', 580, 420)

# Перезапуск игры
def restart():
    global paused, final
    player.rect.x = 5
    player.rect.y = 100
    paused = False
    final = False

pygame.mixer.music.load('jungles.ogg')
pygame.mixer.music.play()
kick = pygame.mixer.Sound('kick.ogg')

my_font = pygame.font.SysFont('verdana', 70)
text_pause = my_font.render('PAUSE', True, )
text_win = my_font.render('WIN', True, )
text_lose = my_font.render('GAME OVER', True, )
my_font = pygame.font.SysFont('verdana', 35)
text_restart = my_font.render('Press SPACE to restart', True, BLACK)
text_continue = my_font.render('Press SPACE to continue', True, BLACK)

text_fin = None
# Управление игровым циклом
run = True
paused = False
final = False

# Игровой цикл
while run:
    # Перебор событий
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE and paused and final:
                restart()
            if e.key == pygame.K_SPACE and not final:
                paused = not paused

    # Проверка паузы
    if not paused:  
        # Отрисовка фона
        window.blit(BG, (0, 0))

        # Обновление спрайтов
        player.update()
        bot.update()

        # Отрисовка спрайтов
        player.draw()
        bot.draw()
        goal.draw()
        walls.draw(window)

        # Проверка коллизии игрока и стен
        if pygame.sprite.spritecollideany(player, walls) or pygame.sprite.collide_rect(player, bot):
            paused = True
            final = True
            text_fin = text_lose
            kick.play()

        if pygame.sprite.collide_rect(player, goal):
            pause = True
            final = True
            text_fin = text_win

    elif paused and final:
        window.blit(GREEN)
        window.blit(text_fin, (150, 200))
        window.blit(text_restart, (160, 290))

    elif paused and not final:
        window.blit(GREEN)
        window.blit(text_pause, (150, 200))
        window.blit(text_continue, (160, 290))

    # Обновление состояния игры
    pygame.display.update()
    # Установка тикрейта
    clock.tick(60)