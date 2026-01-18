# 微博黄金情绪自动分析系统 - 使用指南

## 📋 系统简介

这是一个自动化的微博情绪分析系统，每天抓取微博上关于"黄金"的讨论，并使用AI分析社交媒体的情绪温度。

### 核心功能

1. **自动抓取**: 使用Playwright模拟真实浏览器访问微博
2. **智能清洗**: 自动过滤营销广告和低质量内容
3. **AI分析**: 使用DeepSeek AI分析情绪指数和市场观点
4. **报告生成**: 自动生成Markdown格式的每日分析报告

---

## 🚀 快速开始

### 步骤1: 安装依赖

```bash
# 安装Python包
pip install -r requirements_weibo.txt

# 安装Playwright浏览器
playwright install chromium
```

### 步骤2: 配置API Key

你的DeepSeek API Key已经配置在 `config.py` 中，无需额外设置。

### 步骤3: 运行分析

```bash
python3 weibo_gold_sentiment.py
```

---

## 📖 详细说明

### 运行流程

```
1. 启动浏览器
   ↓
2. 访问微博搜索"黄金"
   ↓
3. 扫码登录（首次需要）
   ↓
4. 抓取3-5页数据
   ↓
5. 数据清洗（去广告、去重）
   ↓
6. DeepSeek AI分析
   ↓
7. 生成Markdown报告
```

### 首次使用

第一次运行时，浏览器会打开微博登录页面：

1. **扫码登录**: 使用微博APP扫描二维码
2. **或账号登录**: 输入账号密码
3. **登录完成**: 按回车键继续

登录后，浏览器会保存cookie，下次运行可能不需要重新登录。

---

## ⚙️ 参数配置

### 修改抓取页数

```python
# 在 weibo_gold_sentiment.py 的 main() 函数中修改
analyzer.run(
    pages=5,        # 改为5页
    headless=False  # False显示浏览器，True后台运行
)
```

### 修改关键词

```python
# 在 scrape_weibo_gold() 方法中修改
weibo_search_url = "https://s.weibo.com/weibo?q=白银"  # 改为搜索"白银"
```

### 修改反爬延时

```python
# 在代码中查找 random.uniform() 并调整范围
wait_time = random.uniform(5, 10)  # 增加等待时间
```

---

## 📊 输出文件

### 1. 原始数据 (CSV)

`weibo_raw_YYYYMMDD_HHMMSS.csv`

包含字段：
- 博主名
- 博文内容
- 发布时间
- 点赞数
- 转发数

### 2. 清洗数据 (CSV)

`weibo_clean_YYYYMMDD_HHMMSS.csv`

过滤后的高质量数据

### 3. 分析报告 (Markdown)

`微博黄金情绪分析_YYYYMMDD.md`

包含内容：
- 数据概况
- AI情绪指数（0-100）
- 用户担心的3个风险点
- 用户期待的3个机会点
- 热门微博TOP 10

---

## 📈 报告示例

```markdown
# 微博黄金情绪分析报告

**生成时间**: 2026年01月14日 16:30:00

---

## 📊 数据概况

- **抓取微博数**: 127 条
- **平均点赞数**: 45
- **平均转发数**: 12
- **最高点赞**: 2341

## 🤖 AI情绪分析

### 黄金看涨情绪指数

**72 / 100** - 乐观

🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜⬜⬜⬜⬜⬜
0    20   40   60   80   100

**今日情绪**: 市场对黄金保持乐观态度，避险需求上升

### ⚠️  用户最担心的3个风险点

1. 美联储加息预期可能压制金价
2. 美元走强对黄金形成压力
3. 短期技术面出现超买信号

### 💡 用户最期待的3个机会点

1. 地缘政治风险推升避险需求
2. 央行持续购金支撑长期走势
3. 通胀预期回升利好黄金配置

## 🔥 热门微博 TOP 10

### 1. @财经观察员

> 黄金突破2100美元，创历史新高！避险情绪持续升温...

- 👍 点赞: 2341 | 🔄 转发: 567 | 📅 2小时前
```

---

## 🛡️ 反爬策略

系统内置多重反爬措施：

### 1. 随机延时

```python
# 页面跳转后等待3-7秒
wait_time = random.uniform(3, 7)
time.sleep(wait_time)

# 滚动加载等待1-2秒
time.sleep(random.uniform(1, 2))

# 翻页等待4-8秒
wait_time = random.uniform(4, 8)
time.sleep(wait_time)
```

### 2. 真实浏览器

- 使用Playwright模拟真实Chrome浏览器
- 完整的JavaScript执行环境
- 真实的User-Agent

### 3. 人工登录

- 支持扫码登录
- 保存登录状态
- 避免频繁登录触发风控

### 4. 适度抓取

- 默认只抓取3页数据
- 每日运行一次
- 不追求速度，稳定第一

---

## 🔧 故障排查

### 问题1: Playwright安装失败

```bash
# 解决方案
pip install playwright
playwright install chromium
```

### 问题2: 浏览器无法启动

```bash
# macOS可能需要安装依赖
brew install chromium

# Linux可能需要安装依赖
sudo apt-get install -y \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2
```

### 问题3: 登录失败

- 确保网络连接正常
- 尝试手动访问 weibo.com 确认可以访问
- 检查是否被微博限制（更换网络或等待）

### 问题4: 抓取不到数据

- 微博页面结构可能变化，需要更新选择器
- 检查是否需要重新登录
- 尝试增加等待时间

### 问题5: AI分析失败

- 检查API Key是否有效
- 确认网络可以访问DeepSeek API
- 查看是否超出API配额

---

## 💡 使用技巧

### 1. 定时运行

**macOS/Linux (crontab)**

```bash
# 编辑crontab
crontab -e

# 每天早上9点运行
0 9 * * * cd /path/to/project && python3 weibo_gold_sentiment.py >> logs/weibo.log 2>&1
```

**Windows (任务计划程序)**

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置每天9:00触发
4. 操作选择运行Python脚本

### 2. 后台运行

```python
# 修改为无头模式（不显示浏览器）
analyzer.run(pages=3, headless=True)
```

注意：首次运行建议使用 `headless=False` 完成登录。

### 3. 批量分析

```python
# 分析多个关键词
keywords = ['黄金', '白银', '原油']

for keyword in keywords:
    # 修改搜索URL
    # 运行分析
    pass
```

### 4. 数据积累

建议每天保存数据，积累一段时间后可以：
- 分析情绪趋势
- 对比历史数据
- 建立预测模型

---

## 📊 数据分析建议

### 情绪指数解读

| 指数范围 | 情绪标签 | 投资建议 |
|---------|---------|---------|
| 0-20 | 极度悲观 | 可能是抄底机会 |
| 21-40 | 悲观 | 谨慎观望 |
| 41-60 | 中性 | 等待明确信号 |
| 61-80 | 乐观 | 可适度参与 |
| 81-100 | 极度乐观 | 警惕过热风险 |

### 结合其他指标

建议将微博情绪与以下指标结合：
- 黄金现货价格
- 美元指数
- 美债收益率
- 地缘政治事件
- 央行购金数据

### 反向指标

当微博情绪极度乐观（>85）时，可能是：
- 市场过热信号
- 散户追高
- 短期调整风险

---

## ⚠️  注意事项

### 1. 合规使用

- 仅用于个人研究
- 不用于商业目的
- 遵守微博使用条款
- 不进行高频抓取

### 2. 数据局限性

- 微博用户不代表全部投资者
- 社交媒体情绪波动大
- 需要结合其他信息源
- AI分析仅供参考

### 3. 隐私保护

- 不保存用户个人信息
- 只分析公开内容
- 不传播敏感信息

### 4. 技术限制

- 依赖微博页面结构
- 页面变化需要更新代码
- 登录状态可能失效
- API可能有调用限制

---

## 🔄 更新日志

### v1.0 (2026-01-14)

- ✅ 初始版本
- ✅ Playwright抓取
- ✅ 数据清洗
- ✅ DeepSeek AI分析
- ✅ Markdown报告生成

---

## 📞 技术支持

如有问题，请检查：

1. Python版本 >= 3.8
2. 依赖包已正确安装
3. Playwright浏览器已安装
4. API Key配置正确
5. 网络连接正常

---

## 📚 相关文档

- [Playwright文档](https://playwright.dev/python/)
- [DeepSeek API文档](https://platform.deepseek.com/docs)
- [Pandas文档](https://pandas.pydata.org/)

---

**版本**: v1.0  
**更新日期**: 2026-01-14  
**许可证**: MIT License

**免责声明**: 本系统仅供学习研究使用，不构成投资建议。使用者需自行承担风险。