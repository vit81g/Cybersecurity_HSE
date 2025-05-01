# 🕵️ Домашнее задание №2 — Основы цифровой форензики (Вариант 1)

## 👨‍🎓 Автор
- **ФИО:** Новиков В. С.
- **Группа:** МКБ 241
- **Преподаватель:** Сорокин А. В.
- **Год:** 2025

## 📂 Структура репозитория

```
HW3/
├── /doc/        # Отчет и сопутствующие документы
├── /screens/    # Скриншоты, подтверждающие выполнение задания
└── /task/       # Исходное задание в формате .doc
```

## 📘 Описание задания

Исследуется образ диска `var1.E01`. Необходимо установить следующие факты:

1. Пользовательские учетные записи
2. Разметка диска
3. ОС устройства: тип, версия, архитектура
4. Время последнего доступа к картинке с закатом
5. Developer Kit какого ПО установлен
6. Какая учетная запись создала документы со словом `spreadsheet`
7. Композиция, воспроизводимая в WMP
8. Адреса, найденные в удаленных .doc файлах
9. Порт, назначенный для NNTP
10. Email-адреса пользователя с `1` в имени

## 🛠 Инструменты

- **Autopsy** под Windows и Kali Linux
- Анализ дампа `var1.E01`
- Поиск по файлам, метаданным и реестру

## 📄 Основные выводы

| № | Вопрос                                                                 | Ответ |
|---|------------------------------------------------------------------------|-------|
| 1 | Учетные записи                                                         | `domex1`, `domex2` |
| 2 | Разметка                                                               | NTFS в диапазоне 63–83859299, C:\ диск |
| 3 | ОС                                                                     | Windows XP SP3, 32-bit (x86) |
| 4 | Sunset.jpg последний доступ                                            | `2008-10-29 19:21:04 (MSK)` |
| 5 | Установлен Developer Kit                                               | `VMware Guest SDK` |
| 6 | Spreadsheet-документы созданы учеткой                                 | `domex1` |
| 7 | Композиция в WMP                                                       | `Beethoven's Symphony No. 9 (Scherzo)` |
| 8 | Удалённые .doc-файлы с адресами                                       | В `Dc3.docx`, `Dc4.xlsx` — адреса не найдены |
| 9 | NNTP-порт                                                              | TCP `119` |
|10 | Email-адреса пользователя `domex1`                                    | См. ниже 👇 |

<details>
  <summary>📧 Список email-адресов (нажмите, чтобы развернуть)</summary>

```
domex1@aol.com  
domex1@aim.com  
domex1@ar.atwola.com  
domex1@at.atwola.com  
domex1@atdmt.com  
domex1@atwola.com  
domex1@c.live  
domex1@c.live.com  
domex1@c.msn.com  
domex1@cdn.at.atwola.com  
domex1@doubleclick.net  
domex1@google.com  
domex1@live.com  
domex1@logservice.live  
domex1@logservice.live.com  
domex1@mail.google.com  
domex1@msn.com  
domex1@msnportal.112.2o7.net  
domex1@my.screenname.aol  
domex1@my.screenname.aol.com  
domex1@rad.msn.com  
domex1@revsci.net  
domex1@www.live  
domex1@www.live.com  
domex1@www.msn.com
```

</details>

## 🖼️ Галерея

Скриншоты с доказательствами — в директории [`/screens`](./screens/).  
Каждый пункт подтверждён как минимум одним снимком Autopsy в Windows и Kali.

## 📎 Документы

- [📄 Отчёт в PDF](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Forensics/HW3/HW3.pdf)
- [📑 Задание в Word](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Forensics/HW3/%D0%9D%D0%BE%D0%B2%D0%B8%D0%BA%D0%BE%D0%B2%20%D0%92.%D0%A1.%20%D0%94%D0%97%202.docx)

---

> _Репозиторий создан в рамках курса "Цифровая криминалистика" направления "Информационная безопасность", НИУ ВШЭ._