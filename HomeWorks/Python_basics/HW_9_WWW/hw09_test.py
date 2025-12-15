"""
Описание задания
Прежде чем выполнять задание:
1. Посмотрите запись видеолекции и вебинара по теме 10 «Взаимодействие Python с WWW».
2. Установите Scapy для работы в Python. Для этого можно использовать команду pip install scapy.

Этапы выполнения задания
Этап 1. Изучение Scapy
● Изучите основы работы с Scapy по документации.
● Настройте Scapy для перехвата HTTP-трафика, используйте скрипт scapy для отправки HTTP-запросов.

Этап 2. Анализ трафика
● Ознакомьтесь с инструментом Google Gruyere и запустите его.
● Запустите Scapy и начните собирать трафик, взаимодействуя с сайтом Google Gruyere.
● Проанализируйте полученные данные, обращая внимание на запросы и ответы HTTP.

Этап 3. Эксплуатация XSS
● Осуществите рекон-анализ сайта Google Gruyere для поиска потенциальных точек входа XSS.
● Попытайтесь эксплуатировать уязвимости XSS, используя обнаруженные точки.
Примеры XSS-атак:
<script>alert('XSS')</script>
<img src="nonexistent.jpg" onerror="alert('XSS')">
● Запишите все свои шаги эксплуатации уязвимостей и полученные результаты, сделайте скриншоты.

Этап 4. Анализ результатов
● Используя Scapy, проанализируйте, как XSS-атака отображается в сетевом трафике (проанализируйте ответ на HTTP-запрос).
● Опишите, какие изменения в трафике произошли во время XSS-атаки.

Этап 5. Отчёт
Подготовьте отчёт: опишите процесс эксплуатации XSS, анализ трафика, выводы и рекомендации по устранению найденных уязвимостей.

Чек-лист самопроверки
Критерии выполнения задания Отметка
о выполнении
Настроен Scapy для перехвата HTTP-трафика ●
Запущен Scapy и выполнен сбор трафика во время взаимодействия с сайтом Google Gruyere ●
Проанализированы полученные запросы и ответы HTTP ●
Проведён рекон-анализ сайта Google Gruyere для поиска потенциальных точек входа XSS ●
Проведена эксплуатация уязвимости XSS ●
Найдены следы XSS-атаки в сетевом трафике ●
Описаны изменения в трафике, которые произошли во время XSS-атаки ●
Подготовлен отчёт:
● Описаны действия, выполненные при эксплуатации уязвимости XSS и представлены скриншоты результатов
● Описан анализ трафика
● Представлены скриншоты следов XSS- атаки в сетевом трафике
● Представлены выводы и рекомендации по устранению найденных уязвимостей
● В LMS прикреплена ссылка на файл с отчётом
● Файл доступен для просмотра другим пользователям, название файла содержит фамилию и имя студента, номер ДЗ
●

Ссылки для 1 этапа:
https://gist.github.com/richarddun/1bb11d32cafc394efbcb8f4a8b6cb130
https://scapy.readthedocs.io/en/latest/layers/http.html
"""

import scapy.all as scapy
import requests
from bs4 import BeautifulSoup
import webbrowser

url = "https://google.com"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
}

# Отправляем GET-запрос
response = requests.get(url, headers=headers)

# Извлекаем содержимое страницы
html_content = response.content

# Создаем объект BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Находим все ссылки на странице
links = soup.find_all("a")

# Перехватываем HTTP-трафик с помощью Scapy
def packet_callback(packet):
    if packet.haslayer(scapy.HTTPRequest):
        print("HTTP Request:")
        print(packet[scapy.HTTPRequest].show())
    elif packet.haslayer(scapy.HTTPResponse):
        print("HTTP Response:")
        print(packet[scapy.HTTPResponse].show())

# Запускаем перехват с помощью Scapy
scapy.sniff(prn=packet_callback, store=0)

# Открываем страницу в браузере
webbrowser.open(url)

# Просматриваем содержимое страницы
print(html_content)

# Просматриваем ссылки на странице
for link in links:
    print(link.get("href"))

# Просматриваем заголовки страницы
print(response.headers)

# Просматриваем тело страницы
print(response.text)

# Просматриваем статус код страницы
print(response.status_code)

# Просматриваем кодировку страницы
print(response.encoding)

# Просматриваем размер страницы
print(response.headers["Content-Length"])

# Просматриваем время загрузки страницы
print(response.elapsed.total_seconds())

# Просматриваем заголовки страницы
print(response.headers)

