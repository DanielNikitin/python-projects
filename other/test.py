

class User:
    def __init__(self, name, x):
        self.name = name
        self.x = x

    def if_connect(self, data):
        data = data.split()
        self.name = data[0]
        self.x = int(data[1])

# CLIENT:
data = input("Your name: ")
# -------

new_player = User(name, x)  # Создаем экземпляр класса User

new_player.if_connect(data)  # Вызываем метод if_connect

print(data[0], data[1])
print(new_player.name, new_player.x)
