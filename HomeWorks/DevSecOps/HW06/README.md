# 🧩 Домашнее задание №6 — Средства защиты приложений (SAST & DAST)

**Дисциплина:** Разработка защищённых программных систем  
**Тема:** Средства защиты приложений (Bandit, OWASP ZAP, Trivy)  
**Преподаватель:** Владимир Телепов  
**Цель:** Научиться использовать средства анализа безопасности приложений — SAST и DAST.  
**Время выполнения:** 1,5–2 часа  

---

## ⚙️ Используемые инструменты

- **Python 3.11**, **pip**, **venv**  
- **Bandit** — статический анализ Python-кода  
- **OWASP ZAP 2.15.0** — динамическое тестирование веб-приложения  
- **JDK 17** — необходим для работы ZAP  
- **Docker** — контейнеризация PyGoat  
- **Trivy, Hadolint** — дополнительные проверки DevSecOps-процесса

---

## 📂 Структура проекта

```
HW06/
├── bash/
│   ├── [bandit.txt](bash/bandit.txt)
│   ├── [goat.txt](bash/goat.txt)
│   └── [ZAP.txt](bash/ZAP.txt)
│
├── SAST/
│   └── [bandit_report.txt](SAST/bandit_report.txt)
│
├── DAST/
│   └── [2025-10-20-ZAP-Report-.html](DAST/2025-10-20-ZAP-Report-.html)
│
├── docs/
│   └── Тема 6 «Средства защиты приложений»-1.pdf
│
├── screens/
│   ├── start_goat.jpg
│   ├── SAST_bandit.jpg
│   └── ZAP.jpg
│
└── README.md
```

---

## 🧰 Этап 1. Установка JDK и OWASP ZAP

ZAP требует установленный JDK версии ≥11. Использован **openjdk-17-jdk**.

```bash
sudo apt update
sudo apt install -y openjdk-17-jdk
cd ~/Downloads
chmod +x ZAP_2_15_0_unix.sh
sudo ./ZAP_2_15_0_unix.sh
```

📄 Команды сохранены в [bash/ZAP.txt](bash/ZAP.txt)

После установки ZAP запускается через:
```bash
/opt/ZAP_2_15_0/zap.sh
```

GUI-скан выполнен через **Quick Start → Automated Scan**, URL:
```
http://127.0.0.1:8000
```

---

## 🧩 Этап 2. Установка и настройка Bandit (SAST)

Bandit устанавливался через `pip` в виртуальное окружение:
```bash
sudo apt install -y python3-pip python3-venv
python3 -m venv ~/bandit_env
source ~/bandit_env/bin/activate
pip install bandit
bandit --version
```

Запуск анализа PyGoat:
```bash
cd ~/devsecops/hw02/PyGoat-master
bandit -r . -ll -f txt -o bandit_report.txt
deactivate
```

📄 Отчёт — [SAST/bandit_report.txt](SAST/bandit_report.txt)  
📸 Скриншот — [screens/SAST_bandit.jpg](screens/SAST_bandit.jpg)

---

## 🐍 Этап 3. Запуск приложения PyGoat

```bash
cd ~/devsecops/hw02/PyGoat-master
sudo docker build -t pygoat:latest .
sudo docker run -d --name pygoat -p 8000:8000 pygoat:latest
```

Проверка:
```
curl http://localhost:8000
```
📸 Скриншот запуска — [screens/start_goat.jpg](screens/start_goat.jpg)

---

## ☣️ Этап 4. Проведение DAST-теста OWASP ZAP (GUI)

1. Запустить ZAP:  
   ```bash
   /opt/ZAP_2_15_0/zap.sh
   ```
2. В **Automated Scan** указать:
   ```
   http://127.0.0.1:8000
   ```
3. Нажать **Attack**, дождаться завершения.
4. Сохранить отчёт в HTML.

📄 Отчёт — [DAST/2025-10-20-ZAP-Report-.html](DAST/2025-10-20-ZAP-Report-.html)  
📸 Скриншот — [screens/ZAP.jpg](screens/ZAP.jpg)

---

## 📊 Этап 5. Результаты анализа

### 🔹 Bandit (SAST)
| Категория | Проблема | Рекомендация |
|------------|-----------|---------------|
| **B301** | Использование `pickle` | Заменить на безопасный формат (JSON) |
| **B303** | MD5 используется для хешей | Использовать `bcrypt` или `argon2` |
| **B602** | `subprocess` с `shell=True` | Использовать безопасный вызов без оболочки |
| **B506** | `yaml.load()` без safe_loader | Использовать `yaml.safe_load()` |

---

### 🔹 OWASP ZAP (DAST)
| Уровень | Уязвимость | Рекомендация |
|----------|-------------|--------------|
| High | Отсутствует `Content-Security-Policy` | Добавить CSP в заголовки HTTP |
| Medium | Cookie без `HttpOnly` / `Secure` | Добавить флаги безопасности |
| Medium | Отсутствует `X-Content-Type-Options` | Добавить `nosniff` |
| Info | Server Disclosure | Удалить заголовки `Server`, `X-Powered-By` |

---

## 🧠 Выводы и предложения по улучшению

1. **Усилить HTTP-защиту**: добавить CSP, HSTS, X-Frame-Options.  
2. **Секреты хранить в `.env`** и Kubernetes Secrets.  
3. **Использовать безопасные хеши (bcrypt, argon2)**.  
4. **Переписать YAML-загрузку** с `safe_load` и валидацией.  
5. **Добавить SAST/DAST в CI/CD (GitHub Actions)**.  
6. **Ограничить права контейнера PyGoat**: `USER nonroot`, `read-only filesystem`.  
7. **Интегрировать результаты ZAP в SIEM** (KUMA / Wazuh).

---

## 🧹 Очистка окружения

```bash
docker stop pygoat
docker rm pygoat
docker image prune -a -f
deactivate  # если активно venv
```

---

## ✅ Итог

- Проведён полный цикл тестирования безопасности приложения **PyGoat**.  
- Получены отчёты **SAST** и **DAST**, выявлены типовые уязвимости.  
- Подготовлены рекомендации по улучшению кода, Dockerfile и конфигурации.  
- Работа выполнена в соответствии с методичкой Телепова (п. «Предложены новые выводы и рекомендации»).

---

**Автор:** _ФИО студента_  
**Группа:** Кибербезопасность (магистратура)  
**Дата выполнения:** 20.10.2025  
**Преподаватель:** В. Телепов
