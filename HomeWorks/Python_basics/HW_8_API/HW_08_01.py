"""
Задание1.ПолучениеданныхизпубличногоAPI
 1. ВыберитепубличныйAPI.Например,JSONPlaceholder.
 2. Напишитескрипт,который:
  отправляетGET-запроск/posts,
  извлекает и выводит заголовки и тела первых 5 постов
"""

import requests
url = "https://jsonplaceholder.typicode.com/posts"

# обработка ошибок/исключений
try:
    # Отправляем GET-запрос
    response = requests.get(url)
    response.raise_for_status()  # Проверка на успешность запроса

    # Извлекаем первые 5 постов  [:5] вернёт пять первых элемента
    posts = response.json()[:2]

    # Выводим заголовки и тела постов
    for i, post in enumerate(posts, 1):
        print(f"Пост {i}:")
        print(f"Заголовок: {post['title']}")
        print(f"Тело: {post['body']}")
        # В данном случае строка "-" повторяется 50 раз, создавая строку из 50 дефисов
        print("-" * 50)
except requests.exceptions.RequestException as e:
    print(f"Ошибка запроса: {e}")