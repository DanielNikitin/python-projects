import random


def create_empty_board(size):
    return [[' ' for _ in range(size)] for _ in range(size)]


def is_valid_placement(board, x, y, ship_size, orientation):
    size = len(board)

    offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    if orientation == 'horizontal':

        for i in range(ship_size):

            if x + i >= size or board[y][x + i] != ' ':
                return False

            for dx, dy in offsets:

                if y + dy >= 0 and y + dy < size and x + i + dx >= 0 and x + i + dx < size:

                    if board[y + dy][x + i + dx] != ' ':
                        return False

    else:

        for i in range(ship_size):

            if y + i >= size or board[y + i][x] != ' ':
                return False

            for dx, dy in offsets:

                if y + i + dy >= 0 and y + i + dy < size and x + dx >= 0 and x + dx < size:

                    if board[y + i + dy][x + dx] != ' ':
                        return False

    return True


def place_ship(board, ship_size):
    size = len(board)

    while True:

        x = random.randint(0, size - 1)

        y = random.randint(0, size - 1)

        orientation = random.choice(['horizontal', 'vertical'])

        if is_valid_placement(board, x, y, ship_size, orientation):

            if orientation == 'horizontal':

                for i in range(ship_size):
                    board[y][x + i] = 'R'

            else:

                for i in range(ship_size):
                    board[y + i][x] = 'R'

            break


def print_board(board):
    size = len(board)

    print('  ' + ' '.join(map(str, range(1, size + 1))))

    print('  ' + '- ' * size)

    for i in range(size):
        print(chr(ord('A') + i) + '|' + ' '.join(board[i]) + '|')


def main():
    size = 10

    board = create_empty_board(size)

    ship_sizes = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

    for ship_size in ship_sizes:
        place_ship(board, ship_size)

    print("Welcome to Battleship!")

    print_board(board)


main()