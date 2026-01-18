# 🚀 下一步操作指南

你的代码已经准备好推送到GitHub了！但首先需要安装Xcode命令行工具。

---

## ⚠️ 第一步：安装Xcode命令行工具（必须！）

打开终端，执行：

```bash
xcode-select --install
```

会弹出安装对话框：
1. 点击"安装"
2. 同意许可协议  
3. 等待5-10分钟完成安装
4. 关闭对话框

**验证安装成功**：
```bash
xcode-select -p
```

应该显示：`/Library/Developer/CommandLineTools`

---

## 🎯 第二步：推送到GitHub

安装完Xcode工具后，有两种方式推送代码：

### 方式A：使用自动化脚本（推荐）

```bash
./push_to_github.sh
```

这个脚本会自动完成：
- ✅ 初始化Git仓库
- ✅ 添加所有文件
- ✅ 提交到本地
- ✅ 关联GitHub远程仓库
- ✅ 推送到GitHub

**注意**：推送时需要输入GitHub认证信息：
- 用户名：`billyxu921`
- 密码：使用**Personal Access Token**（不是GitHub密码！）

### 方式B：手动执行命令

如果你想手动控制每一步，按照以下顺序执行：

```bash
# 1. 初始化Git仓库
git init

# 2. 添加所有文件
git add .

# 3. 查看将要提交的文件
git status

# 4. 提交到本地仓库
git commit -m "Initial commit: A股投资分析自动化系统"

# 5. 关联GitHub远程仓库
git remote add origin https://github.com/billyxu921/股票助手.git

# 6. 切换到main分支
git branch -M main

# 7. 推送到GitHub
git push -u origin main
```

---

## 🔑 如何获取Personal Access Token

推送时需要使用Token而不是密码：

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 勾选 `repo` 权限
4. 点击 "Generate token"
5. **立即复制token**（只显示一次！）
6. 推送时使用这个token作为密码

---

## ✅ 验证推送成功

推送完成后，访问你的GitHub仓库：

https://github.com/billyxu921/股票助手

你应该能看到所有文件已经上传。

---

## 📋 推送后的下一步

### 1. 设置仓库为Private（推荐）

保护你的配置和数据：
- Settings → Danger Zone → Change visibility → Private

### 2. 配置GitHub Secrets（如果要使用GitHub Actions）

进入 Settings → Secrets and variables → Actions，添加：

| Secret名称 | 说明 |
|-----------|------|
| DEEPSEEK_API_KEY | DeepSeek API密钥 |
| SMTP_SERVER | smtp.qq.com |
| SMTP_PORT | 587 |
| SENDER_EMAIL | 你的QQ邮箱 |
| SENDER_PASSWORD | QQ邮箱授权码 |
| RECEIVER_EMAIL | 接收简报的邮箱 |

### 3. 测试GitHub Actions

- 进入 Actions 标签
- 选择 "Daily Stock Analysis Report"
- 点击 "Run workflow"
- 等待10-15分钟
- 检查邮箱是否收到简报

---

## 📚 详细文档

- [PUSH_TO_GITHUB_CHECKLIST.md](PUSH_TO_GITHUB_CHECKLIST.md) - 详细检查清单
- [GIT_PUSH_GUIDE.md](GIT_PUSH_GUIDE.md) - 完整推送指南
- [GITHUB_DEPLOYMENT_GUIDE.md](GITHUB_DEPLOYMENT_GUIDE.md) - GitHub部署指南

---

## ⚠️ 常见问题

### Q: 推送时提示"认证失败"
A: 确保使用Personal Access Token，不是GitHub密码

### Q: 推送时提示"仓库已有内容"
A: 先拉取：`git pull origin main --allow-unrelated-histories`，再推送

### Q: 推送时提示"文件太大"
A: 某些文件超过100MB，需要添加到.gitignore

---

## 🎉 总结

**现在就开始吧！**

1. ⏳ 安装Xcode工具：`xcode-select --install`
2. 🚀 运行推送脚本：`./push_to_github.sh`
3. ✅ 验证推送成功：访问GitHub仓库

**预计总时间**：15-20分钟（包括Xcode安装）

---

**创建时间**：2026年1月18日
**仓库地址**：https://github.com/billyxu921/股票助手
