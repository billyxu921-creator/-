# ✅ GitHub部署检查清单

在开始部署前，请逐项确认以下内容。

---

## 📋 准备阶段

### 1. 账号准备

- [ ] 已有GitHub账号
  - 如果没有，访问 https://github.com 注册
  
- [ ] 已有QQ邮箱
  - 用于发送每日简报
  
- [ ] 已有DeepSeek账号
  - 如果没有，访问 https://platform.deepseek.com 注册

### 2. 获取必要信息

- [ ] **DeepSeek API Key**
  - 登录 https://platform.deepseek.com
  - 进入API Keys页面
  - 创建新的API Key
  - 复制并保存: `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
  
- [ ] **QQ邮箱授权码**（重要：不是QQ密码！）
  - 登录QQ邮箱网页版: https://mail.qq.com
  - 点击【设置】→【账户】
  - 找到【POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务】
  - 开启【IMAP/SMTP服务】
  - 点击【生成授权码】
  - 发送短信验证
  - 复制并保存授权码: `abcdabcdabcdabcd`（16位）

### 3. 确认邮箱信息

- [ ] 发件邮箱: `_______________@qq.com`
- [ ] 收件邮箱: `_______________@_______.com`
- [ ] 授权码: `________________`（16位）

---

## 🚀 部署阶段

### 1. 创建GitHub仓库

- [ ] 登录GitHub
- [ ] 点击右上角【+】→【New repository】
- [ ] 填写仓库信息:
  - Repository name: `stock-analysis-system`
  - Description: `A股投资分析自动化系统`
  - 选择【Private】（推荐）
- [ ] 点击【Create repository】
- [ ] 记录仓库地址: `https://github.com/______/______`

### 2. 上传代码

选择以下方式之一：

**方式A: 使用一键部署脚本（推荐）**
```bash
chmod +x deploy_to_github.sh
./deploy_to_github.sh
```

- [ ] 脚本执行成功
- [ ] 代码已推送到GitHub

**方式B: 手动上传**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git branch -M main
git push -u origin main
```

- [ ] 所有命令执行成功
- [ ] 访问GitHub仓库页面，确认代码已上传

### 3. 配置GitHub Secrets

- [ ] 进入仓库页面
- [ ] 点击【Settings】
- [ ] 左侧菜单: 【Secrets and variables】→【Actions】
- [ ] 添加以下6个Secrets:

| Secret名称 | 值 | 状态 |
|-----------|-----|------|
| `DEEPSEEK_API_KEY` | `sk-8b60ff11aefd4032a572f736087f175f` | [ ] |
| `SMTP_SERVER` | `smtp.qq.com` | [ ] |
| `SMTP_PORT` | `465` | [ ] |
| `SENDER_EMAIL` | 你的QQ邮箱 | [ ] |
| `SENDER_PASSWORD` | QQ邮箱授权码（16位） | [ ] |
| `RECEIVER_EMAIL` | 接收简报的邮箱 | [ ] |

**添加步骤**（每个Secret重复）:
1. 点击【New repository secret】
2. Name: 输入Secret名称
3. Secret: 输入对应的值
4. 点击【Add secret】

- [ ] 所有6个Secrets已添加
- [ ] 在Secrets列表中确认所有名称正确

---

## 🧪 测试阶段

### 1. 手动触发测试

- [ ] 进入仓库页面
- [ ] 点击【Actions】标签
- [ ] 左侧选择【每日投资简报自动推送】
- [ ] 点击右侧【Run workflow】
- [ ] 点击绿色按钮【Run workflow】
- [ ] 等待执行（约5-10分钟）

### 2. 检查执行结果

- [ ] 工作流显示绿色✓（成功）
- [ ] 如果显示红色×，点击查看错误日志

### 3. 检查邮件

- [ ] 打开收件邮箱
- [ ] 查找主题为"📊 每日投资简报"的邮件
- [ ] 如果没收到，检查垃圾邮件箱
- [ ] 确认邮件包含附件

### 4. 下载报告文件

- [ ] 在Actions页面，点击工作流运行记录
- [ ] 滚动到底部【Artifacts】
- [ ] 下载【daily-reports】
- [ ] 解压并查看生成的报告文件

---

## ✅ 完成确认

### 所有检查项都已完成？

- [ ] ✅ GitHub仓库已创建
- [ ] ✅ 代码已上传
- [ ] ✅ 6个Secrets已配置
- [ ] ✅ 手动测试成功
- [ ] ✅ 收到测试邮件
- [ ] ✅ 报告文件正常

**恭喜！部署完成！** 🎉

系统将在每天早上8点自动运行并发送简报。

---

## 🔧 故障排查

### 如果测试失败

1. **查看详细日志**
   - Actions页面 → 点击失败的运行
   - 点击【generate-and-send-report】
   - 展开红色×的步骤
   - 查看错误信息

2. **常见错误**

   **错误: Authentication failed**
   - 检查SENDER_EMAIL和SENDER_PASSWORD是否正确
   - 确认使用的是授权码，不是QQ密码
   - 重新生成QQ邮箱授权码

   **错误: API key invalid**
   - 检查DEEPSEEK_API_KEY是否正确
   - 登录DeepSeek平台确认API Key有效

   **错误: No module named 'xxx'**
   - 检查requirements.txt是否完整
   - 查看"安装Python依赖"步骤的日志

3. **重新测试**
   - 修复问题后
   - 再次点击【Run workflow】测试

### 需要帮助？

查看详细文档:
- [GITHUB_DEPLOYMENT_GUIDE.md](GITHUB_DEPLOYMENT_GUIDE.md) - 完整部署指南
- [QUANT_PICKER_GUIDE.md](QUANT_PICKER_GUIDE.md) - 量化选股说明
- [WEIGHTED_SENTIMENT_GUIDE.md](WEIGHTED_SENTIMENT_GUIDE.md) - 情绪分析说明

---

## 📅 后续维护

### 每周检查

- [ ] 确认每天都收到简报邮件
- [ ] 检查报告内容是否正常
- [ ] 查看GitHub Actions执行状态

### 每月检查

- [ ] 检查DeepSeek API余额
- [ ] 查看GitHub Actions使用时长
- [ ] 下载备份历史报告

### 定期更新

- [ ] 关注项目更新
- [ ] 更新代码: `git pull origin main`
- [ ] 重新推送: `git push origin main`

---

**最后更新**: 2026年1月15日

**祝投资顺利！** 📈
