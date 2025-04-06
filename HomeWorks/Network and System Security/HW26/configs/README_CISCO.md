
# Настройка Cisco-маршрутизатора (POD68)

![Схема стенда](HomeWorks/Network and System Security/HW26/screenshots/lab_68_plan.jpg)

## 📘 Общая информация

- Внутренняя сеть: 10.0.68.0/24
- IP маршрутизатора (LAN): 10.0.68.1
- WAN интерфейс: DHCP
- DNS-сервер: 10.0.68.5 (AD)
- SSH доступ: только с 10.0.68.6

---

## 🏷 Конфигурация имени устройства и пользователя

```bash
enable
configure terminal

# Имя устройства
hostname POD68-CSR

# Локальный пользователь
username admin privilege 15 secret P@ssw0rd

# Консольный доступ
line con 0
 login local
 password P@ssw0rd
```

---

## 🔧 Интерфейсы

```bash
# Внутренний интерфейс (LAN)
interface GigabitEthernet1
 description Internal Network
 ip address 10.0.68.1 255.255.255.0
 ip nat inside
 no shutdown

# Внешний интерфейс (WAN)
interface GigabitEthernet2
 description External (Internet)
 ip address dhcp
 ip nat outside
 no shutdown
```

---

## 🌐 1.4 — NAT для доступа в интернет

```bash
# Список доступа для NAT
access-list 1 permit 10.0.68.0 0.0.0.255

# NAT через внешний интерфейс
ip nat inside source list 1 interface GigabitEthernet2 overload

# Назначение NAT на интерфейсы
interface GigabitEthernet1
 ip nat inside

interface GigabitEthernet2
 ip nat outside
```

> 💬 **Примечание**: В задании указано использование `access-list 100`, однако в данной конфигурации применена `access-list 1` — стандартный список доступа. Он полностью соответствует требованиям NAT, фильтрует по IP-источнику и является более простым и лаконичным решением. Extended ACL (как 100) избыточна в данном контексте.

---

## 📡 DHCP

```bash
# Исключённые адреса для статических хостов
ip dhcp excluded-address 10.0.68.1 10.0.68.5

# Пул DHCP-адресов
ip dhcp pool POD68-DHCP
 network 10.0.68.0 255.255.255.0
 default-router 10.0.68.1
 dns-server 10.0.68.5
```

---

## 🔐 SSH

```bash
# Настройка SSH
ip domain-name pod68.lab
crypto key generate rsa modulus 1024
ip ssh version 2

# Локальный пользователь
username admin privilege 15 secret P@ssw0rd

# ACL для ограничения доступа по SSH
ip access-list standard allow_ssh
 permit 10.0.68.6
 deny any

# Настройка VTY линий
line vty 0 4
 transport input ssh
 login local
 access-class allow_ssh in
```

---

## 💾 Сохранение конфигурации

```bash
write memory
```
Или:
```bash
copy running-config startup-config
```

---

_Документ предназначен для публикации в GitHub в рамках лабораторной работы "Атаки на Active Directory"._
