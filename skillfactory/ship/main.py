from game import Game

try:
    if __name__ == "__main__":
        game = Game(10)
        game.play()
except KeyboardInterrupt:
    print("Quit")
