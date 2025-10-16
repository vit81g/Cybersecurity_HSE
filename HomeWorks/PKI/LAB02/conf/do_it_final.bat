@echo off
chcp 65001 > nul
cd /d C:\Lab02
set OPENSSL=openssl.exe

echo === Автоматическое создание цепочки сертификатов HSE / MKB241 ===
echo Рабочая папка: %CD%
echo.

set PASS_KEY=HSEPassw0rd
set PASS_PFX=UserPass123

rem ============================================================
echo [1/5] Создание Root CA (HSE Root Certification Authority)
%OPENSSL% req -utf8 -new -x509 -newkey rsa:8192 -passout pass:"%PASS_KEY%" -days 3650 ^
 -config openssl.cnf -extensions v3_ca ^
 -subj "/C=RU/ST=Saint Petersburg/L=Saint Petersburg/O=HSE/OU=MKB241/CN=HSE Root Certification Authority/emailAddress=root@hse.ru" ^
 -keyout rootca.key -out rootca.crt

if not exist rootca.crt (
    echo [ОШИБКА] Не создан Root CA (rootca.crt).
    pause
    exit /b
) else (
    echo [OK] Root CA создан.
)
echo.

rem ============================================================
echo [2/5] Создание Group CA (MKB241 Group Certification Authority)
%OPENSSL% req -utf8 -new -newkey rsa:8192 -passout pass:"%PASS_KEY%" -config openssl.cnf ^
 -subj "/C=RU/ST=Saint Petersburg/L=Saint Petersburg/O=HSE/OU=MKB241/CN=MKB241 Group Certification Authority/emailAddress=groupca@hse.ru" ^
 -keyout groupmca.key -out groupmca.csr

%OPENSSL% x509 -req -passin pass:"%PASS_KEY%" -in groupmca.csr -CA rootca.crt -CAkey rootca.key -CAcreateserial -days 1825 ^
 -extfile openssl.cnf -extensions v3_mca -out groupmca.crt

if not exist groupmca.crt (
    echo [ОШИБКА] Не создан Group CA (groupmca.crt).
    pause
    exit /b
) else (
    echo [OK] Group CA создан.
)
echo.

rem ============================================================
echo [3/5] Создание User Certificate (Vitaliy Novikov)
%OPENSSL% req -utf8 -new -newkey rsa:8192 -passout pass:"%PASS_KEY%" -config openssl.cnf ^
 -subj "/C=RU/ST=Saint Petersburg/L=Saint Petersburg/O=HSE/OU=MKB241/CN=Vitaliy Novikov/emailAddress=vsnovikov@edu.hse.ru" ^
 -keyout usercert.key -out usercert.csr

%OPENSSL% x509 -req -passin pass:"%PASS_KEY%" -in usercert.csr -CA groupmca.crt -CAkey groupmca.key -CAcreateserial -days 730 ^
 -extfile openssl.cnf -extensions usr_cert -out usercert.crt

if not exist usercert.crt (
    echo [ОШИБКА] Не создан User Certificate (usercert.crt).
    pause
    exit /b
) else (
    echo [OK] Пользовательский сертификат создан.
)
echo.

rem ============================================================
echo [4/5] Создание контейнера PKCS#12
type usercert.crt groupmca.crt rootca.crt > certs.crt

if not exist certs.crt (
    echo [ОШИБКА] Не удалось создать объединённый файл certs.crt.
    pause
    exit /b
)

%OPENSSL% pkcs12 -export -in certs.crt -inkey usercert.key -out final.p12 ^
 -passin pass:"%PASS_KEY%" -passout pass:"%PASS_PFX%"

if not exist final.p12 (
    echo [ОШИБКА] Не создан файл final.p12.
    pause
    exit /b
) else (
    echo [OK] Контейнер PKCS#12 успешно создан.
)
echo.

rem ============================================================
echo [5/5] Импорт сертификата в хранилище Windows (автоматически, без подтверждения)
cd /d C:\Lab02

if not exist final.p12 (
    echo [ОШИБКА] Файл final.p12 не найден. Проверь предыдущие шаги!
    pause
    exit /b
)

certutil -user -f -p %PASS_PFX% -importpfx "%CD%\final.p12" MY

if %ERRORLEVEL% NEQ 0 (
    echo [ОШИБКА] Импорт сертификата не выполнен. Код ошибки: %ERRORLEVEL%
    pause
    exit /b
) else (
    echo [OK] Импорт сертификата успешно выполнен.
)
echo.
echo === ГОТОВО! Цепочка сертификатов HSE → MKB241 → Vitaliy Novikov создана и установлена. ===
echo Проверь certmgr.msc → Личное → Сертификаты
pause
