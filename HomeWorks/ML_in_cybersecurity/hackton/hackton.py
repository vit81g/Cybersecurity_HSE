"""
Описание:
    Скрипт реализует полный pipeline:
        1. Загрузка данных (train.csv, test.csv)
        2. Извлечение признаков из URL (feature engineering)
        3. Векторизация URL с помощью TF-IDF (на уровне символов)
        4. Объединение признаков
        5. Обучение модели RandomForestClassifier
        6. Кросс-валидация, оценка на hold-out валидации
        7. Предсказание и сохранение сабмита в формате Id,Predicted

Зависимости:
    pandas, numpy, scikit-learn
"""

import pandas as pd
import numpy as np
from urllib.parse import urlparse
import re
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score



# Шаг 1. Загрузка данных
# train.csv — обучающая выборка (около 64 000 строк)
# test.csv  — тестовая выборка (около 16 000 строк)
train_df = pd.read_csv('train.csv')
test_df = pd.read_csv('test.csv')



# Шаг 2. Извлечение признаков (Feature Engineering)

def extract_features(url: str) -> dict:
    """
    Извлекает ручные (tabular) признаки из URL.
    Аргументы: url (str): исходный URL-адрес
    Возвращает: dict: словарь признаков с числовыми значениями
              {
                'url_length': длина строки URL,
                'has_ip': 1/0 (наличие IP-адреса в домене),
                'num_subdomains': количество поддоменов (точек),
                'has_https': 1/0 (наличие HTTPS),
                'num_special_chars': количество символов из набора '@-%=&?',
                'suspicious_words': количество встреч подозрительных токенов
              }
    """

    # Парсим URL для извлечения домена, схемы, пути и т.д.
    parsed_url = urlparse(url)
    features = {}

    # Длина URL
    features['url_length'] = len(url)

    # Проверка, содержит ли домен IP-адрес
    # шаблон IPv4: 111.222.333.444
    features['has_ip'] = 1 if re.match(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$', parsed_url.netloc) else 0

    # Количество поддоменов (число точек в netloc)
    features['num_subdomains'] = parsed_url.netloc.count('.')

    # Используется ли HTTPS в схеме
    features['has_https'] = 1 if parsed_url.scheme == 'https' else 0

    # Подсчёт специальных символов
    special_chars = ['@', '-', '%', '=', '&', '?']
    features['num_special_chars'] = sum(1 for c in url if c in special_chars)

    # Подозрительные слова, часто встречающиеся во фишинговых ссылках
    suspicious_words = ['login', 'secure', 'bank', 'update', 'paypal', 'account', 'verify']
    features['suspicious_words'] = sum(1 for word in suspicious_words if word in url.lower())

    return features


# Применяем функцию ко всем URL в обучающем и тестовом наборе
train_features = pd.DataFrame([extract_features(url) for url in train_df['url']])
test_features = pd.DataFrame([extract_features(url) for url in test_df['url']])



# Шаг 3. TF-IDF векторизация URL как текста (на уровне символов)
# Используем n-граммы (от 2 до 5 символов), ограничивая размер словаря до 5000.
# Это позволяет улавливать локальные паттерны (например, ".ru/", "http", "//lo").
vectorizer = TfidfVectorizer(
    analyzer='char',         # анализ на уровне символов
    ngram_range=(2, 5),      # биграммы–пентаграммы
    max_features=5000        # ограничение числа признаков
)

# Преобразуем train/test URL в TF-IDF матрицы
train_tfidf = vectorizer.fit_transform(train_df['url'])
test_tfidf = vectorizer.transform(test_df['url'])

# Шаг 4. Объединение признаков
# Преобразуем разреженную TF-IDF матрицу в плотный формат и конкатенируем с табличными фичами.
X_train = np.hstack((train_tfidf.toarray(), train_features.values))
X_test = np.hstack((test_tfidf.toarray(), test_features.values))

# Целевая переменная
y_train = train_df['result']

# Шаг 5. Обучение модели (RandomForestClassifier)
# RandomForestClassifier — ансамбль деревьев решений.
# Он устойчив к шуму, обрабатывает как числовые, так и бинарные признаки.
model = RandomForestClassifier(
    n_estimators=100,       # количество деревьев в ансамбле
    random_state=42         # фиксируем зерно для воспроизводимости
)



# Шаг 6. Кросс-валидация (оценка стабильности модели)
cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
print(f"Средняя точность на CV: {cv_scores.mean():.4f} (STD: {cv_scores.std():.4f})")

# Шаг 7. Разделение train/validation и оценка модели
# Разделяем данные для финальной проверки (20% hold-out)
X_tr, X_val, y_tr, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# Обучаем модель на 80% данных
model.fit(X_tr, y_tr)

# Предсказываем на валидационном наборе
val_pred = model.predict(X_val)

# Выводим точность
val_accuracy = accuracy_score(y_val, val_pred)
print(f"Точность на валидации: {val_accuracy:.4f}")



# Шаг 8. Финальное обучение и предсказание на test.csv
# Обучаем модель на всём тренировочном наборе
model.fit(X_train, y_train)

# Предсказываем для тестовых данных
test_pred = model.predict(X_test)



# Шаг 9. Сохранение предсказаний (submit.csv)

submit_df = pd.DataFrame({
    'Id': range(len(test_df)),
    'Predicted': test_pred
})

submit_df.to_csv('submit.csv', index=False)
print("Файл submit.csv сохранен. Формат: Id,Predicted")
