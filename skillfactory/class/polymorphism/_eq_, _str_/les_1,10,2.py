# В классе, написанном в предыдущем задании,
# создайте метод, который будет рассчитывать площадь фигуры.
# Выведите значение площади на экран.

class Rectangle:
    def __init__(self, x, y, width, heigth):
        self.x = x
        self.y = y
        self.width = width
        self.heigth = heigth

    def __str__(self):
        return f'Rectangle : \nx= {self.x},\ny= {self.y}, \nw= {self.width}, \nh= {self.heigth}.'

    def get_area(self):
        return f'S = {self.width * self.heigth}'


rect_1 = Rectangle(5, 10, 50, 100)
print(rect_1)
print(rect_1.get_area())