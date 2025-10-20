import pandas as pd
import numpy as np
from urllib.parse import urlparse
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score

# Шаг 1: Загрузка данных
train_df = pd.read_csv('train.csv')  # >64000 строк
test_df = pd.read_csv('test.csv')  # 16000 строк


# Шаг 2: Извлечение признаков (feature engineering)
def extract_features(url):
    parsed_url = urlparse(url)
    features = {}

    # Длина URL
    features['url_length'] = len(url)

    # Наличие IP в домене (регулярка: \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})
    features['has_ip'] = 1 if re.match(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$', parsed_url.netloc) else 0

    # Количество поддоменов (точек в netloc)
    features['num_subdomains'] = parsed_url.netloc.count('.')

    # HTTPS (проверка scheme)
    features['has_https'] = 1 if parsed_url.scheme == 'https' else 0

    # Специальные символы
    features['num_special_chars'] = sum(1 for c in url if c in ['@', '-', '%', '=', '&', '?'])

    # Подозрительные слова (список из статьи IEEE)
    suspicious_words = ['login', 'secure', 'bank', 'update', 'paypal', 'account', 'verify']
    features['suspicious_words'] = sum(1 for word in suspicious_words if word in url.lower())

    return features


# Применяем к train и test
train_features = pd.DataFrame([extract_features(url) for url in train_df['url']])
test_features = pd.DataFrame([extract_features(url) for url in test_df['url']])

# Добавляем TF-IDF векторизацию URL как текста (char level, ngram 2-5)
vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 5), max_features=5000)
train_tfidf = vectorizer.fit_transform(train_df['url'])
test_tfidf = vectorizer.transform(test_df['url'])

# Объединяем признаки
X_train = np.hstack((train_tfidf.toarray(), train_features.values))
X_test = np.hstack((test_tfidf.toarray(), test_features.values))
y_train = train_df['result']

# Шаг 3: Обучение модели (RandomForest, как в PDF)
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Кросс-валидация (5 folds) для оценки
cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
print(f'Средняя точность на CV: {cv_scores.mean():.4f} (STD: {cv_scores.std():.4f})')  # Ожидаемо ~0.92-0.95

# Разделение на train/val для финальной проверки
X_tr, X_val, y_tr, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)
model.fit(X_tr, y_tr)
val_pred = model.predict(X_val)
print(f'Точность на валидации: {accuracy_score(y_val, val_pred):.4f}')

# Шаг 4: Предсказание на test
model.fit(X_train, y_train)  # Обучаем на полном train
test_pred = model.predict(X_test)

# Шаг 5: Сохранение сабмита
submit_df = pd.DataFrame({'Id': range(len(test_df)), 'Predicted': test_pred})
submit_df.to_csv('submit.csv', index=False)
print('Файл submit.csv сохранен. Формат: Id,Predicted')