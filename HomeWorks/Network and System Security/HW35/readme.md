# Домашнее задание № 35 — «Безопасность IoT‑устройств и каналов передачи данных»

Добро пожаловать в репозиторий задания по дисциплине **«Защита компьютерных сетей и систем»**. Здесь собраны материалы, необходимые для разработки и проверки решения.

## Структура каталога

```
├── docs/   # отчёт и вспомогательные документы
└── map/    # схема сети и Packet Tracer‑файлы
```

| Папка     | Содержимое                                                                                                                                                                                                                                                 |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **docs/** | • `Решение_Тема35.docx` — основной отчёт с выбранным протоколом, диаграммой, STRIDE‑анализом и рекомендациями.<br>• `diagram.png` — экспорт диаграммы коммуникационного уровня.<br>• *другие вспомогательные файлы* (PDF‑версии, презентация, литература). |
| **map/**  | • `iot_home_topology.pkt` — проект Cisco Packet Tracer.<br>• `iot_home_topology.png` — снимок схемы для быстрого просмотра.                                                                                                                                |

## Что требуется сделать

1. **Склонировать репозиторий** и открыть файл `iot_home_topology.pkt` в Cisco Packet Tracer ≥ 8.1.1.
2. Ознакомиться с отчётом (`docs/Решение_Тема35.docx`) и, при необходимости, внести коррективы под вашу топологию (изменить MAC‑адреса, добавить устройства, обновить риски).
   *При редактировании отчёта сохраняйте версию PDF в той же папке.*
3. Убедиться, что схема из `map/` соответствует описанию в отчёте (цвета линий, подписи протоколов, нумерация портов).
4. Сгенерировать и добавить скриншоты или короткое видео‑демо (по усмотрению преподавателя).
5. Сделать коммит с обновлёнными файлами и оформить Pull Request/сдать архив согласно требованиям курса.

## Краткое содержание отчёта

* **Часть 1. Диаграмма коммуникационного уровня**
  Выбор протокола Zigbee 3.0, текстовый ASCII‑чертёж топологии, описание каналов (Ethernet, Wi‑Fi, TLS).
* **Часть 2. Инвентарь поверхности атаки**
  Таблица устройств/сетей, протоколов и взаимных связей.
* **Часть 3. STRIDE‑анализ**
  Перечень угроз (OWASP IoT) и компенсирующие меры.
* **Рекомендации** для повышения безопасности (WPA3, mutual TLS, безопасная загрузка и т.д.).

## Быстрый старт

```bash
# Клонируем
git clone <repo‑url>
cd homework‑iot‑sec‑35

# Открываем документацию
xdg-open docs/Решение_Тема35.pdf   # Linux
office docs/Решение_Тема35.docx    # Windows/Mac

# Запускаем Packet Tracer
packettracer map/iot_home_topology.pkt
```

## Лицензия

Материалы предназначены **исключительно для учебных целей** в рамках курса магистратуры «Кибербезопасность» и не распространяются публично без согласования с авторами.
