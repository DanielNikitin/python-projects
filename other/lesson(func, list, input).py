#---- FUNCTION ----

#try:
    # x = int(input('Введите число'))
#except ValueError:
    #print('Я сказала введите число!!!')

#def say_hello(username, age):
 #   print(f'Hello {username}')
  #  print(f'Your age is {age}')
   # print('-' *20)

# say_hello('Valera', 20)
# say_hello('mr.Matvei', 30)

# say_hello(username='Alex', age=35)
# say_hello(age=40, username='Anna')

#def number_sum(username, num1=1, num2=2):
 #   print(f'Hello {username}!')
  #  print(num1 + num2)
   # print(f'-' * 20)

# number_sum(num1=2, num2=7)
# number_sum(num1=13, num2=5)
# number_sum(num1=78, num2=349)
# number_sum()
# number_sum(username='oLga', num1=78)
# numer_sum('Victor', num1=78)
# number_sum('Vicot')
# number_sum('Max', num1=78, num2=-400)

# ПРИМЕР ФУНКЦИИ
#def check_user(username, age=0):
 #   print(f'Hello {username}!')

  #  if age >= 21:
   #     print('Welcome to the Club!')

    #print(f'-' *20)

    # if age < 18:
    #print("маловато")
#else:
   # print("Добро пожаловать")

#check_user(username='Oleg')
#check_user(username='Sveta', age=22)

#----------------

#---- LIST ----

# my_list_1 = []
# print(type(my_list_1)

# my_list_2 = list()
# print(type(my_list_2))

# my_list = ["hello", 23, 76.2, ("1", "2", "3"), {"user1": "Victor"}, [5, 7, 2, 1], [], ""]
# print(my_list)

my_list_1 = [55, 2, 5, 1]
         #       -4                -3               -2                 -1
        #         0                 1                2                  3
my_list_2 = ["Выпить кофе", "Поссать на куст", "Жахнуть черешенки", "Купить пива"]

# print(my_list_1[0])  # выбираем индекс данных который нужно вывести
# print(my_list_2[2])
# print(my_list_2[-1])

# print(len(my_list_2))  # получаем длинну списка (кол-во индексов) len(имя_списка)
# print(my_list_2[0:2])  # указываем индексы от и до тех данных которые хотим получить
# print(my_list_2[:2])  # от начала до 2 индекса
# print(my_list_2[:])  # весь список

# добавляем обьект в конец списка
my_list_2.append("Купить билеты")
# print(my_list_2)

# Добавляем обьект в список (индекс (на место которого добавляем), "обьект")
my_list_2.insert(1, "Принять душ")
# print(my_list_2)

# Удаляем обьект под указанным индексом и Добавляем измененный список
my_list_2.pop(-2)
# print(my_list_2)

# Метод удалит и вернет ПОСЛЕДНИЙ измененный список
my_list_2.pop()
# print(my_list_2)

# Метод добавления обьектов из одного списка в конец другого списка
list2 = ["Сходить на прогулку", "Пожарить сосиски", "Сходить на прогулку"]
my_list_2.extend(list2)
#print(my_list_2)

# Метод сложения списков
a = [1, 2, 3]
b = [4, 5, 6]
c = a + b
#print(c)

x = ["Hello"] + ["friend"] + [3301]
#print(x)

# Удаляем элемент с переданным значением (Если элементы одинаковые, удаляем первый попавшийся)
#print(my_list_2)
my_list_2.remove("Сходить на прогулку")
#print(my_list_2)

# Метод возвращения индекса элемента
#print(my_list_2)
#print(my_list_2.index("Пожарить сосиски"))

# Метод сортировки
n_list = [22, 1, 66, 23, 62, 3]
n_list.sort()
#print(n_list)

# Метод переворачивания списка
n_list.reverse()
#print(n_list)

# Минимальное и Максимальное значение в списке
#print(n_list)
#print(min(n_list))
#print(max(n_list))

# Список из слов
words_list = ["за", "тобой", "выехали"]

#my_str = "".join(words_list)
#my_str = " ".join(words_list)
#my_str = "-".join(words_list)
#print(my_str)

print(words_list)
# Чистка списка от обьектов
words_list.clear()

#----------------

#---- INPUT ----

# name = input("Имя: ")
# print(name)

# birth_date = input("Введите: ")
# print(birth_date)

# my_var = input("Введите данные: ")
# print(type(my_var))  # любые данные в input это STR

# Преобразуем тип данных в Число
#age = int(input("Введите возраст: "))
#age = age * 2
#print(age)

# Class Person: # - Класс Person
    #def send_hello(x): # self необязательно, пишем любой аргумент
        #print('Hello!')
# p = Person()  # р - экземпляр класса
# p.send_hello() # вызываем функцию Экземпляра класса
# в скобки передается аргумент который указан в функции