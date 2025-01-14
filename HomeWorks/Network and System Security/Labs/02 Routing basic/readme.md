# GNS3 Network Configuration - Cisco Routers and PCs

---

## 📌 PC Configuration:

### PC1:
```plaintext
ip 10.180.8.2 255.255.252.0 10.180.8.1
```

### PC2:
```plaintext
ip 10.180.255.2 255.255.255.0 10.180.255.1
```

### PC3:
```plaintext
ip 10.180.32.194 255.255.255.248 10.180.32.193
```

### PC4:
```plaintext
ip 10.180.64.130 255.255.255.224 10.180.64.129
```

---

## 📌 Router Configuration:

### R1:
```plaintext
enable
configure terminal
hostname R1
username user1 privilege 15 secret P@ssw0rd-ATM
enable secret P@ssw0rd-ATM

interface ethernet 0/0
 ip address 10.180.8.1 255.255.252.0
 no shutdown
exit

interface ethernet 0/1
 ip address 172.16.0.1 255.255.255.252
 no shutdown
exit

interface ethernet 0/2
 ip address 172.16.0.14 255.255.255.252
 no shutdown
exit

do write
```

### R2:
```plaintext
enable
configure terminal
hostname R2
username user1 privilege 15 secret P@ssw0rd-ATM
enable secret P@ssw0rd-ATM

interface ethernet 0/0
 ip address 10.180.255.1 255.255.255.0
 no shutdown
exit

interface ethernet 0/1
 ip address 172.16.0.2 255.255.255.252
 no shutdown
exit

interface ethernet 0/2
 ip address 172.16.0.5 255.255.255.252
 no shutdown
exit

do write
```

### R3:
```plaintext
enable
configure terminal
hostname R3
username user1 privilege 15 secret P@ssw0rd-ATM
enable secret P@ssw0rd-ATM

interface ethernet 0/0
 ip address 10.180.32.193 255.255.255.248
 no shutdown
exit

interface ethernet 0/1
 ip address 172.16.0.6 255.255.255.252
 no shutdown
exit

interface ethernet 0/2
 ip address 172.16.0.9 255.255.255.252
 no shutdown
exit

do write
```

### R4:
```plaintext
enable
configure terminal
hostname R4
username user1 privilege 15 secret P@ssw0rd-ATM
enable secret P@ssw0rd-ATM

interface ethernet 0/0
 ip address 10.180.64.129 255.255.255.224
 no shutdown
exit

interface ethernet 0/1
 ip address 172.16.0.10 255.255.255.252
 no shutdown
exit

interface ethernet 0/2
 ip address 172.16.0.13 255.255.255.252
 no shutdown
exit

do write
```

---

## 📌 Статическая маршрутизация:

### R1:
```plaintext
configure terminal
ip route 10.180.255.0 255.255.255.0 172.16.0.2
ip route 10.180.32.192 255.255.255.248 172.16.0.2
ip route 10.180.64.128 255.255.255.224 172.16.0.13
do write
```
- К сети R2 и R3 через `172.16.0.2`.
- К сети R4 через `172.16.0.13`.

### R2:
```plaintext
configure terminal
ip route 10.180.8.0 255.255.252.0 172.16.0.1
ip route 10.180.32.192 255.255.255.248 172.16.0.6
ip route 10.180.64.128 255.255.255.224 172.16.0.6
do write
```
- К сети R1 через `172.16.0.1`.
- К сети R3 и R4 через `172.16.0.6`.

### R3:
```plaintext
configure terminal
ip route 10.180.8.0 255.255.252.0 172.16.0.1
ip route 10.180.255.0 255.255.255.0 172.16.0.5
ip route 10.180.64.128 255.255.255.224 172.16.0.10
do write
```
- К сети R1 через `172.16.0.1`.
- К сети R2 через `172.16.0.5`.
- К сети R4 через `172.16.0.10`.

### R4:
```plaintext
configure terminal
ip route 10.180.8.0 255.255.252.0 172.16.0.14
ip route 10.180.255.0 255.255.255.0 172.16.0.14
ip route 10.180.32.192 255.255.255.248 172.16.0.9
do write
```
- К сети R1 через `172.16.0.14`.
- К сети R2 через `172.16.0.14`.
- К сети R3 через `172.16.0.9`.

---

## 📌 Проверка связности:

```plaintext
ping 10.180.8.1
ping 10.180.255.1
ping 10.180.32.193
ping 10.180.64.129
```


