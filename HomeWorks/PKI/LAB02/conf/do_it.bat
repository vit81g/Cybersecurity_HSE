@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion
cd /d C:\Lab1

rem ====================================================================
rem  ЛАБОРАТОРНАЯ РАБОТА №2 — OpenSSL PKI (НИУ ВШЭ, МКБ241)
rem  Автор: Vitaliy Novikov
rem  Цель: создание цепочки сертификатов (Root → Group → User) и PKCS#12
rem ====================================================================

set PASS_KEY=HSEPassw0rd
set PASS_PFX=UserPass123
set OPENSSL=openssl.exe

echo === Автоматическое создание цепочки сертификатов HSE / MKB241 ===
echo Рабочая папка: %cd%

rem --------------------------------------------------------------------
echo === [1/5] Создание Root CA (HSE) ===
%OPENSSL% req -utf8 -nameopt multiline,utf8 -batch -x509 -newkey rsa:8192 -passout pass:"%PASS_KEY%" -days 3650 ^
 -config openssl.cnf -extensions v3_ca -keyout rootca.key -out rootca.crt

rem --------------------------------------------------------------------
echo === [2/5] Создание Group CA (MKB241) ===
%OPENSSL% req -utf8 -nameopt multiline,utf8 -batch -newkey rsa:8192 -passout pass:"%PASS_KEY%" ^
 -config openssl.cnf -keyout groupmca.key -out groupmca.csr

%OPENSSL% x509 -req -passin pass:"%PASS_KEY%" -in groupmca.csr -CA rootca.crt -CAkey rootca.key -CAcreateserial ^
 -days 730 -extfile openssl.cnf -extensions v3_mca -out groupmca.crt

rem --------------------------------------------------------------------
echo === [3/5] Создание пользовательского сертификата (Vitaliy Novikov) ===
%OPENSSL% req -utf8 -nameopt multiline,utf8 -batch -newkey rsa:8192 -passout pass:"%PASS_KEY%" ^
 -config openssl.cnf -keyout usercert.key -out usercert.csr

%OPENSSL% x509 -req -passin pass:"%PASS_KEY%" -in usercert.csr -CA groupmca.crt -CAkey groupmca.key -CAcreateserial ^
 -days 365 -extfile openssl.cnf -extensions usr_cert -out usercert.crt

rem --------------------------------------------------------------------
echo === [4/5] Создание контейнера PKCS#12 ===
type usercert.crt groupmca.crt rootca.crt > chain.crt

%OPENSSL% pkcs12 -export -passin pass:"%PASS_KEY%" -passout pass:"%PASS_PFX%" ^
 -in chain.crt -inkey usercert.key -out final.p12

rem --------------------------------------------------------------------
echo === [5/5] Импорт сертификатов в хранилище Windows ===
certutil -f -p %PASS_PFX% -importpfx final.p12

echo === ГОТОВО! Цепочка сертификатов создана и установлена. ===
echo === Проверь certmgr.msc → Личное → Сертификаты ===
timeout /t 5 >nul
endlocal
