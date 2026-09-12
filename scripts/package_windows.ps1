param(
    [string]$Python = "python",
    [string]$OutputDirectory = (Join-Path $PSScriptRoot "../dist"),
    [string]$Version = "1.0.0"
)
$ErrorActionPreference = "Stop"
$projectRoot = Split-Path $PSScriptRoot -Parent
$buildPath = Join-Path $projectRoot "build/package"
New-Item -ItemType Directory -Force -Path $buildPath, $OutputDirectory | Out-Null
& $Python -m PyInstaller --noconfirm --clean --windowed --copy-metadata pywebview --copy-metadata pythonnet --copy-metadata clr-loader --copy-metadata bottle --copy-metadata cffi --copy-metadata pycparser --copy-metadata proxy-tools --name "CozyTank" --distpath $OutputDirectory --workpath $buildPath --specpath $buildPath --add-data "$projectRoot/frontend;frontend" "$projectRoot/tank_game.py"
if ($LASTEXITCODE -ne 0) { throw "PyInstaller failed" }
Copy-Item -LiteralPath (Join-Path $PSScriptRoot "WINDOWS_PACKAGE_README.txt") -Destination (Join-Path $OutputDirectory "CozyTank/使用说明.txt")
$basePython = & $Python -c "import sys; print(sys.base_prefix)"
Copy-Item -LiteralPath (Join-Path $basePython "LICENSE.txt") -Destination (Join-Path $OutputDirectory "CozyTank/LICENSE-Python.txt")
$zipPath = Join-Path $OutputDirectory "CozyTank-v$Version-Windows-x64.zip"
if (Test-Path -LiteralPath $zipPath) { throw "输出包已存在，请使用新的版本号或目录：$zipPath" }
Compress-Archive -LiteralPath (Join-Path $OutputDirectory "CozyTank") -DestinationPath $zipPath
Write-Output $zipPath
