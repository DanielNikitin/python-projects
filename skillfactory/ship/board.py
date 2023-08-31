class Board:
    def __init__(self, size=6):
        self.size = size
        self.board = [['O' for _ in range(size)] for _ in range(size)]

    def print_board(self, player_board, enemy_board):
        print("  " + " ".join([str(i + 1) for i in range(self.size)]))
        print(" +" + "-" * (self.size * 2 - 1) + "+")
        for i, (player_row, enemy_row) in enumerate(zip(player_board, enemy_board)):
            print(str(i + 1) + "|" + " ".join(player_row) + "|   |" + " ".join(enemy_row) + "|")
        print(" +" + "-" * (self.size * 2 - 1) + "+")
