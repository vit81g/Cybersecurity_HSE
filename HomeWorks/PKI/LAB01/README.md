# Лабораторная работа 1 — Создание цепочки сертификатов с помощью OpenSSL

**Дисциплина:** Криптография / Безопасность сетей и систем  
**Тема:** Создание и анализ трёхуровневой цепочки сертификатов X.509  
**Автор:** Vitaliy Novikov, группа МКБ241  
**Дата выполнения:** 08.10.2025  

---

## 🎯 Цель работы

Изучить процесс создания цепочки цифровых сертификатов X.509 с использованием OpenSSL.  
Сформировать иерархию доверия из трёх уровней:

1. **Корневой центр сертификации (Root CA)** — *HSE Root Certification Authority*  
2. **Промежуточный центр сертификации (Group CA)** — *MKB241 Group Certification Authority*  
3. **Пользовательский сертификат** — *Vitaliy Novikov*  

---

## ⚙️ Используемые инструменты

- **OpenSSL 1.0.2j-FIPS (2016)**  
- **Windows 10 / 11**  
- **certmgr.msc** — просмотр установленных сертификатов  
- **cmd / bat script** — автоматизация генерации

---

## 🧩 Структура проекта

```
PKI/
 ├── LAB01/
 │   ├── conf/         # Конфигурационные файлы и скрипты
 │   │    ├── do_it.bat
 │   │    ├── openssl.cnf
 │   │    └── vm.txt
 │   │
 │   ├── cert/         # Сгенерированные сертификаты
 │   │    ├── rootca.crt
 │   │    ├── groupmca.crt
 │   │    └── usercert.crt
 │   │
 │   └── screens/      # Скриншоты выполнения и свойств сертификатов
 │        ├── cert01.jpg
 │        ├── cert02.jpg
 │        ├── cert03.jpg
 │        ├── Details_RootCA.jpg
 │        ├── Details_MKB241.jpg
 │        └── Details_User.jpg
```

---

## 🧠 Основные этапы

1. **Root CA (ВШЭ):**  
   создаётся самоподписанный сертификат с расширениями `basicConstraints = CA:true`, `keyUsage = keyCertSign, cRLSign`.  

2. **Group CA (МКБ241):**  
   подписывается Root CA, содержит `basicConstraints = CA:true, pathlen:0`,  
   а также ограничение пространства имён:  
   ```
   Name Constraints → Имя RFC822 = edu.hse.ru
   ```  

3. **User Certificate (Vitaliy Novikov):**  
   создаётся и подписывается Group CA.  
   Включает:
   - `keyUsage = dataEncipherment, keyEncipherment, digitalSignature`
   - `extendedKeyUsage = emailProtection`
   - `subjectKeyIdentifier` и `authorityKeyIdentifier`

---

## 🧾 Скрипт автоматизации

Файл [`conf/do_it.bat`](../conf/do_it.bat)  
автоматически выполняет следующие шаги:

- генерацию ключей и сертификатов;
- подпись подчинённых центров;
- сборку цепочки `rootca → groupmca → usercert`;
- импорт в хранилище Windows через `certutil`.

---

## ⚙️ Конфигурация OpenSSL

Файл [`conf/openssl.cnf`](../conf/openssl.cnf)  
содержит секции для всех трёх сертификатов, включая `v3_mca` с полем `nameConstraints`:

```ini
[ v3_mca ]
basicConstraints = critical, CA:true, pathlen:0
keyUsage = critical, keyCertSign, cRLSign
extendedKeyUsage = emailProtection
nameConstraints = permitted;email:edu.hse.ru
```

---

## 🖼️ Скриншоты

| Уровень | Состав сертификата | Вкладка |
|----------|--------------------|----------|
| 🟩 Root CA | ![Root CA Details](../screens/Details_RootCA.jpg) | Состав |
| 🟨 Group CA | ![Group CA Details](../screens/Details_MKB241.jpg) | Состав |
| 🟦 User Cert | ![User Cert Details](../screens/Details_User.jpg) | Состав |

| Сертификаты в certmgr.msc | Пример цепочки |
|----------------------------|----------------|
| ![Cert 01](../screens/cert01.jpg) | ![Cert 02](../screens/cert02.jpg) |

---

## ✅ Результат

- Цепочка из трёх сертификатов успешно создана и установлена в хранилище Windows.  
- Все требуемые расширения присутствуют и корректно отображаются.  
- Ошибки и предупреждения отсутствуют.  
- Цель лабораторной работы достигнута.

---

## 📚 Автор
**Vitaliy Novikov**  
НИУ ВШЭ, группа МКБ241
