import pygame

def render_hud(screen, player, extra_data):
    width = 10
    height = 10

    # Отображаем информацию в верхнем левом углу
    render_info(screen, extra_data, width, height)

    # Отображаем HP в правом нижнем углу
    render_hp(screen, player, width, height)

def render_info(screen, extra_data, width, height):
    font = pygame.font.SysFont('calibri', 20)
    info_text = font.render(f"{extra_data['message']}", True, (255, 255, 255))

    # Рисуем текст без рамки
    screen.blit(info_text, (width, height))

def render_hp(screen, player, width, height):
    font_hp = pygame.font.SysFont('calibri', 20)
    hp_text = font_hp.render(f"HP: {player.hp}", True, (255, 255, 255))

    # Создаем поверхность для рамки с прозрачностью
    hp_background = pygame.Surface((hp_text.get_width() + 50, hp_text.get_height() + 10), pygame.SRCALPHA)
    hp_background.fill((0, 0, 0, 50))  # черный с прозрачностью 50%

    # Рисуем текст на поверхности
    hp_background.blit(hp_text, (5, 5))

    # Получаем прямоугольник с координатами для отображения
    hp_text_rect = hp_background.get_rect(bottomright=(width + 490, height + 490))  # Устанавливаем правый нижний угол относительно экрана

    # Отображаем рамку с HP
    screen.blit(hp_background, hp_text_rect)
