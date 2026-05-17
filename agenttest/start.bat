@echo off
chcp 65001 >nul
cd /d D:\云码道\amazon-agent-feature-ui-enhancement\agenttest\src\api
set PYTHONPATH=D:\云码道\amazon-agent-feature-ui-enhancement\agenttest\src
python -m uvicorn server:app --host 127.0.0.1 --port 8001
pause
