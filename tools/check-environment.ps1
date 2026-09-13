. (Join-Path $PSScriptRoot 'env.ps1')
$output = Join-Path $LabRoot 'artifacts/environment-smoke'
New-Item -ItemType Directory -Path $output -Force | Out-Null
$EnvironmentLog = Join-Path $output 'check.log'
Set-Content -LiteralPath $EnvironmentLog -Value '' -Encoding UTF8
@{status='RUNNING'; scope='Environment only'; checkedAt=(Get-Date -Format o)} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $output 'result.json') -Encoding UTF8
Push-Location $LabRoot
try {
    Invoke-Checked $GodotExe @('--version')
    Invoke-Checked $DotnetExe @('--version')
    Invoke-Checked $PythonExe @('--version')
    Invoke-Checked $BlenderExe @('--background','--factory-startup','--python-exit-code','1','--python',(Join-Path $PSScriptRoot 'blender_smoke.py'),'--',$output)
    Invoke-Checked $DotnetExe @('build','game/GodogenLab.csproj','--nologo')
    Invoke-Checked $GodotExe @('--headless','--path','game','--script','res://builders/BuildEnvironment.cs')
    Invoke-Checked $GodotExe @('--headless','--path','game','--editor','--import')
    Invoke-Checked $GodotExe @('--headless','--path','game','--script','res://checks/CheckAsset.cs')
    Invoke-Checked $GodotExe @('--headless','--path','game','--quit-after','3')
    @{status='PASS'; scope='Environment only'; checkedAt=(Get-Date -Format o)} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $output 'result.json') -Encoding UTF8
} finally {
    Pop-Location
}
