import random
import time


class Config:
    def __init__(self):
        self.ai_ship_is_close_message = 1  # 1/0 - Булевая для print(f"Нельзя разместить корабль так близко друг к другу")
        self.ai_shoot_coordinate_message = 1   # 1/0 - Булевая для print(f"Стреляю в координаты:")
        self.ai_ship_place_coordinate_message = 1  # 1/0 - Булевая для print(f"{x, y, r}")
        self.is_position_free_message = 1  # 1/0 -


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pass


class Ship:
    def __init__(self, name, length, health, index):
        self.name = name
        self.length = length
        self.health = health
        self.index = index


class Player:
    def __init__(self, p_name):
        self.ship = Ship(None, None, None, None)
        self.p_name = p_name
                                # Имя, размер, жизни, индекс
        self.ships_count = [Ship("Boost", 3, 3, 1),
                            Ship("Chpoking", 2, 2, 2),
                            Ship("Fire", 2, 2, 3),
                            Ship("Meow", 1, 1, 4),
                            Ship("Кусь", 1, 1, 5),
                            Ship("Чики-бони", 1, 1, 6),
                            Ship("Boomer", 1, 1, 7)]

    def take_damage(self):
        if self.ship.health > 0:  # если жизней больше чем 0
            self.ship.health -= 1  # отнимаем по 1
            print(f"Корабль '{self.ship.name}' получил повреждение. Здоровье: {self.ship.health}")
        else:
            print(f"Корабль '{self.ship.name}' уже уничтожен.")

    def input_coordinates(self):
        while True:
            try:
                x = int(input("Введите координату X от 1 до 6: "))
                y = int(input("Введите координату Y от 1 до 6: "))
                r = int(input("Введите положение корабля 1 или 2: "))
                return x, y, r
            except ValueError:
                print("Неверный ввод. Пожалуйста, введите числовое значение")

    def input_shoot_coordinates(self):
        while True:
            try:
                x = int(input("Введите координату X от 1 до 6: "))
                y = int(input("Введите координату Y от 1 до 6: "))
                return x, y
            except ValueError:
                print("Неверный ввод. Пожалуйста, введите числовое значение")

    def get_ships_count(self):
        return len(self.ships_count)  # len - кол-во элементов в списке


class AIPlayer(Player):
    #  класс AIPlayer является подклассом
    #  (наследует от) класса Player.
    #  Это означает, что AIPlayer получит все свойства и методы,
    #  которые определены в классе Player
    def __init__(self, board_instance):
        # super вызывает родительский метод init, и передает все атрибуты от родителя
        super().__init__("Компик")  # 'компик' это никнейм атрибута 'p_name' у class Player
        self.board_instance = board_instance  # соединяемся с классом Board

    def ai_ship_coordinates(self, ship):
        while True:
            try:
                valid_coordinates = []
                for x in range(1, 6):
                    for y in range(1, 6):
                        for r in range(1, 2):
                            if self.ai_is_valid_placement(x, y, r, ship):
                                valid_coordinates.append((x, y, r))
                if valid_coordinates:
                    return random.choice(valid_coordinates)
            except Exception as e:
                print(f"ai_ship_coordinates: {e} ")

    def ai_is_valid_placement(self, x, y, r, ship):
        if r == 1:  # вертикальная ориентация
            if y + ship.length - 1 <= 6:
                for row in range(y, y + ship.length):
                    if not self.ai_is_position_free(x, row, ship.length, r):
                        return False
            else:
                return False
        elif r == 2:  # горизонтальная ориентация
            if x + ship.length - 1 <= 6:
                for col in range(x, x + ship.length):
                    if not self.ai_is_position_free(col, y, ship.length, r):
                        return False
            else:
                return False
        return True

    def ai_shoot_coordinates(self):
        while True:
            try:
                x = random.randint(1, 6)
                y = random.randint(1, 6)
                return x, y
            except Exception as e:
                print(f"ai_shoot_coord: {e}")
                return False

    def ai_is_position_free(self, x, y, ship_length, r):
        if r == 1:
            for row in range(max(0, y - 1), min(6, y + ship_length)):
                if self.board_instance.ai_board[row][x] in ('■', 'X'):
                    return False
        elif r == 2:
            for col in range(max(0, x - 1), min(6, x + ship_length)):
                if self.board_instance.ai_board[y - 1][col] in ('■', 'X'):
                    return False
        return True


class Board:
    def __init__(self, player):
        # создаем двумерный список, присваемваем функционал для атрибута
        # по принципу действия напоминает генератор (потому что итерируем при вызове)
        # player в init нужен для определения обращения игрок или ии
        self.player_board = [[" " for _ in range(7)] for _ in range(6)]
        self.ai_board = [[" " for _ in range(7)] for _ in range(6)]
        self.player = player
        self.aiplayer = AIPlayer(self) # Создание экземпляра класса AIPlayer
        self.config = Config()  # Создание экземпляра класса Config
        self.current_board_is_player = False # Булевая для установки True (доска игрока)
        self.current_board = self.get_current_board() # Устанавливаем текущую доску по умолчанию

    def switch_current_board(self):
        # Метод для переключения текущей доски между player_board и ai_board
        self.current_board_is_player = not self.current_board_is_player  # переключаем True/False

    def get_current_board(self):
        if self.current_board_is_player:
            print("player board")
            return self.player_board
        else:
            print("ai board")
            return self.ai_board

    def print_board(self):
        print("           [Поле Игрока]        :             [Поле ИИ]")
        print("    1 | 2 | 3 | 4 | 5 | 6 | X   |      1 | 2 | 3 | 4 | 5 | 6 | X")
        for i in range(6):
            player_row = f"{i + 1} "
            ai_row = f"{i + 1} "
            for j in range(6):
                player_row += f"| {self.player_board[i][j+1]} "
                ai_row += f"| {self.ai_board[i][j]} "
            player_row += "|"
            ai_row += "|"
            print(player_row.ljust(30), " | ", ai_row.ljust(30))  # ljust выраввнивание по левому краю
            if i != 5:
                print("-------------------------     |    -------------------------")
        print("Y                                  Y")

    def place_ship(self, ship, x, y, r):
        try:
            if 1 <= x <= 6 and 1 <= y <= 6 and (r == 1 or r == 2):  # проверяем чтобы ввод был соответсующий для X,Y,R
                current_board = self.get_current_board()
                if r == 1:  # Если выбрана вертикальная плоскость
                    if ship.length > 0 and y + ship.length - 2 <= 6:
                        for i in range(ship.length):
                            if not self.is_position_free(x, y - 1 + i, ship):
                                if self.config.ai_ship_is_close_message == 1:
                                    print("Нельзя разместить корабль так близко друг к другу (вертик)")  # вертикаль
                                return False
                        for i in range(ship.length):
                            if current_board[y - 1 + i][x-1] != ' ':
                                print("Корабль уже находится в этой клетке. Пожалуйста, выберите другие координаты.")
                                return False  # return возвращает на стартовую позицию функции, иначе мы сможем поставить корабль на место, где уже есть корабль
                            current_board[y - 1 + i][x-1] = f"{ship.length}"
                    elif ship.length == 1:
                        current_board[y - 1][x] = f"{ship.length}"
                    else:
                        print("Корабль не помещается на доску. Пожалуйста, выберите другие координаты.")
                        return False
                elif r == 2:  # Если выбрана горизонтальная плоскость
                    if ship.length > 0 and x + ship.length - 2 <= 6:
                        for i in range(ship.length):
                            if not self.is_position_free(x + i, y - 1, ship):
                                if self.config.ai_ship_is_close_message == 1:
                                    print("Нельзя разместить корабль так близко друг к другу (горик)")  # горизонт
                                return False
                        for i in range(ship.length):
                            if current_board[y - 1][x + i] != ' ':
                                print("Корабль уже находится в этой клетке. Пожалуйста, выберите другие координаты.")
                                return False  # возвращает на стартовую позицию функции, иначе мы сможем поставить корабль на место, где уже есть корабль
                            current_board[y - 1][x + i] = f"{ship.length}"
                    elif ship.length == 1:
                        current_board[y - 1][x-1] = f"{ship.length}"
                    else:
                        print("Корабль не помещается на доску. Пожалуйста, выберите другие координаты.")
                        return False
                return True
            else:
                print("Неверные координаты или ориентация. Пожалуйста, введите числа от 1 до 6 для X и Y, а для R - 1 или 2.")
                return False
        except Exception as e:
            print(f"place_ship: {e}")
            return False

    def is_position_free(self, x, y, ship):  # проверка на свободную ячейку по указанным координатам
        for col in range(max(1, x - ship.length), min(6, x + ship.length + 1)):  # перебор по горизонтали (х)
            for row in range(max(1, y - ship.length), min(6, y + ship.length + 1)):  # перебор по вертикали (y)
                if self.player_board[row - 1][col - 1] in ('1', '2', '3', 'X'):  # если в ячейке есть что-то, то return False, и проверяем заново
                    print("is_position_free: Return Fault")
                    return False
        if self.config.is_position_free_message:
            print("is_position_free: Return True")
        return True

    def play_game(self):
        # *** Проверка текущего Корабля ***
        current_ships_index = 0  # индекс текущего корабля
        current_ships_count = self.player.get_ships_count()  # текущее кол-во кораблей у player_1
        try:
            for ship in self.player.ships_count:  # итерируем список кораблей у игрока
                print(f"Осталось расставить кораблей: {current_ships_count - current_ships_index}, текущий {ship.name}")
                while True:  # Выполняем цикл до тех пор, пока не разместим корабль успешно.
                    # цикл while будет продолжать запрашивать верный ввод координат ля размещения
                    x, y, r = self.player.input_coordinates()  # получаем координаты x,y,r от игрока
                    if self.place_ship(ship, x, y, r):  # проверяем входные данные
                        self.print_board()  # обновляем игровое поле
                        current_ships_index += 1  # добавляем +1 к индексу
                        break  # Выходим из цикла while, так как успешно разместили корабль, и переходим к следующему
        except Exception as e:
            print(f"play_game: {e}")

    def shoot(self):
        # *** Производим выстрел ***
        start_shooting = True  # показал два варианта исполнения: while true / break; либо кастом переменные
        while start_shooting:
            try:
                x, y = self.player.input_shoot_coordinates()
                print(f"{self.aiplayer.p_name}: Выстрел!")
                if self.ai_board[y-1][x-1] == ' ' or self.ai_board[y-1][x-1] == '■':  # проверяем предел от 1 до 6
                    # так как счёт начинается с '1', а не с '0', использую формулу [y-1]
                    self.ai_board[y-1][x-1] = 'X'
                    time.sleep(0.5)
                    self.print_board()
                    start_shooting = False
                else:
                    print("Неверные координаты. Пожалуйста, введите числа от 1 до 6")
            except Exception as e:
                print(f"shoot: {e}")

    def ai_shoot(self):
        # *** ИИ производит выстрел ***
        while True:
            try:
                x, y = self.aiplayer.ai_shoot_coordinates()  # выбираем random значения от 1 до 6

                if self.config.ai_ship_is_close_message == 1:
                    print(f"Выстрел в {x, y}")

                print(f"{self.aiplayer.p_name}: Выстрел!")
                if self.player_board[y-1][x] == ' ' or self.player_board[y-1][x] == '■':  # если клетка пустая или ■, то
                    # y-1 так как итерация идет от 0, а не с 1
                    self.player_board[y-1][x] = 'X'
                    time.sleep(0.5)
                    self.print_board()
                    break
                else:
                    print(f"{self.aiplayer.p_name}: Эта клетка уже была выбрана. Повторите выстрел.")
            except Exception as e:
                print(f"ai_shoot: {e}")

    def ai_place_ship(self):
        # *** ИИ расставляет корабли ***
        try:
            for ship in self.aiplayer.ships_count:
                while True:
                    time.sleep(0)
                    x, y, r = self.aiplayer.ai_ship_coordinates(ship)
                    if self.place_ship(ship, x, y, r):
                        if self.config.ai_ship_place_coordinate_message:
                            print(f"{x, y, r}")
                        break
            self.print_board()
        except Exception as e:
            print(f"ai_place_ship: {e}")