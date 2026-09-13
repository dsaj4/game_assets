param([ValidateSet('master','previous','wand-roll','desk','map','route','mage','campfire','orb','building','chest','books')][string]$Asset='master')
. (Join-Path $PSScriptRoot 'tools/env.ps1')
$MapAssetFiles = @{
    previous='map-desk-master.blend'; desk='assets/MD-01-desk.blend'; map='assets/MD-02-environment-map.blend'
    route='assets/MD-03-red-route.blend'; mage='assets/MD-04-mage.blend'; campfire='assets/MD-05-campfire.blend'
    orb='assets/MD-06-crystal-ball.blend'; building='assets/MD-07-building.blend'; chest='assets/MD-08-chest.blend'
    books='assets/MD-10-books.blend'
}
$MapAssetRelative = switch ($Asset) {
    'master' { 'art/map-desk-v02/map-desk-master.blend' }
    'wand-roll' { 'art/md-11-v01/MD-11-wand-roll.blend' }
    default { 'art/map-desk-v01/' + $MapAssetFiles[$Asset] }
}
$MapAssetPath = Join-Path $PSScriptRoot $MapAssetRelative
if (-not (Test-Path -LiteralPath $MapAssetPath -PathType Leaf)) { throw "Asset does not exist: $MapAssetPath" }
# This explicitly opens the interactive Blender editor for reviewing an asset.
Start-Process -FilePath $BlenderExe -ArgumentList @('"' + $MapAssetPath + '"')
