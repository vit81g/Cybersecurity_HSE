import argparse

# Создаем парсер аргументов
parser = argparse.ArgumentParser(description='Сложение двух чисел')

# Добавляем два аргумента: первое и второе число
parser.add_argument('num1', type=float, help='Первое число')
parser.add_argument('num2', type=float, help='Второе число')

# Парсим аргументы
args = parser.parse_args()

# Складываем числа
result = args.num1 + args.num2

# Выводим результат
print(f'Результат: {args.num1} + {args.num2} = {result}')
