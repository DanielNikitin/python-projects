import pygame
import random

def respawn_target():  # спавн обьекта в рандом точке экрана
    target_rect.x = random.randint(0, W - target_rect.w)  # target_rect прямоугольная область цели
    target_rect.y = random.randint(0, H - target_rect.h)  # ширина экрана - ширина персонажа

pygame.init()
pygame.font.init()

W = 350
H = 600
SCREEN_SIZE = (W, H)
SCREEN_CENTER = (W // 2, H // 2)
SCREEN_TOP = (W // 2, 0)

screen = pygame.display.set_mode(SCREEN_SIZE)

FPS = 60
clock = pygame.time.Clock()

ARIAL_FONT_PATH = pygame.font.match_font('arial')
ARIAL_46 = pygame.font.Font(ARIAL_FONT_PATH, 46)  # score
ARIAL_36 = pygame.font.Font(ARIAL_FONT_PATH, 36)  # other

INIT_DELAY = 2000  # начальная задержка (2с)
finish_delay = INIT_DELAY  # окончание игры
DECREASE_BASE = 1.002  # на сколько быстро уменьшаем время
last_respawn_time = 0  # переменная которая запоминает последний клик по обьекту

game_over = False
# шрифт.рендер(текст, сглаживание, цвет)
RETRY_SURFACE = ARIAL_36.render('PRESS ANY KEY', True, (0, 0, 0))
RETRY_RECT = RETRY_SURFACE.get_rect()  # прямоугольная поверхность игры
RETRY_RECT.midtop = SCREEN_CENTER

score = 0

TARGET_IMAGE = pygame.image.load('123.jpg')  # грузим картинку
TARGET_IMAGE = pygame.transform.scale(TARGET_IMAGE, (80, 120))  # (W, H)
target_rect = TARGET_IMAGE.get_rect()  # get_rect получаем прямоугольную поверхность
                                        # для проверки на ту облость-ли мы нажали

respawn_target()  # запускаем спавнер персонажа

running = True
while running:
    clock.tick(FPS)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:  # а так же проверим нажатие кнопки
            if game_over:
                score = 0
                finish_delay = INIT_DELAY
                game_over = False
                last_respawn_time = pygame.time.get_ticks()  # вернем обратно время после перезапуска игры
        elif e.type == pygame.MOUSEBUTTONDOWN:  # а так же проверим нажатие кнопки мыши
            if e.button == pygame.BUTTON_LEFT:
                # если игра не закончена и в область прямоугольника попала координата мышки
                if not game_over and target_rect.collidepoint(e.pos):  # e.pos позиция мышки
                    score += 1
                    respawn_target()
                    last_respawn_time = pygame.time.get_ticks()  #
                    finish_delay = INIT_DELAY / (DECREASE_BASE ** score)  # уменьшаем задержку респавна

    screen.fill((255, 208, 202))
    # локальная переменная score_surface (Поверхность с очками)
    score_surface = ARIAL_46.render(str(score), True, (0, 0, 0))
    score_rect = score_surface.get_rect()  # рисуем очки на поверхности прямоугольника score_surface.get_rect

    now = pygame.time.get_ticks()  # время игры на данный момент
    # рассчёт времени между респавном обьекта (elapsed прошедшее)
    elapsed = now - last_respawn_time
    if elapsed > finish_delay:
        game_over = True

        score_rect.midbottom = SCREEN_CENTER  # Положение очков смещаем в центр
        screen.blit(RETRY_SURFACE, RETRY_RECT)  # Рисуем надпись Retry
    else:  # иначе (если мы не проиграли)
        h = H - H * elapsed / finish_delay  # h - формула расчета прямоугольника времени
        # прямоугольник для уменьшения времени 'h'
        time_rect = pygame.Rect((0, 0), (W, h))  # (позиция), (размер)
        time_rect.bottomleft = (0, H)  # перемещаем прямоугольник вниз экрана
        pygame.draw.rect(screen, (232, 255, 208), time_rect)  # рисуем прямоугольник (где, цвет, обьект)

        screen.blit(TARGET_IMAGE, target_rect)  # рисуем (кого? где?)
        score_rect.midtop = SCREEN_TOP  # рисуем очки центр верх у прямоугольника и = верхняя точка экрана

    screen.blit(score_surface, score_rect)  # рисуем очки и до и после смерти

    pygame.display.flip()
pygame.quit()