import pygame as pg

pg.init()
screen = pg.display.set_mode((600, 300))  # flags = pg.NOFRAME
pg.display.set_caption("fastDick the Game")
icon = pg.image.load('images/icon.png')
pg.display.set_icon(icon)


main_font = pg.font.Font('fonts/PTSansNarrow-Bold.ttf', 40)
text_surface = main_font.render('fastDick', True, 'Red')

player_icon = pg.image.load('images/icon.png')
background = pg.image.load('images/background.jpg')

running = True
while running:

    screen.blit(player_icon, (100, 50))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            pg.quit()

    pg.display.update()
