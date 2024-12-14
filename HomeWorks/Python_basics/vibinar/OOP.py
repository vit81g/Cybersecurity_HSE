"""
ООП вебинар
"""
from pyct.cmd import substitute_main


class Animal:
    def __init__(self, color, age):
        self.color = color
        self.age = int(age)

    def age_up(self):
        self.age += 1

cat = Animal(age=5, color='black')
cat.color = 'white'
print(cat.age, cat.color)

print(cat.age, cat.color)
print(repr(cat.age), repr(cat.color))


# создание класса
class Vihicle:
    # конструктор класса
    def __init__(self, make, model, year, price):
        self.make = make
        self.model = model
        self.year = year
        self.price = price

    # метод для вывода информации
    def display_info(self):
        print(f"Make: {self.make}")
        print(f"Model: {self.model}")
        print(f"Year: {self.year}")
        print(f"Price: {self.price}")
        print("---------------")

# наследование классов
class Airplane(Vihicle):
    def __init__(self, make, model, year, price, capacity):
        super().__init__(make, model, year, price)
        self.capacity = capacity

# наследование классов
class Submarine(Vihicle):
    def __init__(self, make, model, year, price, max_depth):
        super().__init__(make, model, year, price)
        self.max_depth = max_depth

# создание объектов классов
substitute_obj = Submarine(make='Broco', model='CB3456', year= 1983, max_depth=4000, price='more than you can pay')
aitplane_obj = Airplane(make='Boeing', model='737', year= 1994, capacity= 200, price='more than you can pay')

# метод для вывода информации
substitute_obj.display_info()
aitplane_obj.display_info()

# доступ к атрибутам
print(substitute_obj.max_depth)
print(aitplane_obj.capacity)


"""
Полиморфизм
"""

class Shape:
    def area(self):
        # реализация метода (пустая функция или пустой метод)
        pass

# наследование классов
class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side * self.side

# наследование классов
class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

#
class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius * self.radius

# создание объектов классов
square = Square(side=5)
rectangle = Rectangle(width=4, height=6)
circle = Circle(radius=3)

# вызов метода
print(square.area())
print(rectangle.area())
print(circle.area())



# множественное наследование классов пример "Ромб смерти"
class Person:

    def hello(self):
        print("Hello, Person")

class Student(Person):

    def hello(self):
        print("Hello, Student")

class Teacher(Person):

    def hello(self):
        print("Hello, Teacher")

class Worker(Student, Teacher):
    pass

# сначала идет (слева на право) Student, потом Teacher и берет первый вариант в котором есть метод
worker = Worker()
worker.hello()

