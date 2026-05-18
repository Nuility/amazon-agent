@echo off
chcp 65001 > nul
echo ============================================================
echo Amazon Ads Agent 项目验证
echo ============================================================
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
echo 请先安装Python 3.8+
echo.
pause
exit /b 1

:found
echo 使用Python: %PYTHON_EXE%
"%PYTHON_EXE%" --version
echo.

cd /d "%~dp0"

echo ============================================================
echo 验证项目结构
echo ============================================================
"%PYTHON_EXE%" tests\validate_structure.py
