#!/bin/bash
# 全网热点发现引擎 - 快速启动脚本

echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║          全网热点发现引擎 - Discovery Engine             ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3"
    echo "请先安装Python3: https://www.python.org/downloads/"
    exit 1
fi

echo "✓ Python3已安装"

# 检查依赖
echo ""
echo "检查依赖..."

if ! python3 -c "import playwright" 2>/dev/null; then
    echo "⚠️  未安装Playwright"
    echo "正在安装依赖..."
    pip3 install playwright pandas requests
    playwright install chromium
else
    echo "✓ 依赖已安装"
fi

# 检查配置
echo ""
echo "检查配置..."

if [ ! -f "config.py" ]; then
    echo "❌ 错误: 未找到config.py"
    echo "请先配置DeepSeek API Key"
    exit 1
fi

echo "✓ 配置文件存在"

# 运行程序
echo ""
echo "启动全网热点发现引擎..."
echo ""

python3 Discovery_Engine.py

echo ""
echo "✅ 程序执行完成"
echo ""
echo "生成的文件:"
echo "  - discovery_raw_*.csv (原始数据)"
echo "  - 全网雷达报告_*.md (分析简报)"
echo ""
