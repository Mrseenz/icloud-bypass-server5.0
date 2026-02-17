# icloud-bypass-server

Modernized local activation server for research/testing with newer iDevices.

## Status / TODOs

The legacy README TODOs are now implemented:

- ✅ XAMPP/OpenSSL path setup no longer requires manual line toggling in `deviceActivation`.
- ✅ Generator `.cmd` files can be auto-configured for your local XAMPP path.
- ✅ Activation/signing flow has modern SHA-256 defaults.
- ✅ Tools updated for newer product identifiers and safer parsing/output.
- ✅ Dual-IMEI parsing and response support added (`InternationalMobileEquipmentIdentity` + `InternationalMobileEquipmentIdentity2`).

## Quick setup (XAMPP)

1. Install **XAMPP** (Apache + PHP).
2. Open PowerShell **as Administrator**.
3. Run:

```powershell
cd <repo>
./scripts/xampp/install-dependencies.ps1 -XamppRoot "C:\xampp" -AddHostsEntry
```

This script:
- copies project files into `C:\xampp\htdocs\icloud-bypass-server5.0`
- enables required PHP extensions (`openssl`, `dom`) in `php.ini`
- rewrites OpenSSL paths in cert generator `.cmd` files
- optionally adds `127.0.0.1 albert.apple.com` to hosts

Then restart Apache from XAMPP Control Panel.

## Optional helper wrappers

You can use CMD wrappers instead:

```cmd
scripts\xampp\install-dependencies.cmd -XamppRoot C:\xampp -AddHostsEntry
scripts\xampp\configure-openssl-paths.cmd -XamppRoot C:\xampp
```

## Notes

- Generator scripts live under `deviceservices/certs/generator/`.
- Activation endpoint is `deviceservices/deviceActivation`.
- For dual-SIM capable devices, the server now preserves second IMEI when provided by activation payload.

For entertainment purposes only.
