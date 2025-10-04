# OpenPhish Parser (ДЗ 1)

Готовый сценарий `openphish_parser.py` для парсинга главной страницы https://openphish.com/ каждые 5 минут в течение 1 часа.
Данные сохраняются в CSV с дедупликацией по (url, attack_time).

## Запуск (локально)
```bash
pip install requests beautifulsoup4 pandas
python openphish_parser.py --interval 300 --duration 3600 --out openphish_data.csv
```

Для быстрого теста (раз в 10 секунд, 1 минута):
```bash
python openphish_parser.py --interval 10 --duration 60 --out test.csv
```

## Что сдавать
- Ссылка на Google Colab **или** GitHub с кодом.
- Google Таблица со сводкой (см. задание).
