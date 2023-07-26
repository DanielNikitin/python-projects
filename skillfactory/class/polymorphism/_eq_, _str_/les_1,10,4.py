# Команда проекта «Дом питомца» планирует большой корпоратив для своих клиентов.
# Вам необходимо написать программу, которая позволит составить список гостей.
# В класс «Клиент» добавьте метод, который будет возвращать информацию
# только об имени, фамилии и городе клиента.
#
# Затем создайте список, в который будут добавлены все клиенты, и выведете его в консоль.

class Customers:
    def __init__(self, first_name, second_name, city, balance):
        self.first_name = first_name
        self.second_name = second_name
        self.balance = balance
        self.city = city

    def __str__(self):
        return f'''"{self.first_name} {self.second_name}". {self.city}. Баланс: {self.balance} руб.'''

    def get_guest(self):
        return f'{self.first_name} {self.second_name}, г. {self.city}'


customer_1 = Customers('Кристина','Рыбачёнок','Таллинн',50)
customer_2 = Customers('Василиса','Варес','Маарду',50)
customer_3 = Customers('СтанисLove','Варес','Маарду',50)

guest_list=[customer_1, customer_2, customer_3]

for guest in guest_list:
    print(guest.get_guest())