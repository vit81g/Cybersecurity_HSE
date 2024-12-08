"""
Реализуйте функцию sum_distance(from, to), которая суммирует все числа от
значения from до величины to включительно.
Примечание. Если пользователь задаст первое число, которое окажется
больше второго, просто поменяйте их местами.
"""

# функция суммирования чисел
def sum_distance(from_value, to_value):
    """
    Функция суммирования
    :param from_value:
    :param to_value:
    :return:
    """
    if from_value > to_value:
        # меняем местами при необходимости
        from_value, to_value = to_value, from_value

    # суммируем числа
    return sum(range(from_value, to_value + 1))

# Получение чисел от пользователя
from_value = int(input("Введите начальное значение: "))
to_value = int(input("Введите конечное значение: "))

# Вычисление и вывод результата - запуск функции с двумя параметрами
result = sum_distance(from_value, to_value)
# вывод результата
print(f"Сумма чисел от {from_value} до {to_value} включительно: {result}")