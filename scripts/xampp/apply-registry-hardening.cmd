@ECHO OFF
SETLOCAL
SET SCRIPT_DIR=%~dp0
powershell -ExecutionPolicy Bypass -File "%SCRIPT_DIR%apply-registry-hardening.ps1" %*
ENDLOCAL
