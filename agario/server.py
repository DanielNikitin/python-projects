# ----Server----


import socket
import pygame
import random
import math

# Настройки сервера
work_on_server = False
server_ip = 'localhost'
FPS = 100  # server speed
WIDHT_ROOM, HEIGHT_ROOM = 4000, 4000  # Размер мира
WIDHT_SERVER_WINDOW, HEIGHT_SERVER_ROOM = 300, 300  # серверное окно

START_PLAYER_SIZE = 50  # пикселей
FOOD_SIZE = 10
MOBS_QUANTITY = 25
FOOD_QUANTITY = (WIDHT_ROOM*HEIGHT_ROOM) // 80000

print('****SERVER STARTED****')
print('START_PLAYER_SIZE ', START_PLAYER_SIZE,
      '\nFOOD_SIZE ', FOOD_SIZE,
      '\nFPS ', FPS,
      '\nWIDHT_ROOM ', WIDHT_ROOM,
      '\nHEIGHT_ROOM ', HEIGHT_ROOM,
      '\nMOBS_QUANTITY ', MOBS_QUANTITY,
      '\n FOOD_QUANTITY ', FOOD_QUANTITY)

colors = {'0': (255, 255, 0),  # кортедж цветов для персонажей в зашифрованном виде
          '1': (255, 0, 0),
          '2': (0, 255, 0),
          '3': (0, 255, 255),
          '4': (128, 0, 128)}


def new_r(r, R):  # вычисляем новый радиус
    return math.sqrt(R**2 + r**2)  # формула Пифагора


def find(s):
    # поиск координат направления вектора из декодированных
    # данных которые мы получаем изначально в строковом формате
    otkr = None  # Открывающаяся скобка еще не обнаружена
    for i in range(len(s)):  # последовательно перебираем символы (i) в строке (s)
        if s[i] == '<':  # если встречаем символ '<'
            otkr = i  # то запоминаем его позицию в переменную otkr
        if s[i] == '>' and otkr is not None:  # если встречаем символ '>', то проверяем
            # нашли-ли мы ранее '<' используя 'otkr is not None
            zakr = i  # если была, то запоминаем '>' в переменную zakr
            res = s[otkr+1:zakr]  # извлекаем значения в строке между скобками и записываем их в 'res'
            res.split(',')  # разбиваем строку 'res' на список 'split('')
            # сохраняем результат в 'res' в виде списка строк
            res = list(map(int, res.split(',')))  # каждый элемент списка преобразуем в целое число
            # с помощью функции 'int и map'
            return res  # возвращаем результат как список целых чисел
    return ''  # если ничего не найдено, то возвращаем пустую строку


class Food:
    def __init__(self, x, y, r, color):
        self.x = x
        self.y = y
        self.r = r
        self.color = color


class Player:  # класс игрок (в скобках указывают наследствие)
    def __init__(self, conn, addr, x, y, r, color):
        # создаем игрока и его МЕШОК данных об персонаже, АТТРИБУТЫ
        self.conn = conn
        self.addr = addr
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.L = 1
        self.score = 0

        self.name = 'Bot'
        self.width_window = 1000
        self.height_window = 800
        self.w_vision = 1000  # ширина видимости
        self.h_vision = 800  # высота видимости

        self.errors = 0  # кол-во сетевых ошибок игрока
        self.dead = 0
        self.ready = False

        self.abs_speed = 30/(self.r**0.5)
        self.speed_x = 0  # скорость по х
        self.speed_y = 0  # скорость по у

    def set_options(self, data):
        data = data[1:-1].split(' ')
        self.name = data[0]
        self.width_window = int(data[1])
        self.height_window = int(data[2])
        self.w_vision = int(data[1])
        self.h_vision = int(data[2])

        print(self.name, 'Присоединился к серверу')

    def change_speed(self, v):  # меняем скорость у себя
        if (v[0] == 0) and (v[1] == 0):  # если вектор по х - 0 и у - 0
            self.speed_x = 0  # то состовляющая по X - 0 (скорость)
            self.speed_y = 0  # то и по - Y то же самое
        else:  # но, если
            lenv = (v[0]**2+v[1]**2)**0.5
            # lenv найдем длинну вектора
            #  по теореме Пифагора, первую состовляющую вектора возвести в квадрат
            # v[0]**2 прибавить вторую состовляющую вектора в квадрате
            # и все это возвести в корень, т.е. в степень 0.5 **0.5
            v = (v[0]/lenv, v[1]/lenv)
            # теперь теряем информацию о длинне вектора, но сохранить направление
            # т.е. Нормировать вектор
            # v[0]/lenv первая координата вектора делится на длинну вектора,
            # и вторую координату вектора поделить на длинну вектора v[1]/lenv
            v = (v[0]*self.abs_speed, v[1]*self.abs_speed)
            # оставляем направление, но изменяем скорость
            # умножаем первую координату вектора на абсолютную скорость
            # и вторую на абсолютную скорость ( перем. abs_speed)
            self.speed_x, self.speed_y = v[0], v[1]
            # изменим горизонтальную состовляющую скорость игрока
            # и вертикальную скорость

    def update(self):  # каждый раз когда обновляем состояние игрока
        # x координатный ограничитель комнаты
        if self.x-self.r <= 0:
            if self.speed_x >= 0:
                self.x += self.speed_x
        else:
            if self.x+self.r >= WIDHT_ROOM:
                if self.speed_x <= 0:
                    self.x += self.speed_x
            else:
                self.x += self.speed_x
        # y координатный ограничитель комнаты
        if self.y-self.r <= 0:
            if self.speed_y >= 0:
                self.y += self.speed_y
        else:
            if self.y+self.r >= HEIGHT_ROOM:
                if self.speed_y <= 0:
                    self.y += self.speed_y
            else:
                self.y += self.speed_y

        # abs speed (absolute)
        if self.r != 0:  #  если r не 0
            self.abs_speed = 30/(self.r**0.5)  # скорость высчитываем по формуле
        else:  # либо, если r = 0
            self.abs_speed = 0  # скорость = 0

        # r  # если радиус >= 100, то уменьшаем радиус видимости
        if self.r >= 10:
            self.r -= self.r/25000

        # L
        if (self.r >= self.w_vision/3) or (self.r >= self.h_vision/3):
            if (self.w_vision <= WIDHT_ROOM) or (self.h_vision <= HEIGHT_ROOM):
                self.L *= 2
                self.w_vision = self.width_window * self.L
                self.h_vision = self.height_window * self.L
        if (self.r < self.w_vision/8) and (self.r < self.h_vision/8):
            if self.L > 1:
                self.L = self.L//2
                self.w_vision = self.width_window * self.L
                self.h_vision = self.height_window * self.L

    def show_score(self, display):
        font = pygame.font.SysFont(None, 25)
        text = font.render("Score: "+str(int(self.score)), True, (255, 255, 255))
        display.blit(text, (0, 0))


# Создание сокета
main_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
main_socket.bind((server_ip, 10000))
main_socket.setblocking(False)
main_socket.listen(5)

# Создание графического окна сервера
pygame.init()  # запуск pygame
if not work_on_server:
    screen = pygame.display.set_mode((WIDHT_SERVER_WINDOW, HEIGHT_SERVER_ROOM))  # выводим экран
clock = pygame.time.Clock()  # частота верхней границы (напр. не быстрее 100 кадров в секунду)

# Создание еды
foods = [Food(random.randint(0, WIDHT_ROOM),  # создаем список food
             random.randint(0, HEIGHT_ROOM),  # задаем рандом координаты
             FOOD_SIZE,  # размер еды
             str(random.randint(0, 4)))  # цвет еды
        for i in range(FOOD_QUANTITY)  # и запускаем спавн еды через цикл
        ]

# Создание мобов
players = [Player(None, None,  # [ Создание списка ]
                  # None - управлением игроком, None - не принадлежит команде
                  random.randint(0, WIDHT_ROOM),
                  random.randint(0, HEIGHT_ROOM),
                  random.randint(10, 100),  # Радиус моба
                  str(random.randint(0, 4))  # Цвет моба
                  )
           for i in range(MOBS_QUANTITY)  # количество мобов на карте
           ]

# while создает и отдает/принимает пакеты (информацию) *ИГРОВОЙ ЦИКЛ*
server_works = True  # сервер работает
tick = -1
while server_works:
    clock.tick(FPS)
    tick += 1
    if tick == 200:
        tick = 0
        try:
            new_socket, addr = main_socket.accept()  # сокет - соединение с нашим игроком
            print('оуе щит мэн присоединился', addr)
            new_socket.setblocking(False)  # делаем не блокирующий сокет
            spawn = random.choice(foods)
            new_player = Player(new_socket, addr,
                                # создаем нового игрока после подключения (new_player), и вызываем конструктор класса Player
                                # перемещаем созданный обьект игрока в переменную New_Player, и храним данные об игроке
                                spawn.x,  # появление в рандом по ширине (X)
                                spawn.y,  # появление в рандом по высоте (Y)
                                START_PLAYER_SIZE,
                                str(random.randint(0, 4)))  # рандом выбор цвета через integer

            foods.remove(spawn)
            players.append(new_player)  # добавляем new_player в СПИСОК (players.append) всех игроков
        except:
            pass
        # дополняем список мобов (респавн)
        for i in range(MOBS_QUANTITY-len(players)):
            if len(foods) != 0:
                spawn = random.choice(foods)
                players.append(Player(None, None,  # append добавить в конец списка
                                      spawn.x,
                                      spawn.y,
                                      random.randint(10, 100),
                                      str(random.randint(0, 4))
                                      )
                               )
                foods.remove(spawn)

        # дополняем список еды (респавн)
        new_foods = [Food(random.randint(0, WIDHT_ROOM),
                          random.randint(0, HEIGHT_ROOM),
                          FOOD_SIZE,
                          str(random.randint(0,4)))
                     for i in range(FOOD_QUANTITY-len(foods))
                     ]
        foods = foods + new_foods

    # считываем команды всех игроков
    for player in players:  # для игрока (player) в списке игроков (players)
        if player.conn is not None:
            try:
                data = player.conn.recv(1024)  # обращаемся к подключению игрока (клиента) и считываем оттуда данные
                data = data.decode()  # декодируем
                if data[0] == '!': # пришло сообщение о готовности к диалогу
                    player.ready = True
                else:
                    if data[0] == '.' and data[-1] == '.': #пришло имя и размер окна
                        player.set_options(data)
                        player.conn.send((str(START_PLAYER_SIZE) +' '+player.color).encode())
                    else:  # пришел курсор
                        data = find(data)  # находим во строковой каше координаты курсора (вектор желаемого направления)
                        player.change_speed(data)  # и передаем его игроку в ФУНКЦИЮ изменить скорость
            except:
                pass
        else:
            if tick == 100:
                data = [random.randint(-100, 100), random.randint(-100, 100)]  # направление движения мобов
                player.change_speed(data)  # изменяем скорость мобов

        player.update()  # обновляем состояние всех игроков

    # определим, что видит каждый игрок
    visible_balls = [[] for i in range(len(players))]  # список видимых шаров

  # ------------- РЕПЛИКАЦИЯ И ВЗАИМОДЕЙСТВИЕ --------------

    for i in range(len(players)):
        # -------- ЕДА --------
        for f in range(len(foods)):  # итерация списка еды (последовательный перебор)
            # какую еду видит игрок
            dist_x = foods[f].x - players[i].x  # определяем дистанцию между player [i] и food [f]
            dist_y = foods[f].y - players[i].y

            # i видит f
            if (
                players[i].w_vision >= 0 and players[i].h_vision >= 0 and  # ширина и высота поля зрения положительные?
                f < len(foods) and  # кол-во f меньше кол-ва элементов в списке? чтобы не выйти за предел поиска
                abs(dist_x) <= players[i].w_vision//2+foods[f].r
                and  # не превышаем половину высоты и ширины поля зрения игрока плюс r еды
                abs(dist_y) <= players[i].h_vision//2+foods[f].r
            ):

                # i может сьесть f
                if (dist_x ** 2 + dist_y ** 2) ** 0.5 <= players[i].r:
                    players[i].r = new_r(players[i].r, foods[f].r)
                    foods[f].r = 0
                if (players[i].conn is not None) and (foods[f].r != 0):
                    # подготовим данные к добавлению в список ВИДИМОЙ ЕДЫ
                    x_ = str(round(dist_x/players[i].L))
                    y_ = str(round(dist_y/players[i].L))
                    r_ = str(round(foods[f].r/players[i].L))
                    c_ = foods[f].color

                    visible_balls[i].append(x_ + ' ' + y_ + ' ' + r_ + ' ' + c_)  # передаем данные видимого шара

        # -------- PLAYER i --------
        for j in range(i+1, len(players)):
            # рассматриваем пару i и j игрока
            dist_x = players[j].x-players[i].x  # дистанция по х
            dist_y = players[j].y-players[i].y  # дистанция по у

            # i видит j
            if (
                abs(dist_x) <= players[i].w_vision//2+players[j].r
                and
                abs(dist_y) <= players[i].h_vision//2+players[j].r
            ):
                # i может сьесть j
                if ((dist_x ** 2 + dist_y ** 2) ** 0.5 <= players[i].r and
                    players[i].r > 1.1*players[j].r):  # проверяем размер игрока [i]
                    players[i].r = new_r(players[i].r, players[j].r)  # изменяем радиус player[i]
                    # изменим радиус j игрока
                    players[j].r, players[j].speed_x, players[j].speed_y = 0,0,0  # удаляем все параметры сьеденого player[j]

                if players[i].conn is not None:
                # подготовим данные к добавлению в список видимых шаров
                    x_ = str(round(dist_x/players[i].L))
                    y_ = str(round(dist_y/players[i].L))
                    r_ = str(round(players[j].r/players[i].L))
                    c_ = players[j].color
                    n_ = players[j].name

                    if players[i].r >= 30*players[j].L:  # если [j].r >= 30, то не показываем ник
                        visible_balls[i].append(x_+' '+y_+' '+r_+' '+c_+' '+n_)
                    else:
                        visible_balls[i].append(x_+' '+y_+' '+r_+' '+c_)  # передаем данные видимого шара

        # -------- PLAYER j --------
        # j видит i
            if (
                abs(dist_x) <= players[j].w_vision//2+players[i].r
                and
                abs(dist_y) <= players[j].h_vision//2+players[i].r
            ):
            #  j может сьесть i
                if ((dist_x ** 2 + dist_y ** 2) ** 0.5 <= players[j].r and
                    players[j].r > 1.1 * players[i].r):  # проверяем размер игрока [j]
                    players[j].r = new_r(players[j].r, players[i].r)  # изменяем радиус player[j]
                    # изменим радиус j игрока
                    players[i].r, players[i].speed_x, players[i].speed_y = 0, 0, 0   # удаляем все параметры сьеденого player[i]

                if players[j].conn is not None:
                    # подготовим данные к добавлению в список видимых шаров
                    x_ = str(round(-dist_x/players[j].L))  # координата x в отображение
                    y_ = str(round(-dist_y/players[j].L))  # координата y в отображение
                    r_ = str(round(players[i].r/players[j].L))  # радиус в отображение
                    c_ = players[i].color  # цвет в отображение
                    n_ = players[i].name  # ник в отображение

                    if players[i].r >= 30 * players[j].L:  # если [i].r >= 30, то не показываем ник
                        visible_balls[j].append(x_ + ' ' + y_ + ' ' + r_ + ' ' + c_ + ' ' + n_)
                    else:
                        visible_balls[j].append(x_ + ' ' + y_ + ' ' + r_ + ' ' + c_)  # передаем данные видимого шара

    # формируем ответ каждому игроку
    otvets = ['' for i in range(len(players))]  # создаем список 'otvets' длинной кол-ва 'players'
    for i in range(len(players)):  # последовательно для каждого игрока в 'players'
        r_ = str(round(players[i].r/players[i].L))
        x_ = str(round(players[i].x/players[i].L))
        y_ = str(round(players[i].y/players[i].L))
        L_ = str(round(players[i].L))  # определяем по отдельности все данные (r, x, y, l)

        visible_balls[i] = [r_+' '+x_+' '+y_+' '+L_] + visible_balls[i]  # сохраняем все в список 'visible_balls'
        otvets[i] = '<'+(','.join(visible_balls[i]))+'>'  # формируем ответ в список 'otvets' через '<,>'

    # отправляем новое состояние игры на клиент
    for i in range(len(players)):  #
        if (players[i].conn is not None) and (players[i].ready):
            try:
                players[i].conn.send(otvets[i].encode())  # отправляем 'otvets' - новое состояние игры
                players[i].errors = 0  # если удалось, то обнуляем все ошибки
            except:  # если не удалось отправить игроку состояние игры
                players[i].errors += 1  # то добавляем ему свойство errors "+1"

    # чистим список от отключенных игроков
    for player in players:
        if player.r == 0:  # проверяем радиус игрока
            if player.conn is not None:  # если не отключился
                player.dead += 1  # добавляем в переменную dead '+1'
            else:  # до тех пор, пока
                player.dead += 10  # не наберем 300 смертей

        if (player.errors == 100): #or (player.dead == 300):  # если набралось 100 ошибок, или dead, то
            if player.conn is not None:  # если соединение не прервалось
                player.conn.close()  # закрываем ему сокет
            players.remove(player)  # удаляем игрока из списка

    # чистим список от еды которую сьели
    for d in foods:  # проверяем внутри списка foods - значения внутри переменной 'd'
        if d.r == 0: foods.remove(d)  # если еду сьели, то она изменит r (radius) на 0, и если это так, то remove

# -------- SERVER --------
    if not work_on_server:
        # Рисуем состояние комнаты в окне сервера
        screen.fill('BLACK')  # черный фон окна сервера
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                server_works = False
                print('Сервер выключен')

        for player in players:
            # вычисляем координаты где рисовать, размеры игроков и оптимизируем эти данные для маленького окна сервера
            x = round(player.x*WIDHT_SERVER_WINDOW/WIDHT_ROOM)
            y = round(player.y*HEIGHT_SERVER_ROOM/HEIGHT_ROOM)
            r = round(player.r*WIDHT_SERVER_WINDOW/WIDHT_ROOM)
            c = colors[player.color]

            pygame.draw.circle(screen, c, (x, y), r)  # рисуем на серверном окне - игрока
            # (где, цвет, координаты, радиус, ширина)
        pygame.display.update()

# закрываем сервер
pygame.quit()
# закрываем сокеты
main_socket.close()