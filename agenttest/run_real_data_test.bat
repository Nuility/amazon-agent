@echo off
chcp 65001 > nul
echo ============================================================
echo Amazon Ads Agent 智能体功能测试（使用真实数据）
echo ============================================================
echo 测试数据: C:\1\挑战杯\测试数据
echo.

REM 查找Python
set PYTHON_EXE=

if exist "%LOCALAPPDATA%\Programs\Python\Python314\python.exe" (
    set PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python314\python.exe
    goto :found
)

if exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" (
    set PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python313\python.exe
    goto :found
)

if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python312\python.exe
    goto :found
)

where python >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_EXE=python
    goto :found
)

echo 错误: 未找到Python
pause
exit /b 1

:found
echo 使用Python: %PYTHON_EXE%
"%PYTHON_EXE%" --version
echo.

cd /d "%~dp0"

echo ============================================================
echo 开始测试...
echo ============================================================
echo.

"%PYTHON_EXE%" tests\test_with_real_data.py

echo.
echo ============================================================
echo 测试完成！
echo ============================================================
pause
