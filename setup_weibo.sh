#!/bin/bash
# 微博黄金情绪分析系统 - 安装脚本

echo "================================"
echo "微博黄金情绪分析系统 - 安装向导"
echo "================================"
echo ""

# 检查Python版本
echo "检查Python版本..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ 错误: 未找到Python3"
    echo "请先安装Python 3.8或更高版本"
    exit 1
fi

echo "✓ Python已安装"
echo ""

# 安装Python依赖
echo "步骤1: 安装Python依赖包..."
pip3 install -r requirements_weibo.txt

if [ $? -ne 0 ]; then
    echo "❌ 依赖包安装失败"
    exit 1
fi

echo "✓ Python依赖包安装完成"
echo ""

# 安装Playwright浏览器
echo "步骤2: 安装Playwright浏览器..."
playwright install chromium

if [ $? -ne 0 ]; then
    echo "❌ Playwright浏览器安装失败"
    exit 1
fi

echo "✓ Playwright浏览器安装完成"
echo ""

# 检查配置文件
echo "步骤3: 检查配置文件..."
if [ -f "config.py" ]; then
    echo "✓ 配置文件已存在"
else
    echo "⚠️  警告: 未找到config.py"
    echo "请确保已配置DeepSeek API Key"
fi

echo ""
echo "================================"
echo "✅ 安装完成！"
echo "================================"
echo ""
echo "运行分析:"
echo "  python3 weibo_gold_sentiment.py"
echo ""
echo "查看文档:"
echo "  cat WEIBO_SENTIMENT_GUIDE.md"
echo ""