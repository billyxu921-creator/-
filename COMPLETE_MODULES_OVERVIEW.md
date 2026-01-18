# 📊 系统所有模块详细说明

## 目录
1. [黄金股票筛选器](#1-黄金股票筛选器)
2. [AI量化选股器](#2-ai量化选股器)
3. [微博情绪分析](#3-微博情绪分析)
4. [全网热点发现引擎](#4-全网热点发现引擎)
5. [政客交易追踪](#5-政客交易追踪)
6. [每日自动推送系统](#6-每日自动推送系统)

---

## 1. 黄金股票筛选器 🏆

### 📁 文件
- **主文件**: `gold_stock_screener.py`
- **文档**: `README.md`（包含说明）

### 🎯 功能目标
从全A股中筛选出符合特定条件的黄金概念股，识别具有投资价值的标的。

### 📊 筛选条件

#### 硬性指标
1. **总股本**: 8亿 ≤ 总股本 ≤ 15亿股
2. **流通市值**: 105亿 ≤ 流通市值 ≤ 195亿元（目标150亿±30%）
3. **行业关键词**: 包含"黄金"、"矿产"、"贵金属"等

#### 软性指标
1. **官方背书**: 检测十大股东中是否有：
   - 社保基金
   - 国资委
   - 中央汇金
   - 证金公司
   
2. **市值匹配度**: 越接近150亿越好

### 🏆 评分系统（总分100分）

| 维度 | 分数 | 说明 |
|------|------|------|
| 股本匹配 | 25分 | 8-12亿股得25分，12-15亿股得20分 |
| 官方背书 | 30分 | 包含官方资本得30分 |
| 市值匹配 | 20分 | 越接近150亿分数越高 |
| 行业匹配 | 25分 | 黄金行业相关度 |

### 📈 输出结果

**CSV文件**: `gold_stocks_analysis_YYYYMMDD_HHMMSS.csv`

包含字段：
- 股票代码、股票名称
- 总股本（亿股）
- 流通市值（亿元）
- 股本匹配分、官方背书分、市值匹配分、行业匹配分
- 综合评分
- 是否有官方背书

**示例输出**:
```
排名  股票名称    股票代码  综合评分  流通市值
1    山东黄金    600547    85.0     145.2亿
2    中金黄金    600489    82.5     138.6亿
3    赤峰黄金    600988    80.0     152.3亿
```

### 🔧 使用方法

```bash
# 直接运行
python3 gold_stock_screener.py

# 在代码中使用
from gold_stock_screener import GoldStockScreener
screener = GoldStockScreener()
results = screener.screen_stocks()
```

### 💡 核心逻辑

```python
# 1. 获取全A股数据
stocks = ak.stock_zh_a_spot_em()

# 2. 筛选条件
filtered = stocks[
    (stocks['总股本'] >= 8亿) & 
    (stocks['总股本'] <= 15亿) &
    (stocks['流通市值'] >= 105亿) &
    (stocks['流通市值'] <= 195亿)
]

# 3. 计算评分
score = (
    股本匹配分 * 0.25 +
    官方背书分 * 0.30 +
    市值匹配分 * 0.20 +
    行业匹配分 * 0.25
)

# 4. 排序输出
results.sort_values('综合评分', ascending=False)
```

### ⏱️ 运行时间
约2-3分钟

### 📊 数据来源
AkShare - `ak.stock_zh_a_spot_em()`

---

## 2. AI量化选股器 🤖

### 📁 文件
- **主文件**: `Quant_Picker.py`
- **测试**: `test_quant_picker.py`
- **文档**: `QUANT_PICKER_GUIDE.md`, `QUANT_PICKER_README.md`

### 🎯 功能目标
结合技术指标、舆情热度、AI分析，从全A股中挑选出最具潜力的3只股票。

### 🔄 四步流程

#### Step 1: AkShare指标初选

**筛选条件**:
- 60亿 < 市值 < 200亿
- 2% < 涨幅 < 6%
- 换手率 > 5%

**目的**: 筛选出中小盘、有热度、有涨幅的股票

#### Step 2: 舆情碰撞

**数据源**:
- 微博热点数据
- 小红书热点数据

**匹配逻辑**:
- 将股票名称与舆情数据匹配
- 百万粉丝博主提及 → 权重×10
- 包含"重组"、"利好"等关键词 → 高优先级

**舆情评分公式**:
```
舆情评分 = (基础分50 + 关键词加分) × 影响力权重
归一化到0-100
```

#### Step 3: 综合评分

**评分公式**:
```
综合得分 = 涨幅×30% + 换手率×20% + 舆情评分×50%
```

**排序**: 按综合得分降序，取TOP 10

#### Step 4: DeepSeek终极筛选

**输入**: TOP 10股票的[名称、涨跌幅、最新新闻摘要]

**Prompt**:
```
你是一位资深基金经理，请从这10只票中选出3只今日最具潜力的股票。
要求：
1. 给出推荐理由（必须包含技术面和舆情面的结合点）
2. 预测一个短期止盈位
```

**输出**: TOP 3潜力股 + 推荐理由 + 止盈位

### 📈 输出结果

**Markdown报告**: `AI潜力股推荐_YYYYMMDD_HHMMSS.md`

**CSV数据**: `quant_picker_candidates_YYYYMMDD_HHMMSS.csv`

**报告结构**:
```markdown
# 🚀 AI潜力股推荐

## 📊 筛选概览
- 初选股票数: 50只
- 舆情匹配: 15只
- TOP 10候选: 10只
- 最终推荐: 3只

## 🎯 TOP 3 推荐

### 1. 某某股份 (600XXX)

**技术面**:
- 当前价格: 25.60元
- 涨跌幅: +3.5%
- 换手率: 8.2%
- 市值: 120亿

**舆情面**:
- 舆情评分: 85/100
- 热度来源: 微博财经大V提及
- 关键词: 重组、业绩拐点

**AI推荐理由**:
技术面显示资金持续流入，舆情面显示市场关注度激增，
两者共振，短期有望继续上涨。

**止盈位**: 27.50元 (+7.4%)

**风险提示**: 注意大盘波动影响
```

### 🔧 使用方法

```bash
# 直接运行
python3 Quant_Picker.py

# 测试
python3 test_quant_picker.py
```

### 💡 核心算法

**舆情加权**:
```python
# 博主影响力权重
if followers >= 1000000:
    weight = 10
elif followers >= 100000:
    weight = 3
else:
    weight = 1

# 关键词加成
keywords = ['涨停', '重组', '入股', '利好']
if any(k in text for k in keywords):
    bonus = 20  # 20%加成

# 最终评分
sentiment_score = (base_score + bonus) * weight
normalized_score = min(sentiment_score / 12, 100)  # 归一化
```

**综合评分**:
```python
final_score = (
    change_pct * 0.30 +      # 涨幅权重30%
    turnover_rate * 0.20 +   # 换手率权重20%
    sentiment_score * 0.50   # 舆情权重50%
)
```

### ⏱️ 运行时间
约5-8分钟

### 📊 数据来源
- AkShare: 实时行情
- 微博/小红书: 舆情数据
- DeepSeek API: AI分析

---

## 3. 微博情绪分析 📱

### 📁 文件
- **主文件**: `weibo_sentiment_weighted.py`（加权版）
- **基础版**: `weibo_gold_sentiment.py`
- **测试**: `test_weighted_sentiment.py`
- **文档**: `WEIGHTED_SENTIMENT_GUIDE.md`, `WEIBO_SENTIMENT_GUIDE.md`

### 🎯 功能目标
抓取微博上关于"黄金"的讨论，通过博主影响力加权和关键词加成，
生成0-100的情绪指数，识别市场情绪和投资机会。

### 🔄 五步流程

#### Step 1: 数据抓取

**工具**: Playwright（真实浏览器）

**目标页面**: 微博搜索"黄金"

**抓取字段**:
- 博主昵称
- 粉丝数（followers_count）
- 微博内容
- 发布时间
- 点赞数、评论数、转发数

**反爬策略**:
- headless=False（支持扫码登录）
- 随机等待3-7秒
- 真实User-Agent
- 人工登录

#### Step 2: 数据清洗

**过滤规则**:
1. 过滤广告：包含"抽奖"、"转运珠"、"代购"
2. 去重：相同内容只保留一条
3. 长度过滤：内容长度>10字

**清洗后数据**: `weibo_clean_test_YYYYMMDD_HHMMSS.csv`

#### Step 3: 影响力加权

**粉丝数权重**:
```python
if followers >= 1000000:    # 100万+
    weight = 10
elif followers >= 100000:   # 10万+
    weight = 3
else:
    weight = 1
```

**示例**:
- 普通用户（5000粉丝）: 权重×1
- 财经博主（50万粉丝）: 权重×3
- 顶级大V（200万粉丝）: 权重×10

#### Step 4: 关键词加成

**关键词列表**:
- 涨停、重组、入股
- 利好、突破、暴涨
- 政策、拨款、项目

**加成规则**:
```python
if any(keyword in text for keyword in keywords):
    bonus = 20  # 给予20%加成
```

**加权公式**:
```
Final_Score = (AI_Sentiment_Score + Keyword_Bonus) × Influence_Weight
```

#### Step 5: DeepSeek AI分析

**输入**: 清洗后的微博内容

**分析维度**:
1. **情绪量化**: 0-100分
   - 0-30: 极度悲观
   - 30-50: 偏悲观
   - 50-70: 中性偏乐观
   - 70-100: 极度乐观

2. **风险点**: 提取3个主要风险
3. **机会点**: 提取3个投资机会

**归一化**:
```python
# 最大可能值: (100 + 20) × 10 = 1200
normalized_score = (weighted_score / 1200) * 100
```

### 📈 输出结果

**Markdown报告**: `微博黄金情绪分析_YYYYMMDD.md`

**报告结构**:
```markdown
# 📱 微博黄金情绪分析

## 📊 情绪指数: 72/100

**情绪判断**: 偏乐观

## 📈 数据概览
- 抓取微博数: 50条
- 有效数据: 38条
- 平均粉丝数: 15.2万
- 百万粉丝博主: 3位

## 🔥 高影响力博主 TOP 5
1. 财经大V张三 (200万粉丝) - 权重×10
2. 黄金分析师李四 (80万粉丝) - 权重×3
...

## ⚠️ 3个风险点
1. 美联储加息预期升温
2. 美元指数走强
3. 技术面短期超买

## 💡 3个机会点
1. 地缘政治不确定性增加
2. 央行持续购金
3. 通胀预期回升

## 📊 影响力分布
- 百万粉丝: 3位 (权重×10)
- 十万粉丝: 12位 (权重×3)
- 其他: 23位 (权重×1)

## 🔑 关键词统计
- "利好": 8次
- "突破": 5次
- "政策": 3次
```

### 🔧 使用方法

```bash
# 运行加权版
python3 weibo_sentiment_weighted.py

# 测试
python3 test_weighted_sentiment.py
```

### 💡 核心算法

**加权计算**:
```python
total_weighted_score = 0
total_weight = 0

for post in posts:
    # 1. 获取AI情绪分数
    ai_score = deepseek_analyze(post['content'])
    
    # 2. 关键词加成
    bonus = 20 if has_keywords(post['content']) else 0
    
    # 3. 影响力权重
    weight = get_weight(post['followers'])
    
    # 4. 加权累加
    weighted_score = (ai_score + bonus) * weight
    total_weighted_score += weighted_score
    total_weight += weight

# 5. 归一化
final_score = (total_weighted_score / (total_weight * 120)) * 100
```

### ⏱️ 运行时间
约5-10分钟（取决于网络和登录）

### 📊 数据来源
- 微博搜索页面
- DeepSeek API

### ⚠️ 注意事项
- 首次运行需要扫码登录
- 需要稳定的网络连接
- 建议headless=False方便登录

---

## 4. 全网热点发现引擎 🔍

### 📁 文件
- **主文件**: `Discovery_Engine.py`
- **测试**: `test_discovery_engine.py`
- **文档**: `DISCOVERY_ENGINE_GUIDE.md`, `DISCOVERY_ENGINE_README.md`

### 🎯 功能目标
自动识别小红书和微博上讨论度异常升高的股票板块，
发现你可能错过的投资机会。

### 🔄 四步流程

#### Step 1: 多源探测

**数据源1: 小红书财经频道**
- 推荐流前50条内容
- 提取财经相关帖子
- 记录讨论的板块和股票

**数据源2: 微博财经热搜**
- 财经热搜榜TOP 50
- 股票超话讨论
- 财经大V推荐

**数据源3: 股票超话**
- 各板块超话热度
- 讨论量统计

**反爬策略**:
- headless=False（支持扫码登录）
- 随机等待5.5-12.2秒
- 拟人滚动（模拟真实浏览）
- 真实User-Agent
- 验证码蜂鸣提示

#### Step 2: 关键词提取

**扩展关键词库（49个）**:

**基础板块（10个）**:
- 新能源、芯片、医药、军工、消费
- 地产、金融、周期、科技、农业

**行业板块（39个）**:
- 肥料板块: 肥料、化肥、磷肥、钾肥、氮肥
- 战争/军工: 战争、军工、国防、武器、军事
- 卫星/航天: 卫星、航天、火箭、太空、北斗
- 脑机接口: 脑机接口、脑机、神经、马斯克、Neuralink
- ... 等

**提取逻辑**:
```python
# 今日词频统计
today_keywords = {}
for post in today_posts:
    for keyword in all_keywords:
        if keyword in post:
            today_keywords[keyword] += 1

# 昨日词频统计（从历史文件读取）
yesterday_keywords = load_history()
```

#### Step 3: 对比分析

**动量计算**:
```python
momentum = {}
for keyword in today_keywords:
    today_count = today_keywords[keyword]
    yesterday_count = yesterday_keywords.get(keyword, 0)
    
    # 计算增长率
    if yesterday_count > 0:
        growth_rate = (today_count - yesterday_count) / yesterday_count
    else:
        growth_rate = float('inf') if today_count > 0 else 0
    
    momentum[keyword] = {
        'today': today_count,
        'yesterday': yesterday_count,
        'growth': growth_rate
    }
```

**排序**: 按增长率降序

**过滤**: 排除预设的10个基础板块，只保留新发现的板块

#### Step 4: AI智能识别

**输入**: 动量最大的前10个关键词

**DeepSeek分析**:
```
请从以下热度异常升高的关键词中，识别出3个最值得关注的投资板块。

关键词及热度变化:
1. 脑机接口: 今日50次，昨日5次，增长900%
2. 卫星: 今日35次，昨日8次，增长337%
...

要求:
1. 选出3个最具投资价值的板块
2. 说明为什么热度突然升高
3. 给出投资建议和风险提示
```

**输出**: TOP 3热点板块 + 分析 + 建议

### 📈 输出结果

**Markdown报告**: `全网雷达_YYYYMMDD_HHMMSS.md`

**历史数据**: `discovery_history/keywords_YYYYMMDD.json`

**报告结构**:
```markdown
# 🔍 全网雷达：你可能错过的热门机会

## 📊 本期发现

**监测时间**: 2026年1月15日
**数据来源**: 小红书 + 微博
**监测帖子**: 150条

## 🔥 异常升温板块 TOP 3

### 1. 脑机接口板块 🧠

**热度变化**:
- 今日讨论: 50次
- 昨日讨论: 5次
- 增长率: +900%

**升温原因**:
马斯克Neuralink公司宣布人体试验取得突破，
引发市场对脑机接口技术的关注。

**相关股票**:
- 创新医疗 (002173)
- 世纪华通 (002602)
- 三博脑科 (301293)

**投资建议**:
短期炒作为主，关注政策催化和技术突破。
建议轻仓参与，设置止损。

**风险提示**:
技术商业化尚需时日，警惕概念炒作。

---

### 2. 卫星互联网板块 🛰️

**热度变化**:
- 今日讨论: 35次
- 昨日讨论: 8次
- 增长率: +337%

**升温原因**:
国家发改委发布卫星互联网建设规划，
多家公司获得项目订单。

**相关股票**:
- 中国卫星 (600118)
- 航天电子 (600879)
- 华力创通 (300045)

**投资建议**:
政策驱动明确，可中长期关注。
建议分批建仓，关注订单落地情况。

**风险提示**:
行业竞争激烈，关注公司基本面。

---

### 3. 肥料板块 🌾

**热度变化**:
- 今日讨论: 28次
- 昨日讨论: 6次
- 增长率: +366%

**升温原因**:
春耕临近，化肥价格上涨，
叠加粮食安全政策支持。

**相关股票**:
- 云天化 (600096)
- 新洋丰 (000902)
- 史丹利 (002588)

**投资建议**:
季节性机会，关注价格走势。
建议短期波段操作。

**风险提示**:
原材料价格波动，关注成本变化。
```

### 🔧 使用方法

```bash
# 直接运行
python3 Discovery_Engine.py

# 测试
python3 test_discovery_engine.py
```

### 💡 核心算法

**异常检测**:
```python
def detect_anomaly(today, yesterday):
    """检测异常升温"""
    if yesterday == 0:
        return today > 5  # 新出现且热度>5
    
    growth_rate = (today - yesterday) / yesterday
    return growth_rate > 2.0  # 增长率>200%
```

**智能过滤**:
```python
# 排除预设板块
preset_sectors = ['新能源', '芯片', '医药', ...]
new_discoveries = [
    k for k in hot_keywords 
    if k not in preset_sectors
]
```

### ⏱️ 运行时间
约10-15分钟

### 📊 数据来源
- 小红书财经频道
- 微博财经热搜
- 股票超话

### ⚠️ 注意事项
- 需要扫码登录小红书和微博
- 首次运行会创建历史数据文件
- 建议每天运行，积累历史数据

---

## 5. 政客交易追踪 🏛️

### 📁 文件
- **主文件**: `politician_trade_tracker.py`
- **测试**: `test_politician_tracker.py`
- **集成**: `run_with_politician_tracker.py`
- **文档**: `POLITICIAN_TRACKER_GUIDE.md`, `POLITICIAN_TRACKER_INTEGRATION.md`

### 🎯 功能目标
追踪美国国会议员的股票交易，识别高置信度投资信号，
发现可能的政策动向和投资机会。

### 🔄 五步流程

#### Step 1: 数据获取

**数据源1: Quiver Quantitative API**
- 专业的政客交易数据平台
- 需要付费订阅（$30-100/月）
- 数据全面、更新及时

**数据源2: Unusual Whales**
- 网页爬取
- 需要登录
- 免费但可能有反爬

**获取字段**:
- 议员姓名（politician）
- 股票代码（ticker）
- 交易类型（Buy/Sell）
- 交易金额区间（amount_range）
- 交易日期（transaction_date）
- 披露日期（disclosure_date）
- 所属委员会（committee）

**示例数据**:
```python
{
    'politician': 'Nancy Pelosi',
    'ticker': 'NVDA',
    'transaction_type': 'Buy',
    'amount_range': '$500,001 - $1,000,000',
    'transaction_date': '2026-01-12',
    'disclosure_date': '2026-01-15',
    'committee': 'Technology'
}
```

#### Step 2: 置信度分析

**评分维度**:

1. **委员会成员（+30分）**
   - 检查是否是重要委员会成员
   - Energy委员会 → 能源股
   - Finance委员会 → 金融股
   - Technology委员会 → 科技股
   - Armed Services委员会 → 军工股

2. **交易金额（+10-40分）**
   - $500,001+: +40分（大额交易）
   - $250,001-$500,000: +25分（中等交易）
   - <$250,000: +10分（小额交易）

3. **交易方向（+5-20分）**
   - Buy: +20分（买入信号更有价值）
   - Sell: +5分（可能是止盈）

4. **披露时效（+5-10分）**
   - ≤3天: +10分（新鲜披露）
   - 4-7天: +5分（近期披露）
   - >7天: 0分（时效性降低）

**高置信度阈值**: ≥70分

**示例分析**:
```
议员: Nancy Pelosi
股票: NVDA
交易: 买入 $500,001 - $1,000,000
委员会: Technology
披露: 3天前

评分:
- 委员会成员: +30分
- 大额交易: +40分
- 买入信号: +20分
- 新鲜披露: +10分
总分: 100分 🔥🔥🔥 极强
```

#### Step 3: 逻辑关联

**委员会与行业匹配**:
```python
committee_industries = {
    'Energy': ['能源', '石油', '天然气', '新能源'],
    'Finance': ['金融', '银行', '保险', '投资'],
    'Technology': ['科技', '互联网', '半导体', 'AI'],
    'Armed Services': ['国防', '军工', '航空航天'],
    'Intelligence': ['网络安全', '情报', '监控']
}
```

**关联检测**:
- 能源委员会成员买入能源股 → 高置信度
- 科技委员会成员买入科技股 → 高置信度
- 普通议员买入无关股票 → 低置信度

#### Step 4: 实时表现匹配

**获取股票实时数据**:
- 当前价格
- 涨跌幅
- 成交量
- 市值

**对比分析**:
- 披露后股价表现
- 是否已经反应
- 是否还有机会

#### Step 5: Twitter讨论分析

**抓取相关推文**:
- 搜索股票代码相关讨论
- 统计讨论热度

**DeepSeek过滤**:

**保留的实词**:
- 政策、法案、拨款、项目
- 考察、调研、合同、订单
- 投资、并购、监管、审批
- 基础设施、补贴、税收

**排除的口水话**:
- "涨了好多啊"
- "买买买"
- "to the moon"
- 大量感叹号

**示例**:
```
原始推文:
1. "NVDA新数据中心订单激增" ✅ 保留
2. "英伟达获得政府项目拨款" ✅ 保留
3. "今天NVDA涨了好多啊！" ❌ 排除
4. "买买买！to the moon!" ❌ 排除
5. "国会通过AI法案，NVDA受益" ✅ 保留

过滤结果: 保留1、2、5
```

### 📈 输出结果

**Markdown报告**: `权力资金动态_YYYYMMDD_HHMMSS.md`

**报告结构**:
```markdown
# 🏛️ 权力资金动态

## 📊 本期概览
- 监控交易数: 15笔
- 高置信度信号: 3个
- 涉及议员: 8位

## 🔥 高置信度信号

### 1. NVDA - Nancy Pelosi

**交易信息**:
- 议员: Nancy Pelosi
- 股票代码: NVDA
- 交易类型: 🟢 买入
- 交易金额: $500,001 - $1,000,000
- 披露时间: 3天前

**置信度分析**:
- 置信度评分: 85/100
- 信号强度: 🔥🔥🔥 极强
- 关键因素: Technology委员会成员, 大额交易, 买入信号, 新鲜披露

**实时表现**:
- 当前价格: $450.25
- 涨跌幅: +2.5%
- 成交量: 15.2M

**社交媒体热度**:
- 相关推文: 156条
- 有价值内容: 12条

**关键话题**:
- NVDA新数据中心订单激增，AI芯片需求强劲
- 英伟达获得政府项目拨款，用于AI基础设施建设
- 国会通过AI法案，NVDA将受益于政策支持

**AI分析建议**:
- 🎯 **强烈关注**: 委员会成员大额买入，建议深入研究

---

## ⚠️ 风险提示
1. 信息滞后: 披露有45天延迟
2. 动机多样: 可能是个人财务规划
3. 独立判断: 仅供参考，不构成投资建议
4. 合规风险: 跟随交易需谨慎
```

### 🔧 使用方法

```bash
# 直接运行
python3 politician_trade_tracker.py

# 测试
python3 test_politician_tracker.py

# 完整集成（包含所有5个模块）
python3 run_with_politician_tracker.py
```

### 💡 核心算法

**置信度计算**:
```python
def analyze_confidence_level(trade):
    score = 0
    reasons = []
    
    # 1. 委员会成员
    if is_committee_member(trade['politician']):
        score += 30
        reasons.append("委员会成员")
    
    # 2. 交易金额
    if trade['amount'] > 500000:
        score += 40
        reasons.append("大额交易")
    elif trade['amount'] > 250000:
        score += 25
        reasons.append("中等交易")
    else:
        score += 10
        reasons.append("小额交易")
    
    # 3. 交易方向
    if trade['type'] == 'Buy':
        score += 20
        reasons.append("买入信号")
    else:
        score += 5
        reasons.append("卖出信号")
    
    # 4. 时效性
    days_ago = (now - trade['disclosure_date']).days
    if days_ago <= 3:
        score += 10
        reasons.append("新鲜披露")
    elif days_ago <= 7:
        score += 5
        reasons.append("近期披露")
    
    return score, reasons
```

### ⏱️ 运行时间
约3-5分钟

### 📊 数据来源
- Quiver Quantitative API
- Unusual Whales
- Twitter API
- AkShare（美股数据）

### ⚠️ 注意事项
- 披露有45天延迟
- 需要Quiver API Key（付费）
- 仅供参考，不构成投资建议
- 注意法律合规风险

---

## 6. 每日自动推送系统 📧

### 📁 文件
- **本地完整版**: `daily_email_sender.py`
- **GitHub简化版**: `github_daily_sender.py`
- **定时调度**: `schedule_daily_report.py`
- **GitHub Actions**: `.github/workflows/daily-report.yml`
- **macOS启动**: `com.stockanalysis.dailyreport.plist`

### 🎯 功能目标
每天早上8点自动运行所有分析模块，生成综合简报，
并通过邮件推送到指定邮箱。

### 🔄 完整流程

#### Step 1: 运行所有分析模块

**本地完整版（5个模块）**:
```
1. 黄金股票筛选 (2-3分钟)
2. AI量化选股 (5-8分钟)
3. 微博情绪分析 (5-10分钟)
4. 全网热点发现 (10-15分钟)
5. 政客交易追踪 (3-5分钟)

总计: 约25-40分钟
```

**GitHub简化版（3个模块）**:
```
1. 黄金股票筛选 (2-3分钟)
2. AI量化选股 (5-8分钟)
3. 政客交易追踪 (3-5分钟)

总计: 约10-15分钟

不包含: 微博、全网热点（需要浏览器登录）
```

#### Step 2: 生成综合简报

**汇总所有模块的结果**:

```markdown
# 📊 每日投资简报

**生成时间**: 2026年1月15日 08:00:00

---

## 1. 黄金股票筛选 TOP 5

| 排名 | 股票名称 | 股票代码 | 综合评分 | 流通市值 |
|------|----------|----------|----------|----------|
| 1 | 山东黄金 | 600547 | 85.0 | 145.2亿 |
| 2 | 中金黄金 | 600489 | 82.5 | 138.6亿 |
| 3 | 赤峰黄金 | 600988 | 80.0 | 152.3亿 |
| 4 | 紫金矿业 | 601899 | 78.5 | 168.9亿 |
| 5 | 湖南黄金 | 002155 | 76.0 | 125.4亿 |

详细数据请查看附件《黄金股票分析数据》

---

## 2. AI量化选股 TOP 3

### 1. 某某股份 (600XXX)
- 当前价格: 25.60元 (+3.5%)
- 舆情评分: 85/100
- AI推荐理由: 技术面+舆情面共振
- 止盈位: 27.50元

### 2. 某某科技 (300XXX)
- 当前价格: 18.20元 (+4.2%)
- 舆情评分: 78/100
- AI推荐理由: 资金持续流入
- 止盈位: 19.80元

### 3. 某某新材 (002XXX)
- 当前价格: 32.10元 (+2.8%)
- 舆情评分: 72/100
- AI推荐理由: 业绩拐点+政策利好
- 止盈位: 34.50元

详细分析请查看附件《AI潜力股推荐》

---

## 3. 微博黄金情绪指数

**情绪指数**: 72/100 (偏乐观)

**3个风险点**:
1. 美联储加息预期升温
2. 美元指数走强
3. 技术面短期超买

**3个机会点**:
1. 地缘政治不确定性增加
2. 央行持续购金
3. 通胀预期回升

详细分析请查看附件《微博黄金情绪分析》

---

## 4. 全网热点雷达

**本期发现 3 个异常升温板块**:

1. **脑机接口板块** (+900%)
   - 马斯克Neuralink突破
   - 相关股票: 创新医疗、世纪华通

2. **卫星互联网板块** (+337%)
   - 国家发改委规划发布
   - 相关股票: 中国卫星、航天电子

3. **肥料板块** (+366%)
   - 春耕临近，价格上涨
   - 相关股票: 云天化、新洋丰

详细分析请查看附件《全网热点雷达》

---

## 5. 🏛️ 权力资金动态

**监控到 3 个高置信度信号**:

1. **NVDA** - Nancy Pelosi (Technology委员会)
   - 买入 $500,001 - $1,000,000
   - 置信度: 85/100 🔥🔥🔥

2. **XOM** - Joe Manchin (Energy委员会)
   - 买入 $250,001 - $500,000
   - 置信度: 75/100 🔥🔥

3. **CRWD** - Mark Warner (Intelligence委员会)
   - 买入 $100,001 - $250,000
   - 置信度: 70/100 🔥

详细分析请查看附件《权力资金动态》

---

## ⚠️ 免责声明

本简报由AI自动生成，仅供参考学习，不构成任何投资建议。
股票投资有风险，入市需谨慎。请根据自身情况理性投资。

---

**数据来源**: AkShare / 微博 / 小红书 / Quiver Quantitative
**分析引擎**: DeepSeek AI
**生成系统**: A股投资分析自动化系统 v1.0.0
```

#### Step 3: 发送邮件

**邮件配置**:
```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.qq.com',
    'smtp_port': 465,
    'sender_email': 'your_email@qq.com',
    'sender_password': 'your_auth_code',  # QQ邮箱授权码
    'receiver_emails': ['receiver@example.com']
}
```

**邮件内容**:
- **主题**: 📊 每日投资简报 - 2026年01月15日
- **正文**: HTML格式，包含简报概览
- **附件**:
  1. 每日投资简报.md（综合简报）
  2. gold_stocks_analysis_YYYYMMDD.csv（黄金股票数据）
  3. AI潜力股推荐_YYYYMMDD.md（量化选股报告）
  4. 微博黄金情绪分析_YYYYMMDD.md（情绪分析）
  5. 全网雷达_YYYYMMDD.md（热点发现）
  6. 权力资金动态_YYYYMMDD.md（政客交易）

### 🔧 三种运行方式

#### 方式1: 本地手动运行

```bash
# 运行完整版（包含所有模块）
python3 daily_email_sender.py

# 或运行集成版（包含政客追踪）
python3 run_with_politician_tracker.py
```

#### 方式2: 本地定时运行

**使用schedule库**:
```bash
# 启动定时任务（每天8点运行）
python3 schedule_daily_report.py
```

**使用macOS launchd**:
```bash
# 复制plist文件
cp com.stockanalysis.dailyreport.plist ~/Library/LaunchAgents/

# 加载任务
launchctl load ~/Library/LaunchAgents/com.stockanalysis.dailyreport.plist

# 查看状态
launchctl list | grep stockanalysis
```

#### 方式3: GitHub Actions自动运行

**配置步骤**:
1. 上传代码到GitHub
2. 配置6个Secrets:
   - DEEPSEEK_API_KEY
   - SMTP_SERVER
   - SMTP_PORT
   - SENDER_EMAIL
   - SENDER_PASSWORD
   - RECEIVER_EMAIL
3. 每天UTC 0:00自动运行（北京时间8:00）

**工作流配置**: `.github/workflows/daily-report.yml`

### 📊 运行对比

| 特性 | 本地完整版 | GitHub Actions |
|------|-----------|---------------|
| 黄金股票筛选 | ✅ | ✅ |
| AI量化选股 | ✅ | ✅ |
| 微博情绪分析 | ✅ | ❌ |
| 全网热点发现 | ✅ | ❌ |
| 政客交易追踪 | ✅ | ✅ |
| 需要浏览器 | 是 | 否 |
| 需要本地运行 | 是 | 否 |
| 完全自动化 | 需要开机 | 完全自动 |
| 成本 | 免费 | 免费 |

### 💡 核心代码

**运行所有模块**:
```python
def run_all_analysis(self):
    modules = [
        ('黄金股票筛选', 'gold_stock_screener.py', 300),
        ('AI量化选股', 'Quant_Picker.py', 600),
        ('微博情绪分析', 'weibo_sentiment_weighted.py', 600),
        ('全网热点发现', 'Discovery_Engine.py', 900),
        ('政客交易追踪', 'politician_trade_tracker.py', 300)
    ]
    
    for name, script, timeout in modules:
        subprocess.run(['python3', script], timeout=timeout)
```

**发送邮件**:
```python
def send_email(self, summary_file):
    msg = MIMEMultipart()
    msg['From'] = self.email_config['sender_email']
    msg['To'] = ', '.join(self.email_config['receiver_emails'])
    msg['Subject'] = f"📊 每日投资简报 - {datetime.now().strftime('%Y年%m月%d日')}"
    
    # 添加正文
    msg.attach(MIMEText(html_body, 'html', 'utf-8'))
    
    # 添加附件
    for file in report_files:
        self._attach_file(msg, file)
    
    # 发送
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg)
```

### ⏱️ 运行时间
- 本地完整版: 25-40分钟
- GitHub Actions: 10-15分钟

### 📧 邮件示例

**收到的邮件**:
```
发件人: 股票分析系统 <your_email@qq.com>
收件人: receiver@example.com
主题: 📊 每日投资简报 - 2026年01月15日

正文:
[HTML格式的简报概览]

附件:
📎 每日投资简报_20260115.md (15KB)
📎 gold_stocks_analysis_20260115.csv (8KB)
📎 AI潜力股推荐_20260115.md (12KB)
📎 微博黄金情绪分析_20260115.md (10KB)
📎 全网雷达_20260115.md (14KB)
📎 权力资金动态_20260115.md (11KB)
```

### ⚠️ 注意事项
- QQ邮箱需要使用授权码（不是密码）
- GitHub Actions不支持需要浏览器的模块
- 建议本地运行完整版，GitHub运行基础版
- 定期检查邮件是否正常接收

---

## 📊 模块对比总览

### 功能对比表

| 模块 | 数据源 | 运行时间 | 需要浏览器 | 需要API | 输出格式 |
|------|--------|---------|-----------|---------|---------|
| 黄金股票筛选 | AkShare | 2-3分钟 | ❌ | ❌ | CSV |
| AI量化选股 | AkShare + 舆情 | 5-8分钟 | ⚠️ | DeepSeek | MD + CSV |
| 微博情绪分析 | 微博 | 5-10分钟 | ✅ | DeepSeek | MD + CSV |
| 全网热点发现 | 微博 + 小红书 | 10-15分钟 | ✅ | DeepSeek | MD + JSON |
| 政客交易追踪 | Quiver/Twitter | 3-5分钟 | ⚠️ | DeepSeek + Quiver | MD |
| 每日推送 | 汇总所有 | 25-40分钟 | ✅ | 所有 | Email |

**说明**:
- ✅ 必需
- ❌ 不需要
- ⚠️ 可选（有更好，没有也能运行）

### 技术栈对比

| 模块 | 主要技术 | 难度 | 稳定性 |
|------|---------|------|--------|
| 黄金股票筛选 | Pandas + AkShare | ⭐⭐ | ⭐⭐⭐⭐⭐ |
| AI量化选股 | Pandas + DeepSeek | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| 微博情绪分析 | Playwright + DeepSeek | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| 全网热点发现 | Playwright + DeepSeek | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 政客交易追踪 | API + Playwright | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| 每日推送 | SMTP + 调度 | ⭐⭐ | ⭐⭐⭐⭐⭐ |

### 成本对比

| 模块 | 免费方案 | 付费方案 | 推荐 |
|------|---------|---------|------|
| 黄金股票筛选 | ✅ 完全免费 | - | 免费 |
| AI量化选股 | DeepSeek免费额度 | DeepSeek付费 | 免费额度 |
| 微博情绪分析 | ✅ 完全免费 | - | 免费 |
| 全网热点发现 | ✅ 完全免费 | - | 免费 |
| 政客交易追踪 | 爬虫免费 | Quiver $30-100/月 | 看需求 |
| 每日推送 | ✅ 完全免费 | - | 免费 |

**总成本**: 
- 最低: 免费（使用DeepSeek免费额度）
- 推荐: $5-10/月（DeepSeek付费）
- 专业: $35-110/月（DeepSeek + Quiver）

---

## 🎯 使用建议

### 新手入门

**推荐模块**:
1. 黄金股票筛选（最简单）
2. AI量化选股（核心功能）
3. 每日推送（自动化）

**运行方式**: GitHub Actions

**预计时间**: 10-15分钟/天

### 进阶使用

**推荐模块**:
1. 黄金股票筛选
2. AI量化选股
3. 微博情绪分析
4. 每日推送

**运行方式**: 本地定时运行

**预计时间**: 15-25分钟/天

### 专业使用

**推荐模块**: 全部6个模块

**运行方式**: 
- 本地: 完整版（每天）
- GitHub: 基础版（备份）

**预计时间**: 25-40分钟/天

---

## 📚 文档导航

### 快速开始
- [START_HERE_GITHUB.md](START_HERE_GITHUB.md) - 从这里开始
- [QUICK_START_GITHUB.md](QUICK_START_GITHUB.md) - 5分钟快速部署

### 模块文档
- [QUANT_PICKER_GUIDE.md](QUANT_PICKER_GUIDE.md) - 量化选股详细说明
- [WEIGHTED_SENTIMENT_GUIDE.md](WEIGHTED_SENTIMENT_GUIDE.md) - 情绪分析详细说明
- [DISCOVERY_ENGINE_GUIDE.md](DISCOVERY_ENGINE_GUIDE.md) - 热点发现详细说明
- [POLITICIAN_TRACKER_GUIDE.md](POLITICIAN_TRACKER_GUIDE.md) - 政客追踪详细说明

### 部署文档
- [GITHUB_DEPLOYMENT_GUIDE.md](GITHUB_DEPLOYMENT_GUIDE.md) - GitHub部署完整指南
- [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - 部署检查清单

### 技术文档
- [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) - 系统架构说明
- [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) - 文档索引

---

## 🔧 快速命令

### 测试单个模块

```bash
# 测试黄金股票筛选
python3 gold_stock_screener.py

# 测试AI量化选股
python3 Quant_Picker.py

# 测试微博情绪分析
python3 weibo_sentiment_weighted.py

# 测试全网热点发现
python3 Discovery_Engine.py

# 测试政客交易追踪
python3 politician_trade_tracker.py
```

### 运行完整分析

```bash
# 运行所有5个模块
python3 run_with_politician_tracker.py

# 运行并发送邮件
python3 daily_email_sender.py
```

### 测试配置

```bash
# 测试配置是否正确
python3 test_config.py
```

### 部署到GitHub

```bash
# 一键部署
./deploy_to_github.sh
```

---

## ⚠️ 常见问题

### Q1: 哪些模块必须运行？

**A**: 
- 必需: 黄金股票筛选、AI量化选股
- 推荐: 微博情绪分析、政客交易追踪
- 可选: 全网热点发现

### Q2: GitHub Actions能运行哪些模块？

**A**: 
- ✅ 黄金股票筛选
- ✅ AI量化选股
- ✅ 政客交易追踪（如果用API）
- ❌ 微博情绪分析（需要浏览器）
- ❌ 全网热点发现（需要浏览器）

### Q3: 每天需要多长时间？

**A**:
- GitHub版: 10-15分钟（自动）
- 本地完整版: 25-40分钟（自动）
- 手动运行: 0分钟（设置好后无需干预）

### Q4: 成本是多少？

**A**:
- GitHub Actions: 免费
- QQ邮箱: 免费
- DeepSeek API: $5-10/月（推荐）
- Quiver API: $30-100/月（可选）

### Q5: 数据准确吗？

**A**:
- 数据来源: 官方API（AkShare、Quiver）
- AI分析: DeepSeek深度学习
- 准确性: 仅供参考，不构成投资建议

---

## 🎉 总结

### 系统特点

✅ **完整**: 6大核心模块，覆盖多个维度
✅ **智能**: DeepSeek AI深度分析
✅ **自动**: 每天自动运行并推送
✅ **免费**: 基础功能完全免费
✅ **开源**: 所有代码可见可修改
✅ **文档**: 24个详细文档

### 核心价值

1. **节省时间**: 自动化分析，无需手动操作
2. **多维度**: 技术面+舆情面+政策面
3. **AI增强**: DeepSeek智能分析
4. **及时性**: 每天早上8点准时推送
5. **学习价值**: 理解量化投资思维

### 开始使用

**3步快速开始**:
1. 查看 [START_HERE_GITHUB.md](START_HERE_GITHUB.md)
2. 运行 `./deploy_to_github.sh`
3. 等待每天早上8点收简报

---

**祝你投资顺利！** 📈💰🎉

---

**最后更新**: 2026年1月15日
**版本**: v1.0.0
**文档**: COMPLETE_MODULES_OVERVIEW.md
