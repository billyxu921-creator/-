# 📦 Git推送到GitHub指南

## 🔧 前置准备

### 1. 安装Xcode命令行工具 ⚠️ 必须先完成！

你的系统需要先安装Xcode命令行工具才能使用Git。

**✅ 推荐方法: 通过命令行安装**

打开终端（Terminal），执行：
```bash
xcode-select --install
```

执行后会弹出安装对话框：
1. 点击"安装"按钮
2. 同意许可协议
3. 等待下载和安装完成（约5-10分钟，取决于网速）
4. 安装完成后关闭对话框

**验证是否安装成功**:
```bash
xcode-select -p
```

如果显示路径（如 `/Library/Developer/CommandLineTools`），说明已安装成功。

**如果安装失败**:
- 检查网络连接
- 确保有足够的磁盘空间（至少5GB）
- 尝试重启Mac后再次安装

---

## 🚀 推送步骤

### 步骤1: 初始化Git仓库

```bash
cd ~/Desktop/股票助手
git init
```

### 步骤2: 创建.gitignore文件

```bash
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

# 数据文件（不上传生成的报告）
*.csv
*.txt
!requirements.txt
!requirements_weibo.txt
微博*.md
权力资金动态*.md
AI潜力股推荐*.md
全网雷达*.md
每日投资简报*.md
gold_stocks_analysis_*.csv
quant_picker_candidates_*.csv
deepseek_analysis_mock_*.csv
dark_horse_report_*.txt
intelligence_report_*.csv
guba_posts_*.csv
stock_results_*.csv
weibo_clean_test_*.csv
weibo_raw_test_*.csv

# 日志
logs/
*.log

# 临时文件
.DS_Store
.vscode/
.idea/

# 历史数据
discovery_history/

# macOS
.DS_Store
.AppleDouble
.LSOverride
EOF
```

### 步骤3: 添加所有文件

```bash
git add .
```

### 步骤4: 提交

```bash
git commit -m "Initial commit: A股投资分析自动化系统

- 黄金股票筛选器
- AI量化选股器
- 微博情绪分析（加权版）
- 全网热点发现引擎
- 政客交易追踪
- 每日自动推送系统
- 防幻觉机制
- 完整文档系统（27个文档）"
```

### 步骤5: 关联远程仓库

```bash
git remote add origin https://github.com/billyxu921/股票助手.git
```

### 步骤6: 推送到GitHub

```bash
git branch -M main
git push -u origin main
```

---

## ⚠️ 可能遇到的问题

### 问题1: 需要GitHub认证

**解决方法**: 使用Personal Access Token

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 勾选 `repo` 权限
4. 生成并复制token
5. 推送时使用token作为密码

### 问题2: 仓库已存在内容

如果GitHub仓库已有README等文件，需要先拉取：

```bash
git pull origin main --allow-unrelated-histories
```

然后再推送：

```bash
git push -u origin main
```

### 问题3: 文件太大

如果有文件超过100MB，GitHub会拒绝推送。

**解决方法**: 将大文件添加到.gitignore

```bash
echo "大文件名" >> .gitignore
git rm --cached 大文件名
git commit -m "Remove large file"
git push
```

---

## 📋 完整命令清单

```bash
# 1. 安装Xcode命令行工具（如果需要）
xcode-select --install

# 2. 进入项目目录
cd ~/Desktop/股票助手

# 3. 初始化Git
git init

# 4. 创建.gitignore（见上面的内容）
# 手动创建或使用cat命令

# 5. 添加所有文件
git add .

# 6. 查看将要提交的文件
git status

# 7. 提交
git commit -m "Initial commit: A股投资分析自动化系统"

# 8. 关联远程仓库
git remote add origin https://github.com/billyxu921/股票助手.git

# 9. 推送到main分支
git branch -M main
git push -u origin main
```

---

## ✅ 验证推送成功

推送成功后，访问你的GitHub仓库：
https://github.com/billyxu921/股票助手

你应该能看到所有文件已经上传。

---

## 🔄 后续更新

以后修改代码后，使用以下命令推送更新：

```bash
# 1. 查看修改的文件
git status

# 2. 添加修改的文件
git add .

# 3. 提交
git commit -m "更新说明"

# 4. 推送
git push
```

---

## 📝 建议的.gitignore内容

为了保护敏感信息和避免上传临时文件，建议使用以下.gitignore：

```
# Python
__pycache__/
*.py[cod]
*.so
venv/
ENV/

# 敏感配置
config.py

# 生成的报告文件
*.csv
微博*.md
权力资金动态*.md
AI潜力股推荐*.md
全网雷达*.md
每日投资简报*.md

# 但保留requirements文件
!requirements.txt
!requirements_weibo.txt

# 日志和临时文件
logs/
*.log
.DS_Store
discovery_history/
```

---

## 🎯 推送后的下一步

推送成功后，建议：

1. **设置GitHub Secrets**（如果要使用GitHub Actions）
   - 进入仓库 Settings → Secrets and variables → Actions
   - 添加必要的Secrets（见GITHUB_DEPLOYMENT_GUIDE.md）

2. **更新README**
   - 添加仓库链接
   - 添加使用说明

3. **设置仓库为Private**（推荐）
   - Settings → Danger Zone → Change visibility
   - 保护你的配置和数据

---

**祝推送顺利！** 🎉

如果遇到问题，请查看GitHub的帮助文档：
https://docs.github.com/cn/get-started/importing-your-projects-to-github/importing-source-code-to-github/adding-locally-hosted-code-to-github

---

**最后更新**: 2026年1月15日
