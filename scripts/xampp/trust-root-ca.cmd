@ECHO OFF
SETLOCAL
SET SCRIPT_DIR=%~dp0
powershell -ExecutionPolicy Bypass -File "%SCRIPT_DIR%trust-root-ca.ps1" %*
ENDLOCAL
