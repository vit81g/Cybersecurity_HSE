


chcp 1251 > nul

openssl dgst -sign usercert.key -passin pass:"HSEPassw0rd" -sha256 -out novikov.txt.sig -binary novikov.txt

pause

openssl x509 -inform PEM -in usercert.crt -passin pass:"HSEPassw0rd" > usercert.pem
openssl x509 -in usercert.pem -noout -pubkey -passin pass:"HSEPassw0rd" > pubkey.usercert.pem

pause

openssl dgst -verify pubkey.usercert.pem -passin pass:"HSEPassw0rd" -sha256 -signature novikov.txt.sig -binary novikov.txt

pause

openssl dgst -verify pubkey.usercert.pem -passin pass:"HSEPassw0rd" -sha256 -signature novikov.txt.sig -binary novikov.txt

pause