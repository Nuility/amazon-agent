@echo off
chcp 65001 >nul
title 用户管理智能体系统
color 0A

echo ============================================================
echo 用户管理智能体系统 - 服务启动器
echo ============================================================
echo.

cd /d D:\云码道\amazon-agent-feature-ui-enhancement\agenttest\src\api
set PYTHONPATH=D:\云码道\amazon-agent-feature-ui-enhancement\agenttest\src

echo [配置信息]
echo   监听地址: 0.0.0.0:8001
echo   访问地址: http://localhost:8001
echo   API文档: http://localhost:8001/docs
echo   健康检查: http://localhost:8001/api/health
echo.
echo [启动服务]
echo 按 Ctrl+C 停止服务
echo ============================================================
echo.

python -m uvicorn server:app --host 0.0.0.0 --port 8001 --log-level info

if errorlevel 1 (
    echo.
    echo [错误] 服务启动失败！
    echo 请检查错误信息
    pause
    exit /b 1
)

pause
