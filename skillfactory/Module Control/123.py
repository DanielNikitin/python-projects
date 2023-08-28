def place_ship(self, ship, x, y, r):
    try:
        for i in range(ship.length):
            print(f"Попытка {i + 1}: Размещение корабля '{ship.name}' в ({x}, {y - 1 + i})")
        if 1 <= x <= 6 and 1 <= y <= 6 and (r == 1 or r == 2):  # проверяем чтобы ввод был соответсующий для X,Y,R
            if r == 1:  # Если выбрана вертикальная плоскость
                if ship.length > 0 and y + ship.length - 2 <= 6:
                    for i in range(ship.length):
                        if not self.is_position_free(x, y - 1 + i):
                            if self.config.ai_ship_place_message == 1:
                                print("Нельзя разместить корабль так близко друг к другу (верт)")  # вертикаль
                            return False
                    for i in range(ship.length):
                        if self.current_board[y - 1 + i][x] != ' ':
                            print("Корабль уже находится в этой клетке. Пожалуйста, выберите другие координаты.")
                            return False  # return возвращает на стартовую позицию функции, иначе мы сможем поставить корабль на место, где уже есть корабль
                        self.current_board[y - 1 + i][x] = '■'
                elif ship.length == 1:
                    self.current_board[y - 1][x] = '■'
                else:
                    print("Корабль не помещается на доску. Пожалуйста, выберите другие координаты.")
                    return False
            elif r == 2:  # Если выбрана горизонтальная плоскость
                if ship.length > 0 and x + ship.length - 2 <= 6:
                    for i in range(ship.length):
                        if not self.is_position_free(x + i, y - 1):
                            if self.config.ai_ship_place_message == 1:
                                print("Нельзя разместить корабль так близко друг к другу (гор)")  # горизонт
                            return False
                    for i in range(ship.length):
                        if self.current_board[y - 1][x + i] != ' ':
                            print("Корабль уже находится в этой клетке. Пожалуйста, выберите другие координаты.")
                            return False  # возвращает на стартовую позицию функции, иначе мы сможем поставить корабль на место, где уже есть корабль
                        self.current_board[y - 1][x + i] = '■'
                elif ship.length == 1:
                    self.current_board[y - 1][x] = '■'
                else:
                    print("Корабль не помещается на доску. Пожалуйста, выберите другие координаты.")
                    return False
            return True
        else:
            print(
                "Неверные координаты или ориентация. Пожалуйста, введите числа от 1 до 6 для X и Y, а для R - 1 или 2.")
            return False
    except Exception as e:
        print(f"Ошибка: {e}")
        return False


def is_position_free(self, x, y):  # проверка на свободную ячейку по указанным координатам
    for col in range(max(0, x - 1), min(6, x + 2)):  # перебор по горизонтали (х)
        for row in range(max(0, y - 1), min(6, y + 2)):  # перебор по вертикали (y)
            if self.player_board[row][col] in ('■', 'X'):  # если в ячейке есть что-то, то return False, и проверяем заново
                #    if self.game_board[row][col] == '■' or self.game_board[row][col] == 'X':  # сначала этот метод использовал
                return False
    return True