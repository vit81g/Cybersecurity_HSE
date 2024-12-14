"""
@property decorator
@getter
@setter
"""

class Person:
    def __init__(self, name1):
        self.name1 = name1

    @property
    def name1(self):
        print("Getting name")
        return f'{self.name1}'

#p = Person("John")
#print(p.name1)


"""
__add__
__eq__
"""
class Room:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.area = self.width * self.height

        def __add__(self, room_obj):
            if isinstance(room_obj, Room):
                return self.area + room_obj.area
            raise TypeError("Not a room")

        def __eq__(self, room_obj):
            if isinstance(room_obj, Room):
                return self.area == room_obj.area
            raise TypeError("Not a room")

room1 = Room(10, 20)
room2 = Room(10, 20)

#print(room1 + room2)
print(room1 != room2)
print(room1 == room2)
print(room1.area)
print(room1.width)


