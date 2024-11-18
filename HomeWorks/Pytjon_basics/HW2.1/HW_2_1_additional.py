"""
Вы делаете MVP (минимально жизнеспособный продукт) dating-сервиса.
У вас есть список юношей и девушек.
Выдвигаем гипотезу: лучшие рекомендации получатся, если просто
отсортировать имена по алфавиту и познакомить людей с одинаковыми
индексами после сортировки. Но вы не будете никого знакомить, если кто-то
может остаться без пары.
Примеры работы программы:
boys = ['Peter', 'Alex', 'John', 'Arthur', 'Richard']
girls = ['Kate', 'Liza', 'Kira', 'Emma', 'Trisha']
Результат:
Идеальные пары:
Alex и Emma
Arthur и Kate
John и Kira
Peter и Liza
Richard и Trisha
boys = ['Peter', 'Alex', 'John', 'Arthur', 'Richard', 'Michael']
girls = ['Kate', 'Liza', 'Kira', 'Emma', 'Trisha']
Результат: Внимание, кто-то может остаться без пары!
"""

boys: str = input('Введите имена мужчин через пробел: ')
girls: str = input('Введите имена девушек через пробел: ')

# создаем списки
# boys = ['Peter', 'Alex', 'John', 'Arthur', 'Richard', 'Michael']
# girls = ['Kate', 'Liza', 'Kira', 'Emma', 'Trisha']
boys = boys.split(' ')
girls = girls.split(' ')

# boys.sort()
# girls.sort()
boys.sort()
girls.sort()

# print(boys)
# print(girls)
if len(boys) == len(girls):
    print('Идеальные пары:')
    #     for i in range(len(boys)):
    #         print(boys[i], 'и', girls[i])
    for i in range(len(boys)):
        print(boys[i], 'и', girls[i])
# если условие не выполняется
else:
    print('Внимание, кто-то может остаться без пары!')

