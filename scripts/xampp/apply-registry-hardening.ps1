param(
    [string]$RegistryFilePath = (Join-Path $PSScriptRoot 'enable-modern-tls.reg')
)

if (-not (Test-Path $RegistryFilePath)) {
    throw "Registry file not found: $RegistryFilePath"
}

Write-Host "Importing registry settings from $RegistryFilePath"
reg import "$RegistryFilePath"
if ($LASTEXITCODE -ne 0) {
    throw 'Failed to import registry settings.'
}

Write-Host 'Registry updates applied successfully. Reboot is recommended.'
