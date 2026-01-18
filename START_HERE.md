# 🎉 欢迎使用全网热点发现引擎！

> Discovery Engine - 自动识别小红书和微博上讨论度异常升高的股票板块

---

## 🚀 快速开始（3步）

### 第1步：安装依赖

```bash
pip3 install playwright pandas requests
playwright install chromium
```

### 第2步：检查配置

确保 `config.py` 文件存在且包含DeepSeek API Key。

### 第3步：运行程序

```bash
./run_discovery.sh
```

**就这么简单！** 🎊

---

## 📚 文档导航

### 🔰 新手必读

1. **[QUICK_START.md](QUICK_START.md)** ⭐ 推荐
   - 5分钟快速上手
   - 详细的使用流程
   - 常见问题解答

2. **[INSTALLATION_TEST.md](INSTALLATION_TEST.md)**
   - 完整的安装步骤
   - 测试验证流程
   - 故障排查指南

### 📖 功能说明

3. **[DISCOVERY_ENGINE_README.md](DISCOVERY_ENGINE_README.md)**
   - 功能概述
   - 输出文件说明
   - 工作流程图

4. **[NEW_FEATURE_DISCOVERY_ENGINE.md](NEW_FEATURE_DISCOVERY_ENGINE.md)**
   - 新功能亮点
   - 使用场景
   - 对比分析

### 🔧 详细指南

5. **[DISCOVERY_ENGINE_GUIDE.md](DISCOVERY_ENGINE_GUIDE.md)**
   - 详细使用说明
   - 技术架构
   - 最佳实践
   - 进阶配置

### 📊 项目信息

6. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)**
   - 7个模块总览
   - 文件结构
   - 技术栈

7. **[COMPLETION_SUMMARY.md](COMPLETION_SUMMARY.md)**
   - 任务完成报告
   - 交付清单
   - 统计数据

---

## 🎯 推荐阅读路径

### 路径1：快速体验（10分钟）

```
START_HERE.md (本文件)
    ↓
QUICK_START.md (快速开始)
    ↓
运行程序
    ↓
查看生成的报告
```

### 路径2：完整学习（30分钟）

```
START_HERE.md
    ↓
INSTALLATION_TEST.md (安装测试)
    ↓
QUICK_START.md (快速开始)
    ↓
DISCOVERY_ENGINE_README.md (功能说明)
    ↓
DISCOVERY_ENGINE_GUIDE.md (详细指南)
    ↓
运行程序
```

### 路径3：深入研究（1小时）

```
阅读所有文档
    ↓
运行测试脚本
    ↓
运行完整程序
    ↓
分析生成的报告
    ↓
查看源代码
    ↓
自定义配置
```

---

## 📁 文件清单

### 核心文件
- `Discovery_Engine.py` (34KB, 931行) - 主程序
- `test_discovery_engine.py` (1.7KB, 63行) - 测试脚本
- `run_discovery.sh` (1.6KB, 48行) - 快速启动脚本

### 文档文件
- `QUICK_START.md` (5.2KB) - 快速开始 ⭐
- `DISCOVERY_ENGINE_README.md` (4.9KB) - 功能说明
- `DISCOVERY_ENGINE_GUIDE.md` (8.6KB) - 详细指南
- `INSTALLATION_TEST.md` (7.0KB) - 安装测试
- `NEW_FEATURE_DISCOVERY_ENGINE.md` (11KB) - 新功能说明
- `PROJECT_SUMMARY.md` (10KB) - 项目总结
- `COMPLETION_SUMMARY.md` (10KB) - 完成报告
- `START_HERE.md` (本文件) - 导航页

---

## 🎬 使用演示

### 运行程序

```bash
$ ./run_discovery.sh

╔══════════════════════════════════════════════════════════╗
║          全网热点发现引擎 - Discovery Engine             ║
╚══════════════════════════════════════════════════════════╝

✓ Python3已安装
✓ 依赖已安装
✓ 配置文件存在

启动全网热点发现引擎...

============================================================
全网热点发现引擎 - Discovery Engine
============================================================

【第1步】抓取小红书财经频道...
启动浏览器 (headless=False)...
⏳ 随机等待 7.3 秒...
✓ 小红书: 48 条

【第2步】抓取微博财经热搜和股票超话...
✓ 微博: 35 条

【第3步】保存今日数据...
✓ 今日数据已保存

【第4步】加载昨日数据...
✓ 加载昨日数据: 42 条

【第5步】AI智能发现分析...
正在调用DeepSeek API进行智能分析...
✓ AI分析完成

【第6步】生成全网雷达简报...
✓ 简报已保存: 全网雷达报告_20260115.md

============================================================
✅ 全网热点发现完成！
============================================================

生成文件:
  - 原始数据: discovery_raw_20260115_093045.csv
  - 雷达简报: 全网雷达报告_20260115.md
```

### 查看报告

```bash
$ open 全网雷达报告_20260115.md
```

报告内容示例：

```markdown
# 【全网雷达：你可能错过的热门机会】

## 🔥 讨论度异常升高的板块 TOP 3

### 1. 煤炭板块 🚀
**增长率**: 250%
**讨论热度**: 今日45次 vs 昨日13次
**火爆原因**: 政策催化，煤炭保供政策出台
**置信度**: 85%

### 2. 核电板块 🚀
**增长率**: 180%
...
```

---

## ⚡ 常见问题

### Q: 需要什么环境？
A: Python 3.7+, macOS/Linux/Windows, 稳定网络

### Q: 需要登录吗？
A: 是的，需要登录小红书和微博（扫码或账号密码）

### Q: 运行多久？
A: 首次运行约15-30分钟（包含登录时间）

### Q: 多久运行一次？
A: 建议每天运行1次（早上9点）

### Q: 遇到验证码怎么办？
A: 程序会发出提示音，手动完成验证码后按回车继续

### Q: 首次运行效果如何？
A: 首次运行没有昨日数据，对比效果有限。建议连续运行3-5天。

---

## 🎁 核心特性

### 🔍 智能发现
自动识别讨论度异常升高的板块，不再错过热门机会！

### 📡 多源探测
小红书 + 微博双平台，全面覆盖社交媒体热点。

### 🤖 AI分析
DeepSeek AI对比今日vs昨日，识别动量最大的3个板块。

### 🛡️ 反爬稳定
5.5-12.2秒随机等待 + 拟人滚动 + 验证码提示，稳定运行。

### 📊 自动报告
生成Markdown格式的【全网雷达简报】，清晰易读。

---

## 🎯 下一步

### 立即开始

```bash
# 1. 安装依赖
pip3 install playwright pandas requests
playwright install chromium

# 2. 运行测试（可选）
python3 test_discovery_engine.py

# 3. 运行完整版
./run_discovery.sh
```

### 深入学习

1. 阅读 [QUICK_START.md](QUICK_START.md)
2. 查看 [DISCOVERY_ENGINE_GUIDE.md](DISCOVERY_ENGINE_GUIDE.md)
3. 了解 [NEW_FEATURE_DISCOVERY_ENGINE.md](NEW_FEATURE_DISCOVERY_ENGINE.md)

---

## 📞 需要帮助？

### 文档资源
- **快速开始**: [QUICK_START.md](QUICK_START.md)
- **安装测试**: [INSTALLATION_TEST.md](INSTALLATION_TEST.md)
- **详细指南**: [DISCOVERY_ENGINE_GUIDE.md](DISCOVERY_ENGINE_GUIDE.md)

### 测试脚本
```bash
# API测试
python3 test_api_key.py

# 功能测试
python3 test_discovery_engine.py
```

### 查看日志
程序会输出详细的执行日志，帮助你了解运行状态。

---

## ⚖️ 免责声明

- 仅供学习和研究使用
- 请遵守平台服务条款
- 不构成投资建议
- 投资有风险，决策需谨慎

---

## 🎊 准备好了吗？

**开始你的全网热点发现之旅！** 🚀

```bash
./run_discovery.sh
```

---

**版本**: v1.0  
**发布日期**: 2026-01-15  
**状态**: ✅ 已完成

---

💡 **提示**: 建议先阅读 [QUICK_START.md](QUICK_START.md) 了解详细使用流程。
