#!/bin/bash
# GitHub一键部署脚本

echo "=========================================="
echo "  📦 股票分析系统 - GitHub部署助手"
echo "=========================================="
echo ""

# 检查是否已经初始化Git
if [ ! -d ".git" ]; then
    echo "📝 初始化Git仓库..."
    git init
    echo "✓ Git仓库初始化完成"
else
    echo "✓ Git仓库已存在"
fi

echo ""
echo "请输入你的GitHub仓库信息："
echo ""

# 获取用户输入
read -p "GitHub用户名: " github_username
read -p "仓库名称 (如 stock-analysis-system): " repo_name

echo ""
echo "=========================================="
echo "  准备上传代码..."
echo "=========================================="
echo ""

# 创建.gitignore
echo "📝 创建.gitignore文件..."
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# 敏感配置（不上传真实配置）
config.py

# 数据文件
*.csv
*.txt
*.md
!README.md
!*_GUIDE.md
!*_README.md
!GITHUB_DEPLOYMENT_GUIDE.md

# 日志
logs/
*.log

# 临时文件
.DS_Store
.vscode/
.idea/

# 历史数据
discovery_history/
EOF

echo "✓ .gitignore创建完成"
echo ""

# 创建示例配置文件
echo "📝 创建config.example.py..."
cat > config.example.py << 'EOF'
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件示例
请复制此文件为config.py并填入真实配置
"""

# DeepSeek API 配置
DEEPSEEK_CONFIG = {
    'api_key': 'your_deepseek_api_key_here',
    'api_base': 'https://api.deepseek.com/v1',
    'model': 'deepseek-chat',
    'temperature': 0.3,
    'max_tokens': 500,
    'timeout': 30
}

# 邮件配置
EMAIL_CONFIG = {
    'smtp_server': 'smtp.qq.com',
    'smtp_port': 465,
    'sender_email': 'your_email@qq.com',
    'sender_password': 'your_qq_auth_code',
    'receiver_emails': ['receiver@example.com'],
    'subject_prefix': '📊 每日投资简报',
    'attach_files': True,
    'max_attachment_size': 25
}

# 分析参数配置
ANALYSIS_CONFIG = {
    'batch_size': 10,
    'request_delay': 1,
    'max_posts': 100,
    'enable_ai_analysis': True,
    'enable_traditional_analysis': True
}

# 输出配置
OUTPUT_CONFIG = {
    'output_dir': 'reports',
    'save_detailed_log': True,
    'generate_html_report': True
}

# 定时任务配置
SCHEDULE_CONFIG = {
    'daily_run_time': '08:00',
    'timezone': 'Asia/Shanghai',
    'enable_schedule': True,
    'retry_times': 3,
    'retry_interval': 10
}
EOF

echo "✓ config.example.py创建完成"
echo ""

# 添加文件
echo "📦 添加文件到Git..."
git add .

# 提交
echo "💾 提交代码..."
git commit -m "Initial commit: 股票分析自动化系统"

# 设置远程仓库
echo "🔗 关联GitHub仓库..."
git remote remove origin 2>/dev/null
git remote add origin "https://github.com/${github_username}/${repo_name}.git"

# 推送
echo "🚀 推送到GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "=========================================="
echo "  ✅ 代码上传完成！"
echo "=========================================="
echo ""
echo "下一步："
echo "1. 访问 https://github.com/${github_username}/${repo_name}"
echo "2. 进入 Settings → Secrets and variables → Actions"
echo "3. 添加以下6个Secrets："
echo "   - DEEPSEEK_API_KEY"
echo "   - SMTP_SERVER"
echo "   - SMTP_PORT"
echo "   - SENDER_EMAIL"
echo "   - SENDER_PASSWORD"
echo "   - RECEIVER_EMAIL"
echo ""
echo "详细步骤请查看: GITHUB_DEPLOYMENT_GUIDE.md"
echo ""
