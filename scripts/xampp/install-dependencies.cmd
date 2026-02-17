@ECHO OFF
SETLOCAL
SET SCRIPT_DIR=%~dp0
powershell -ExecutionPolicy Bypass -File "%SCRIPT_DIR%install-dependencies.ps1" %*
ENDLOCAL
