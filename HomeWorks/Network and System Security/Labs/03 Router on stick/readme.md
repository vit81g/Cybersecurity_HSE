# GNS3 Network Configuration - Cisco Routers and PCs
# 📡 Конфигурация сетевых устройств (Router on Stick)
## Схема задания

![Схема задания](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Network%20and%20System%20Security/Labs/03%20Router%20on%20stick/task03.jpg)

Схема задания: Ссылка на схему
## R1 (Router)

```plaintext
### Включение режима привилегированного доступа
enable

# Переход в режим конфигурации
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

# Включение интерфейсов и саб-интерфейсов (Router on Stick)
interface ethernet 0/0 
no shutdown 
exit 

interface ethernet 0/1 
ip address 172.31.128.193 255.255.255.252 
no shutdown 
exit 

interface ethernet 0/0.152 
encapsulation dot1q 152 
ip address 10.132.12.1 255.255.255.0 
exit 

interface ethernet 0/0.412 
encapsulation dot1q 412 
ip address 10.255.48.1 255.255.255.0 
exit 

# Включение маршрутизации и статических маршрутов
ip routing 
ip route 192.168.48.0 255.255.255.0 172.31.128.194 
ip route 192.168.1.0 255.255.255.0 172.31.128.194 

# Сохранение конфигурации
exit
write
```

### R2 (Router)
```plaintext
# Включение режима привилегированного доступа
enable

# Переход в режим конфигурации
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

# Включение интерфейсов и саб-интерфейсов (Router on Stick)
interface ethernet 0/0
no shutdown
exit

interface ethernet 0/1
ip address 172.31.128.194 255.255.255.252
no shutdown
exit

interface ethernet 0/0.152
encapsulation dot1q 152
ip address 192.168.48.1 255.255.255.0
exit

interface ethernet 0/0.952
encapsulation dot1q 952
ip address 192.168.1.1 255.255.255.0
exit

# Включение маршрутизации и статических маршрутов
ip routing
ip route 10.132.12.0 255.255.255.0 172.31.128.193
ip route 10.255.48.0 255.255.255.0 172.31.128.193

# Сохранение конфигурации
exit
write
```

### SW1 (Switch)
```plaintext
# Включение режима привилегированного доступа
enable

# Переход в режим конфигурации
configure terminal

# Установка имени устройства
hostname SW1

# Создание пользователя с привилегиями уровня 15
username user1 privilege 15 secret P@ssw0rd-ATM

# Установка пароля для режима привилегированного доступа
enable secret P@ssw0rd-ATM

# Настройка SSH
ip domain-name SW1.local
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

# Создание VLAN и настройка портов
vlan 152
name VLAN_152
exit

vlan 412
name VLAN_412
exit

# Trunk порт для подключения к R1
interface ethernet 0/0
switchport mode trunk
switchport trunk allowed vlan 152,412
switchport trunk native vlan 1
no shutdown
exit

# Access порт для PC1 (VLAN 152)
interface ethernet 0/1
switchport mode access
switchport access vlan 152
no shutdown
exit

# Access порт для PC2 (VLAN 412)
interface ethernet 0/2
switchport mode access
switchport access vlan 412
no shutdown
exit

# Сохранение конфигурации
exit
write
```

### SW2 (Switch)
```plaintext
# Включение режима привилегированного доступа
enable

# Переход в режим конфигурации
configure terminal

# Установка имени устройства
hostname SW2

# Создание пользователя с привилегиями уровня 15
username user1 privilege 15 secret P@ssw0rd-ATM

# Установка пароля для режима привилегированного доступа
enable secret P@ssw0rd-ATM

# Настройка SSH
ip domain-name SW2.local
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

# Создание VLAN и настройка портов
vlan 152
name VLAN_152
exit

vlan 952
name VLAN_952
exit

# Trunk порт для подключения к R2
interface ethernet 0/0
switchport mode trunk
switchport trunk allowed vlan 152,952
switchport trunk native vlan 1
no shutdown
exit

# Access порт для PC3 (VLAN 152)
interface ethernet 0/1
switchport mode access
switchport access vlan 152
no shutdown
exit

# Access порт для PC4 (VLAN 952)
interface ethernet 0/2
switchport mode access
switchport access vlan 952
no shutdown
exit

# Сохранение конфигурации
exit
write
```

## ✅ Безопасность
```plaintext
    SSH: Версия SSH 2 настроена, включая генерацию RSA-ключа и указание доменного имени.
    Пользователи: Создан пользователь user1 с привилегиями уровня 15.
    Пароли: Добавлены пароли для привилегированного режима (enable secret) и консоли (line console).
    Безопасность: Отключен Telnet, оставлен только SSH (transport input ssh).
```