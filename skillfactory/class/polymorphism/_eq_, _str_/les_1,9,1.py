# Добавьте ещё один класс — круг (class Circle), конструктор которого
# содержит параметр радиус. Добавьте метод для расчёта площади круга (вспомните формулу).

# Далее сделайте вывод информации о площади в консоль.

class Rectangle:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def get_area(self):
        return self.a * self.b


class Square:
    def __init__(self, a):
        self.a = a

    def get_area_square(self):
        return self.a ** 2


class Circle:
    def __init__(self, r):
        self.r = r

    def get_area_circle(self):  # метод для расчёта площади круга ( S = пr**2 = п/4*D**2
        return (self.r ** 2) * 3.14  # Площадь = Пи * радиус в квадрате = Пи / 4 * Диаметр в квадрате


rect_1 = Rectangle(3, 4)
rect_2 = Rectangle(12, 5)
square_1 = Square(5)
square_2 = Square(10)
circle_1 = Circle(1)
circle_2 = Circle(2)

figures = [rect_1, rect_2, square_1, square_2, circle_1, circle_2]
for figure in figures:
    if isinstance(figure, Square):
        print(figure.get_area_square())
    elif isinstance(figure, Rectangle):
        print(figure.get_area())
    else:
        print(figure.get_area_circle())