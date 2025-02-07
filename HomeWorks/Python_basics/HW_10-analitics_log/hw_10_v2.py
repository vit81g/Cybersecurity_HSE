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
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Анализ данных: группировка по типу события
event_counts = df['signature'].value_counts()

# Визуализация распределения событий
plt.figure(figsize=(10, 6))
sns.barplot(y=event_counts.index, x=event_counts.values, palette='viridis')
plt.xlabel('Количество событий', fontsize=12)
plt.ylabel('Тип события', fontsize=12)
plt.title('Распределение событий информационной безопасности', fontsize=12)
plt.show()
