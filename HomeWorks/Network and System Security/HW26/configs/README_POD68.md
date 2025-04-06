
# Cisco Router Configuration for AD Lab (POD68)

## 🔧 Стендовая конфигурация

- Внутренняя сеть: `10.0.68.0/24`
- IP маршрутизатора (LAN): `10.0.68.1`
- IP маршрутизатора (WAN): DHCP
- DNS-сервер: `10.0.68.5`
- DHCP для клиентов: от `10.0.68.6`
- SSH доступ только с `10.0.68.6`

## ✅ Настройка интерфейсов

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

## 🌐 NAT

```bash
access-list 1 permit 10.0.68.0 0.0.0.255
ip nat inside source list 1 interface GigabitEthernet2 overload
```

## 📡 DHCP

```bash
ip dhcp excluded-address 10.0.68.1 10.0.68.5

ip dhcp pool POD68-DHCP
 network 10.0.68.0 255.255.255.0
 default-router 10.0.68.1
 dns-server 10.0.68.5
```

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

## 🛠 Дополнительно

Скрипты, скриншоты и тесты подключений можно найти в `/docs/` или `screenshots/`.

---

_Проект для лабораторных работ по курсу "Защита компьютерных сетей и систем", подготовка стенда для атаки на AD._
