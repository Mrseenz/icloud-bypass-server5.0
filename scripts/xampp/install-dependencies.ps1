param(
    [string]$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path,
    [string]$XamppRoot = 'C:\xampp',
    [switch]$AddHostsEntry,
    [switch]$InstallRootCertificate,
    [switch]$ApplyRegistryHardening
)

$phpIni = Join-Path $XamppRoot 'php\php.ini'
$htdocsTarget = Join-Path $XamppRoot 'htdocs\icloud-bypass-server5.0'

if (-not (Test-Path $phpIni)) {
    throw "php.ini not found at $phpIni"
}

if (-not (Test-Path (Join-Path $XamppRoot 'apache\bin\openssl.exe'))) {
    throw "openssl.exe not found in $XamppRoot\apache\bin"
}

Copy-Item -Path $RepoRoot -Destination $htdocsTarget -Recurse -Force
Write-Host "Copied project to $htdocsTarget"

$phpIniContent = Get-Content -Raw $phpIni
foreach ($ext in @('openssl','dom')) {
    $phpIniContent = [regex]::Replace(
        $phpIniContent,
        "(?m)^\s*;\s*extension=$ext\s*$",
        "extension=$ext"
    )
}
Set-Content -Path $phpIni -Value $phpIniContent -NoNewline
Write-Host "Enabled required PHP extensions in php.ini (openssl, dom)."

& (Join-Path $PSScriptRoot 'configure-openssl-paths.ps1') -RepoRoot $RepoRoot -XamppRoot $XamppRoot

if ($AddHostsEntry) {
    $hostsPath = "$env:WINDIR\System32\drivers\etc\hosts"
    $line = '127.0.0.1 albert.apple.com'
    $existing = Get-Content $hostsPath -ErrorAction Stop
    if ($existing -notcontains $line) {
        Add-Content -Path $hostsPath -Value $line
        Write-Host "Added hosts entry: $line"
    } else {
        Write-Host "Hosts entry already present: $line"
    }
}

if ($ApplyRegistryHardening) {
    & (Join-Path $PSScriptRoot 'apply-registry-hardening.ps1')
}

if ($InstallRootCertificate) {
    & (Join-Path $PSScriptRoot 'trust-root-ca.ps1') -RepoRoot $RepoRoot
}

Write-Host "Done. Restart Apache in XAMPP control panel."
