# Каков механизм работы? Когда вы создаёте объект класса Rectangle,
# конструктор этого класса будет вызван для создания объекта,
# а атрибутам объекта будут присвоены значения из параметра.

from rectangle import Rectangle

r2 = Rectangle(1, 2)

print("r2.width =", r2.width)
print("r2.height =", r2.height)
print("r2.get_width =", r2.get_width())
print("r2.get_height =", r2.get_height())
print("r2.get_area =", r2.get_area())