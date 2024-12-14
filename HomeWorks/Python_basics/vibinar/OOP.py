"""
ООП вебинар
"""

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

