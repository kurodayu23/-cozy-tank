@echo off
chcp 65001 >nul
title Cozy Tank - 启动中...
cd /d "%~dp0"

echo.
echo   ╔══════════════════════════════════╗
echo   ║   🎮 Cozy Tank - 坦克大战       ║
echo   ╚══════════════════════════════════╝
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Check and install dependencies
echo [1/2] 检查依赖...
python -m pip show pywebview >nul 2>&1
if errorlevel 1 (
    echo [1/2] 正在安装 pywebview...
    python -m pip install -r "%~dp0requirements.txt"
    if errorlevel 1 (
        echo [错误] 安装 pywebview 失败，请手动运行: python -m pip install -r requirements.txt
        pause
        exit /b 1
    )
)
echo [1/2] 依赖就绪 ✓

:: Launch game
echo [2/2] 启动游戏...
echo.
python "%~dp0tank_game.py"

if errorlevel 1 (
    echo.
    echo [错误] 游戏异常退出
    pause
)
