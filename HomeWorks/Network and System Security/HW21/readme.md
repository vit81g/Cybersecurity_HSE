# Cisco Packet Tracer 
# 📡 Конфигурация сетевых устройств
## Схема задания
![Схема задания](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Network%20and%20System%20Security/HW21/map.jpg)

Сетевой администратор хочет подключить управляющий компьютер к коммутатору SW-A. Управляющий компьютер должен иметь возможность подключаться ко всем коммутаторам и маршрутизатору, но любые другие  устройства не должны подключаться к управляющему компьютеру или коммутаторам. Администратор хочет создать новую сеть VLAN 20 для целей управления.

# 📌 Настройка сети

## **🔹 Подключение кабелей**
1. **Подключить кабель между ПК и коммутатором SW-A**  
   - Тип: **Copper Straight-Through**  
   - **PC-PT C1 (Ethernet) → SW-A (FastEthernet0/1)**  

2. **Подключить кабель между коммутаторами SW-1 и SW-2**  
   - Тип: **Copper Crossover**  
   - **SW-1 (FastEthernet0/23) → SW-2 (FastEthernet0/23)**  

3. **Подключить кабель между коммутаторами и маршрутизатором**  
   - Тип: **Copper Straight-Through**  
   - **SW-1 (GigabitEthernet0/1) → Central (GigabitEthernet0/1)**  
   - **SW-2 (GigabitEthernet0/1) → Central (GigabitEthernet0/2)**  
   - **Central (GigabitEthernet0/1) → R1 (GigabitEthernet0/0)**  

---

## **🔹 Конфигурация коммутатора SW-A**
```bash
enable
configure terminal

# Создаём VLAN 20 для управления
vlan 20
name Management

# Настроим интерфейс FastEthernet0/1 для управляющего ПК
interface FastEthernet0/1
switchport mode access
switchport access vlan 20
no shutdown

# Назначаем IP-адрес для VLAN 20
interface vlan 20
ip address 192.168.20.2 255.255.255.0
no shutdown

exit
write memory
```

## **🔹 Конфигурация коммутатора SW-1**
```bash
enable
configure terminal

# Создаём VLAN 20
vlan 20
name Management

# Включаем транк на портах связи с другими коммутаторами
interface FastEthernet0/23
switchport mode trunk
switchport trunk native vlan 15
switchport nonegotiate
no shutdown

interface GigabitEthernet0/1
switchport mode trunk
switchport trunk native vlan 15
switchport nonegotiate
no shutdown

# Назначаем IP-адрес для VLAN 20
interface vlan 20
ip address 192.168.20.4 255.255.255.0
no shutdown

exit
write memory
```

## **🔹 Конфигурация коммутатора SW-2**
```bash
enable
configure terminal

# Создаём VLAN 20
vlan 20
name Management

# Включаем транк на портах связи с другими коммутаторами
interface FastEthernet0/23
switchport mode trunk
switchport trunk native vlan 15
switchport nonegotiate
no shutdown

interface GigabitEthernet0/1
switchport mode trunk
switchport trunk native vlan 15
switchport nonegotiate
no shutdown

# Назначаем IP-адрес для VLAN 20
interface vlan 20
ip address 192.168.20.5 255.255.255.0
no shutdown

exit
write memory

```

## **🔹 Конфигурация коммутатора Central**
```bash
enable
configure terminal

# Создаём VLAN 20
vlan 20
name Management

# Включаем транк на портах связи с маршрутизатором
interface GigabitEthernet0/1
switchport mode trunk
switchport trunk native vlan 15
switchport nonegotiate
no shutdown

interface GigabitEthernet0/2
switchport mode trunk
switchport trunk native vlan 15
switchport nonegotiate
no shutdown

# Назначаем IP-адрес для VLAN 20
interface vlan 20
ip address 192.168.20.6 255.255.255.0
no shutdown

exit
write memory

```


## **🔹 Конфигурация маршрутизатора R1**
```bash
enable
configure terminal

# Создаём субинтерфейсы для VLAN 20
interface GigabitEthernet0/0.3
encapsulation dot1q 20
ip address 192.168.20.1 255.255.255.0
no shutdown

exit
write memory

```

## **🔹 Конфигурация управляющего ПК (PC-PT C1)**
📌 Проверка VLAN 20
```plaintext
Открыть Config → FastEthernet0
Установить:

    IP Address: 192.168.20.100
    Subnet Mask: 255.255.255.0
    Default Gateway: 192.168.20.1
```

## **🔹 Проверка работоспособности**
```plaintext
show vlan brief
```
✅ Должны быть настроены VLAN 20 на всех коммутаторах.

## **🔹 Проверка транкинга**
```plaintext
show vlan brief
```
✅ FastEthernet0/23 и GigabitEthernet0/1 должны быть в режиме trunk.

📌 Проверка связи
```plaintext
ping 192.168.20.1   # Проверка связи с маршрутизатором R1
ping 192.168.20.2   # Проверка связи с SW-A
ping 192.168.20.4   # Проверка связи с SW-1
ping 192.168.20.5   # Проверка связи с SW-2
ping 192.168.20.6   # Проверка связи с Central
```
✅ Если пинг проходит – сеть полностью настроена!

📌 Проверка SSH-доступа
```plaintext
ssh -l SSHadmin 192.168.20.1
```
    Имя пользователя: SSHadmin
    Пароль: ciscosshpa55

![Схема задания](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Network%20and%20System%20Security/HW21/ssh.jpg)
✅ Если подключение успешно – всё работает!


## ✅ Безопасность
```plaintext
    Пароли: Добавлены пароли для привилегированного режима (enable secret) и консоли (line console).
```
