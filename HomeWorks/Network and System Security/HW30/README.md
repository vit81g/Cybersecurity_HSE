# Лабораторная работа: Защита сетевых устройств (Тема 31)

![](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Network%20and%20System%20Security/HW30/screens/task.jpg)

## 📂 Содержание проекта

Данная работа посвящена настройке защищённого взаимодействия маршрутизаторов с использованием следующих механизмов:

- OSPF с аутентификацией MD5
- Синхронизация времени с NTP-сервером
- Регистрация событий через Syslog
- Настройка защищённого удалённого доступа по SSH

---

## 📄 Документы ([docs/](docs/))

- [ДЗ тема 31 Защита сетевых устройств.docx](docs/ДЗ%20тема%2031%20Защита%20сетевых%20устройств.docx)
- [Syslog, NTP, and SSH.pka](docs/Syslog,%20NTP,%20and%20SSH.pka)

---

## 🖥 Скриншоты ([screens/](screens/))

| Название файла         | Описание                             |
|------------------------|--------------------------------------|
| `NTP_time_data.jpg`    | Состояние времени после настройки NTP |
| `R1_R2_R3_NTP.jpg`     | Проверка NTP-синхронизации на всех маршрутизаторах |
| `Syslog.jpg`           | Скрин с регистрацией логов |
| `ssh.jpg`              | Настройка SSH на маршрутизаторе |
| `ssh_PC_R3.jpg`        | Успешное подключение по SSH с PC к R3 |
| `ssh_R2_R3.jpg`        | Успешное подключение по SSH с R2 к R3 |

---

## ⚙ Конфигурации маршрутизаторов ([config/](config/))

- [R1](config/R1.txt)
- [R2](config/R2.txt)
- [R3](config/R3.txt)

---

## 📌 Примечания

- В ходе настройки на маршрутизаторе R3 была предпринята попытка удалить RSA-ключи командой `crypto key zeroize rsa`. Система вернула сообщение о том, что ключи отсутствуют.
- Генерация ключей RSA выполнена с длиной 1024 бита.
- Для каждого из сервисов (NTP, Syslog, SSH) были проведены проверки и сделаны скриншоты результатов.

---

> _Репозиторий создан в рамках курса "Защита компьютерных сетей и систем" направления "Кибербезопасность", НИУ ВШЭ._