"""
Напишите код на Python для решения следующей задачи.
Реализуйте функцию trim_and_repeat(), которая принимает три параметра:
● строку;
● offset — число символов, на которое нужно обрезать строку слева;
● repetitions — сколько раз нужно повторить строку перед возвратом получившейся строки.
Число символов для среза по умолчанию равно 0, а количество повторений — 1.
Функция должна возвращать полученную строку.
"""

# функция
def trim_and_repeat(text, offset=0, repetitions=1):
    """
    :param text:
    :param offset:
    :param repetitions:
    :return:
    """
    return text[offset:] * repetitions

# запрос строки
text: str = input('Введите текст: ')

# запрос параметров (offset)
offset_input: int = input('Введите число символов, на которое нужно обрезать строку слева (по умолчанию 0): ')
# если введено пустое значение, то offset = 0
offset_value: int = int(offset_input) if offset_input else 0
# запрос параметров (repetitions)
repetitions_input = input('Введите количество повторений (по умолчанию 1): ')
# если введено пустое значение, то repetitions = 1
repetitions_value = int(repetitions_input) if repetitions_input else 1

# вызов функции в print() с параметрами и ввод результата
print(trim_and_repeat(text, offset_value, repetitions_value))
#print(trim_and_repeat(text, 3))
#print(trim_and_repeat(text, 3, 2))
#print(trim_and_repeat(text, repetitions=2))