@echo off
chcp 65001 >nul
echo ========================================
echo   用户管理智能体系统
echo ========================================
echo.

cd /d D:\云码道\amazon-agent-feature-ui-enhancement\agenttest\src\api
set PYTHONPATH=D:\云码道\amazon-agent-feature-ui-enhancement\agenttest\src

echo [启动信息]
echo   Web界面: http://127.0.0.1:8001
echo   API文档: http://127.0.0.1:8001/docs
echo   健康检查: http://127.0.0.1:8001/api/health
echo.
echo 按 Ctrl+C 停止服务
echo.

python -m uvicorn server:app --host 127.0.0.1 --port 8001 --log-level info

pause
