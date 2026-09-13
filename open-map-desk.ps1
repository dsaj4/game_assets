param([ValidateSet('master','desk','map','route','mage','campfire','orb','building','chest','books')][string]$Asset='master')
. (Join-Path $PSScriptRoot 'tools/env.ps1')
$MapAssetFiles = @{
    master='map-desk-master.blend'; desk='assets/MD-01-desk.blend'; map='assets/MD-02-environment-map.blend'
    route='assets/MD-03-red-route.blend'; mage='assets/MD-04-mage.blend'; campfire='assets/MD-05-campfire.blend'
    orb='assets/MD-06-crystal-ball.blend'; building='assets/MD-07-building.blend'; chest='assets/MD-08-chest.blend'
    books='assets/MD-10-books.blend'
}
$MapAssetPath = Join-Path $PSScriptRoot ('art/map-desk-v01/' + $MapAssetFiles[$Asset])
if (-not (Test-Path -LiteralPath $MapAssetPath -PathType Leaf)) { throw "Asset does not exist: $MapAssetPath" }
# This explicitly opens the interactive Blender editor for reviewing an asset.
Start-Process -FilePath $BlenderExe -ArgumentList @('"' + $MapAssetPath + '"')
