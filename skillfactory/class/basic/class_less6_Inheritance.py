import datetime

# class ПроизводныйКласс (БазовыйКласс):
#     # Тело класса
# Таким образом, классы умеют наследовать друг у друга,
# причём не только атрибуты, но и методы.

# Это значит, что родительские атрибуты и методы
# будут доступны у так называемых дочерних (или производных) классов

class Product:
    max_quantity = 100000

    def __init__(self, name, category, quantity_in_stock):
        self.name = name
        self.category = category
        self.quantity_in_stock = quantity_in_stock

    def is_available(self):
        return True if self.quantity_in_stock > 0 else False

# Чтобы задать родительский класс, надо указать его
# в скобках при объявлении производного класса,
# как будто это аргумент функции:

class Food(Product):
    is_critical = True
    needs_to_be_refreshed = True
    refresh_frequency = datetime.timedelta(days=1)


eggs = Food(name="eggs", category="food", quantity_in_stock=5)
print(eggs.max_quantity)
print(eggs.is_available())

# Мы видим, что мы создавали объект eggs
# как экземпляр класса Food, но при этом ему
# доступны как атрибуты родительского класса (max_quantity),
# так и его методы (is_available).
#
# Фактически произошло ещё более интересное:
# для создания экземпляра класса Food мы использовали
# конструктор его родительского класса Product.