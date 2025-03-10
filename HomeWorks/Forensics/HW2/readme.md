```plaintext
Присутствующий на месте эксперт-криминалист провел первоначальный криминалистический анализ компьютера Джона и предал дамп памяти, который он создал на компьютере. Вы должны найти в нем следующую информацию.

1.	Определите семейство и версию операционной системы на компьютере Джона.
2.	Какой процесс на компьютере Джона установил сетевое соединение с участием порта 554?
3.	Устанавливались ли сетевые соединения компьютера Джона с участием локальных портов в диапазоне 135-140?
4.	Если такие соединения устанавливались, укажите идентификаторы процессов, устанавливавших такие соединения.
5.	Укажите идентификатор процессов-родителей данных процессов. 
6.	Укажите все процессы, порожденные процессами, устанавливавшими выявленные в пункте 3 соединения.
7.	Установите, сколько различных процессов svchost.exe запускалось, приведите идентификаторы запущенных процессов.
8.	Укажите имена исполняемых файлов, запустивших эти процессы.
9.	Среди процессов, выявленных в пункте 7, определите те, которые содержат признаки заражения.
10.	Установите, какое сообщение написал Джон в командной строке в ходе сеанса, в момент которого был создан дамп. 
'''

1. Определите семейство и версию операционной системы на компьютере Джона.
✅ Win7SP1x64 
![Скриншот](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Network%20and%20System%20Security/Labs/04%20RIP%20and%20OSPF%20config/task04.jpg)



2. Какой процесс на компьютере Джона установил сетевое соединение с участием порта 554?
✅ Процесс: wmpnetwk.exe
✅ PID: 2368
✅ Порт: 554 (RTSP)
![Скриншот](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Network%20and%20System%20Security/Labs/04%20RIP%20and%20OSPF%20config/task04.jpg)

3. Устанавливались ли сетевые соединения компьютера Джона с участием локальных портов в диапазоне 135-140?
✅ На портах с 135 по 140 соединения не устанавливались.
![Скриншот](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Network%20and%20System%20Security/Labs/04%20RIP%20and%20OSPF%20config/task04.jpg)

4. Если такие соединения устанавливались, укажите идентификаторы процессов, устанавливавших такие соединения.
✅ Идентификаторы процессов отсутствуют.
![Скриншот](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Network%20and%20System%20Security/Labs/04%20RIP%20and%20OSPF%20config/task04.jpg)

5. Укажите идентификатор процессов-родителей данных процессов. 
✅ Ответ на 5 вопрос:
идентификаторы отсутствуют, так как сетевые соединения на указанных портах (135-140) не устанавливались, и соответственно, процессы-родители отсутствуют.
![Скриншот](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Network%20and%20System%20Security/Labs/04%20RIP%20and%20OSPF%20config/task04.jpg)

6. Укажите все процессы, порожденные процессами, устанавливавшими выявленные в пункте 3 соединения.
✅ Ответ на 6 вопрос: 
процессы отсутствуют, так как в пункте 3 не выявлено процессов, устанавливающих соединения.
![Скриншот](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Network%20and%20System%20Security/Labs/04%20RIP%20and%20OSPF%20config/task04.jpg)

7. Установите, сколько различных процессов svchost.exe запускалось, приведите идентификаторы запущенных процессов.
✅ Ответ на 7 вопрос:
11 различных процессов svchost.exe:
PID: 896, 1408, 940, 296, 812, 700, 852, 2008, 1248, 612, 2632
![Скриншот](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Network%20and%20System%20Security/Labs/04%20RIP%20and%20OSPF%20config/task04.jpg)

8. Укажите имена исполняемых файлов, запустивших эти процессы.
```plaintext
PID 896 (svchost.exe) → PPID 508 (services.exe)
PID 1408 (svchost.exe) → PPID 508 (services.exe)
PID 940 (svchost.exe) → PPID 508 (services.exe)
PID 296 (svchost.exe) → PPID 508 (services.exe)
PID 812 (svchost.exe) → PPID 508 (services.exe)
PID 700 (svchost.exe) → PPID 508 (services.exe)
PID 852 (svchost.exe) → PPID 508 (services.exe)
PID 2008 (svchost.exe) → PPID 508 (services.exe)
PID 1248 (svchost.exe) → PPID 508 (services.exe)
PID 612 (svchost.exe) → PPID 508 (services.exe)
PID 2632 (svchost.exe) → PPID 508 (services.exe)
```
✅ Итоговый ответ на 8 вопрос будет выглядеть так:
Имя исполняемого файла, запустившего процессы svchost.exe:
services.exe (полный путь: C:\Windows\system32\services.exe, PID 508).
![Скриншот](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Network%20and%20System%20Security/Labs/04%20RIP%20and%20OSPF%20config/task04.jpg)

9. Среди процессов, выявленных в пункте 7, определите те, которые содержат признаки заражения.
✅ Ответ на 9 вопрос:
Подозрительный код в области памяти - PAGE_EXECUTE_READWRITE.
Подозрительные (заражённые) процессы:
```plaintext
✅ Process: svchost.exe Pid: 812 Address: 0x1430000
✅ Process: svchost.exe Pid: 296 Address: 0xeb0000
✅ Process: svchost.exe Pid: 2008 Address: 0x2600000
✅ Process: svchost.exe Pid: 2008 Address: 0x4ea0000
```
![Скриншот](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Network%20and%20System%20Security/Labs/04%20RIP%20and%20OSPF%20config/task04.jpg)

10. Установите, какое сообщение написал Джон в командной строке в ходе сеанса, в момент которого был создан дамп. 
✅ Ответ на 10 вопрос:
```plaintext
THM{You_found_me}
```
Остальные команды в командной строке не являются сообщениями, это просто команды cd, dir, cls и т.д.
![Скриншот](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Network%20and%20System%20Security/Labs/04%20RIP%20and%20OSPF%20config/task04.jpg)





