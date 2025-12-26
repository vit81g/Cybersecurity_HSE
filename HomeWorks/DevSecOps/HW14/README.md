# Итоговое домашнее задание  
## по дисциплине «Разработка защищённых программных систем»

**Студент:** Novikov V. S.  
**Группа:** МКБ-241  
**Преподаватель:** Телепов Владимир  
**Дата выполнения:** 26 декабря 2025 года  

---

## Структура репозитория

```text
HW14/
├── DAST/
│   └── 2025-12-26-ZAP-Report-.html
├── SAST/
│   └── semgrep-report.json
├── solution/
│   └── NVS_DevSecOps.docx
├── task/
│   └── Итог.pdf
└── README.md
```

---

## Этап 0. Изучение теоретических материалов

На данном этапе были изучены лекционные и практические материалы по следующим темам:

- статический анализ исходного кода (SAST);
- динамический анализ веб-приложений (DAST);
- моделирование угроз;
- базовые подходы к secure code review.

Также были повторены предыдущие домашние задания по дисциплине.

**Источник:**  
Методические указания «Итог-1.pdf», стр. 2, раздел *«Этап 0»*.

---

## Этап 1. Клонирование и запуск проекта

В качестве объекта исследования выбран **вариант 5**.

### Исходный проект

GitHub-репозиторий:  
https://github.com/dharaneesh71/API-Secure-A-Flask-Based-Web-Application-Security-Simulator

### Клонирование репозитория

```bash
git clone https://github.com/dharaneesh71/API-Secure-A-Flask-Based-Web-Application-Security-Simulator.git
cd API-Secure-A-Flask-Based-Web-Application-Security-Simulator
```

### Подготовка окружения

```bash
pip install flask sqlalchemy bleach flask-limiter flask-sqlalchemy requests
```

### Запуск приложения

```bash
python secure_API/file1.py
```

Приложение доступно по адресу:  
http://127.0.0.1:5000

---

## Этап 2. Сканирование SAST и DAST

### SAST — Semgrep

```bash
pip install semgrep
semgrep scan --config auto --json > semgrep-report.json secure_API
```

Результат: выявлено 5 предупреждений уровня Medium/High.  
Отчёт сохранён в `SAST/semgrep-report.json`.

### DAST — OWASP ZAP

```bash
sudo apt install zaproxy
```

Проведён активный автоматический скан приложения  
`http://127.0.0.1:5000`.

Результат: выявлено 11 находок (Medium, Low, Informational).  
Отчёт сохранён в `DAST/2025-12-26-ZAP-Report-.html`.

---

## Этап 3. Анализ выявленных проблем

- Проанализированы все находки выше уровня Low.
- Для каждой уязвимости определено, является ли она ложным срабатыванием.
- Для уязвимостей уровня Medium сформированы рекомендации.

Критических (High) уязвимостей не выявлено.

Подробный анализ представлен в файле:  
`solution/NVS_DevSecOps.docx`.

---

## Выводы

В рамках работы выполнен полный цикл анализа безопасности (SAST + DAST),  
проведена интерпретация результатов и сформированы рекомендации по повышению защищённости веб-приложения.
