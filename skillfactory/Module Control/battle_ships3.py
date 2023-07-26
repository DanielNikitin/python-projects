import random

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Ship:
    def __init__(self, size):
        self.size = size
        self.hp = size

class Board:
    def __init__(self):
        self.size = 6
        self.ships = [Ship(3), Ship(2), Ship(1)]
        self.grid = [[' ' for _ in range(self.size)] for _ in range(self.size)]
        self.ai_grid = [[' ' for _ in range(self.size)] for _ in range(self.size)]

    def print_board(self, hidden=False):
        print("   0  1  2  3  4  5       0  1  2  3  4  5")
        for i in range(self.size):
            row_str = f"{i} {' | '.join(self.grid[i])}   {i} {' | '.join(self.ai_grid[i])}"
            print(row_str)
            if i < self.size - 1:
                print("  " + "-" * (4 * self.size - 1) + "   " + "-" * (4 * self.size - 1))

    def is_valid_position(self, ship, x, y):
        if 0 <= x < self.size and 0 <= y < self.size:
            if self.grid[x][y] == ' ':
                return True
        return False

    def place_ship(self, ship, x, y):
        self.grid[x][y] = '■'
        ship.hp = ship.size

    def random_place_ships(self):
        for ship in self.ships:
            while True:
                x = random.randint(0, self.size - 1)
                y = random.randint(0, self.size - 1)

                if self.is_valid_position(ship, x, y):
                    self.place_ship(ship, x, y)
                    break

class Player:
    def __init__(self, name):
        self.name = name
        self.ships = [Ship(3), Ship(2), Ship(1)]
        self.board = Board()

    def place_ships(self):
        print(f"{self.name}, расставьте ваши корабли:")
        for ship in self.ships:
            while True:
                self.board.print_board(hidden=False)
                print(f"У вас осталось {ship.size} палуб(ы)")
                while True:
                    try:
                        x = int(input("Введите координату X (0-5): "))
                        y = int(input("Введите координату Y (0-5): "))
                        break
                    except ValueError:
                        print("Неверный ввод. Пожалуйста, введите числовое значение.")

                if self.board.is_valid_position(ship, x, y):
                    self.board.place_ship(ship, x, y)
                    self.board.print_board(hidden=False)
                    break
                else:
                    print("Неверные координаты или клетка уже занята. Попробуйте снова.")

class AIPlayer(Player):
    def __init__(self):
        super().__init__("Компьютер")

    def place_ships(self):
        self.board.random_place_ships()

    def make_random_move(self):
        while True:
            x = random.randint(0, self.board.size - 1)
            y = random.randint(0, self.board.size - 1)
            if self.board.grid[x][y] == ' ' or self.board.grid[x][y] == '■':
                return Dot(x, y)

def play_game():
    print("Добро пожаловать в Морской Бой!")
    player_name = input("Введите ваше имя: ")
    player = Player(player_name)
    ai_player = AIPlayer()

    print("Расставьте свои корабли:")
    player.place_ships()

    print("Компьютер расставляет свои корабли...")
    ai_player.place_ships()

    current_player = player

    while True:
        print(f"\nХодит {current_player.name}")
        current_player.board.print_board(hidden=current_player == ai_player)

        if current_player == player:
            while True:
                while True:
                    try:
                        x = int(input("Введите координату X (0-5): "))
                        y = int(input("Введите координату Y (0-5): "))
                        break
                    except ValueError:
                        print("Неверный ввод. Пожалуйста, введите числовое значение.")

                if 0 <= x < player.board.size and 0 <= y < player.board.size:
                    target = Dot(x, y)
                    if ai_player.board.grid[target.x][target.y] == 'X' or ai_player.board.grid[target.x][
                        target.y] == ' ':
                        break
                    else:
                        print("Вы уже стреляли в эту клетку. Попробуйте снова.")
                else:
                    print("Неверные координаты. Попробуйте снова.")

            if ai_player.board.grid[target.x][target.y] == '■':
                print("Попадание!")
                ai_player.board.grid[target.x][target.y] = 'X'
                for ship in ai_player.ships:
                    if Dot(target.x, target.y) in [Dot(x, y) for x in range(ai_player.board.size) for y in
                                                   range(ai_player.board.size)]:
                        ship.hp -= 1
                        if ship.hp == 0:
                            print(f"Вы потопили корабль компьютера размером {ship.size} палубы!")
                            ai_player.ships.remove(ship)
                            break
            else:
                print("Мимо!")

            if not ai_player.ships:
                print("Вы победили!")
                break

        else:
            target = ai_player.make_random_move()
            print(f"Компьютер стреляет в клетку {target.x}, {target.y}")

            if player.board.grid[target.x][target.y] == '■':
                print("Попадание!")
                player.board.grid[target.x][target.y] = 'X'
                for ship in player.ships:
                    if Dot(target.x, target.y) in [Dot(x, y) for x in range(player.board.size) for y in
                                                   range(player.board.size)]:
                        ship.hp -= 1
                        if ship.hp == 0:
                            print(f"Компьютер потопил ваш корабль размером {ship.size} палубы!")
                            player.ships.remove(ship)
                            break
            else:
                print("Мимо!")

            if not player.ships:
                print("Компьютер победил!")
                break

        if current_player == player:
            current_player = ai_player
        else:
            current_player = player

if __name__ == "__main__":
    play_game()
