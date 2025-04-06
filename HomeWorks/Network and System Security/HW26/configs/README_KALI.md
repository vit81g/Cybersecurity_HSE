
# Настройка Kali Linux

## 1. Сетевая конфигурация

На Kali Linux используется автоматическое получение IP-адреса по DHCP.

Интерфейс `eth0` получает настройки автоматически от маршрутизатора Cisco:

- Примерный IP-адрес: `10.0.68.X` (из пула DHCP)
- Маска подсети: `255.255.255.0`
- Шлюз по умолчанию: `10.0.68.1`
- DNS-серверы:
  - `10.0.68.5` (контроллер домена)
  - `8.8.8.8` (публичный DNS от Google)

> ✅ DHCP настроен на маршрутизаторе Cisco, Kali получает доступ в интернет и может взаимодействовать с Active Directory.

### Вывод команды `ip -a`

![ip a](https://github.com/vit81g/Cybersecurity_HSE/blob/main/HomeWorks/Network%20and%20System%20Security/HW26/screenshots/4_2_kali_ip_a.jpg)

---

## 2. Установка инструментов

Для проведения атак на Active Directory планируется использовать:

- `mitm6` — атаки на протоколы IPv6
- `impacket` — набор инструментов для работы с AD (например, `secretsdump`, `wmiexec`, `smbexec`)
- `responder` — захват хэшей через NBNS и LLMNR

Установка mitm6:
```bash
sudo apt update
sudo apt install mitm6
```

---

## 3. Прочее

- Kali подключён к виртуальному коммутатору VMware
- Получает сетевые настройки от маршрутизатора Cisco (DHCP)
- Доступ в интернет активен
