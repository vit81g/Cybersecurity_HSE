"""
Переведите содержимое файла purchase_log.txt в словарь purchases вида:
{'1840e0b9d4': 'Продукты', ...}
Пример работы программы при выводе первых двух элементов словаря
purchases:
1840e0b9d4 ‘Продукты‘
4e4f90fcfb ‘Электроника‘
"""

# импортируем модуль json для перевода строки в словарь
import json
from fileinput import close

# открываем и читаем файл purchase_log.txt в кодировке utf-8
with open('purchase_log.txt', 'r', encoding='utf-8') as file:
    # проходим по каждой строке файла
    for line in file:
        # переводим строку в словарь
        data_dict = json.loads(line)
        # выводим словарь с ключами user_id и category
        print(data_dict.get('user_id'), data_dict.get('category'))

# закрываем файл
file.close()




















