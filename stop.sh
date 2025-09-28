#!/bin/bash

echo "Stopping Resume Doctor services..."

# 停止 Flask 后端服务
echo "1. Stopping Flask backend..."
FLASK_PID=$(ps aux | grep '[p]ython3 app.py' | awk '{print $2}')
if [ -n "$FLASK_PID" ]; then
  kill "$FLASK_PID"
  echo "Flask backend (PID: $FLASK_PID) stopped."
else
  echo "Flask backend is not running."
fi

# 停止 Vite 前端 preview 服务（监听端口 5173）
echo "2. Stopping Vite frontend preview (port 5173)..."
VITE_PID=$(lsof -t -i:5173)
if [ -n "$VITE_PID" ]; then
  kill "$VITE_PID"
  echo "Vite frontend (PID: $VITE_PID) stopped."
else
  echo "Vite frontend preview is not running."
fi

echo "All services stopped."

