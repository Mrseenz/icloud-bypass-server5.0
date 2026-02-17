param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path,
    [string]$XamppRoot = 'C:\xampp'
)

$opensslConf = Join-Path $XamppRoot 'apache\conf\openssl.cnf'
$opensslBin = Join-Path $XamppRoot 'apache\bin'

if (-not (Test-Path $RepoRoot)) {
    throw "Repository root not found: $RepoRoot"
}
if (-not (Test-Path $opensslConf)) {
    throw "OpenSSL config not found at $opensslConf"
}
if (-not (Test-Path (Join-Path $opensslBin 'openssl.exe'))) {
    throw "openssl.exe not found in $opensslBin"
}

$cmdFiles = Get-ChildItem -Path (Join-Path $RepoRoot 'deviceservices\certs\generator') -Recurse -Filter '*.cmd'

foreach ($file in $cmdFiles) {
    $content = Get-Content -Raw -Path $file.FullName
    $content = [regex]::Replace($content, 'SET OPENSSL_CONF=.*', "SET OPENSSL_CONF=$opensslConf")
    $content = [regex]::Replace($content, 'PATH=%PATH%;.*', "PATH=%PATH%;$opensslBin")
    Set-Content -Path $file.FullName -Value $content -NoNewline
    Write-Host "Updated $($file.FullName)"
}

Write-Host "All generator .cmd files now point to XAMPP OpenSSL paths."
