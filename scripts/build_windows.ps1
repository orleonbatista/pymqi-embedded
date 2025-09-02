$ErrorActionPreference = 'Stop'
param(
    [string]$MqClientZipUrl,
    [string]$MqClientZipPath
)

$root = Resolve-Path -Path (Join-Path $PSScriptRoot '..')
$vendor = Join-Path $root 'vendor/mq'
Remove-Item -Recurse -Force $vendor -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Path $vendor | Out-Null

if ($MqClientZipPath) {
    Expand-Archive -Path $MqClientZipPath -DestinationPath $vendor
} elseif ($MqClientZipUrl) {
    Invoke-WebRequest -Uri $MqClientZipUrl -OutFile "$env:TEMP/mqclient.zip"
    Expand-Archive -Path "$env:TEMP/mqclient.zip" -DestinationPath $vendor
} else {
    throw 'Provide -MqClientZipUrl or -MqClientZipPath'
}

& py -3 (Join-Path $root 'scripts/sync_upstream.py')
py -3 -m compileall src tests

$pythons = @('38','39','310','311','312')
foreach ($ver in $pythons) {
    $py = "C:/Python$ver/python.exe"
    $env:MQ_INSTALLATION_PATH = $vendor
    & $py -m build --wheel
    Get-ChildItem dist/pymqi_embedded-*.whl | ForEach-Object {
        delvewheel repair $_.FullName -w dist
        Remove-Item $_.FullName
    }
    Remove-Item -Recurse -Force build,pymqi_embedded.egg-info
    git checkout -- src/pymqi
    & py -3 (Join-Path $root 'scripts/sync_upstream.py')
    py -3 -m compileall src tests
}
