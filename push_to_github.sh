#!/bin/bash

# 📦 自动推送到GitHub脚本
# 使用前请确保已安装Xcode命令行工具: xcode-select --install

set -e  # 遇到错误立即退出

echo "=========================================="
echo "📦 开始推送代码到GitHub"
echo "=========================================="
echo ""

# 检查是否安装了Xcode命令行工具
echo "🔍 检查Xcode命令行工具..."
if ! xcode-select -p &> /dev/null; then
    echo "❌ 错误: 未安装Xcode命令行工具"
    echo ""
    echo "请先运行以下命令安装:"
    echo "  xcode-select --install"
    echo ""
    echo "安装完成后再次运行此脚本。"
    exit 1
fi
echo "✅ Xcode命令行工具已安装"
echo ""

# 检查是否已经是Git仓库
if [ -d ".git" ]; then
    echo "⚠️  检测到已存在的Git仓库"
    read -p "是否要重新初始化？这将删除现有的Git历史 (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  删除现有Git仓库..."
        rm -rf .git
    else
        echo "❌ 取消操作"
        exit 1
    fi
fi

# 初始化Git仓库
echo "🔧 初始化Git仓库..."
git init
echo "✅ Git仓库初始化完成"
echo ""

# 添加所有文件
echo "📁 添加文件到Git..."
git add .
echo "✅ 文件添加完成"
echo ""

# 显示将要提交的文件
echo "📋 将要提交的文件:"
git status --short | head -20
echo ""
file_count=$(git status --short | wc -l)
echo "总计: $file_count 个文件"
echo ""

# 确认是否继续
read -p "是否继续提交？(Y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Nn]$ ]]; then
    echo "❌ 取消操作"
    exit 1
fi

# 提交
echo "💾 提交到本地仓库..."
git commit -m "Initial commit: A股投资分析自动化系统

包含功能:
- 黄金股票筛选器
- AI量化选股器  
- 微博情绪分析（加权版）
- 全网热点发现引擎
- 政客交易追踪
- 每日自动推送系统
- 防幻觉机制
- 完整文档系统（27个文档）"
echo "✅ 提交完成"
echo ""

# 关联远程仓库
echo "🔗 关联GitHub远程仓库..."
REPO_URL="https://github.com/billyxu921/股票助手.git"

# 检查是否已有remote
if git remote | grep -q "origin"; then
    echo "⚠️  已存在origin远程仓库，删除旧的..."
    git remote remove origin
fi

git remote add origin "$REPO_URL"
echo "✅ 远程仓库关联完成"
echo ""

# 切换到main分支
echo "🌿 切换到main分支..."
git branch -M main
echo "✅ 分支切换完成"
echo ""

# 推送到GitHub
echo "🚀 推送到GitHub..."
echo ""
echo "⚠️  注意: 如果提示输入密码，请使用Personal Access Token，不是GitHub密码！"
echo ""
echo "如何获取Token:"
echo "1. 访问 https://github.com/settings/tokens"
echo "2. 点击 'Generate new token (classic)'"
echo "3. 勾选 'repo' 权限"
echo "4. 生成并复制token"
echo ""
read -p "按Enter键继续推送..." 

if git push -u origin main; then
    echo ""
    echo "=========================================="
    echo "🎉 成功推送到GitHub！"
    echo "=========================================="
    echo ""
    echo "📍 仓库地址: $REPO_URL"
    echo ""
    echo "🔍 验证: 访问上面的地址查看你的代码"
    echo ""
    echo "📋 下一步:"
    echo "1. 设置仓库为Private（推荐）"
    echo "2. 配置GitHub Secrets（如果要使用GitHub Actions）"
    echo "3. 测试GitHub Actions工作流"
    echo ""
    echo "详细说明请查看: GITHUB_DEPLOYMENT_GUIDE.md"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "❌ 推送失败"
    echo "=========================================="
    echo ""
    echo "可能的原因:"
    echo "1. 认证失败 - 确保使用Personal Access Token"
    echo "2. 网络问题 - 检查网络连接"
    echo "3. 仓库已有内容 - 需要先拉取"
    echo ""
    echo "如果仓库已有内容，运行:"
    echo "  git pull origin main --allow-unrelated-histories"
    echo "  git push -u origin main"
    echo ""
    echo "详细说明请查看: GIT_PUSH_GUIDE.md"
    echo ""
    exit 1
fi
