@ECHO OFF
SET OPENSSL_CONF=C:\OpenServer\modules\http\Apache-2.4\conf\openssl.cnf
PATH=%PATH%;C:\OpenServer\modules\http\Apache-2.4\bin
openssl genpkey -algorithm RSA -out signature_private.key -pkeyopt rsa_keygen_bits:2048
rem openssl rsa -in signature_private.key -pubout -outform PEM -out signature_public.key
pause