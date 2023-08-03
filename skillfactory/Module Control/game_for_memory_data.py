def main():
    health = 100
    while True:
        print("Player health is", health)
        key = input("Press 'H' to decrease health: ")

        if key.lower() == 'h':
            health -= 15

        if health <= 0:
            print("Player is dead!")
            break


if __name__ == "__main__":
    main()
