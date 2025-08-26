$ErrorActionPreference = 'Stop'

$pythons = @('38','39','310','311','312')
foreach ($ver in $pythons) {
    $py = "C:/Python$ver/python.exe"
    & $py -m pip install --upgrade pip setuptools wheel
    & $py -m pip wheel . -w dist
}

Get-ChildItem dist/*.whl | ForEach-Object {
    delvewheel repair $_.FullName -w dist
}
