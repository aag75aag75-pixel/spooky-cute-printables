$edge = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
$htmlDir = 'C:\Users\aag75\AppData\Local\Temp\opencode\pins\html'
$outDir  = 'D:\проэкт\pins\covers'
$files = Get-ChildItem $htmlDir -Filter 'pin-*.html' | Sort-Object Name
foreach ($f in $files) {
  $png = Join-Path $outDir ($f.BaseName + '.png')
  & $edge --headless --disable-gpu --no-sandbox --hide-scrollbars `
    --window-size=1080,1350 --default-background-color=00000000 `
    --screenshot="$png" ("file:///" + $f.FullName.Replace('\','/')) *>$null
  if (Test-Path $png) { "$($f.BaseName) OK $((Get-Item $png).Length) bytes" } else { "$($f.BaseName) FAIL" }
}
