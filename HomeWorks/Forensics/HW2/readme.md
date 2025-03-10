# Отчет по анализу дампа памяти (Volatility)

### 1. Определите семейство и версию операционной системы

✅ **Ответ:** Win7SP1x64  
![Версия ОС](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Forensics/HW2/image_info.jpg)

---

### 2. Процесс, установивший соединение на порту 554

✅ **Ответ:** Процесс **wmpnetwk.exe** (PID: 2368), порт: **554 (RTSP)**

![Соединение с портом 554](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Forensics/HW2/01_netstat.jpg)

---

### 3. Устанавливались ли соединения на портах 135-140?

✅ **Ответ:** Нет, соединения не устанавливались.

---

### 4. Идентификаторы процессов, установивших соединения (порты 135-140)

✅ **Ответ:** Отсутствуют (соединения не устанавливались).

---

### 5. Идентификаторы процессов-родителей

✅ **Ответ:** Отсутствуют (соединения не устанавливались).

---

### 6. Порожденные процессы (порты 135-140)

✅ **Ответ:** Отсутствуют (соединения не устанавливались).

---

### 7. Количество и PID процессов svchost.exe

✅ **Ответ:** 11 процессов svchost.exe

**PID:** `896, 1408, 940, 296, 812, 700, 852, 2008, 1248, 612, 2632`

![Процессы svchost.exe](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Forensics/HW2/07_pstree.jpg)

---

### 8. Имена исполняемых файлов, запустивших процессы svchost.exe

✅ **Ответ:** Все процессы svchost.exe были запущены процессом:

- **services.exe** (PID: 508, путь: `C:\Windows\system32\services.exe`).

![Исполняемый файл](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Forensics/HW2/08_dlllist.jpg)

---

### 9. Процессы svchost.exe с признаками заражения

✅ **Ответ:** Подозрительный код в памяти (**PAGE_EXECUTE_READWRITE**):

| Процесс    | PID  | Адрес памяти  |
|------------|------|---------------|
| svchost.exe| 812  | 0x1430000     |
| svchost.exe| 296  | 0xeb0000      |
| svchost.exe| 2008 | 0x2600000     |
| svchost.exe| 2008 | 0x4ea0000     |

![malfind #1](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Forensics/HW2/09_01_malfind.jpg)  
![malfind #2](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Forensics/HW2/09_02_malfind.jpg)  
![malfind #3](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Forensics/HW2/09_03_malfind.jpg)  
![malfind #4](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Forensics/HW2/09_04_malfind.jpg)

---

### 10. Сообщение, написанное Джоном в командной строке

✅ **Ответ:**

```
THM{You_found_me}
```

Другие команды (`cd`, `dir`, `cls`) не являются сообщениями.

![cmdscan](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Forensics/HW2/10_cmdscan.jpg)

---