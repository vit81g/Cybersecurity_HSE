"""
wine_analysis.py
=================

Практическая работа №2 по дисциплине "Применение ML в кибербезопасности".
Тема: применение статистики и визуализации данных.

Цель:
- изучение и визуализация данных о качестве вина (красное и белое);
- проверка данных на пропуски и выбросы;
- формирование бинарной метки ("хорошее"/"плохое" вино);
- анализ распределений и корреляций между признаками.

"""
# 1. Импорт библиотек
import pandas as pd  # Для анализа данных и таблиц
import numpy as np  # Для числовых расчётов
import matplotlib.pyplot as plt  # Для построения графиков
import seaborn as sns  # Для продвинутой визуализации



# 2. Загрузка и первичная обработка данных
def load_data(file_path: str) -> pd.DataFrame:
    """
    Загружает данные о вине из CSV-файла.
    Args: file_path (str) - путь к CSV-файлу (например, 'winequality-red.csv').
    Returns: pd.DataFrame - таблица с данными о химических свойствах и качестве вина.
    """
    df = pd.read_csv(file_path, sep=';')  # В оригинале используется ';' как разделитель
    return df


def check_missing_data(df: pd.DataFrame) -> pd.Series:
    """
    Проверяет наличие пропущенных значений в датасете.
    Args: df (pd.DataFrame) - исходный датафрейм.
    Returns: pd.Series - количество пропусков по каждому столбцу.
    """
    return df.isnull().sum()


def add_binary_quality(df: pd.DataFrame) -> pd.DataFrame:
    """
    Добавляет бинарную метку "хорошее вино" (1 — качество >= 6, 0 — иначе).
    Args: df (pd.DataFrame) - исходный датафрейм с признаком 'quality'.
    Returns: pd.DataFrame - новый датафрейм с дополнительным столбцом 'good_quality'.
    """
    df['good_quality'] = (df['quality'] >= 6).astype(int)
    return df

# 3. Анализ выбросов и статистика


def remove_outliers(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Удаляет выбросы по указанному столбцу, используя межквартильный размах (IQR).
    Args: df (pd.DataFrame) - исходный датафрейм и column (str) - название столбца для анализа выбросов.
    Returns: pd.DataFrame - датафрейм без выбросов.
    """
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    print(f"\n[{column}] Q1={Q1}, Q3={Q3}, IQR={IQR}")
    print(f"Допустимый диапазон: {lower_bound:.2f} — {upper_bound:.2f}")

    df_filtered = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    print(f"Удалено выбросов: {len(df) - len(df_filtered)} строк")
    return df_filtered


def compute_medians(df: pd.DataFrame) -> pd.Series:
    """
    Вычисляет медиану по каждому признаку.
    Args: df (pd.DataFrame) - датафрейм без выбросов.
    Returns: pd.Series - медианные значения признаков.
    """
    return df.median(numeric_only=True)



# 4. Визуализация данных

def plot_quality_distribution(df: pd.DataFrame):
    """Строит график распределения по качеству вина."""
    plt.figure(figsize=(8, 5))
    sns.histplot(df['quality'], kde=True, color='skyblue', bins=10)
    plt.title("Распределение качества вина")
    plt.xlabel("Качество")
    plt.ylabel("Количество образцов")
    plt.grid(True)
    plt.show()


def plot_binary_balance(df: pd.DataFrame):
    """Строит график баланса бинарных классов (0 — плохое, 1 — хорошее)."""
    plt.figure(figsize=(6, 4))
    sns.countplot(x='good_quality', hue='good_quality', data=df, palette='Set2', legend=False)
    plt.title("Баланс классов по качеству вина")
    plt.xlabel("Класс (0 — плохое, 1 — хорошее)")
    plt.ylabel("Количество образцов")
    plt.show()


def plot_boxplot_quality(df: pd.DataFrame):
    """Строит график 'ящик с усами' для признака качества."""
    plt.figure(figsize=(6, 5))
    sns.boxplot(y='quality', data=df, color='lightgreen')
    plt.title("Ящик с усами по показателю качества")
    plt.ylabel("Качество")
    plt.show()


def plot_feature_distributions(df: pd.DataFrame):
    """Строит распределения для всех числовых признаков."""
    df_features = df.drop(columns=['quality', 'good_quality'])
    df_features.hist(bins=20, figsize=(15, 10), color='orange', edgecolor='black')
    plt.suptitle("Распределения признаков вина")
    plt.show()


def plot_correlation_matrix(df: pd.DataFrame):
    """Строит тепловую карту корреляции между признаками."""
    plt.figure(figsize=(12, 10))
    corr = df.corr(numeric_only=True)
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Матрица корреляции признаков вина")
    plt.show()



# 5. Основной блок выполнения

def main():
    """
    Основная функция анализа данных:
    - загружает датасет;
    - проверяет пропуски;
    - добавляет бинарную метку;
    - удаляет выбросы;
    - строит визуализации.
    """
    # Загрузка данных о красном вине
    df_red = load_data("winequality-red.csv")
    print(f"Загружено {len(df_red)} строк данных о красном вине.")

    # Проверка пропусков
    print("\nПроверка пропусков:")
    print(check_missing_data(df_red))

    # Добавляем бинарный класс
    df_red = add_binary_quality(df_red)

    # Удаляем выбросы по столбцу "quality"
    df_red_clean = remove_outliers(df_red, 'quality')

    # Визуализации
    plot_quality_distribution(df_red_clean)
    plot_binary_balance(df_red_clean)
    plot_boxplot_quality(df_red_clean)
    plot_feature_distributions(df_red_clean)
    plot_correlation_matrix(df_red_clean)

    # Медианные значения
    print("\nМедианные значения признаков:")
    print(compute_medians(df_red_clean))


# =============================================================
# 6. Точка входа
# =============================================================

if __name__ == "__main__":
    main()
