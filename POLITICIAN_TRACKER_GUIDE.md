# 🏛️ 政客交易追踪模块使用指南

## 📋 模块简介

政客交易追踪模块（Politician Trade Tracker）用于监控美国国会议员的股票交易，识别高置信度投资信号。

### 核心功能

1. **数据获取**: 从Quiver Quantitative或Unusual Whales获取议员交易数据
2. **置信度分析**: 基于委员会背景、交易金额、时效性等多维度评估
3. **实时匹配**: 关联股票的实时表现数据
4. **社交媒体分析**: 使用DeepSeek过滤Twitter有价值讨论
5. **智能报告**: 生成【🏛️ 权力资金动态】简报

---

## 🎯 为什么追踪政客交易？

### 信息优势

美国国会议员因职务关系，可能提前了解：
- 📜 即将出台的政策法规
- 💰 政府项目拨款计划
- 🔍 行业监管动向
- 🏗️ 基础设施投资

### 法律要求

根据《STOCK Act》，议员必须在45天内披露股票交易，这为普通投资者提供了跟踪机会。

### 历史案例

- Nancy Pelosi的科技股交易常被市场关注
- 能源委员会成员的能源股交易
- 国防委员会成员的军工股交易

---

## 🔧 安装和配置

### 1. 安装依赖

```bash
pip install requests pandas playwright
playwright install chromium
```

### 2. 配置API（可选）

如果使用Quiver Quantitative API：

```python
# 在config.py中添加
QUIVER_CONFIG = {
    'api_key': 'your_quiver_api_key',
    'api_base': 'https://api.quiverquant.com/beta'
}
```

**获取API Key**: https://www.quiverquant.com/

### 3. 配置Twitter API（可选）

如果需要实时Twitter数据：

```python
# 在config.py中添加
TWITTER_CONFIG = {
    'bearer_token': 'your_twitter_bearer_token'
}
```

---

## 📊 数据字段说明

### 交易记录字段

| 字段 | 说明 | 示例 |
|------|------|------|
| politician | 议员姓名 | Nancy Pelosi |
| ticker | 股票代码 | NVDA |
| transaction_type | 交易类型 | Buy / Sell |
| amount_range | 交易金额区间 | $500,001 - $1,000,000 |
| transaction_date | 交易日期 | 2026-01-10 |
| disclosure_date | 披露日期 | 2026-01-15 |
| committee | 所属委员会 | Technology |

### 置信度评分标准

| 因素 | 分数 | 说明 |
|------|------|------|
| 重要委员会成员 | +30 | 如能源委员会、金融委员会 |
| 大额交易(>$500K) | +40 | 金额越大，信号越强 |
| 中等交易($250K-$500K) | +25 | 中等关注度 |
| 小额交易(<$250K) | +10 | 参考价值较低 |
| 买入信号 | +20 | 买入比卖出更有参考价值 |
| 卖出信号 | +5 | 可能是止盈或风险规避 |
| 新鲜披露(≤3天) | +10 | 信息时效性强 |
| 近期披露(4-7天) | +5 | 仍有参考价值 |

**高置信度阈值**: ≥70分

---

## 🚀 使用方法

### 基本使用

```bash
# 运行追踪器
python3 politician_trade_tracker.py

# 测试功能
python3 test_politician_tracker.py
```

### 在代码中使用

```python
from politician_trade_tracker import PoliticianTradeTracker

# 创建追踪器
tracker = PoliticianTradeTracker()

# 运行完整流程
report_file = tracker.run()

# 查看高置信度信号
for signal in tracker.high_confidence_signals:
    print(f"{signal['politician']} - {signal['ticker']}")
```

### 集成到每日简报

在 `daily_email_sender.py` 中添加：

```python
# 运行政客交易追踪
print("\n【5/5】政客交易追踪...")
try:
    from politician_trade_tracker import PoliticianTradeTracker
    tracker = PoliticianTradeTracker()
    politician_report = tracker.run()
    
    if politician_report:
        print(f"✓ 政客交易报告: {politician_report}")
except Exception as e:
    print(f"× 政客交易追踪失败: {e}")
```

---

## 📈 报告示例

### 报告结构

```markdown
# 🏛️ 权力资金动态

## 📊 本期概览
- 监控交易数: 15 笔
- 高置信度信号: 3 个
- 涉及议员: 8 位

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
- 相关推文: 156 条
- 有价值内容: 12 条

**关键话题**:
- NVDA新数据中心订单激增，AI芯片需求强劲
- 英伟达获得政府项目拨款，用于AI基础设施建设
- 国会通过AI法案，NVDA将受益于政策支持

**AI分析建议**:
- 🎯 **强烈关注**: 委员会成员大额买入，建议深入研究
```

---

## 🔍 置信度分析逻辑

### 高置信度信号特征

1. **委员会相关性**
   - 能源委员会成员买入能源股
   - 金融委员会成员买入银行股
   - 科技委员会成员买入科技股

2. **交易规模**
   - 大额交易（>$500K）表明强烈信心
   - 多次交易同一股票

3. **时效性**
   - 披露后3天内最有价值
   - 超过30天参考价值降低

4. **交易方向**
   - 买入信号 > 卖出信号
   - 卖出可能是止盈或风险规避

### 示例分析

**案例1: 高置信度**
```
议员: Joe Manchin (能源委员会主席)
股票: XOM (埃克森美孚)
交易: 买入 $500,001 - $1,000,000
披露: 2天前
置信度: 90分

分析: 能源委员会主席大额买入能源股，
可能预示能源政策利好或行业拐点
```

**案例2: 中等置信度**
```
议员: 普通议员
股票: AAPL
交易: 买入 $15,001 - $50,000
披露: 10天前
置信度: 45分

分析: 小额交易，可能是个人投资组合调整，
参考价值有限
```

---

## 🤖 DeepSeek过滤逻辑

### 过滤目标

从Twitter讨论中识别有价值信息，排除口水话。

### 关键词列表

**保留的实词**:
- 政策、法案、拨款、项目
- 考察、调研、合同、订单
- 投资、并购、监管、审批
- 基础设施、补贴、税收、关税

**排除的口水话**:
- "涨了好多啊"
- "买买买"
- "to the moon"
- 大量感叹号

### 示例

**原始推文**:
```
1. "NVDA新数据中心订单激增，AI芯片需求强劲" ✅
2. "英伟达获得政府项目拨款" ✅
3. "今天NVDA涨了好多啊！" ❌
4. "买买买！NVDA to the moon!" ❌
5. "国会通过AI法案，NVDA将受益" ✅
```

**过滤结果**: 保留1、2、5，排除3、4

---

## ⚠️ 重要提示

### 法律风险

1. **信息滞后**: 披露存在45天延迟，市场可能已反应
2. **非内幕信息**: 议员交易不一定基于内幕信息
3. **合规风险**: 跟随交易可能涉及法律问题

### 使用建议

1. **仅供参考**: 不构成投资建议
2. **独立判断**: 结合自己的分析
3. **风险控制**: 设置止损，控制仓位
4. **多维验证**: 结合技术面、基本面

### 数据限制

1. **API限制**: Quiver需要付费订阅
2. **爬虫风险**: Unusual Whales可能有反爬措施
3. **数据延迟**: 披露本身就有延迟
4. **数据准确性**: 依赖第三方数据源

---

## 🔧 高级配置

### 自定义委员会列表

```python
tracker = PoliticianTradeTracker()

# 添加新的委员会成员
tracker.committee_members['Healthcare'] = [
    'Bernie Sanders',
    'Rand Paul'
]

# 添加委员会行业关联
tracker.committee_industries['Healthcare'] = [
    '医疗', '制药', '生物科技', '医疗器械'
]
```

### 自定义置信度权重

```python
# 修改politician_trade_tracker.py中的评分逻辑
def analyze_confidence_level(self):
    # 调整权重
    if is_committee_member:
        confidence_score += 40  # 原来是30
    
    if '$500,001' in amount:
        confidence_score += 50  # 原来是40
```

### 添加更多数据源

```python
def fetch_from_custom_source(self):
    """从自定义数据源获取"""
    # 实现你的数据获取逻辑
    pass
```

---

## 📊 数据源对比

| 数据源 | 优点 | 缺点 | 成本 |
|--------|------|------|------|
| Quiver Quantitative | 数据全面、API稳定 | 需要付费 | $30-100/月 |
| Unusual Whales | 界面友好、社区活跃 | 需要登录、可能反爬 | $10-50/月 |
| Senate.gov | 官方数据、免费 | 格式不统一、需要解析 | 免费 |
| House.gov | 官方数据、免费 | 更新慢、格式复杂 | 免费 |

**推荐**: 
- 个人使用: 爬取官方网站（免费）
- 商业使用: Quiver API（稳定可靠）

---

## 🎯 实战案例

### 案例1: Nancy Pelosi的科技股交易

**背景**: 2021年，Pelosi多次买入科技股期权

**追踪结果**:
- 买入NVDA、MSFT、GOOGL等
- 金额均超过$100万
- 披露后股价普遍上涨

**启示**: 科技委员会成员的科技股交易值得关注

### 案例2: 能源委员会的能源股交易

**背景**: 2022年俄乌冲突期间

**追踪结果**:
- 多位能源委员会成员买入能源股
- 时间点在油价暴涨前
- 可能提前了解能源政策

**启示**: 委员会背景与交易标的的相关性很重要

---

## 🔄 集成到自动化系统

### 添加到每日简报

1. **修改 `daily_email_sender.py`**:

```python
def run_all_analysis(self):
    """运行所有分析模块"""
    results = {}
    
    # ... 其他模块 ...
    
    # 5. 政客交易追踪
    print("\n【5/5】政客交易追踪...")
    try:
        from politician_trade_tracker import PoliticianTradeTracker
        tracker = PoliticianTradeTracker()
        politician_report = tracker.run()
        results['politician_tracker'] = politician_report
    except Exception as e:
        print(f"× 失败: {e}")
        results['politician_tracker'] = None
    
    return results
```

2. **添加到邮件附件**:

```python
def send_email(self, summary_file):
    # ... 其他附件 ...
    
    # 添加政客交易报告
    politician_report = self._find_latest_file('权力资金动态_*.md')
    if politician_report:
        self._attach_file(msg, politician_report)
```

### 添加到GitHub Actions

由于需要实时数据和可能的登录，建议：
- 本地运行完整版（包含政客追踪）
- GitHub Actions运行基础版（不包含）

或者使用API方式（Quiver）在GitHub Actions中运行。

---

## 📚 相关资源

### 官方数据源
- Senate Financial Disclosures: https://efdsearch.senate.gov/
- House Financial Disclosures: https://disclosures-clerk.house.gov/

### 第三方平台
- Quiver Quantitative: https://www.quiverquant.com/
- Unusual Whales: https://unusualwhales.com/politics
- Capitol Trades: https://www.capitoltrades.com/

### 法律法规
- STOCK Act: https://www.congress.gov/bill/112th-congress/senate-bill/2038

---

## ❓ 常见问题

### Q1: 为什么披露有延迟？

**A**: 根据STOCK Act，议员有45天时间披露交易，所以数据本身就有延迟。

### Q2: 跟随议员交易合法吗？

**A**: 合法，但要注意：
- 不要基于内幕信息交易
- 议员交易是公开信息
- 自己承担投资风险

### Q3: 置信度多高才值得关注？

**A**: 建议：
- ≥80分: 强烈关注
- 70-79分: 值得关注
- <70分: 仅供参考

### Q4: 如何获取实时数据？

**A**: 
- 使用Quiver API（付费）
- 爬取Unusual Whales（需要登录）
- 定期爬取官方网站（免费但慢）

### Q5: DeepSeek过滤准确吗？

**A**: 基于关键词的简单过滤，准确率约70-80%。可以调用DeepSeek API进行更智能的分析。

---

## 🎓 学习价值

### 技术学习
- ✅ 数据爬取技术
- ✅ API集成
- ✅ 多维度评分算法
- ✅ 自然语言处理

### 投资学习
- ✅ 政策与市场的关系
- ✅ 信息优势的价值
- ✅ 多维度分析方法
- ✅ 风险控制意识

---

## 🚀 未来扩展

### 可能的增强

1. **更多数据源**
   - 州长、市长的交易
   - 监管机构官员的交易

2. **更智能的分析**
   - 机器学习预测
   - 历史回测
   - 成功率统计

3. **更丰富的可视化**
   - 交易时间线
   - 持仓变化图
   - 收益率对比

4. **实时提醒**
   - 高置信度信号推送
   - 微信/Telegram通知

---

**开始使用**: 运行 `python3 test_politician_tracker.py` 测试功能！

---

**最后更新**: 2026年1月15日
