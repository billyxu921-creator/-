# 👋 从这里开始

欢迎使用 **A股投资分析自动化系统**！

这个文档会帮你快速上手。

---

## 🎯 这个系统能做什么？

每天早上8点，你会收到一封邮件，包含：

1. **黄金股票筛选 TOP 5** - 综合评分最高的黄金概念股
2. **AI量化选股 TOP 3** - DeepSeek AI推荐的潜力股
3. **微博情绪指数** - 黄金市场情绪分析（本地运行）
4. **全网热点雷达** - 异常升温的投资板块（本地运行）

**完全自动化，无需人工干预！**

---

## ⚡ 3步快速开始

### 第1步: 选择部署方式（1分钟）

**不确定选哪个？** 查看 → [WHICH_WAY_TO_DEPLOY.md](WHICH_WAY_TO_DEPLOY.md)

**大多数人推荐**: GitHub自动化（简单、免费、自动）

### 第2步: 准备必要信息（5分钟）

需要准备：
- ✅ GitHub账号
- ✅ QQ邮箱授权码（不是密码！）
- ✅ DeepSeek API Key: `sk-8b60ff11aefd4032a572f736087f175f`

**如何获取授权码？** 查看 → [QUICK_START_GITHUB.md](QUICK_START_GITHUB.md)

### 第3步: 部署（3分钟）

运行一键部署脚本：
```bash
./deploy_to_github.sh
```

然后配置6个Secrets，完成！

**详细步骤** → [QUICK_START_GITHUB.md](QUICK_START_GITHUB.md)

---

## 📚 文档导航

### 🚀 快速开始（推荐新手）

1. **[WHICH_WAY_TO_DEPLOY.md](WHICH_WAY_TO_DEPLOY.md)** ⭐
   - 帮你选择合适的部署方式
   - 对比GitHub vs 本地运行
   - 2分钟做出决定

2. **[QUICK_START_GITHUB.md](QUICK_START_GITHUB.md)** ⭐
   - 5分钟快速部署到GitHub
   - 最简化的步骤
   - 适合新手

3. **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)**
   - 逐项检查清单
   - 确保不遗漏任何步骤
   - 包含故障排查

### 📖 详细指南（需要更多信息）

1. **[README.md](README.md)**
   - 项目总览
   - 功能介绍
   - 本地运行指南

2. **[GITHUB_DEPLOYMENT_GUIDE.md](GITHUB_DEPLOYMENT_GUIDE.md)**
   - 完整的GitHub部署指南
   - 包含所有细节
   - 常见问题解答

3. **[PROJECT_COMPLETE.md](PROJECT_COMPLETE.md)**
   - 项目完成总结
   - 所有功能列表
   - 技术栈说明

### 🔧 功能文档（了解具体模块）

1. **[QUANT_PICKER_GUIDE.md](QUANT_PICKER_GUIDE.md)**
   - AI量化选股详细说明
   - 算法原理
   - 使用方法

2. **[WEIGHTED_SENTIMENT_GUIDE.md](WEIGHTED_SENTIMENT_GUIDE.md)**
   - 微博情绪分析说明
   - 加权算法
   - 影响力计算

3. **[DISCOVERY_ENGINE_GUIDE.md](DISCOVERY_ENGINE_GUIDE.md)**
   - 全网热点发现引擎
   - 多平台探测
   - AI识别算法

---

## 🎯 根据你的情况选择

### 我是技术小白

**推荐路径**:
1. 阅读 [WHICH_WAY_TO_DEPLOY.md](WHICH_WAY_TO_DEPLOY.md)
2. 选择"GitHub自动化"
3. 按照 [QUICK_START_GITHUB.md](QUICK_START_GITHUB.md) 部署
4. 完成！

**预计时间**: 10分钟

### 我有一定技术基础

**推荐路径**:
1. 阅读 [README.md](README.md) 了解项目
2. 阅读 [WHICH_WAY_TO_DEPLOY.md](WHICH_WAY_TO_DEPLOY.md) 选择方式
3. 按照 [GITHUB_DEPLOYMENT_GUIDE.md](GITHUB_DEPLOYMENT_GUIDE.md) 详细部署
4. 可选：配置本地运行环境

**预计时间**: 30分钟

### 我是技术达人

**推荐路径**:
1. 阅读 [PROJECT_COMPLETE.md](PROJECT_COMPLETE.md) 了解全貌
2. 部署GitHub自动化
3. 配置本地完整环境
4. 查看各模块详细文档，自定义功能

**预计时间**: 1小时

---

## 🤔 常见问题

### Q: 完全免费吗？

**A**: GitHub Actions免费，QQ邮箱免费，只有DeepSeek API按使用量计费（每天约几分钱）。

### Q: 需要懂编程吗？

**A**: 不需要！按照文档操作即可。所有代码都已经写好。

### Q: 多久能收到第一份简报？

**A**: 部署完成后，第二天早上8点就能收到。也可以手动测试立即收到。

### Q: 简报准确吗？

**A**: 系统结合技术指标、舆情分析、AI判断，提供参考。但投资需谨慎，不构成投资建议。

### Q: 可以自定义吗？

**A**: 可以！所有代码开源，可以根据需要修改。

---

## 🎁 额外资源

### 测试工具

- **配置测试**: `python3 test_config.py`
  - 验证配置是否正确
  - 测试API连接
  - 测试邮件发送

- **一键部署**: `./deploy_to_github.sh`
  - 自动上传代码到GitHub
  - 交互式配置
  - 自动创建必要文件

### 示例文件

- **config.example.py** - 配置文件模板
- **requirements.txt** - Python依赖列表
- **.github/workflows/daily-report.yml** - GitHub Actions配置

---

## 📞 需要帮助？

### 部署遇到问题

1. 查看 [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) 的故障排查部分
2. 查看 [GITHUB_DEPLOYMENT_GUIDE.md](GITHUB_DEPLOYMENT_GUIDE.md) 的常见问题
3. 运行 `python3 test_config.py` 测试配置

### 想了解更多

1. 查看 [PROJECT_COMPLETE.md](PROJECT_COMPLETE.md) 了解项目全貌
2. 查看各模块的详细文档
3. 阅读代码中的注释（都有详细的中文注释）

---

## ✅ 准备好了吗？

选择你的起点：

- 🚀 **快速开始** → [QUICK_START_GITHUB.md](QUICK_START_GITHUB.md)
- 🤔 **选择方式** → [WHICH_WAY_TO_DEPLOY.md](WHICH_WAY_TO_DEPLOY.md)
- 📖 **详细了解** → [README.md](README.md)
- ✅ **检查清单** → [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)

---

## 🎉 开始你的投资分析之旅！

**记住**: 
- 📊 系统提供参考，不构成投资建议
- ⚠️ 股票投资有风险，入市需谨慎
- 💡 理性投资，独立思考

**祝你投资顺利！** 📈

---

**最后更新**: 2026年1月15日

**版本**: v1.0.0
