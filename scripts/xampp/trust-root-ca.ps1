param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path,
    [string]$RootCertificatePath = '',
    [switch]$CurrentUserOnly
)

if ([string]::IsNullOrWhiteSpace($RootCertificatePath)) {
    $RootCertificatePath = Join-Path $RepoRoot 'deviceservices\certs\generator\RootCA.crt'
}

if (-not (Test-Path $RootCertificatePath)) {
    throw "Root certificate file not found: $RootCertificatePath"
}

Write-Host "Installing root certificate from $RootCertificatePath"

if ($CurrentUserOnly) {
    certutil -user -addstore -f Root $RootCertificatePath | Out-Host
    Write-Host 'Installed certificate into CurrentUser Root store.'
} else {
    certutil -addstore -f Root $RootCertificatePath | Out-Host
    certutil -addstore -f CA $RootCertificatePath | Out-Host
    Write-Host 'Installed certificate into LocalMachine Root and CA stores.'
}
