#!/bin/bash
# ============================================
# XActions 安装脚本 (macOS)
# 用途：自动评论指定推文
# ============================================

echo "========== XActions 安装 =========="

# 1. 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "未检测到 Node.js，正在安装..."
    brew install node
fi
echo "Node.js 版本: $(node --version)"

# 2. 创建项目目录
mkdir -p ~/xactions-project && cd ~/xactions-project

# 3. 初始化并安装 xactions
npm init -y
npm install xactions

echo ""
echo "========== 安装完成 =========="
echo ""
echo "接下来你需要登录 X 账号："
echo "  npx xactions login"
echo ""
echo "获取 auth_token 的方法："
echo "  1. 在 Chrome 中打开 x.com 并登录"
echo "  2. 按 F12 打开开发者工具"
echo "  3. 切换到 Application 标签"
echo "  4. 左侧找到 Cookies -> https://x.com"
echo "  5. 找到 auth_token，复制它的值"
echo "  6. 粘贴到终端提示中"
echo ""
echo "登录成功后，运行评论脚本："
echo "  node reply.js <推文链接> <评论内容>"
