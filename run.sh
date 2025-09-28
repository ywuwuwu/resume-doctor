#!/bin/bash

echo "1. 启动 Flask 后端..."
cd ~/resume-doctor/backend
nohup python3 app.py > backend.log 2>&1 &
echo "Flask 启动完成，日志见 backend.log"

echo "2. 安装并构建前端..."
cd ~/resume-doctor/frontend
npm install
npm run build

echo "3. 前端构建完成，静态资源已生成在 dist/ 目录"
echo "使用 Nginx 代理 dist/，访问地址：http://demo02.2brain.ai"
echo "All services are up!"

