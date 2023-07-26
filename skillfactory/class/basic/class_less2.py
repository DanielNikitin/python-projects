# Метод — это всего лишь функция, реализованная внутри класса,
# и первым аргументом принимающая self:

class Product:
    def __init__(self, name, category, quantity_in_stock):  # Конструктор класса
        self.name = name
        self.category = category
        self.quantity_in_stock = quantity_in_stock

    def is_available(self):  # Метод
        return True if self.quantity_in_stock > 0 else False

# Здесь и __init__, и is_available — это методы.
eggs = Product("eggs", "food", 1)
print(eggs.is_available())
# Так как функции находятся в одном Классе Product
# Можно вытаскивать атрибуты(переменные) в разных методах (функциях).
# Разница между методом и функцией только в том,
# что метод вызывается от конкретного объекта и
# реализован внутри класса, а функция работает сама по себе.

class Player:
    def __init__(self, p_name, ships_count):
        self.p_name = p_name
        self.ships_count = ships_count

player_1 = Player(input("new name: "), 3)
print("Now your name is: ", player_1.p_name)