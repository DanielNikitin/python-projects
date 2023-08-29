import random
from board import Board
from ship import Ship

class Game:
    def __init__(self, board_size):
        self.board_size = board_size
        self.player_board = Board(board_size)
        self.enemy_board = Board(board_size)
        self.ships = [
            Ship('Авианосец', 5),
            Ship('Линкор', 4),
            Ship('Крейсер', 3),
            Ship('Эсминец', 3),
            Ship('Катер', 2)
        ]

    def place_ships(self, board):
        for ship in self.ships:
            board.print_board(self.player_board.board, self.enemy_board.board)
            print(f"Разместите корабль '{ship.name}' размером {ship.size}:")
            while True:
                row = int(input("Введите номер строки: ")) - 1
                col = int(input("Введите номер столбца: ")) - 1
                orientation = input("Введите ориентацию (горизонтально - H, вертикально - V): ").upper()

                if orientation == 'H' and col + ship.size > self.board_size:
                    print("Корабль не может быть размещен в данной позиции!")
                    continue
                elif orientation == 'V' and row + ship.size > self.board_size:
                    print("Корабль не может быть размещен в данной позиции!")
                    continue

                ship_coords = []
                for i in range(ship.size):
                    if orientation == 'H':
                        ship_coords.append((row, col + i))
                    else:
                        ship_coords.append((row + i, col))

                if any(ship.covers_coord(coord) for coord in ship_coords):
                    print("Корабль перекрывает другой корабль!")
                    continue

                for coord in ship_coords:
                    ship.add_coord(coord)
                    board.board[coord[0]][coord[1]] = 'S'

                break

    def check_hit(self, coord, ships):
        for ship in ships:
            if ship.covers_coord(coord):
                ship.coords.remove(coord)
                return True
        return False

    def play(self):
        print("Добро пожаловать в игру 'Морской бой'!")

        print("Разместите свои корабли:")
        self.place_ships(self.player_board)

        while True:
            self.player_board.print_board(self.player_board.board, self.enemy_board.board)

            print("Ваш ход:")
            while True:
                guess_row = int(input("Введите номер строки: ")) - 1
                guess_col = int(input("Введите номер столбца: ")) - 1

                if (
                    guess_row < 0 or guess_row >= self.board_size or
                    guess_col < 0 or guess_col >= self.board_size
                ):
                    print("Вы ввели некорректные координаты!")
                elif self.enemy_board.board[guess_row][guess_col] != 'O':
                    print("Вы уже стреляли в эту клетку!")
                else:
                    break

            if self.check_hit((guess_row, guess_col), self.ships):
                print("Поздравляю! Вы потопили корабль бота!")
                self.enemy_board.board[guess_row][guess_col] = 'X'

                if all(ship.is_sunk() for ship in self.ships):
                    print("Вы победили! Все корабли бота потоплены!")
                    break
            else:
                print("Мимо!")
                self.enemy_board.board[guess_row][guess_col] = '.'

            while True:
                bot_guess_row = random.randint(0, self.board_size - 1)
                bot_guess_col = random.randint(0, self.board_size - 1)

                if self.player_board.board[bot_guess_row][bot_guess_col] == 'O':
                    break

            if self.check_hit((bot_guess_row, bot_guess_col), self.ships):
                print("Бот потопил ваш корабль!")
                self.player_board.board[bot_guess_row][bot_guess_col] = 'X'

                if all(ship.is_sunk() for ship in self.ships):
                    print("Бот победил! Все ваши корабли потоплены!")
                    break
            else:
                print("Бот промахнулся!")
                self.player_board.board[bot_guess_row][bot_guess_col] = '.'
