# 🔧 GitHub Workflow 修复指南

## 📋 当前状态

你已经将代码上传到GitHub，但workflow可能无法正常运行。需要进行以下修复。

---

## ✅ 第一步：配置GitHub Secrets（必须！）

进入你的GitHub仓库：https://github.com/billyxu921/股票助手

### 操作步骤

1. 点击 **Settings** 标签
2. 左侧菜单选择 **Secrets and variables** → **Actions**
3. 点击 **New repository secret** 按钮
4. 添加以下6个Secrets：

| Secret名称 | 值 | 说明 |
|-----------|-----|------|
| `DEEPSEEK_API_KEY` | `sk-8b60ff11aefd4032a572f736087f175f` | DeepSeek API密钥 |
| `SMTP_SERVER` | `smtp.qq.com` | QQ邮箱SMTP服务器 |
| `SMTP_PORT` | `465` | SMTP端口（SSL） |
| `SENDER_EMAIL` | `你的QQ邮箱@qq.com` | 发件人邮箱 |
| `SENDER_PASSWORD` | `你的QQ邮箱授权码` | QQ邮箱授权码（不是密码！） |
| `RECEIVER_EMAIL` | `接收邮箱@qq.com` | 收件人邮箱 |

### ⚠️  重要提示

**QQ邮箱授权码获取方法**：
1. 登录QQ邮箱网页版
2. 设置 → 账户
3. 找到"POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务"
4. 开启"POP3/SMTP服务"
5. 点击"生成授权码"
6. 复制生成的授权码（16位字符）

---

## ✅ 第二步：推送修复后的代码

你需要推送以下修复：

### 1. 修复 `daily_report_system.py`（已完成）

这个文件已经修复了 KeyError 问题，需要推送到GitHub。

### 2. 新增测试文件（可选）

- `test_daily_report_fix.py` - 测试兼容性
- `BUG_FIX_SUMMARY.md` - 修复说明

### 推送命令

```bash
# 如果你还没有安装Xcode命令行工具
xcode-select --install

# 等待安装完成后，执行以下命令
cd ~/Desktop/股票助手

# 添加修改的文件
git add daily_report_system.py
git add test_daily_report_fix.py
git add BUG_FIX_SUMMARY.md
git add GITHUB_WORKFLOW_FIX_GUIDE.md

# 提交
git commit -m "修复daily_report_system.py的KeyError问题，兼容新旧数据格式"

# 推送到GitHub
git push origin main
```

---

## ✅ 第三步：测试Workflow

### 手动触发测试

1. 进入GitHub仓库
2. 点击 **Actions** 标签
3. 左侧选择 "每日投资简报自动推送"
4. 点击右侧 **Run workflow** 按钮
5. 点击绿色的 **Run workflow** 确认

### 查看运行结果

- 等待约5-10分钟
- 查看运行日志，检查是否有错误
- 检查邮箱是否收到简报

---

## 🔍 可能遇到的问题

### 问题1: Workflow运行失败 - "未找到邮件配置"

**原因**: GitHub Secrets未配置或配置错误

**解决方法**:
1. 检查所有6个Secrets是否都已添加
2. 检查Secret名称是否完全一致（区分大小写）
3. 检查SMTP_PORT是否为数字465（不要加引号）

### 问题2: 邮件发送失败 - "认证失败"

**原因**: QQ邮箱授权码错误

**解决方法**:
1. 重新生成QQ邮箱授权码
2. 确保使用的是授权码，不是QQ密码
3. 更新GitHub Secret中的SENDER_PASSWORD

### 问题3: 黄金股票筛选失败

**原因**: AkShare数据源问题或网络问题

**解决方法**:
- Workflow已设置 `continue-on-error: true`
- 即使失败也会继续执行其他模块
- 检查日志查看具体错误

### 问题4: 量化选股失败

**原因**: DeepSeek API调用失败

**解决方法**:
1. 检查DEEPSEEK_API_KEY是否正确
2. 检查DeepSeek账户余额
3. 查看workflow日志中的具体错误信息

---

## 📊 Workflow运行内容

GitHub Actions版本会运行以下模块：

### ✅ 会运行的模块

1. **黄金股票筛选** (`gold_stock_screener.py`)
   - 不需要浏览器
   - 使用AkShare API
   - 生成CSV文件

2. **AI量化选股** (`Quant_Picker.py`)
   - 不需要浏览器
   - 使用DeepSeek API
   - 生成Markdown报告

3. **邮件推送** (`github_daily_sender.py`)
   - 汇总结果
   - 生成简报
   - 发送邮件

### ❌ 不会运行的模块

1. **微博情绪分析** - 需要浏览器登录
2. **全网热点发现** - 需要浏览器登录
3. **政客交易追踪** - 需要额外API（可选）

---

## 🎯 完整检查清单

推送代码前检查：

- [ ] 已修复 `daily_report_system.py` 的 KeyError 问题
- [ ] 已添加新文件到Git
- [ ] 已提交并推送到GitHub

配置GitHub Secrets：

- [ ] DEEPSEEK_API_KEY 已配置
- [ ] SMTP_SERVER 已配置（smtp.qq.com）
- [ ] SMTP_PORT 已配置（465）
- [ ] SENDER_EMAIL 已配置
- [ ] SENDER_PASSWORD 已配置（QQ邮箱授权码）
- [ ] RECEIVER_EMAIL 已配置

测试Workflow：

- [ ] 手动触发workflow
- [ ] 查看运行日志
- [ ] 检查邮箱是否收到简报
- [ ] 验证附件是否正确

---

## 📧 预期邮件内容

成功运行后，你会收到一封邮件：

**主题**: 📊 每日投资简报 - 2026年01月18日

**正文**: 
- 生成时间
- 简要说明
- 提示查看附件

**附件**:
1. `每日投资简报_20260118.md` - 综合简报
2. `gold_stocks_analysis_20260118.csv` - 黄金股票数据
3. `AI潜力股推荐_20260118.md` - AI推荐（如果成功）

---

## 🔄 定时运行

配置成功后，workflow会：

- **每天UTC 0:00自动运行**（北京时间早上8:00）
- 自动生成简报
- 自动发送到你的邮箱
- 无需任何手动操作

---

## 🆘 需要帮助？

如果遇到问题：

1. **查看Actions日志**
   - GitHub仓库 → Actions → 点击失败的运行
   - 查看详细错误信息

2. **检查配置**
   - 确认所有Secrets都已正确配置
   - 确认QQ邮箱授权码有效

3. **测试本地运行**
   ```bash
   # 测试黄金股票筛选
   python3 gold_stock_screener.py
   
   # 测试量化选股
   python3 Quant_Picker.py
   
   # 测试邮件发送
   python3 github_daily_sender.py
   ```

---

## 📝 快速命令参考

```bash
# 1. 安装Xcode工具（如果还没安装）
xcode-select --install

# 2. 进入项目目录
cd ~/Desktop/股票助手

# 3. 查看修改的文件
git status

# 4. 添加所有修改
git add .

# 5. 提交
git commit -m "修复workflow兼容性问题"

# 6. 推送
git push origin main
```

---

**创建时间**: 2026年1月18日
**状态**: 等待推送和配置

