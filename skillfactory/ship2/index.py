import random

class BattleshipGame:
    def __init__(self):
        self.LENGTH_OF_SHIPS = [1, 1, 1, 1]
        self.PLAYER_BOARD = [[" "] * 6 for _ in range(6)]
        self.COMPUTER_BOARD = [[" "] * 6 for _ in range(6)]
        self.PLAYER_GUESS_BOARD = [[" "] * 6 for _ in range(6)]
        self.COMPUTER_GUESS_BOARD = [[" "] * 6 for _ in range(6)]
        self.LETTERS_TO_NUMBERS = {'1': 0, '2': 1, '3': 2, '4': 3, '5': 4, '6': 5}

    def print_board(self, board):
        print("  1 2 3 4 5 6")
        print("  +-+-+-+-+-+")
        row_number = 1
        for row in board:
            print("%d|%s|" % (row_number, "|".join(row)))
            row_number += 1

    def place_ships(self, board):
        for ship_length in self.LENGTH_OF_SHIPS:
            while True:
                if board == self.COMPUTER_BOARD:
                    orientation = random.choice(["H", "V"])
                    row = random.randint(0, 5)
                    column = random.randint(0, 5)
                    if self.check_ship_fit(ship_length, row, column, orientation):
                        if not self.ship_overlaps(board, row, column, orientation, ship_length):
                            if orientation == "H":
                                for i in range(column, column + ship_length):
                                    board[row][i] = "X"
                            else:
                                for i in range(row, row + ship_length):
                                    board[i][column] = "X"
                            break
                else:
                    place_ship = True
                    print('Place the ship with a length of ' + str(ship_length))
                    row, column, orientation = self.user_input(place_ship)
                    if self.check_ship_fit(ship_length, row, column, orientation):
                        if not self.ship_overlaps(board, row, column, orientation, ship_length):
                            if orientation == "H":
                                for i in range(column, column + ship_length):
                                    board[row][i] = "X"
                            else:
                                for i in range(row, row + ship_length):
                                    board[i][column] = "X"
                            self.print_board(self.PLAYER_BOARD)
                            break

    def check_ship_fit(self, ship_length, row, column, orientation):
        if orientation == "H":
            if column + ship_length > 6:
                return False
            else:
                return True
        else:
            if row + ship_length > 6:
                return False
            else:
                return True

    def ship_overlaps(self, board, row, column, orientation, ship_length):
        if orientation == "H":
            for i in range(column, column + ship_length):
                if board[row][i] == "X":
                    return True
        else:
            for i in range(row, row + ship_length):
                if board[i][column] == "X":
                    return True
        return False

    def user_input(self, place_ship):
        if place_ship:
            while True:
                try:
                    orientation = input("Enter orientation (H or V): ").upper()
                    if orientation == "H" or orientation == "V":
                        break
                except TypeError:
                    print('Enter a valid orientation H or V')
            while True:
                try:
                    row = input("Enter the row 1-6 of the ship: ")
                    if row in '123456':
                        row = int(row) - 1
                        break
                except ValueError:
                    print('Enter a valid letter between 1-6')
            while True:
                try:
                    column = input("Enter the column of the ship: ").upper()
                    if column in '12345':
                        column = self.LETTERS_TO_NUMBERS[column]
                        break
                except KeyError:
                    print('Enter a valid letter between A-F')
            return row, column, orientation
        else:
            while True:
                try:
                    row = input("Enter the row 1-6 of the ship: ")
                    if row in '123456':
                        row = int(row) - 1
                        break
                except ValueError:
                    print('Enter a valid letter between 1-6')
            while True:
                try:
                    column = input("Enter the column of the ship: ").upper()
                    if column in 'ABCDEF':
                        column = self.LETTERS_TO_NUMBERS[column]
                        break
                except KeyError:
                    print('Enter a valid letter between A-F')
            return row, column

    def count_hit_ships(self, board):
        count = 0
        for row in board:
            for column in row:
                if column == "X":
                    count += 1
        return count

    def turn(self, board):
        if board == self.PLAYER_GUESS_BOARD:
            row, column = self.user_input(self.PLAYER_GUESS_BOARD)
            if board[row][column] == "-":
                self.turn(board)
            elif board[row][column] == "X":
                self.turn(board)
            elif self.COMPUTER_BOARD[row][column] == "X":
                board[row][column] = "X"
            else:
                board[row][column] = "-"
        else:
            row, column = random.randint(0, 5), random.randint(0, 5)
            if board[row][column] == "-":
                self.turn(board)
            elif board[row][column] == "X":
                self.turn(board)
            elif self.PLAYER_BOARD[row][column] == "X":
                board[row][column] = "X"
            else:
                board[row][column] = "-"

if __name__ == "__main__":
    print("\n======= Welcome to Battleship =======\n\n")
    game = BattleshipGame()
    game.place_ships(game.COMPUTER_BOARD)
    game.print_board(game.PLAYER_BOARD)
    game.place_ships(game.PLAYER_BOARD)

    while True:
        while True:
            print("\n -- Player Turn --\n")
            print('Guess enemy location\n')
            game.print_board(game.PLAYER_GUESS_BOARD)
            game.turn(game.PLAYER_GUESS_BOARD)
            break
        if game.count_hit_ships(game.PLAYER_GUESS_BOARD) == 17:
            print("You win!")
            break

        while True:
            print("\n-- Computer Turn --\n")
            game.turn(game.COMPUTER_GUESS_BOARD)
            break
        game.print_board(game.COMPUTER_GUESS_BOARD)
        if game.count_hit_ships(game.COMPUTER_GUESS_BOARD) == 17:
            print("Sorry, the computer won.")
            break
