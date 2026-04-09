#!/bin/bash
# Anthropic Computer Use Demo 启动脚本
# 使用前请确保：
#   1. 已安装 Docker (https://www.docker.com/products/docker-desktop/)
#   2. 已获取 Anthropic API Key (https://console.anthropic.com)

# ========== 在这里填入你的 API Key ==========
ANTHROPIC_API_KEY="在此粘贴你的API密钥"
# =============================================

if [ "$ANTHROPIC_API_KEY" = "在此粘贴你的API密钥" ]; then
    echo "请先编辑此脚本，填入你的 Anthropic API Key"
    exit 1
fi

echo "正在拉取 Computer Use Demo 镜像..."
docker pull ghcr.io/anthropics/anthropic-quickstarts:computer-use-demo-latest

echo ""
echo "正在启动 Computer Use Demo..."
docker run \
    -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
    -v $HOME/.anthropic:/home/computeruse/.anthropic \
    -p 5900:5900 \
    -p 8501:8501 \
    -p 6080:6080 \
    -p 8080:8080 \
    -it ghcr.io/anthropics/anthropic-quickstarts:computer-use-demo-latest

# 启动后访问：
#   综合界面:  http://localhost:8080
#   聊天界面:  http://localhost:8501
#   桌面视图:  http://localhost:6080/vnc.html
