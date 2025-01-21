# GNS3 Network Configuration - Cisco Routers and PCs
# 📡 Конфигурация сетевых устройств (RIP and OSPF config)
## Схема задания
![Схема задания](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Network%20and%20System%20Security/Labs/04%20RIP%20and%20OSPF%20config/task04.jpg)

##  📌 Настройка первичной конфигурации
### R1 (Router)
```plaintext
enable
configure terminal

# Установка имени устройства
hostname R1

# Создание пользователя с привилегиями уровня 15
username user1 privilege 15 secret P@ssw0rd-ATM

# Установка пароля для режима привилегированного доступа
enable secret P@ssw0rd-ATM

# Настройка SSH
ip domain-name R1.local
crypto key generate rsa
# Введите 1024 в качестве размера ключа
ip ssh version 2

# Настройка виртуальных терминальных линий (vty) для SSH
line vty 0 4
 login local
 transport input ssh
 exit

# Включение консольного доступа с аутентификацией
line console 0 
 password P@ssw0rd-ATM 
 login 
 exit 

# R1 и R2
interface e0/0
ip address 10.0.0.1 255.255.255.252
no shutdown
exit

# R1 и R3
interface e0/1
ip address 10.0.0.5 255.255.255.252
no shutdown
exit

# R1 и PC3
interface e0/2
ip address 192.168.0.1 255.255.255.0
no shutdown
exit

```

### R2 (Router 2)
```plaintext
enable
configure terminal

# Установка имени устройства
hostname R2

# Создание пользователя с привилегиями уровня 15
username user1 privilege 15 secret P@ssw0rd-ATM

# Установка пароля для режима привилегированного доступа
enable secret P@ssw0rd-ATM

# Настройка SSH
ip domain-name R2.local
crypto key generate rsa
# Введите 1024 в качестве размера ключа
ip ssh version 2

# Настройка виртуальных терминальных линий (vty) для SSH
line vty 0 4
 login local
 transport input ssh
 exit

# Включение консольного доступа с аутентификацией
line console 0
 password P@ssw0rd-ATM
 login
 exit

# R2 и R1
interface e0/0
ip address 10.0.0.2 255.255.255.252
no shutdown
exit

# R2 и R3
interface e0/1
ip address 10.0.0.9 255.255.255.252
no shutdown
exit

# R2 и PC1
interface e0/2
ip address 192.168.1.1 255.255.255.0
no shutdown
exit

```

### R3 (Router 3)
```plaintext
enable
configure terminal

# Установка имени устройства
hostname R3

# Создание пользователя с привилегиями уровня 15
username user1 privilege 15 secret P@ssw0rd-ATM

# Установка пароля для режима привилегированного доступа
enable secret P@ssw0rd-ATM

# Настройка SSH
ip domain-name R3.local
crypto key generate rsa
# Введите 1024 в качестве размера ключа
ip ssh version 2

# Настройка виртуальных терминальных линий (vty) для SSH
line vty 0 4
 login local
 transport input ssh
 exit

# Включение консольного доступа с аутентификацией
line console 0
 password P@ssw0rd-ATM
 login
 exit


# R3 и R1
interface e0/0
ip address 10.0.0.6 255.255.255.252
no shutdown
exit

# R3 и R2
interface e0/1
ip address 10.0.0.10 255.255.255.252
no shutdown
exit

# R3 и PC2
interface e0/2
ip address 192.168.2.1 255.255.255.0
no shutdown
exit

```

## 📌 PC Configuration:
### PC1:
```plaintext
ip 192.168.1.10 255.255.255.0 192.168.1.1
write
```
### PC2:
```plaintext
ip 192.168.2.10 255.255.255.0 192.ip 168.2.1
write
```
### PC3:
```plaintext
ip 192.168.0.10 255.255.255.0 192.168.0.1
write
```

## 📌 Проверка связности:
```plaintext
На маршрутизаторах:

ping 10.0.0.x
ping 192.168.x.x
```

## 📌 Настройка RIP

RIP будет использоваться временно для проверки маршрутизации. Конфигурация на каждом маршрутизаторе:

### R1 (Router 1)
```plaintext
enable
configure terminal
router rip
version 2
network 10.0.0.0
network 192.168.0.0
passive-interface e0/2
exit
```

### R2 (Router 2)
```plaintext
enable
configure terminal
router rip
version 2
network 10.0.0.0
network 192.168.1.0
passive-interface e0/2
exit
```

### R3 (Router 3)
```plaintext
enable
configure terminal
router rip
version 2
network 10.0.0.0
network 192.168.2.0
passive-interface e0/2
exit
```

### Проверка:
```plaintext
    Убедитесь, что VPCS могут пинговать друг друга.
    После тестирования отключите RIP:
    no router rip
```

## 📌 Настройка OSPF

Для OSPF используется номер процесса 100 и идентификаторы роутеров.

### R1 (Router 1)
```plaintext
enable
configure terminal
router ospf 100
router-id 1.1.1.1
network 10.0.0.0 0.0.0.3 area 0
network 192.168.0.0 0.0.0.255 area 0
passive-interface e0/2
exit
```

### R2 (Router 2)
```plaintext
enable
configure terminal
router ospf 100
router-id 2.2.2.2
network 10.0.0.0 0.0.0.3 area 0
network 10.0.0.8 0.0.0.3 area 0
network 192.168.1.0 0.0.0.255 area 0
passive-interface e0/2
exit
```

### R3 (Router 3)
```plaintext
enable
configure terminal
router ospf 100
router-id 3.3.3.3
network 10.0.0.4 0.0.0.3 area 0
network 10.0.0.8 0.0.0.3 area 0
network 192.168.2.0 0.0.0.255 area 0
passive-interface e0/2
exit
```

## 📌 Проверка:
```plaintext
    Пингуйте устройства PC1-PC3.
    Проверьте таблицу маршрутизации:

show ip route
```

## ✅ Безопасность
```plaintext
    SSH: Версия SSH 2 настроена, включая генерацию RSA-ключа и указание доменного имени.
    Пользователи: Создан пользователь user1 с привилегиями уровня 15.
    Пароли: Добавлены пароли для привилегированного режима (enable secret) и консоли (line console).
    Безопасность: Отключен Telnet, оставлен только SSH (transport input ssh).
```
