# Настройка IPSec VPN между двумя маршрутизаторами Cisco

![](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Network%20and%20System%20Security/HW29/screens/task_ipsec.jpg)

## 📘 Общая информация

- Внутренняя сеть POD68: `10.0.68.0/24`
- Внутренняя сеть POD72: `10.0.72.0/24`
- WAN интерфейс (POD68): `DHCP`, IP: `10.121.1.201`
- WAN интерфейс (POD72): `DHCP`, IP: `10.121.1.249`
- DNS сервер (AD): `10.0.68.5`
- Общий Pre-Shared Key (PSK): `P@ssw0rd-PSK6872`

## 🎯 Цель
Обеспечить безопасное соединение между двумя подсетями через IPSec VPN.

## ⚙️ Этапы настройки

# IPSec VPN между роутерами POD68 и POD72

## 📃 Общие данные

| Сторона       | Внутренняя сеть | IP WAN              | Роутер WAN       | Сервер |
|------------------|-----------------------|---------------------|----------------------|---------|
| POD68            | 10.0.68.0/24          | 10.121.1.201 (DHCP) | POD68-CSR Gi2       | 10.0.68.5|
| POD72            | 10.0.72.0/24          | 10.121.1.249        | POD72-CSR Gi2       | 10.0.72.5|

- DNS: 10.0.68.5 (AD)
- SSH доступ только с 10.0.68.6
- Общий предшаренный ключ (PSK): `P@ssw0rd-PSK6872`

## 🔧 Настройка IPSec VPN

### 1. Конфигурация интерфейсов
```bash
show ip interface brief
```
![](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Network%20and%20System%20Security/HW29/screens/brief.jpg)

### 2. NAT

📅 Удален NAT overload:
```bash
no ip nat inside source list 1 interface GigabitEthernet2 overload
```

🔎 Проверка:
```bash
show ip nat translations
```
![](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Network%20and%20System%20Security/HW29/screens/nat.jpg)

### 3. Создание Access List
```bash
access-list 100 permit ip 10.0.68.0 0.0.0.255 10.0.72.0 0.0.0.255
```
![](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Network%20and%20System%20Security/HW29/screens/access_list.jpg)

### 4. Настройка ISAKMP/IKE
```bash
crypto isakmp policy 1
 encr aes
 authentication pre-share
 group 5
crypto isakmp key P@ssw0rd-PSK6872 address 10.0.72.1
```

### 5. Трансформ-сет и карта
```bash
crypto ipsec transform-set VPN-SET esp-aes esp-sha-hmac
crypto map VPN-MAP 10 ipsec-isakmp
 set peer 10.121.1.249
 set transform-set VPN-SET
 set pfs group5
 match address VPN-TRAFFIC
```
![](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Network%20and%20System%20Security/HW29/screens/section_crypto.jpg)

### 6. Применение crypto map
```bash
interface GigabitEthernet2
 crypto map VPN-MAP
```

### 7. Проверка

- **ISAKMP:**
```bash
show crypto isakmp sa
```
![](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Network%20and%20System%20Security/HW29/screens/crypto_sa.jpg)

- **IPSec:**
```bash
show crypto ipsec sa
```
![](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Network%20and%20System%20Security/HW29/screens/ipsec_sa_01.jpg)
![](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Network%20and%20System%20Security/HW29/screens/ipsec_sa_02.jpg)

### 8. Тест соединения
```bash
ping 10.0.72.5
```
![](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Network%20and%20System%20Security/HW29/screens/ping.jpg)

## 📂 Итог

Соединение IPSec на стороне POD68 было настроено. Подключения и перехват трафика IPSec пока не последовали, скорее всего, на стороне POD72 не запущен VPN.

## 📂 Примечания

> _Репозиторий создан в рамках курса "Защита компьютерных сетей и систем" направления "Кибербезопасность", НИУ ВШЭ._