param([ValidateSet('assembly','leather','rack','raw','rhythm','ember','parchment','controls')][string]$Asset = 'assembly')
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'tools/env.ps1')
$files = @{
    assembly = 'art/wand-management-v01/wand-management-master.blend'
    leather = 'art/wand-management-v01/assets/WM-01-deployed-leather.blend'
    rack = 'art/wand-management-v01/assets/WM-02-reserve-rack.blend'
    raw = 'art/wand-management-v01/assets/WM-03-raw-wood-staff.blend'
    rhythm = 'art/wand-management-v01/assets/WM-04-rhythm-staff.blend'
    ember = 'art/wand-management-v01/assets/WM-05-ember-staff.blend'
    parchment = 'art/wand-management-v01/assets/WM-06-configuration-parchment.blend'
    controls = 'art/wand-management-v01/assets/WM-07-tags-and-controls.blend'
}
$assetPath = Join-Path $PSScriptRoot $files[$Asset]
if (-not (Test-Path -LiteralPath $assetPath)) { throw "Missing native asset: $assetPath" }
# This entry point explicitly opens the interactive Blender review window.
Start-Process -FilePath $BlenderExe -ArgumentList @('"' + $assetPath + '"') -WorkingDirectory $PSScriptRoot
