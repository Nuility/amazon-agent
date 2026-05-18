@echo off
chcp 65001 > nul
echo ============================================================
echo Amazon Ads Agent 综合测试
echo ============================================================
echo.

REM 查找Python
set PYTHON_EXE=

REM 尝试常见Python路径
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

if exist "C:\Python314\python.exe" (
    set PYTHON_EXE=C:\Python314\python.exe
    goto :found
)

if exist "C:\Python313\python.exe" (
    set PYTHON_EXE=C:\Python313\python.exe
    goto :found
)

if exist "C:\Python312\python.exe" (
    set PYTHON_EXE=C:\Python312\python.exe
    goto :found
)

REM 尝试使用python命令
where python >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_EXE=python
    goto :found
)

echo 错误: 未找到Python，请先安装Python 3.8+
echo.
pause
exit /b 1

:found
echo 使用Python: %PYTHON_EXE%
echo.

REM 切换到项目目录
cd /d "%~dp0"

REM 运行测试
echo 运行综合测试...
echo ============================================================
echo.

"%PYTHON_EXE%" tests\comprehensive_test.py

echo.
echo ============================================================
echo 测试完成
echo ============================================================
pause
