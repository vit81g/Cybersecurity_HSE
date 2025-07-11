
# PPCS Infrastructure Redesign (2025) — Network & System Security Final Project

## Общее описание

Проект направлен на полную переработку существующей инфраструктуры площадки PPCS для  
обеспечения изоляции данных МРТ, запуска IaaS-сервиса и организации резервной площадки (DR).  
Представляет собой архитектуру Spine/Leaf с поддержкой сегментации (VRF), отказоустойчивыми  
межсетевыми экранами и туннелем ГОСТ-VPN до головного офиса.

Выполнен в рамках финального задания по курсу "Защита компьютерных сетей и систем".

---

## Структура проекта

```bash
final_task/
├── analysis/              # Анализ исходной архитектуры
│   ├── problems.txt       # Список технических проблем текущей сети
│   └── task_bisnes.txt    # Требования бизнес- и тех. сторон
├── docs/                  # Документация из задания
│   ├── Итоговое задание 2025.pdf
│   ├── Описание кейса.pdf
│   ├── PPCS.jpg           # Старая схема (визуализация)
│   └── PPCS.vsdx          # Исходный Visio-файл
├── projects/              # Финальная реализация проекта
│   ├── net.png            # Финальная схема (PNG)
│   ├── PPCS_new.jpg       # Отрисованная схема в JPG
│   ├── PPCS_new.vsdx      # Схема в Visio
│   ├── readme.md          # Этот файл
│   ├── text.txt           # Подробности для презентации
│   └── Зачем меняем PPCS.pptx  # Презентация к защите проекта
```

---

## Содержание проекта

### Проблемы старой схемы
- Нет сегментации клиентов: заражение = весь периметр
- Опубликованы сервисы без DMZ/фаерволов
- Один D-Link, один MikroTik = SPOF + отсутствие резервирования
- Виртуализация на пиратском vSphere 7 без защиты

### Цели
- Обособить стойки МРТ (VRF 10) с ГОСТ-шифрованием
- Создать IaaS-зону для перспективных клиентов (OpenStack)
- Обновить маршрутизацию, фаервол, сегментацию
- Обеспечить DR-сценарий с Flex.One (2 шт)

### Ключевые технические решения
- Cisco FTD 2140 (HA-pair, NAT, IPS)
- Spine/Leaf 2x40GbE (ToR/магистраль)
- Континент 3.9 / ViPNet HW для туннеля HQ
- Репликация данных по eBGP EVPN (10 GbE)
- VRF 10/20/30/40 с NAT и ACL по зонам

---

## Используемые сокращения

| Сокр.     | Расшифровка                                | Назначение                                 |
|----------|---------------------------------------------|---------------------------------------------|
| FTD      | Firepower Threat Defense (Cisco)            | Межсетевой экран L4-7                       |
| HA       | High Availability                           | Резерв Active/Standby                       |
| NAT      | Network Address Translation                 | Подмена IP-адресов при выходе наружу       |
| ACL      | Access Control List                         | Правила фильтрации трафика                 |
| VRF      | Virtual Routing and Forwarding              | Логически изолированные маршруты           |
| ToR      | Top of Rack                                 | Leaf-коммутаторы у стоек                   |
| Spine    | Spine Switch (магистраль)                   | Соединяет Leaf в один 1-hop fabric         |
| DR       | Disaster Recovery                           | Резервная площадка                         |
| IaaS     | Infrastructure as a Service                 | Облачные ресурсы (CPU, RAM, Storage)       |
| EVPN     | Ethernet VPN                                | L2/L3-оверлей через BGP                    |
| HQ       | Headquarters                                | Головной офис                              |
| ГОСТ-VPN | Шифрование по ГОСТ (Континент, ViPNet)      | КС3, защита персональных данных            |

---

**Материалы предназначены исключительно для учебных целей** в рамках курса магистратуры «Кибербезопасность» и не распространяются публично без согласования с авторами.  
**Автор:** Виталий Новиков  
**Дата:** Июнь 2025
