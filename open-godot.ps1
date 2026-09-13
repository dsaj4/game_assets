. (Join-Path $PSScriptRoot 'tools/env.ps1')
Invoke-Checked $GodotExe @('--editor','--path',(Join-Path $LabRoot 'game'))
