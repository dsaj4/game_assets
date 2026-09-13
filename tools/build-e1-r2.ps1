param([switch]$SkipAssets)
. (Join-Path $PSScriptRoot 'env.ps1')
$out = Join-Path $LabRoot 'artifacts/ui-experiment/E1-r2'
[System.IO.Directory]::CreateDirectory($out) | Out-Null
$EnvironmentLog = Join-Path $out 'build.log'
Set-Content -LiteralPath $EnvironmentLog -Value 'E1 R2 build started' -Encoding UTF8
Push-Location $LabRoot
try {
    if (-not $SkipAssets) {
        $uiSource = Join-Path $LabRoot 'art/e1/e1-r2-ui.blend'
        $refineScript = Join-Path $LabRoot 'art/refine_e1_r2.py'
        foreach ($source in @($uiSource, $refineScript)) {
            if (-not (Test-Path -LiteralPath $source -PathType Leaf)) {
                throw "E1 R2 source missing: $source"
            }
        }
        # The refinement script loads the UI-edited source and writes the R2
        # master, manifest and the shared runtime base/ink GLB paths.
        Invoke-Checked $BlenderExe @('--background','--factory-startup','--python-exit-code','1','--python',$refineScript)
    }
    Invoke-Checked $DotnetExe @('build','game/GodogenLab.csproj','--nologo')
    Invoke-Checked $GodotExe @('--headless','--path',(Join-Path $LabRoot 'game'),'--editor','--import')
    Invoke-Checked $GodotExe @('--headless','--path',(Join-Path $LabRoot 'game'),'--script','res://builders/BuildE1.cs')
    Invoke-Checked $GodotExe @('--headless','--path',(Join-Path $LabRoot 'game'),'res://scenes/E1Ink.tscn','--resolution','1280x720','--quit-after','2')
} finally { Pop-Location }
