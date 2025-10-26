@echo off
chcp 65001 > nul
cd /d %~dp0
set OPENSSL=openssl.exe

echo === 1. Создание корневого сертификата Root CA ===

openssl.exe req -x509 -newkey rsa:8192 -passout pass:"SecurePassHSE" -days 3650 -subj "/C=RU/ST=Moscow/L=Moscow/O=HSE/CN=HSE RootCA" -config openssl.cnf -extensions v3_ca -keyout rootca.key -out rootca.crt

echo === 2. Создание промежуточного сертификата ===

openssl.exe req -newkey rsa:8192 -passout pass:"SecurePassHSE" -subj "/C=RU/ST=Moscow/L=Moscow/O=HSE/CN=Group MCS242" -config openssl.cnf -keyout groupmca.key -out groupmca.csr

echo === 2.1. Подпись запроса и создание серверного сертификата ===

openssl.exe x509 -req -passin pass:"SecurePassHSE" -in groupmca.csr -CA rootca.crt -CAkey rootca.key -CAcreateserial -days 365 -extfile openssl.cnf -extensions v3_mca -out groupmca.crt


echo === 3. Создание конфигурационного файла для пользовательского сертификата с кириллицей ===

echo [ req ] > user_req.cnf
echo default_bits = 8192 >> user_req.cnf
echo distinguished_name = req_distinguished_name >> user_req.cnf
echo prompt = no >> user_req.cnf
echo string_mask = utf8only >> user_req.cnf
echo. >> user_req.cnf
echo [ req_distinguished_name ] >> user_req.cnf
echo C = RU >> user_req.cnf
echo ST = Москва >> user_req.cnf
echo L = Москва >> user_req.cnf
echo O = НИУ ВШЭ >> user_req.cnf
echo OU = МИЭМ >> user_req.cnf
echo CN = Виталий Новиков >> user_req.cnf

echo === 3.1 Создание пользовательского сертификата с кириллицей ===

openssl.exe req -newkey rsa:8192 -passout pass:"SecurePassHSE" -config user_req.cnf -keyout usercert.key -out usercert.csr -utf8

с
openssl.exe x509 -req -passin pass:"SecurePassHSE" -in usercert.csr -CA groupmca.crt -CAkey groupmca.key -CAcreateserial -days 90 -extfile openssl.cnf -extensions usr_cert -out usercert.crt

echo === 4. Создание контейнера ===

type usercert.crt groupmca.crt rootca.crt > certs.crt
openssl.exe pkcs12 -export -passin pass:"SecurePassHSE" -passout pass:"P12PassHSE" -in certs.crt -inkey usercert.key -out final.p12

echo === 5 Установка ===
certutil -f -p P12PassHSE -importpfx final.p12


echo.
echo Корневой сертификат (rootca.crt):
openssl x509 -in rootca.crt -subject -nameopt utf8,-esc_msb -noout
echo.
echo Промежуточный сертификат (groupmca.crt):
openssl x509 -in groupmca.crt -subject -nameopt utf8,-esc_msb -noout
echo.
echo Пользовательский сертификат (usercert.crt):
openssl x509 -in usercert.crt -subject -nameopt utf8,-esc_msb -noout

rem 7 Удаление временных файлов
del user_req.cnf

echo.
pause