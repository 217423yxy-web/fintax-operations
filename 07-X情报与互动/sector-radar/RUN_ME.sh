#!/bin/bash
# =======================================
# Sector Radar 一键启动脚本
# =======================================

cd "$(dirname "$0")"

echo "安装依赖..."
pip install requests openpyxl -q

echo ""
echo "可用赛道:"
python run.py --list-sectors

echo ""
echo "开始运行全赛道发现 Pipeline..."
export TWITTER_API_KEY="new1_ad975caf0bde4ecb860267533dcfb662"
python run.py --all --target 100 -v

echo ""
echo "完成！结果在 ./output/ 目录下"
ls -la ./output/
