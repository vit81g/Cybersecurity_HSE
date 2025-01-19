# GNS3 Network Configuration - Cisco Routers
# 📡 Конфигурация сетевых устройств (Basic configs)
## Схема задания

![Схема задания](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Network%20and%20System%20Security/Labs/01_Basic%20configs/task01.jpg)

## 📌 Router Configuration:

### Конфигурация маршрутизатора ViOSRouter-2 (TstRTR-1):
```plaintext
enable
configure terminal

hostname TstRTR-1

# Создание пользователя с зашифрованным паролем:

username user1 privilege 15 secret P@ssw0rd-ATM

# Установка пароля для режима привилегированного доступа:

enable secret P@ssw0rd-ATM

# Включение SSH:

ip domain-name tst.local
crypto key generate rsa
  (введите размер ключа, например, 1024)
ip ssh version 2

# Настройка виртуальных терминальных линий (vty) для SSH:

line vty 0 4
 login local
 transport input ssh
 exit

# Включение консольного доступа с аутентификацией:

line console 0
 password P@ssw0rd-ATM
 login
 exit

# Назначение IP-адреса на интерфейсе Gi0/0:

interface ethernet 0/0
 ip address 10.212.241.1 255.255.255.0
 no shutdown
exit

# Сохранение конфигурации:

do write
```


### Конфигурация коммутатора ViOSSwitch-1 (TstSW-1):
```plaintext
enable
configure terminal

Установка имени устройства:

hostname TstSW-1

# Создание пользователя с зашифрованным паролем:

username user1 privilege 15 secret P@ssw0rd-ATM

# Установка пароля для привилегированного режима:

enable secret P@ssw0rd-ATM

# Включение SSH:

ip domain-name tst.local
crypto key generate rsa
 (введите размер ключа, например, 1024)
ip ssh version 2

# Настройка виртуальных терминальных линий (vty) для SSH:

line vty 0 4
 login local
 transport input ssh
 exit

# Включение консольного доступа с паролем:

line console 0
 password P@ssw0rd-ATM
 login
 exit

# Создание VLAN 100, 200, 300:

vlan 100
vlan 200
vlan 300
exit

# Назначение VLAN управления (200) и IP-адреса:

interface vlan 200
 ip address 10.212.241.2 255.255.255.0
 no shutdown
exit

# Перенос интерфейса Gi0/0 в VLAN 200:

interface ethernet 0/0
 switchport mode access
 switchport access vlan 200
 no shutdown
exit

# Сохранение конфигурации:

do write
```