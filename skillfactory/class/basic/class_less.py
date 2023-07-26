#class User:
   # pass

#peter = User()  # экземпляр класса User
#peter.name = "Peter Robertson"  # Здесь .name атрибут экземпляра класса

#julia = User()  # экземпляр класса User
#julia.name = "Julia Donaldson"

#print(peter.name)
#print(julia.name)

#  магический метод-конструктор класса - __init__.
# который заранее определяет атрибуты новых экземпляров.
# Первым аргументом он обязательно принимает на вход self,
# а дальше — произвольный набор аргументов, как обычная функция:
class User:
    def __init__(self, name, email): # конструктор класса
        self.name = name # атрибуты
        self.email = email # атрибуты

# User - это определение класса
# Атрибуты (переменные) и Методы (функции)
# def __init__(self, name, email): - это конструктор класса.
# self - это ссылка на текущий объект
# self.name
# self.email - это атрибуты объекта класса User
# После создания объекта класса User, эти атрибуты
# будут хранить значения, переданные в конструктор
# при его вызове. Например, если создать объект user1 класса User,
# то user1.name и user1.email будут представлять имя
# и адрес электронной почты пользователя user1

user1 = User("John", "john@example.com")
print(user1.name)  # Выведет: John
print(user1.email)  # Выведет: john@example.com

