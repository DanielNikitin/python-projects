# ----Client----


import socket
import pygame


class Me:
    def __init__(self, data):
        data = data.split()
        self.r = int(data[0])
        self.color = data[1]

    def update(self, new_r):
        self.r = new_r

    def draw(self):
        if self.r != 0:  # если r не = 0, то
            pygame.draw.circle(screen, colors[self.color],
                               (WIDTH_WINDOW//2, HEIGHT_WINDOW/2), self.r)
            write_name(WIDTH_WINDOW//2, HEIGHT_WINDOW//2, self.r, p_name)


class Player:
    def __init__(self, conn):
        self.conn = conn


def find(s):
    otkr = None
    for i in range(len(s)):
        if s[i] == '<':
            otkr = i
        if s[i] == '>':
            zakr = i
            res = s[otkr+1:zakr]
            return res
    return ''


def write_name(x, y, r, name):
    font = pygame.font.Font(None, r)
    text = font.render(name, True, (0, 0, 0))
    rect = text.get_rect(center=(x, y))
    screen.blit(text, rect)


def draw_opponents(data):  # получаем данные об игроке от сервера
    for i in range(len(data)):
        j = data[i].split(' ')

        x = WIDTH_WINDOW//2+int(j[0])
        y = HEIGHT_WINDOW//2+int(j[1])
        r = int(j[2])
        c = colors[j[3]]
        pygame.draw.circle(screen, c, (x, y), r)

        if len(j) == 5:
            write_name(x, y, r, j[4])  # пишем ник в зависимости от размера игрока


class Grid:
    def __init__(self, screen):
        self.screen = screen
        self.x = 500
        self.y = 500
        self.start_size = 200
        self.size = self.start_size

    def update(self, r_x, r_y, L):
        self.size = self.start_size//L
        self.x = -self.size + (-r_x) % (self.size)
        self.y = -self.size + (-r_y) % (self.size)


    def draw(self):
        for i in range(WIDTH_WINDOW//self.size+2):
            pygame.draw.line(self.screen, GRID_THEME,
                             [self.x + i*self.size, 0],  # координаты верхнего конца отрезка
                             [self.x + i*self.size, HEIGHT_WINDOW],  # координаты нижнего конца отрезка
                             1)
        for i in range(HEIGHT_WINDOW//self.size+2):
            pygame.draw.line(self.screen, GRID_THEME,
                             [0, self.y + i*self.size],
                             [WIDTH_WINDOW, self.y + i*self.size],
                             1)

# Настройки окна
WIDTH_WINDOW, HEIGHT_WINDOW = 1000, 800

p_name = input("Name: ")
GRID_THEME = (150, 150, 150)

# Создание окна игры
pygame.init()  # активация pygame
screen = pygame.display.set_mode((WIDTH_WINDOW, HEIGHT_WINDOW))
# создаем окно и помещаем переменную screen, задаем размеры
pygame.display.set_caption('fastDik prodaction')
print('Окно создано')

# Подключение к серверу
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
sock.connect(('localhost', 10000))
print('Присоединился к серверу')

# Отправляем серверу свой Ник и Размеры окна
sock.send(('.'+p_name+' '+str(WIDTH_WINDOW)+' '+str(HEIGHT_WINDOW)+'.').encode())

# Получаем от сервера свой Размер и Цвет
data = sock.recv(64).decode()

# Подтверждаем получение
sock.send('!'.encode())

me = Me(data)
player = Player(sock)
grid = Grid(screen)

v = (0, 0)  # изначальная позиция нового вектора, idle состояние
old_v = (0, 0)  # изначальная позиция старого вектора, idle состояние
running = True  # булевая для цикла while

colors = {'0': (255, 255, 0),
          '1': (255, 0, 0),
          '2': (0, 255, 0),
          '3': (0, 255, 255),
          '4': (128, 0, 128)}

while running:
    # обработка событий, что происходит в окне
    for event in pygame.event.get():  # показывает список произошедших действий (при помощи цикла for)
        if event.type == pygame.QUIT:
            running = False
    # считаем координаты положения мыши
    if pygame.mouse.get_focused():  # находится ли курсор мыши на окошке игры
        pos = pygame.mouse.get_pos()  # получаем координаты мыши и записываем их в переменную pos
        v = (pos[0]-WIDTH_WINDOW//2, pos[1]-HEIGHT_WINDOW//2)  # считываем Вектор желаемого направления движения

    #  ЕСЛИ НЕ ДВИГАЕМСЯ
  #  if (v[0])**2+(v[1])**2 <= me.r**2:  # (**2 - квадрат), расчет по теореме пифагора -> если кусор на бактерии
     #   v = (0, 0)  # то не двигаемся

    # -- отправляем закодированный вектор направления движения, если он поменялся
    if v != old_v:  # если новый вектор не совпадает со старым ( != не равно)
        old_v = v  # то счИтаем Новый вектор -> старым, чтобы обновлять с кем сравнивать
        message = '<'+str(v[0])+','+str(v[1])+'>'  # переменная которая пакует координаты в скобки
        sock.send(message.encode())  # encode - кодирование

    # получаем от сервера новое состояние
    try:
        data = sock.recv(2**20)  # получаем данные с сервера (recv 1024 обмен данными, 1024 макс. байты за 1 раз)
    except:
        running = False
        continue
    data = data.decode()
    data = find(data)
    data = data.split(',')

    # обработка сообщений с сервера
    if data != ['']:
        parameters = list(map(int, data[0].split(' ')))
        me.update(parameters[0])
        grid.update(parameters[1], parameters[2], parameters[3])
        screen.fill('gray25')  # 25 оттенок серого цвета задний фон
        grid.draw()
        draw_opponents(data[1:])
        me.draw()

    pygame.display.update()  # обновляем окно
pygame.quit()  # закрываем окно
print('Окно закрыто')