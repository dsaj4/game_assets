. (Join-Path $PSScriptRoot 'env.ps1')
$out = Join-Path $LabRoot 'artifacts/ui-experiment/E1'
[System.IO.Directory]::CreateDirectory($out) | Out-Null
foreach ($size in @('1920x1080','1280x720')) {
    foreach ($variant in @('Base','Ink')) {
        $stem = "godot-$($variant.ToLower())-$size"
        $stdout = Join-Path $out "$stem.log"
        $stderr = Join-Path $out "$stem-error.log"
        $image = Join-Path $out "$stem-final.png"
        $proc = Start-Process -FilePath $GodotExe -ArgumentList @(
            '--path',('"'+(Join-Path $LabRoot 'game')+'"'),
            "res://scenes/E1$variant.tscn",'--resolution',$size,
            '--','--capture',('"'+$image+'"')
        ) -WindowStyle Hidden -RedirectStandardOutput $stdout -RedirectStandardError $stderr -PassThru
        if (-not $proc.WaitForExit(45000)) { $proc.Kill(); throw "E1 capture timed out: $stem" }
        if ($proc.ExitCode -ne 0) { throw "E1 capture failed: $stem" }
        if (-not (Test-Path -LiteralPath $image)) { throw "Capture missing: $image" }
        $log = Get-Content -LiteralPath $stdout -Raw -Encoding UTF8
        if ($log -notmatch 'E1_TEXT_BOUNDS=PASS' -or $log -notmatch 'NVIDIA' -or $log -notmatch "E1_CAPTURE_SAVED=$size") { throw "E1 capture validation missing: $stem" }
        if ((Get-Item -LiteralPath $stderr).Length -gt 0) { throw "Inspect runtime diagnostics: $stderr" }
        Write-Output "E1_CAPTURE_PASS $stem"
    }
}
