import json

# Пример строк, которые нужно обработать
lines = [
    '{"user_id": "df85c3cd61", "category": "Бытовая техника"}',
    '{"user_id": "1840e0b9d4", "category": "Продукты"}',
    '{"user_id": "4e4f90fcfb", "category": "Электроника"}'
]

# Итоговый словарь
combined_dict = {}

# Цикл для обработки строк
for line in lines:
    # Преобразование строки в словарь
    record = json.loads(line)
    # Добавление записи в общий словарь
    combined_dict[record['user_id']] = record['category']

# Вывод результата
print(combined_dict)