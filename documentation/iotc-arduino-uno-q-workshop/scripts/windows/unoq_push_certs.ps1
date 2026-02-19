param(
    [string]$DownloadsDir = "$env:USERPROFILE\Downloads",
    [string]$DemoDir = "/opt/demo",
    [switch]$SkipAdbInstall
)

$ErrorActionPreference = "Stop"

function Ensure-Adb {
    if (Get-Command adb -ErrorAction SilentlyContinue) {
        return
    }

    if ($SkipAdbInstall) {
        throw "adb not found and -SkipAdbInstall was set. Install Android Platform Tools and retry."
    }

    $zipUrl = "https://dl.google.com/android/repository/platform-tools-latest-windows.zip"
    $destDir = "$env:USERPROFILE\android-platform-tools"
    $zipPath = "$env:TEMP\platform-tools-latest-windows.zip"

    Write-Host "Downloading Android Platform Tools..."
    Invoke-WebRequest -Uri $zipUrl -OutFile $zipPath

    if (-not (Test-Path $destDir)) {
        New-Item -ItemType Directory -Path $destDir | Out-Null
    }

    Write-Host "Extracting to $destDir"
    Expand-Archive -Path $zipPath -DestinationPath $destDir -Force

    $adbPath = Join-Path $destDir "platform-tools\adb.exe"
    if (-not (Test-Path $adbPath)) {
        throw "adb.exe not found after extraction."
    }

    $env:PATH = "$($env:PATH);$([IO.Path]::GetDirectoryName($adbPath))"
}

function Find-ConfigFile {
    $config = Join-Path $DownloadsDir "iotcDeviceConfig.json"
    if (Test-Path $config) { return $config }

    $config = Get-ChildItem -Path $DownloadsDir -Filter "iotcDeviceConfig.json" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($config) { return $config.FullName }

    throw "iotcDeviceConfig.json not found in $DownloadsDir"
}

function Find-CertsZip {
    $zip = Get-ChildItem -Path $DownloadsDir -Filter "*cert*.zip" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($zip) { return $zip.FullName }

    throw "Certificate zip not found in $DownloadsDir (expected something like *cert*.zip)"
}

function Extract-Certs($zipPath, $extractDir) {
    Expand-Archive -Path $zipPath -DestinationPath $extractDir -Force

    $cert = Get-ChildItem -Path $extractDir -Recurse -Include "cert_*.crt","cert_*.pem" | Select-Object -First 1
    $key  = Get-ChildItem -Path $extractDir -Recurse -Include "pk_*.pem","key_*.key","key_*.pem" | Select-Object -First 1

    if (-not $cert) { throw "Certificate file not found in extracted zip." }
    if (-not $key) { throw "Private key file not found in extracted zip." }

    return @{ Cert = $cert.FullName; Key = $key.FullName }
}

function Push-To-UnoQ($configPath, $certPath, $keyPath) {
    Write-Host "Checking adb devices..."
    adb devices

    Write-Host "Creating demo dir on UNO Q: $DemoDir"
    adb shell "mkdir -p $DemoDir"

    $stage = Join-Path $env:TEMP "iotc_unoq_stage"
    if (Test-Path $stage) { Remove-Item -Recurse -Force $stage }
    New-Item -ItemType Directory -Path $stage | Out-Null

    Copy-Item $configPath (Join-Path $stage "iotcDeviceConfig.json") -Force
    Copy-Item $certPath (Join-Path $stage "device-cert.pem") -Force
    Copy-Item $keyPath  (Join-Path $stage "device-pkey.pem") -Force

    Write-Host "Pushing files to UNO Q..."
    adb push (Join-Path $stage "iotcDeviceConfig.json") "$DemoDir/"
    adb push (Join-Path $stage "device-cert.pem") "$DemoDir/"
    adb push (Join-Path $stage "device-pkey.pem") "$DemoDir/"

    Write-Host "Done. Files are on UNO Q at $DemoDir"
}

Ensure-Adb

$config = Find-ConfigFile
$zip = Find-CertsZip

$extractDir = Join-Path $env:TEMP "iotc_unoq_extract"
if (Test-Path $extractDir) { Remove-Item -Recurse -Force $extractDir }
New-Item -ItemType Directory -Path $extractDir | Out-Null

$certs = Extract-Certs $zip $extractDir

Push-To-UnoQ $config $certs.Cert $certs.Key
