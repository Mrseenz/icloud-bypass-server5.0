@ECHO OFF
SETLOCAL
SET SCRIPT_DIR=%~dp0
powershell -ExecutionPolicy Bypass -File "%SCRIPT_DIR%configure-openssl-paths.ps1" %*
ENDLOCAL
