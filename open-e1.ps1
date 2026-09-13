param([ValidateSet('Ink','Base')][string]$Variant = 'Ink')
. (Join-Path $PSScriptRoot 'tools/env.ps1')
# User-invoked review window. A/B keys compare materials; this is not gameplay.
& $GodotExe --path (Join-Path $LabRoot 'game') "res://scenes/E1$Variant.tscn" --resolution 1280x720
