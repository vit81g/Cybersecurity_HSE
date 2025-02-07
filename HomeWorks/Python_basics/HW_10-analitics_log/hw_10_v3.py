import json
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Парсинг аргументов командной строки
parser = argparse.ArgumentParser(description='Анализ событий информационной безопасности')
parser.add_argument('file_path', type=str, help='Путь к JSON-файлу с событиями')
args = parser.parse_args()

# Загрузка данных из JSON-файла
with open(args.file_path, 'r') as file:
    data = json.load(file)

df = pd.DataFrame(data['events'])

# Преобразование timestamp в datetime
# Это позволяет удобнее работать с датами и выполнять сортировку или фильтрацию
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Анализ данных: группировка по типу события
event_counts = df['signature'].value_counts()

# Визуализация распределения событий
# Устанавливает размер графика
plt.figure(figsize=(12, 8))
# Построение гистограммы. Строим столбчатый график
sns.barplot(y=event_counts.index, x=event_counts.values, palette='viridis')
# Установка названий осей. Подписываем ось X
plt.xlabel('Количество событий', fontsize=12)
# Установка названий осей. Подписываем ось Y
plt.ylabel('Тип события', fontsize=12)
# Установка названий графика. Заголовок графика
plt.title('Распределение событий информационной безопасности', fontsize=14)
# Установка размера шрифта
# Настраиваем размер шрифта оси X
plt.xticks(fontsize=10)
# Настраиваем размер шрифта оси Y
plt.yticks(fontsize=8)
# Установка размера легенды. Автоматически корректирует параметры графика, чтобы избежать наложения элементов
plt.tight_layout()
# Отображение графика
plt.show()
