@ECHO OFF
SET OPENSSL_CONF=C:\OpenServer\modules\http\Apache-2.4\conf\openssl.cnf
PATH=%PATH%;C:\OpenServer\modules\http\Apache-2.4\bin
rem openssl pkeyutl -sign -in accounttoken.txt -out signature.txt -inkey signature_private.key
openssl pkeyutl -verifyrecover -in _signature.txt -out _accounttoken.txt -inkey ../signature_public.key -pubin

pause