"""
Напишите функцию date_range, которая возвращает список дат за период от start_date
до end_date. Даты должны вводиться в формате YYYY-MM-DD. В случае неверного
формата или при start_date > end_date должен возвращаться пустой список.
Примеры работы программы:
date_range(‘2022-01-01’, ‘2022-01-03’)
[‘2022-01-01’, ‘2022-01-02’, ‘2022-01-03’]
"""

# Импорт модуля datetime для работы с датами
import datetime

# Данные для проверки
data_string_start = '2022-01-01'
data_string_end = '2022-01-03'

# Функция для получения списка дат
def data_range(start_date, end_date):
    """
    :param start_date:
    :param end_date:
    :return:
    """
    # проверка валидности дат
    try:
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        # проверка дат
        if start_date > end_date:
            return []
        # формирование списка
        list_date = []
        # цикл по датам
        while start_date <= end_date:
            list_date.append(start_date.strftime('%Y-%m-%d'))
            start_date += datetime.timedelta(days=1)
        # возврат списка
        return list_date
    # вывод ошибки
    except ValueError:
        # возврат пустого списка
        return []

print(data_range(data_string_start, data_string_end))
print(data_range('2022-01-01', '2022-01-03'))
print(data_range('', ''))