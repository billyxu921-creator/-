# 🚀 5分钟快速部署到GitHub

这是最简化的部署指南，帮助你快速上手。

---

## 📝 准备清单（5分钟）

### 1. 获取QQ邮箱授权码

1. 打开 https://mail.qq.com
2. 设置 → 账户 → 开启SMTP服务
3. 生成授权码（发短信验证）
4. **复制保存这个16位授权码**

### 2. 确认DeepSeek API Key

你的API Key: `sk-8b60ff11aefd4032a572f736087f175f`

---

## 🚀 部署步骤（3步完成）

### 步骤1: 上传代码到GitHub

在项目目录执行：

```bash
./deploy_to_github.sh
```

按提示输入：
- GitHub用户名
- 仓库名称（如：stock-analysis-system）

### 步骤2: 配置Secrets

1. 打开你的GitHub仓库
2. Settings → Secrets and variables → Actions
3. 点击【New repository secret】，添加6个Secrets：

```
名称: DEEPSEEK_API_KEY
值: sk-8b60ff11aefd4032a572f736087f175f

名称: SMTP_SERVER
值: smtp.qq.com

名称: SMTP_PORT
值: 465

名称: SENDER_EMAIL
值: 你的QQ邮箱@qq.com

名称: SENDER_PASSWORD
值: 你的16位授权码

名称: RECEIVER_EMAIL
值: 接收简报的邮箱
```

### 步骤3: 测试运行

1. 进入仓库的 Actions 标签
2. 选择【每日投资简报自动推送】
3. 点击【Run workflow】→【Run workflow】
4. 等待5-10分钟
5. 检查邮箱是否收到简报

---

## ✅ 完成！

如果收到邮件，说明部署成功！

系统将在每天早上8点自动运行并发送简报。

---

## 🔧 遇到问题？

### 邮件发送失败

- 确认使用的是**授权码**，不是QQ密码
- 重新生成授权码试试

### API调用失败

- 检查DeepSeek API Key是否正确
- 登录 https://platform.deepseek.com 查看余额

### 工作流失败

- 点击失败的运行记录
- 查看红色×步骤的详细日志
- 根据错误信息修复

---

## 📚 详细文档

需要更多帮助？查看：

- [完整部署指南](GITHUB_DEPLOYMENT_GUIDE.md)
- [部署检查清单](DEPLOYMENT_CHECKLIST.md)
- [项目README](README.md)

---

**祝部署顺利！** 🎉
