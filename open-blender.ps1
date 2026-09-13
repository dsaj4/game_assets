. (Join-Path $PSScriptRoot 'tools/env.ps1')
Invoke-Checked $BlenderExe @('--factory-startup')
