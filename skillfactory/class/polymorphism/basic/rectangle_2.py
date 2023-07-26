from les_1 import Rectangle, Square

# Выполним импорт класса Rectangle
# далее создаём два прямоугольника

rect_1 = Rectangle(3,4)
rect_2 = Rectangle(12,5)
# вывод площади наших двух прямоугольников
print(rect_1.get_area())
print(rect_2.get_area())

# добавляем новый обьект

square_1 = Square(5)
square_2 = Square(10)

print(square_1.get_area_square(),
      square_2.get_area_square())  # более лаконично

# Теперь мы хотим в нашей программе все объекты перенести в единую коллекцию.

figures = [rect_1, rect_2, square_1, square_2]
for figure in figures:
    if isinstance (figure, Square):
        print("-------")
        print(figure.get_area_square())
    else:
        print("_______")
        print(figure.get_area())

# если экземпляр класса figure является квадратом, то вызываем метод get_area_square();
# в противном случае мы обрабатываем данные для прямоугольника методом get_area().

# В условии есть функция isinstance, поддерживающая наследование.
# Функция возвращает True, если первый аргумент функции является экземпляром класса,
# где класс задается вторым аргументом. Иными словами, функция проверяет,
# принадлежит ли объект к классу.