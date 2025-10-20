import pandas as pd
import numpy as np
from urllib.parse import urlparse
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, cross_val_score

# Шаг 1: Загрузка данных (добавлены with_content)
train_df = pd.read_csv('train.csv')
test_df = pd.read_csv('test.csv')
train_content_df = pd.read_csv('train_with_content.csv')  # Предполагаем столбцы: url, content, result
test_content_df = pd.read_csv('test_with_content.csv')  # url, content

# Объединяем с базовыми (если content отдельно)
train_df = train_df.merge(train_content_df[['url', 'content']], on='url', how='left')
test_df = test_df.merge(test_content_df[['url', 'content']], on='url', how='left')


# Шаг 2: Извлечение признаков (добавлены из content)
def extract_features(url, content=''):
    parsed_url = urlparse(url)
    features = {}
    features['url_length'] = len(url)
    features['has_ip'] = 1 if re.match(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$', parsed_url.netloc) else 0
    features['num_subdomains'] = parsed_url.netloc.count('.')
    features['has_https'] = 1 if parsed_url.scheme == 'https' else 0
    features['num_special_chars'] = sum(1 for c in url if c in ['@', '-', '%', '=', '&', '?'])
    suspicious_words_url = ['login', 'secure', 'bank', 'update']
    features['suspicious_words_url'] = sum(1 for word in suspicious_words_url if word in url.lower())

    # Признаки из content (если доступен)
    if content:
        features['has_login_form'] = 1 if '<form' in content.lower() and 'password' in content.lower() else 0
        suspicious_words_content = ['login', 'password', 'verify', 'account']
        features['suspicious_words_content'] = sum(1 for word in suspicious_words_content if word in content.lower())
    else:
        features['has_login_form'] = 0
        features['suspicious_words_content'] = 0

    return features


train_features = pd.DataFrame([extract_features(row['url'], row.get('content', '')) for _, row in train_df.iterrows()])
test_features = pd.DataFrame([extract_features(row['url'], row.get('content', '')) for _, row in test_df.iterrows()])

# TF-IDF для URL
url_vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 5), max_features=5000)
train_url_tfidf = url_vectorizer.fit_transform(train_df['url'])
test_url_tfidf = url_vectorizer.transform(test_df['url'])

# TF-IDF для content (если есть)
content_vectorizer = TfidfVectorizer(max_features=2000)
train_content_tfidf = content_vectorizer.fit_transform(train_df['content'].fillna(''))
test_content_tfidf = content_vectorizer.transform(test_df['content'].fillna(''))

# Объединение
X_train = np.hstack((train_url_tfidf.toarray(), train_content_tfidf.toarray(), train_features.values))
X_test = np.hstack((test_url_tfidf.toarray(), test_content_tfidf.toarray(), test_features.values))
y_train = train_df['result']

# Шаг 3: Обучение (RandomForest)
model = RandomForestClassifier(n_estimators=100, random_state=42)
cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
print(f'Средняя точность на CV: {cv_scores.mean():.4f}')  # Ожидаемо ~0.95+ с content

X_tr, X_val, y_tr, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)
model.fit(X_tr, y_tr)
print(f'Точность на валидации: {accuracy_score(y_val, model.predict(X_val)):.4f}')

# Шаг 4: Предсказание и сабмит
model.fit(X_train, y_train)
test_pred = model.predict(X_test)
submit_df = pd.DataFrame({'Id': range(len(test_df)), 'Predicted': test_pred})
submit_df.to_csv('submit.csv', index=False)