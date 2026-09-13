$ErrorActionPreference = 'Stop'
$LabRoot = Split-Path -Parent $PSScriptRoot
$config = Get-Content -LiteralPath (Join-Path $LabRoot 'environment.local.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$GodotExe = Join-Path $LabRoot $config.godot
$BlenderExe = Join-Path $LabRoot $config.blender
$PythonExe = Join-Path $LabRoot '.venv/Scripts/python.exe'
$DotnetExe = $config.dotnet
foreach ($exe in @($GodotExe, $BlenderExe, $PythonExe, $DotnetExe)) {
    if (-not (Test-Path -LiteralPath $exe)) { throw "Missing tool: $exe" }
}
$env:DOTNET_ROOT = Split-Path -Parent $DotnetExe
$env:PATH = "$env:DOTNET_ROOT;$(Split-Path -Parent $GodotExe);$(Split-Path -Parent $BlenderExe);$env:PATH"
$env:DOTNET_CLI_TELEMETRY_OPTOUT = '1'
$env:PYTHONUTF8 = '1'
function Invoke-Checked([string]$Exe, [string[]]$Arguments) {
    if ($EnvironmentLog) { & $Exe @Arguments 2>&1 | Tee-Object -FilePath $EnvironmentLog -Append }
    else { & $Exe @Arguments }
    if ($LASTEXITCODE -ne 0) { throw "$Exe exited $LASTEXITCODE" }
}
