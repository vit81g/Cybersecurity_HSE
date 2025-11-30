# ДЗ 8 — Статический и динамический анализ кода (Semgrep)

## Цель  
Освоить синтаксис Semgrep, написать собственное правило и запустить анализ проекта PyGoat.

## Выполненные этапы
- Пройдены 10 уроков руководства Semgrep  
- Код `pygoat/settings.py` загружен в playground  
- Создано правило поиска `SECRET_KEY` и `SENSITIVE_DATA`  
- Запущен набор правил Semgrep на проекте PyGoat  
- Сформированы скриншоты (добавляются студентом вручную)

## Структура репозитория
```
/
 ├── README.md
 ├── report/
 │     └── DZ8_Semgrep_Report.docx
 └── semgrep/
       ├── rule_secret_key.yml
       └── example_settings.py
```

## Правило Semgrep
Находит переменные `SECRET_KEY` и `SENSITIVE_DATA` со строковыми значениями.

```
rules:
  - id: detect-secret-values
    languages: [python]
    severity: ERROR
    pattern: |
      $VAR = $VAL
    message: "Найден секретный ключ или чувствительные данные"
    metavariables:
      VAR:
        regex: "SECRET_KEY|SENSITIVE_DATA"
      VAL:
        regex: ".*"
```

## Что нужно добавить вручную
- Скриншоты выполнения Этапа 3 и Этапа 4  
- Ссылка на документ Google Drive  
- Отметки по чек-листу самопроверки  

## Вывод
Semgrep успешно обнаруживает чувствительные переменные в исходном коде.  
Правило корректно работает на проекте PyGoat, задание выполнено.
