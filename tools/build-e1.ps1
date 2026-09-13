param([switch]$SkipAssets)
. (Join-Path $PSScriptRoot 'env.ps1')
$out = Join-Path $LabRoot 'artifacts/ui-experiment/E1'
[System.IO.Directory]::CreateDirectory($out) | Out-Null
$EnvironmentLog = Join-Path $out 'build.log'
Set-Content -LiteralPath $EnvironmentLog -Value 'E1 build started' -Encoding UTF8
Push-Location $LabRoot
try {
    if (-not $SkipAssets) {
        Invoke-Checked $BlenderExe @('--background','--factory-startup','--python-exit-code','1','--python',(Join-Path $LabRoot 'art/build_e1.py'))
    }
    Invoke-Checked $DotnetExe @('build','game/GodogenLab.csproj','--nologo')
    Invoke-Checked $GodotExe @('--headless','--path',(Join-Path $LabRoot 'game'),'--editor','--import')
    Invoke-Checked $GodotExe @('--headless','--path',(Join-Path $LabRoot 'game'),'--script','res://builders/BuildE1.cs')
    Invoke-Checked $GodotExe @('--headless','--path',(Join-Path $LabRoot 'game'),'res://scenes/E1Ink.tscn','--resolution','1280x720','--quit-after','2')
} finally { Pop-Location }
