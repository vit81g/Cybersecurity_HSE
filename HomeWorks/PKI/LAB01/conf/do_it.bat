@echo off
chcp 65001 > nul
cd /d C:\Lab1

rem ================================================================
rem Автоматическое создание дерева сертификатов
rem Root CA – ВШЭ (HSE)
rem Group CA – МКБ241 (MKB241)
rem User – Vitaliy Novikov
rem ================================================================

set PASS=HSEPassw0rd
set OPENSSL=openssl.exe

echo === Автоматическое создание цепочки сертификатов HSE / MKB241 ===
echo Рабочая папка: %cd%

rem ----------------------------------------------------------------
rem 1. СОЗДАНИЕ КОРНЕВОГО СЕРТИФИКАТА (HSE Root Certification Authority)
rem ----------------------------------------------------------------
echo === [1/5] Создание Root CA (HSE) ===
%OPENSSL% req -new -x509 -newkey rsa:2048 -sha256 ^
 -days 3650 -config "%~dp0openssl.cnf" -extensions v3_ca ^
 -keyout rootca.key -out rootca.crt ^
 -passout pass:%PASS% ^
 -subj "/C=RU/ST=Saint Petersburg/L=Saint Petersburg/O=HSE/OU=RootCA/CN=HSE Root Certification Authority/emailAddress=ca@hse.ru"

rem ----------------------------------------------------------------
rem 2. СОЗДАНИЕ ПРОМЕЖУТОЧНОГО УЦ (Group CA – МКБ241)
rem ----------------------------------------------------------------
echo === [2/5] Создание Group CA (MKB241) ===
%OPENSSL% req -new -newkey rsa:2048 -sha256 ^
 -config "%~dp0openssl.cnf" -keyout groupmca.key -out groupmca.csr ^
 -passout pass:%PASS% ^
 -subj "/C=RU/ST=Saint Petersburg/L=Saint Petersburg/O=HSE/OU=MKB241/CN=MKB241 Group Certification Authority"

%OPENSSL% x509 -req -in groupmca.csr -CA rootca.crt -CAkey rootca.key -CAcreateserial ^
 -days 1825 -sha256 -extfile "%~dp0openssl.cnf" -extensions v3_mca ^
 -passin pass:%PASS% -out groupmca.crt

rem ----------------------------------------------------------------
rem 3. СОЗДАНИЕ ПОЛЬЗОВАТЕЛЬСКОГО СЕРТИФИКАТА (Vitaliy Novikov)
rem ----------------------------------------------------------------
echo === [3/5] Создание пользовательского сертификата (Vitaliy Novikov) ===
%OPENSSL% req -new -newkey rsa:2048 -sha256 ^
 -config "%~dp0openssl.cnf" -keyout usercert.key -out usercert.csr ^
 -passout pass:%PASS% ^
 -subj "/C=RU/ST=Saint Petersburg/L=Saint Petersburg/O=HSE/OU=MKB241/CN=Vitaliy Novikov/emailAddress=vsnovikov@edu.hse.ru"

%OPENSSL% x509 -req -in usercert.csr -CA groupmca.crt -CAkey groupmca.key -CAcreateserial ^
 -days 730 -sha256 -extfile "%~dp0openssl.cnf" -extensions usr_cert ^
 -passin pass:%PASS% -out usercert.crt

rem ----------------------------------------------------------------
rem 4. СОЗДАНИЕ КОНТЕЙНЕРА PKCS#12
rem ----------------------------------------------------------------
echo === [4/5] Создание контейнера PKCS#12 ===
type usercert.crt groupmca.crt rootca.crt > chain.crt

%OPENSSL% pkcs12 -export -inkey usercert.key -in usercert.crt ^
 -certfile chain.crt -out final.p12 ^
 -passin pass:%PASS% -passout pass:%PASS% -name "Vitaliy Novikov (MKB241)"

rem ----------------------------------------------------------------
rem 5. УСТАНОВКА В ХРАНИЛИЩЕ WINDOWS
rem ----------------------------------------------------------------
echo === [5/5] Импорт сертификатов в хранилище Windows ===
certutil -f -p %PASS% -importpfx final.p12

echo === ГОТОВО! Цепочка сертификатов создана и установлена. ===
echo === Проверь certmgr.msc → Личное → Сертификаты ===
pause
