
# Настройка Cisco-маршрутизатора (POD68)

## 📘 Общая информация

- Внутренняя сеть: 10.0.68.0/24
- IP маршрутизатора (LAN): 10.0.68.1
- WAN интерфейс: DHCP
- DNS-сервер: 10.0.68.5 (AD)
- SSH доступ: только с 10.0.68.6

---

## Конфигурация имени устройства

```bash
enable
configure terminal

hostname POD68-CSR                    ! Имя устройства
```

## 🔧 Интерфейсы

```bash
interface GigabitEthernet1
 description Internal Network
 ip address 10.0.68.1 255.255.255.0
 ip nat inside
 no shutdown

interface GigabitEthernet2
 description External (Internet)
 ip address dhcp
 ip nat outside
 no shutdown
```

---

## 🌐 1.4 — NAT для доступа в интернет

```bash
access-list 1 permit 10.0.68.0 0.0.0.255       ! Разрешаем NAT для локальной сети

ip nat inside source list 1 interface GigabitEthernet2 overload

interface GigabitEthernet1
 ip nat inside                                ! Внутренний интерфейс

interface GigabitEthernet2
 ip nat outside                               ! Внешний интерфейс
```

> 💬 **Примечание**: В задании указано использование `access-list 100`, однако в данной конфигурации применена `access-list 1` — стандартный список доступа. Он полностью соответствует требованиям NAT, фильтрует по IP-источнику и является более простым и лаконичным решением. Extended ACL (как 100) избыточна в данном контексте.

---

## 📡 DHCP

```bash
ip dhcp excluded-address 10.0.68.1 10.0.68.5

ip dhcp pool POD68-DHCP
 network 10.0.68.0 255.255.255.0
 default-router 10.0.68.1
 dns-server 10.0.68.5
```

---

## 🔐 SSH

```bash
ip domain-name pod68.lab
crypto key generate rsa modulus 1024
ip ssh version 2

username admin privilege 15 secret P@ssw0rd

ip access-list standard allow_ssh
 permit 10.0.68.6
 deny any

line vty 0 4
 transport input ssh
 login local
 access-class allow_ssh in
```

---

_Документ предназначен для публикации в GitHub в рамках лабораторной работы "Атаки на Active Directory"._
