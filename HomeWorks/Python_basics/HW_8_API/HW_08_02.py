"""
Задание 2. Работа с параметрами запроса
 1. Используйте API OpenWeather для получения данных о погоде.
 2. Напишите программу, которая:
 a) принимает название города от пользователя,
 b) отправляет GET-запрос к API и выводит текущую температуру и
 описание погоды.
"""

from dotenv import load_dotenv
import os
import requests


"""
Проверка получения ключа из файла .env (нельзя хранить ключи API в коде, дополнительно информацию
можно зашифровать, а при запуске кода запускать расшифровку)
"""
# Загружаем переменные из файла .env
load_dotenv()

# Получаем ключ API
api_key = os.getenv("OPENWEATHER_API_KEY")

if not api_key:
    raise ValueError("Ключ API не найден! Убедитесь, что файл .env содержит ключ.")

print(f"Ваш ключ API: {api_key}")

"""
Решение задания
"""

# Получение ключа API из .env
api_key = os.getenv("OPENWEATHER_API_KEY")

if not api_key:
    raise ValueError("Ключ API не найден! Убедитесь, что файл .env содержит ключ API и он правильно указан.")

# Ваш код запроса
url = "https://api.openweathermap.org/data/2.5/weather"
city = input("Введите название города: ")

params = {
    "q": city,
    "appid": api_key,
    "units": "metric",  # Температура в градусах Цельсия
    "lang": "ru"  # Ответ на русском языке
}

# обработка ошибок
try:
    # Отправка GET-запроса
    response = requests.get(url, params=params)
    response.raise_for_status()  # Проверка на успешность запроса
    weather_data = response.json()

    # Извлечение данных о погоде
    temperature = weather_data["main"]["temp"]
    description = weather_data["weather"][0]["description"]

    print(f"В городе {city} сейчас {temperature}°C.")
    print(f"Погодные условия: {description}.")
except requests.exceptions.RequestException as e:
    print(f"Ошибка при выполнении запроса: {e}")
except KeyError:
    print("Ошибка обработки данных. Проверьте корректность введённого города.")
