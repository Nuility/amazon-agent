@echo off
chcp 65001 >nul
echo ========================================
echo    用户管理智能体 - Agent UI 启动器
echo ========================================
echo.

set PYTHON_PATH=%LOCALAPPDATA%\Programs\Python\Python314\python.exe

if not exist "%PYTHON_PATH%" (
    echo [错误] 未找到Python，请先安装Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/3] 检查依赖...
cd /d "%~dp0"
"%PYTHON_PATH%" -m pip install -r ..\requirements.txt -q

echo [2/3] 启动服务...
echo.
echo 服务地址: http://localhost:8001
echo 按 Ctrl+C 停止服务
echo.

cd /d "%~dp0"
"%PYTHON_PATH%" run_server.py

pause
