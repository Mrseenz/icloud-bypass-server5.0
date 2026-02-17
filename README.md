# icloud-bypass-server

Modernized local activation server for research/testing with newer iDevices.

## Status / TODOs

The legacy README TODOs are now implemented:

- ✅ XAMPP/OpenSSL path setup no longer requires manual line toggling in `deviceActivation`.
- ✅ Generator `.cmd` files can be auto-configured for your local XAMPP path.
- ✅ Activation/signing flow has modern SHA-256 defaults.
- ✅ Tools updated for newer product identifiers and safer parsing/output.
- ✅ Dual-IMEI parsing and response support added (`InternationalMobileEquipmentIdentity` + `InternationalMobileEquipmentIdentity2`).
- ✅ System trust + registry hardening automation scripts added.

## Quick setup (XAMPP)

1. Install **XAMPP** (Apache + PHP).
2. Open PowerShell **as Administrator**.
3. Run:

```powershell
cd <repo>
./scripts/xampp/install-dependencies.ps1 -XamppRoot "C:\xampp" -AddHostsEntry -ApplyRegistryHardening -InstallRootCertificate
```

This script:
- copies project files into `C:\xampp\htdocs\icloud-bypass-server5.0`
- enables required PHP extensions (`openssl`, `dom`) in `php.ini`
- rewrites OpenSSL paths in cert generator `.cmd` files
- optionally adds `127.0.0.1 albert.apple.com` to hosts
- optionally applies modern TLS registry settings
- optionally installs `deviceservices/certs/generator/RootCA.crt` into the Windows trust stores

Then restart Apache from XAMPP Control Panel.

## Certificate trust / registry scripts

- `scripts/xampp/trust-root-ca.ps1` (`.cmd` wrapper available)
  - Installs local Root CA into Windows certificate stores so apps trust certificates issued by this CA.
- `scripts/xampp/apply-registry-hardening.ps1` (`.cmd` wrapper available)
  - Imports `scripts/xampp/enable-modern-tls.reg` to enable modern TLS defaults.

## Optional helper wrappers

```cmd
scripts\xampp\install-dependencies.cmd -XamppRoot C:\xampp -AddHostsEntry -ApplyRegistryHardening -InstallRootCertificate
scripts\xampp\configure-openssl-paths.cmd -XamppRoot C:\xampp
scripts\xampp\trust-root-ca.cmd
scripts\xampp\apply-registry-hardening.cmd
```

## Notes

- Generator scripts live under `deviceservices/certs/generator/`.
- Activation endpoint is `deviceservices/deviceActivation`.
- For dual-SIM capable devices, the server preserves second IMEI when provided by activation payload.
- Admin permissions are required for hosts edits, registry imports, and LocalMachine certificate store changes.

For entertainment purposes only.
