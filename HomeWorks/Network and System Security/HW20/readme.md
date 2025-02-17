# GNS3 Network Configuration - Cisco Routers and PCs
# 📡 Конфигурация сетевых устройств (RIP and OSPF config)
## Схема задания
![Схема задания](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Network%20and%20System%20Security/Labs/04%20RIP%20and%20OSPF%20config/task04.jpg)

##  📌 Настройка первичной конфигурации
# Настройка OSPFv2 и безопасности на маршрутизаторах

## 1. Настройка OSPFv2

### 1.1 Настройка OSPF на RA
```plaintext
enable
configure terminal
router ospf 1
network 192.168.1.0 0.0.0.255 area 0
exit

interface GigabitEthernet0/0
ip ospf priority 150
ip ospf hello-interval 5
ip ospf dead-interval 20
ip ospf message-digest-key 1 md5 Area0pa55
ip ospf authentication message-digest
exit
```

### 1.2 Настройка OSPF на RB
```plaintext
enable
configure terminal
router ospf 1
network 192.168.1.0 0.0.0.255 area 0
exit

interface GigabitEthernet0/0
ip ospf priority 100
ip ospf hello-interval 5
ip ospf dead-interval 20
ip ospf message-digest-key 1 md5 Area0pa55
ip ospf authentication message-digest
exit
```

### 1.3 Настройка OSPF на RC
```plaintext
enable
configure terminal
router ospf 1
network 192.168.1.0 0.0.0.255 area 0
passive-interface default
no passive-interface GigabitEthernet0/0
default-information originate
exit

ip route 0.0.0.0 0.0.0.0 209.165.200.226

interface GigabitEthernet0/0
ip ospf priority 50
ip ospf hello-interval 5
ip ospf dead-interval 20
ip ospf message-digest-key 1 md5 Area0pa55
ip ospf authentication message-digest
exit
```

## 2. Настройка безопасности

### 2.1 Защита доступа к маршрутизатору
```plaintext
configure terminal
line console 0
password passwd55
login
exit

enable secret passwd55
service password-encryption
```

### 2.2 Ограничение попыток входа
```plaintext
login block-for 120 attempts 3 within 60
```

### 2.3 Отключение неиспользуемых интерфейсов
```plaintext
interface GigabitEthernet0/1
shutdown
exit

interface range FastEthernet0/2 - 24
shutdown
exit
```

## 3. Проверка конфигурации

### 3.1 Проверка соседей OSPF
```plaintext
show ip ospf neighbor
```

### 3.2 Проверка таблицы маршрутизации
```plaintext
show ip route
```

### 3.3 Проверка доступности Web Server
```plaintext
ping 64.100.1.2
```

### 3.4 Очистка OSPF при проблемах
```plaintext
clear ip ospf process
```

### 3.5 Проверка зашифрованных паролей
```plaintext
show running-config
```

### 3.6 Сохранение конфигурации
```plaintext
write memory


## ✅ Безопасность
```plaintext
    Пароли: Добавлены пароли для привилегированного режима (enable secret) и консоли (line console).
```
