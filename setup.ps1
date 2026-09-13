param(
    [string]$DotnetPath = 'C:\Program Files\dotnet\dotnet.exe',
    [string]$PythonPath = 'C:\Users\Administrator\AppData\Local\Programs\Python\Python314\python.exe'
)
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
$lock = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'toolchain.lock.json') -Raw -Encoding UTF8 | ConvertFrom-Json
foreach ($exe in @($DotnetPath,$PythonPath)) {
    if (-not (Test-Path -LiteralPath $exe)) { throw "Required existing runtime missing: $exe. Pass its absolute path." }
}
New-Item -ItemType Directory -Path (Join-Path $PSScriptRoot '.tools/downloads') -Force | Out-Null
foreach ($name in @('godot','blender')) {
    $item = $lock.$name
    if (Test-Path -LiteralPath (Join-Path $PSScriptRoot $item.exe)) { continue }
    $zip = Join-Path $PSScriptRoot ".tools/downloads/$name.zip"
    if (-not (Test-Path -LiteralPath $zip)) { Invoke-WebRequest -Uri $item.url -OutFile $zip }
    if ((Get-FileHash -LiteralPath $zip -Algorithm SHA256).Hash -ne $item.sha256) { throw "$name checksum mismatch; preserve and inspect $zip" }
    Expand-Archive -LiteralPath $zip -DestinationPath (Join-Path $PSScriptRoot ".tools/$name") -Force
}
if (-not (Test-Path -LiteralPath (Join-Path $PSScriptRoot '.venv/Scripts/python.exe'))) {
    & $PythonPath -m venv (Join-Path $PSScriptRoot '.venv')
    if ($LASTEXITCODE -ne 0) { throw 'Python environment creation failed' }
}
@{godot=$lock.godot.exe; blender=$lock.blender.exe; dotnet=$DotnetPath; python=$PythonPath} |
    ConvertTo-Json | Set-Content -LiteralPath (Join-Path $PSScriptRoot 'environment.local.json') -Encoding UTF8
# Upstream source fetching is intentionally separate: follow the local skill registry process before fetching its bundled SKILL.md.
& (Join-Path $PSScriptRoot 'tools/check-environment.ps1')
