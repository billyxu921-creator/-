# 📊 A股投资分析自动化系统

一个集成多维度分析的A股投资决策辅助系统，每日自动生成投资简报并推送到邮箱。

---

## 🎯 新手？从这里开始！

**👉 [START_HERE_GITHUB.md](START_HERE_GITHUB.md) - 10分钟快速上手指南**

不确定如何开始？这个文档会引导你完成所有步骤。

---

## ✨ 核心功能

### 1. 黄金股票筛选 🏆
- 精准筛选符合条件的黄金概念股
- 官方资本背书检测（社保、汇金、证金）
- 综合评分系统（股本、市值、行业匹配）

### 2. AI量化选股 🤖
- 技术指标初选（市值、涨幅、换手率）
- 舆情碰撞分析（微博、小红书热度）
- DeepSeek AI终极筛选
- 自动预测止盈位

### 3. 微博情绪分析 📱
- 实时抓取微博黄金相关讨论
- 博主影响力加权计算
- 关键词情绪加成
- AI生成0-100情绪指数

### 4. 全网热点发现 🔍
- 多平台热点探测（小红书、微博）
- AI智能识别异常升温板块
- 自动发现非预设投资机会

### 5. 政客交易追踪 🏛️
- 监控美国国会议员股票交易
- 委员会背景关联分析
- 高置信度信号识别
- DeepSeek过滤Twitter有价值讨论

### 6. 每日自动推送 📧
- 每天早上8点自动运行
- 生成综合投资简报
- 邮件推送到指定邮箱
- GitHub Actions云端执行

## 🚀 快速开始

### 方式一：GitHub自动化部署（推荐）

**适合**: 希望每天自动接收简报，无需本地运行

1. **上传代码到GitHub**
```bash
# 使用一键部署脚本
chmod +x deploy_to_github.sh
./deploy_to_github.sh
```

2. **配置GitHub Secrets**
   - 进入仓库 Settings → Secrets and variables → Actions
   - 添加6个必需的Secrets（详见部署指南）

3. **测试运行**
   - 进入 Actions 标签
   - 手动触发工作流测试

**详细步骤**: 查看 [GITHUB_DEPLOYMENT_GUIDE.md](GITHUB_DEPLOYMENT_GUIDE.md)

### 方式二：本地运行

**适合**: 需要完整功能（包含微博、小红书抓取）

1. **安装依赖**
```bash
pip install -r requirements.txt
pip install -r requirements_weibo.txt
playwright install chromium
```

2. **配置文件**
```bash
# 复制示例配置
cp config.example.py config.py

# 编辑config.py，填入真实配置
# - DeepSeek API Key
# - 邮箱配置
```

3. **运行完整分析**
```bash
# 运行所有模块并发送邮件
python3 daily_email_sender.py

# 或者单独运行各模块
python3 gold_stock_screener.py      # 黄金股票筛选
python3 Quant_Picker.py             # AI量化选股
python3 weibo_sentiment_weighted.py # 微博情绪分析
python3 Discovery_Engine.py         # 全网热点发现
python3 politician_trade_tracker.py # 政客交易追踪
```

## 📦 项目结构

```
├── gold_stock_screener.py          # 黄金股票筛选器
├── Quant_Picker.py                 # AI量化选股器
├── weibo_sentiment_weighted.py     # 微博情绪分析（加权版）
├── Discovery_Engine.py             # 全网热点发现引擎
├── politician_trade_tracker.py     # 政客交易追踪器
├── daily_email_sender.py           # 本地邮件推送系统
├── github_daily_sender.py          # GitHub Actions专用推送
├── schedule_daily_report.py        # 本地定时任务调度
├── config.py                       # 配置文件（需自行创建）
├── config.example.py               # 配置文件示例
├── requirements.txt                # Python依赖
├── requirements_weibo.txt          # 微博抓取依赖
├── .github/workflows/              # GitHub Actions配置
│   └── daily-report.yml
└── 文档/
    ├── GITHUB_DEPLOYMENT_GUIDE.md  # GitHub部署完整指南
    ├── QUANT_PICKER_GUIDE.md       # 量化选股使用指南
    ├── WEIGHTED_SENTIMENT_GUIDE.md # 微博情绪分析指南
    ├── DISCOVERY_ENGINE_GUIDE.md   # 热点发现引擎指南
    └── POLITICIAN_TRACKER_GUIDE.md # 政客交易追踪指南
```

## 📋 系统要求

### GitHub Actions运行
- GitHub账号
- QQ邮箱（用于发送简报）
- DeepSeek API Key

### 本地运行
- Python 3.8+
- macOS / Linux / Windows
- 稳定的网络连接
- Chromium浏览器（用于微博、小红书抓取）

## 🔧 配置说明

### 必需配置

1. **DeepSeek API Key**
   - 获取地址: https://platform.deepseek.com
   - 用于AI分析和选股

2. **QQ邮箱授权码**
   - 登录QQ邮箱 → 设置 → 账户
   - 开启SMTP服务 → 生成授权码
   - 注意：是授权码，不是QQ密码！

3. **GitHub Secrets**（仅GitHub部署需要）
   - DEEPSEEK_API_KEY
   - SMTP_SERVER
   - SMTP_PORT
   - SENDER_EMAIL
   - SENDER_PASSWORD
   - RECEIVER_EMAIL

## 📊 简报内容

每日简报包含：

1. **黄金股票筛选 TOP 5**
   - 综合评分排名
   - 股本、市值、官方背书分析

2. **AI量化选股 TOP 3**
   - 技术面+舆情面结合分析
   - DeepSeek AI推荐理由
   - 短期止盈位预测

3. **微博黄金情绪指数**（本地运行）
   - 0-100情绪评分
   - 3个风险点
   - 3个机会点

4. **全网热点雷达**（本地运行）
   - 异常升温的3个板块
   - 热度变化趋势

## ⚙️ 运行模式对比

| 功能模块 | GitHub Actions | 本地运行 |
|---------|---------------|---------|
| 黄金股票筛选 | ✅ | ✅ |
| AI量化选股 | ✅ | ✅ |
| 微博情绪分析 | ❌ | ✅ |
| 全网热点发现 | ❌ | ✅ |
| 政客交易追踪 | ✅ | ✅ |
| 自动定时运行 | ✅ | ✅ |
| 邮件推送 | ✅ | ✅ |

**说明**: GitHub Actions无法运行需要浏览器登录的模块（微博、小红书）

## 🔒 安全说明

- ✅ 所有敏感信息使用GitHub Secrets存储
- ✅ 不在代码中硬编码密码
- ✅ 建议设置仓库为Private
- ✅ 定期更换API Key和授权码

## 💰 成本说明

- **GitHub Actions**: 免费（每月2000分钟，本项目约300分钟）
- **QQ邮箱**: 免费
- **DeepSeek API**: 根据套餐计费（每天约10-20次调用）

## 📚 详细文档

- [GitHub部署完整指南](GITHUB_DEPLOYMENT_GUIDE.md)
- [量化选股使用指南](QUANT_PICKER_GUIDE.md)
- [微博情绪分析指南](WEIGHTED_SENTIMENT_GUIDE.md)
- [热点发现引擎指南](DISCOVERY_ENGINE_GUIDE.md)
- [政客交易追踪指南](POLITICIAN_TRACKER_GUIDE.md)

## ⚠️ 免责声明

本系统由AI自动生成分析报告，仅供参考学习，不构成任何投资建议。

股票投资有风险，入市需谨慎。请根据自身情况理性投资。

## 📝 更新日志

### v1.0.0 (2026-01-15)
- ✅ 黄金股票筛选系统
- ✅ AI量化选股器
- ✅ 微博情绪分析（加权版）
- ✅ 全网热点发现引擎
- ✅ GitHub Actions自动化部署
- ✅ 每日邮件推送

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

---

**开始使用**: 查看 [GITHUB_DEPLOYMENT_GUIDE.md](GITHUB_DEPLOYMENT_GUIDE.md) 开始部署！