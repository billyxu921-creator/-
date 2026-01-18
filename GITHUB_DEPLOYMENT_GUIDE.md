# 📦 GitHub自动化部署完整指南

## 📋 目录
1. [准备工作](#准备工作)
2. [上传代码到GitHub](#上传代码到github)
3. [配置GitHub Secrets](#配置github-secrets)
4. [测试自动化工作流](#测试自动化工作流)
5. [常见问题](#常见问题)

---

## 1. 准备工作

### 1.1 获取QQ邮箱授权码

**重要**: GitHub Actions需要使用QQ邮箱授权码，不是QQ密码！

1. 登录QQ邮箱网页版：https://mail.qq.com
2. 点击【设置】→【账户】
3. 找到【POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务】
4. 开启【IMAP/SMTP服务】或【POP3/SMTP服务】
5. 点击【生成授权码】
6. 按提示发送短信验证
7. **保存生成的授权码**（16位字符，如：abcdabcdabcdabcd）

### 1.2 确认DeepSeek API Key

你的API Key: `sk-8b60ff11aefd4032a572f736087f175f`

---

## 2. 上传代码到GitHub

### 2.1 创建GitHub仓库

1. 登录GitHub: https://github.com
2. 点击右上角【+】→【New repository】
3. 填写仓库信息：
   - Repository name: `stock-analysis-system`（或其他名称）
   - Description: `A股投资分析自动化系统`
   - 选择【Private】（推荐，保护你的配置）
4. 点击【Create repository】

### 2.2 上传代码

在你的项目目录下执行：

```bash
# 初始化Git仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: 股票分析自动化系统"

# 关联远程仓库（替换YOUR_USERNAME和YOUR_REPO）
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# 推送到GitHub
git branch -M main
git push -u origin main
```

**注意**: 上传前确保 `config.py` 中的敏感信息已经被替换为占位符！

---

## 3. 配置GitHub Secrets

### 3.1 进入Secrets设置

1. 打开你的GitHub仓库页面
2. 点击【Settings】（设置）
3. 左侧菜单找到【Secrets and variables】→【Actions】
4. 点击【New repository secret】

### 3.2 添加以下Secrets

**必须添加的6个Secrets**:

| Secret名称 | 值 | 说明 |
|-----------|-----|------|
| `DEEPSEEK_API_KEY` | `sk-8b60ff11aefd4032a572f736087f175f` | DeepSeek API密钥 |
| `SMTP_SERVER` | `smtp.qq.com` | QQ邮箱SMTP服务器 |
| `SMTP_PORT` | `465` | SMTP端口（SSL） |
| `SENDER_EMAIL` | `your_email@qq.com` | 你的QQ邮箱 |
| `SENDER_PASSWORD` | `abcdabcdabcdabcd` | QQ邮箱授权码（16位） |
| `RECEIVER_EMAIL` | `receiver@example.com` | 接收简报的邮箱 |

**添加步骤**（每个Secret重复以下步骤）:
1. 点击【New repository secret】
2. Name: 输入Secret名称（如 `DEEPSEEK_API_KEY`）
3. Secret: 输入对应的值
4. 点击【Add secret】

### 3.3 验证Secrets

添加完成后，你应该看到6个Secrets：
- ✅ DEEPSEEK_API_KEY
- ✅ SMTP_SERVER
- ✅ SMTP_PORT
- ✅ SENDER_EMAIL
- ✅ SENDER_PASSWORD
- ✅ RECEIVER_EMAIL

---

## 4. 测试自动化工作流

### 4.1 手动触发测试

1. 进入仓库页面
2. 点击【Actions】标签
3. 左侧选择【每日投资简报自动推送】
4. 点击右侧【Run workflow】→【Run workflow】
5. 等待执行完成（约5-10分钟）

### 4.2 查看执行结果

**成功标志**:
- ✅ 工作流显示绿色对勾
- ✅ 你的邮箱收到简报邮件
- ✅ Actions页面可以下载报告文件

**查看详细日志**:
1. 点击工作流运行记录
2. 点击【generate-and-send-report】
3. 展开各个步骤查看日志

### 4.3 下载生成的报告

1. 在工作流运行页面底部找到【Artifacts】
2. 下载【daily-reports】（包含所有生成的报告）
3. 下载【logs】（包含执行日志）

---

## 5. 自动化运行说明

### 5.1 运行时间

- **自动运行**: 每天北京时间早上8:00
- **GitHub Actions时区**: UTC 0:00（对应北京时间8:00）
- **执行时长**: 约5-10分钟

### 5.2 运行内容

GitHub Actions版本会运行以下模块：

✅ **包含的模块**:
- 黄金股票筛选（`gold_stock_screener.py`）
- AI量化选股（`Quant_Picker.py`）
- 综合简报生成
- 邮件推送

⊘ **不包含的模块**（需要浏览器环境）:
- 微博情绪分析（需要扫码登录）
- 小红书热点发现（需要扫码登录）
- 全网热点发现引擎（需要浏览器）

### 5.3 本地完整版运行

如果需要运行完整版（包含微博、小红书），在本地执行：

```bash
# 运行完整版（包含浏览器抓取）
python3 daily_email_sender.py
```

---

## 6. 常见问题

### Q1: 邮件发送失败

**可能原因**:
- QQ邮箱授权码错误（不是QQ密码！）
- SMTP服务未开启
- 邮箱被QQ安全策略限制

**解决方法**:
1. 重新生成QQ邮箱授权码
2. 确认SMTP服务已开启
3. 在QQ邮箱设置中添加GitHub Actions的IP到白名单

### Q2: DeepSeek API调用失败

**可能原因**:
- API Key错误
- API额度用完
- 网络连接问题

**解决方法**:
1. 检查API Key是否正确
2. 登录DeepSeek查看API额度
3. 查看Actions日志中的详细错误信息

### Q3: 工作流执行失败

**排查步骤**:
1. 点击失败的工作流
2. 查看红色×的步骤
3. 展开查看详细错误日志
4. 根据错误信息修复问题

### Q4: 没有收到邮件

**检查清单**:
- ✅ Secrets配置正确
- ✅ 工作流执行成功
- ✅ 检查垃圾邮件箱
- ✅ 确认收件人邮箱正确

### Q5: 想修改运行时间

编辑 `.github/workflows/daily-report.yml`:

```yaml
schedule:
  - cron: '0 0 * * *'  # UTC 0:00 = 北京时间 8:00
```

**常用时间对照**:
- 北京时间 7:00 → UTC 23:00 → `'0 23 * * *'`
- 北京时间 8:00 → UTC 0:00 → `'0 0 * * *'`
- 北京时间 9:00 → UTC 1:00 → `'0 1 * * *'`

---

## 7. 维护建议

### 7.1 定期检查

- 每周检查一次邮件是否正常接收
- 每月检查一次DeepSeek API额度
- 关注GitHub Actions的执行状态

### 7.2 更新代码

```bash
# 拉取最新代码
git pull origin main

# 修改代码后提交
git add .
git commit -m "更新说明"
git push origin main
```

### 7.3 备份数据

GitHub Actions会自动保存30天的报告文件，建议定期下载备份。

---

## 8. 成本说明

### 8.1 GitHub Actions

- **免费额度**: 每月2000分钟（私有仓库）
- **本项目消耗**: 每天约10分钟 = 每月300分钟
- **结论**: 完全免费 ✅

### 8.2 DeepSeek API

- 根据你的API套餐计费
- 每天约调用10-20次
- 建议定期检查余额

### 8.3 QQ邮箱

- 完全免费 ✅

---

## 9. 安全建议

### 9.1 保护敏感信息

- ✅ 使用GitHub Secrets存储密钥
- ✅ 不要在代码中硬编码密码
- ✅ 设置仓库为Private

### 9.2 API Key安全

- 定期更换API Key
- 不要分享给他人
- 监控API使用情况

### 9.3 邮箱安全

- 使用授权码而非密码
- 定期更换授权码
- 开启QQ邮箱的登录保护

---

## 10. 联系支持

如果遇到问题：

1. 查看GitHub Actions日志
2. 检查本文档的常见问题部分
3. 查看各模块的详细文档：
   - `QUANT_PICKER_GUIDE.md`
   - `WEIGHTED_SENTIMENT_GUIDE.md`
   - `DISCOVERY_ENGINE_GUIDE.md`

---

## ✅ 部署检查清单

部署前请确认：

- [ ] 已创建GitHub仓库
- [ ] 已获取QQ邮箱授权码
- [ ] 已添加6个GitHub Secrets
- [ ] 已上传代码到GitHub
- [ ] 已手动测试工作流
- [ ] 已收到测试邮件
- [ ] 已设置仓库为Private（推荐）

**全部完成后，系统将每天早上8点自动运行并发送简报！** 🎉

---

**最后更新**: 2026年1月15日
