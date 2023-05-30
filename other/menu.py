import pygame as pg

size = (800, 600)

screen = pg.display.set_mode(size)

pg.font.init()

ARIAL_50 = pg.font.SysFont("Arial", 25)

class Menu:
    def __init__(self):
        self._option_surfaces = []  # список пунктов меню
        self._callback = []  # функции которые активируют пункты меню
        self._current_option_index = 0  # текущий индекс (опция)

    def append_option(self, option, callback):  # добавить опцию в меню
           self._option_surfaces.append(ARIAL_50.render(option, True, (255, 255, 255)))  # сглаживание текста
           self._callback.append(callback)

    def switch(self, direction):  # Переключает с одной опции на другую
           self._current_option_index = max(0, min(self._current_option_index + direction, len(self._option_surfaces) - 1))  # проверка на направление

    def select(self):  # Вызываем выбранный callback (опцию)
           self._callback[self._current_option_index]()  # выбираем callback по индексу

    def draw(self, surf, x, y, option_y_padding):  # draw - отрисовка, padding отступы между
           for i, option in enumerate(self._option_surfaces):  # enumerate возвращает обьект с индексом и элементом массива
               option_rect = option.get_rect()  # прямоугольная область
               option_rect.topleft = (x, y + i * option_y_padding)  # для каждого индекса будет свой отступ и своя позиция
               if i == self._current_option_index:  # если наш индекс равен выбранному индексу то текущая опция выбрана
                   pg.draw.rect(surf, (0, 100, 0), option_rect)  # рисуем на ее месте прямоугольную поверхность
               surf.blit(option, option_rect)  # рисуем текст (option) и место (option_rect)

menu = Menu()
menu.append_option('Hello World', lambda: print('Hello'))
menu.append_option('Quit', quit)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_w:
                menu.switch(-1)
            elif event.key == pg.K_s:
                menu.switch(1)
            elif event.key == pg.K_SPACE:
                menu.select()

    screen.fill("Black")

    menu.draw(screen, 100, 100, 75)

    pg.display.flip()
quit()
