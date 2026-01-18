# 微博黄金情绪自动分析系统 - 完成总结

## ✅ 系统完成

我已经按照你的要求创建了一个完整的微博黄金情绪自动分析系统。

---

## 📁 文件清单

### 核心文件

1. **weibo_gold_sentiment.py** - 主程序（包含详细中文注释）
2. **test_weibo_system.py** - 测试脚本（使用模拟数据）
3. **requirements_weibo.txt** - 依赖包列表
4. **setup_weibo.sh** - 自动安装脚本
5. **WEIBO_SENTIMENT_GUIDE.md** - 详细使用指南
6. **WEIBO_SYSTEM_SUMMARY.md** - 本文档

### 配置文件

- **config.py** - 已包含你的DeepSeek API Key

---

## 🎯 功能实现

### 1. 采集模块 (Playwright) ✅

- ✅ 使用Playwright启动Chromium浏览器
- ✅ 支持 `headless=False` 方便扫码登录
- ✅ 自动导航到微博搜索"黄金"
- ✅ 模拟滚动加载3-5页数据
- ✅ 反爬策略：`random.sleep(3, 7)` 随机等待
- ✅ 提取字段：博主名、博文内容、发布时间、点赞数、转发数

### 2. 数据预处理 (Pandas) ✅

- ✅ 存入Pandas DataFrame
- ✅ 清洗逻辑：剔除"抽奖"、"转运珠"、"代购"等营销广告
- ✅ 去重：根据博文内容去重

### 3. AI分析模块 (DeepSeek) ✅

- ✅ 合并清洗后的博文内容
- ✅ 发送给DeepSeek API
- ✅ AI指令：行为金融学专家分析
- ✅ 输出：0-100的黄金看涨情绪指数
- ✅ 总结：最担心的3个风险点
- ✅ 总结：最期待的3个机会点

### 4. 运行与输出 ✅

- ✅ 保存为Markdown格式
- ✅ 文件名以日期命名
- ✅ 详细的中文注释

---

## 🚀 快速开始

### 方法1: 自动安装（推荐）

```bash
# 运行安装脚本
./setup_weibo.sh

# 测试系统（使用模拟数据）
python3 test_weibo_system.py

# 运行真实分析
python3 weibo_gold_sentiment.py
```

### 方法2: 手动安装

```bash
# 1. 安装Python依赖
pip3 install -r requirements_weibo.txt

# 2. 安装Playwright浏览器
playwright install chromium

# 3. 运行测试
python3 test_weibo_system.py

# 4. 运行真实分析
python3 weibo_gold_sentiment.py
```

---

## 📊 使用流程

### 首次运行

```bash
python3 weibo_gold_sentiment.py
```

1. 浏览器会自动打开
2. 显示微博登录页面
3. 使用微博APP扫码登录
4. 登录完成后按回车
5. 系统自动抓取和分析
6. 生成Markdown报告

### 日常运行

登录状态会保存，后续运行可能不需要重新登录。

---

## 📄 输出示例

### 生成的文件

```
微博黄金情绪分析_20260114.md
weibo_raw_20260114_160000.csv
weibo_clean_20260114_160000.csv
```

### 报告内容

```markdown
# 微博黄金情绪分析报告

**生成时间**: 2026年01月14日 16:00:00

---

## 📊 数据概况

- **抓取微博数**: 127 条
- **平均点赞数**: 45
- **平均转发数**: 12

## 🤖 AI情绪分析

### 黄金看涨情绪指数

**72 / 100** - 乐观

🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩⬜⬜⬜⬜⬜⬜

**今日情绪**: 市场对黄金保持乐观态度

### ⚠️  用户最担心的3个风险点

1. 美联储加息预期可能压制金价
2. 美元走强对黄金形成压力
3. 短期技术面出现超买信号

### 💡 用户最期待的3个机会点

1. 地缘政治风险推升避险需求
2. 央行持续购金支撑长期走势
3. 通胀预期回升利好黄金配置

## 🔥 热门微博 TOP 10

...
```

---

## 🛡️ 反爬策略

系统内置多重反爬措施，确保稳定性：

### 1. 随机延时

```python
# 页面跳转: 3-7秒
wait_time = random.uniform(3, 7)

# 滚动加载: 1-2秒
time.sleep(random.uniform(1, 2))

# 翻页: 4-8秒
wait_time = random.uniform(4, 8)
```

### 2. 真实浏览器

- Playwright模拟真实Chrome
- 完整JavaScript环境
- 真实User-Agent

### 3. 人工登录

- 支持扫码登录
- 保存登录状态
- 避免频繁登录

### 4. 适度抓取

- 默认3页数据
- 每日运行一次
- 稳定性优先

---

## 💡 代码注释示例

所有代码都包含详细的中文注释：

```python
def scrape_weibo_gold(self, pages=3, headless=False):
    """
    使用Playwright抓取微博黄金相关内容
    
    参数:
        pages: 抓取页数（默认3页）
        headless: 是否无头模式（False方便扫码登录）
        
    返回:
        DataFrame: 包含微博数据
    """
    print("开始抓取微博黄金相关内容")
    
    # 启动浏览器（headless=False方便扫码登录）
    browser = p.chromium.launch(headless=headless)
    
    # 创建浏览器上下文（模拟真实用户）
    context = browser.new_context(...)
    
    # ... 更多注释
```

---

## 🔧 自定义配置

### 修改抓取页数

```python
# 在 main() 函数中
analyzer.run(pages=5, headless=False)  # 改为5页
```

### 修改搜索关键词

```python
# 在 scrape_weibo_gold() 方法中
weibo_search_url = "https://s.weibo.com/weibo?q=白银"
```

### 修改反爬延时

```python
# 增加等待时间
wait_time = random.uniform(5, 10)  # 改为5-10秒
```

### 修改AI提示词

```python
# 在 __init__() 方法中修改 self.system_prompt
```

---

## 📅 定时运行

### macOS/Linux

```bash
# 编辑crontab
crontab -e

# 每天早上9点运行
0 9 * * * cd /path/to/project && python3 weibo_gold_sentiment.py >> logs/weibo.log 2>&1
```

### Windows

使用"任务计划程序"设置每天定时运行。

---

## ⚠️  注意事项

### 1. 首次使用

- 需要手动登录微博（扫码或账号密码）
- 建议使用 `headless=False` 查看浏览器
- 登录后状态会保存

### 2. 稳定性优先

- 不追求速度，每日运行一次即可
- 随机延时避免被识别为爬虫
- 适度抓取，默认3页数据

### 3. 数据质量

- 自动过滤营销广告
- 去除重复内容
- 只分析高质量微博

### 4. 合规使用

- 仅用于个人研究
- 不用于商业目的
- 遵守微博使用条款

---

## 🔍 故障排查

### 问题1: Playwright安装失败

```bash
pip install playwright
playwright install chromium
```

### 问题2: 浏览器无法启动

检查系统依赖，参考 `WEIBO_SENTIMENT_GUIDE.md`

### 问题3: 登录失败

- 检查网络连接
- 尝试手动访问 weibo.com
- 更换网络或等待

### 问题4: 抓取不到数据

- 微博页面可能变化
- 检查是否需要重新登录
- 增加等待时间

### 问题5: AI分析失败

- 检查API Key
- 确认网络可访问DeepSeek
- 查看API配额

---

## 📈 数据分析建议

### 情绪指数解读

| 指数 | 标签 | 建议 |
|-----|------|------|
| 0-20 | 极度悲观 | 可能是抄底机会 |
| 21-40 | 悲观 | 谨慎观望 |
| 41-60 | 中性 | 等待信号 |
| 61-80 | 乐观 | 可适度参与 |
| 81-100 | 极度乐观 | 警惕过热 |

### 结合其他指标

- 黄金现货价格
- 美元指数
- 美债收益率
- 地缘政治事件

---

## 🎓 技术栈

- **Playwright**: 浏览器自动化
- **Pandas**: 数据处理
- **DeepSeek AI**: 情绪分析
- **Python 3.8+**: 编程语言

---

## 📚 相关文档

1. **WEIBO_SENTIMENT_GUIDE.md** - 详细使用指南
2. **weibo_gold_sentiment.py** - 主程序（含注释）
3. **test_weibo_system.py** - 测试脚本

---

## ✅ 完成清单

- [x] Playwright采集模块
- [x] 反爬策略（随机延时）
- [x] 数据清洗（去广告、去重）
- [x] DeepSeek AI分析
- [x] 情绪指数（0-100）
- [x] 风险点和机会点提取
- [x] Markdown报告生成
- [x] 详细中文注释
- [x] 测试脚本
- [x] 安装脚本
- [x] 使用文档

---

## 🎉 总结

系统已完全按照你的要求实现：

1. ✅ **稳定性第一**: 随机延时、真实浏览器、适度抓取
2. ✅ **反爬避让**: 多重策略确保不被识别
3. ✅ **数据质量**: 自动清洗、去重、过滤广告
4. ✅ **AI分析**: DeepSeek专业分析，输出结构化结果
5. ✅ **易于使用**: 详细注释、测试脚本、自动安装
6. ✅ **每日运行**: 支持定时任务，自动生成报告

现在你可以：
1. 运行测试：`python3 test_weibo_system.py`
2. 运行真实分析：`python3 weibo_gold_sentiment.py`
3. 查看文档：`cat WEIBO_SENTIMENT_GUIDE.md`

---

**版本**: v1.0  
**完成日期**: 2026-01-14  
**状态**: ✅ 已完成并测试