# 安装和测试指南

> 全网热点发现引擎 - 完整安装和测试流程

---

## 📋 系统要求

- **操作系统**: macOS / Linux / Windows
- **Python版本**: 3.7+
- **网络**: 稳定的互联网连接
- **浏览器**: Chromium（自动安装）

---

## 🔧 安装步骤

### 第1步：检查Python版本

```bash
python3 --version
```

**期望输出**: `Python 3.7.0` 或更高版本

如果未安装Python，请访问: https://www.python.org/downloads/

---

### 第2步：安装依赖包

```bash
# 安装Python包
pip3 install playwright pandas requests

# 验证安装
pip3 list | grep -E "playwright|pandas|requests"
```

**期望输出**:
```
pandas         2.x.x
playwright     1.x.x
requests       2.x.x
```

---

### 第3步：安装浏览器驱动

```bash
# 安装Chromium浏览器
playwright install chromium

# 验证安装
playwright --version
```

**期望输出**: `Version 1.x.x`

---

### 第4步：检查配置文件

```bash
# 检查config.py是否存在
ls -lh config.py
```

**期望输出**: 显示config.py文件信息

如果不存在，请从 `config.example.py` 复制：
```bash
cp config.example.py config.py
```

---

### 第5步：验证API Key

```bash
# 测试DeepSeek API连接
python3 test_api_key.py
```

**期望输出**:
```
测试DeepSeek API连接...
✓ API连接成功
✓ 模型: deepseek-chat
```

如果失败，请检查 `config.py` 中的API Key是否正确。

---

## 🧪 测试流程

### 测试1：语法检查

```bash
# 检查Python语法
python3 -m py_compile Discovery_Engine.py
python3 -m py_compile test_discovery_engine.py
```

**期望输出**: 无错误信息

**状态**: ✅ 已通过

---

### 测试2：导入测试

```bash
# 测试模块导入
python3 -c "from Discovery_Engine import DiscoveryEngine; print('✓ 模块导入成功')"
```

**期望输出**: `✓ 模块导入成功`

---

### 测试3：配置测试

```bash
# 测试配置加载
python3 -c "from config import DEEPSEEK_CONFIG; print('✓ 配置加载成功'); print('API Key:', DEEPSEEK_CONFIG['api_key'][:20] + '...')"
```

**期望输出**:
```
✓ 配置加载成功
API Key: sk-8b60ff11aefd4032...
```

---

### 测试4：功能测试（简化版）

```bash
# 运行测试脚本（减少抓取量）
python3 test_discovery_engine.py
```

**测试流程**:
1. 程序启动
2. 打开浏览器
3. 提示是否继续（输入 `y`）
4. 抓取小红书（20条，测试用）
5. 抓取微博
6. AI分析
7. 生成报告

**期望输出**:
```
测试全网热点发现引擎
============================================================

⚠️  重要提示:
1. 本测试需要真实浏览器环境（headless=False）
2. 需要手动登录小红书和微博（扫码或账号密码）
3. 抓取过程较慢（5.5-12.2秒随机等待），请耐心等待
4. 如遇验证码，会发出提示音，请手动处理

是否继续测试？(y/n): y

开始测试...

============================================================
开始抓取小红书财经频道
============================================================
启动浏览器 (headless=False)...
...
✓ 小红书抓取完成，共获取 20 条笔记

============================================================
开始抓取微博财经热搜和股票超话
============================================================
...
✓ 微博抓取完成，共获取 15 条

✅ 测试完成！

请查看生成的文件:
  - discovery_raw_*.csv (原始数据)
  - 全网雷达报告_*.md (分析简报)
```

---

### 测试5：完整运行（可选）

```bash
# 运行完整版本（50条小红书笔记）
python3 Discovery_Engine.py

# 或使用快速启动脚本
./run_discovery.sh
```

**注意**: 完整运行需要15-30分钟，取决于网络速度和登录时间。

---

## ✅ 验证清单

完成以下检查，确保系统正常运行：

- [ ] Python 3.7+ 已安装
- [ ] playwright, pandas, requests 已安装
- [ ] Chromium浏览器已安装
- [ ] config.py 文件存在
- [ ] DeepSeek API Key 已配置
- [ ] API连接测试通过
- [ ] 语法检查通过
- [ ] 模块导入成功
- [ ] 配置加载成功
- [ ] 测试脚本运行成功

---

## 🐛 常见问题排查

### 问题1: pip3 command not found

**解决方案**:
```bash
# macOS
brew install python3

# 或使用python自带的pip
python3 -m pip install playwright pandas requests
```

---

### 问题2: playwright install 失败

**解决方案**:
```bash
# 使用代理（如果在国内）
export PLAYWRIGHT_DOWNLOAD_HOST=https://playwright.azureedge.net

# 重新安装
playwright install chromium
```

---

### 问题3: ModuleNotFoundError: No module named 'playwright'

**解决方案**:
```bash
# 确认pip安装路径
which pip3

# 使用python -m pip安装
python3 -m pip install playwright pandas requests
```

---

### 问题4: API连接失败

**可能原因**:
1. API Key错误
2. 网络问题
3. API服务不可用

**解决方案**:
```bash
# 检查API Key
cat config.py | grep api_key

# 测试网络连接
curl -I https://api.deepseek.com

# 重新测试
python3 test_api_key.py
```

---

### 问题5: 浏览器无法启动

**解决方案**:
```bash
# 重新安装浏览器
playwright install --force chromium

# 检查浏览器路径
playwright show-trace
```

---

### 问题6: 登录后仍提示需要登录

**解决方案**:
1. 确保登录成功后页面已完全加载
2. 等待3-5秒后再按回车
3. 如果仍然失败，关闭程序重新运行

---

### 问题7: 抓取数据为空

**可能原因**:
1. 页面结构变化
2. 网络超时
3. 被反爬拦截

**解决方案**:
1. 检查网络连接
2. 增加等待时间
3. 检查是否出现验证码
4. 重新运行程序

---

## 📊 性能基准

### 测试环境
- **系统**: macOS 14.0
- **CPU**: Apple M1
- **内存**: 16GB
- **网络**: 100Mbps

### 性能数据

| 操作 | 时间 | 说明 |
|------|------|------|
| 安装依赖 | 2-5分钟 | 首次安装 |
| 浏览器安装 | 1-3分钟 | 下载Chromium |
| 小红书抓取 | 5-10分钟 | 50条笔记 |
| 微博抓取 | 3-5分钟 | 热搜+超话 |
| AI分析 | 10-30秒 | DeepSeek API |
| 生成报告 | 1-2秒 | Markdown |
| **总计** | **15-30分钟** | 完整流程 |

---

## 🎯 下一步

安装和测试完成后，你可以：

1. **查看快速开始指南**: [QUICK_START.md](QUICK_START.md)
2. **阅读详细文档**: [DISCOVERY_ENGINE_GUIDE.md](DISCOVERY_ENGINE_GUIDE.md)
3. **了解新功能**: [NEW_FEATURE_DISCOVERY_ENGINE.md](NEW_FEATURE_DISCOVERY_ENGINE.md)
4. **查看项目总结**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

---

## 📞 技术支持

如果遇到问题：

1. **查看日志**: 程序会输出详细的执行日志
2. **运行测试**: `python3 test_discovery_engine.py`
3. **检查配置**: 确认 `config.py` 正确
4. **查看文档**: 阅读相关指南文档

---

## ⚖️ 免责声明

本工具仅供学习和研究使用，请遵守相关平台的服务条款。

---

**版本**: v1.0  
**更新日期**: 2026-01-15  
**状态**: ✅ 已完成

---

🎉 **安装完成！开始你的全网热点发现之旅！**

```bash
./run_discovery.sh
```
