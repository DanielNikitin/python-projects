from cat import Cat

meow_1 = Cat("Cat: Boost,", "male,", 1.5) # экземпляр класса
meow_2 = Cat("Cat: Chanel,", "female,", 3) # экземпляр класса

print(meow_1.get_name(), meow_1.get_sex(), meow_1.get_age())
print(meow_2.get_name(), meow_2.get_sex(), meow_2.get_age())


# Создайте класс Dog с помощью наследования класса Cat.
# Создайте метод get_pet() таким образом, чтобы он возвращал
# только имя и возраст

class Dog(Cat):
    def get_pet(self):
        return f'{self.get_name()} {self.get_age()}'

dog_1 = Dog("Dog: Boost,", "boy,", 2)
print(dog_1.get_pet())