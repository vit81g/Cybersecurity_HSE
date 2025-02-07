import sys
import dask.dataframe as dd
import matplotlib.pyplot as plt
import seaborn as sns

# Проверка наличия аргумента командной строки
if len(sys.argv) < 2:
    print("Ошибка: укажите имя JSON-файла!")
    sys.exit(1)

file_path = sys.argv[1]  # Получаем путь к файлу из аргументов командной строки

# Загрузка данных в потоковом режиме с использованием Dask
df = dd.read_json(file_path, lines=True)

# Преобразование timestamp в datetime
df['timestamp'] = dd.to_datetime(df['timestamp'])

# Анализ данных: группировка по типу события (ленивая загрузка)
event_counts = df['signature'].value_counts().compute()

# Визуализация распределения событий
plt.figure(figsize=(12, 8))  # Устанавливает размер графика
sns.barplot(y=event_counts.index, x=event_counts.values, palette='viridis')  # Строим столбчатый график
plt.xlabel('Количество событий', fontsize=12)  # Подписываем ось X
plt.ylabel('Тип события', fontsize=12)  # Подписываем ось Y
plt.title('Распределение событий информационной безопасности', fontsize=14)  # Заголовок графика
plt.xticks(fontsize=10)  # Настраиваем размер шрифта оси X
plt.yticks(fontsize=8)  # Настраиваем размер шрифта оси Y
plt.tight_layout()  # Автоматически корректирует параметры графика, чтобы избежать наложения элементов
plt.show()  # Отображаем график
