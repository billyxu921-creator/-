# 每日投资简报系统 - 使用指南

## 快速开始

### 1. 生成完整的每日简报

```bash
python3 daily_report_system.py
```

这将生成包含以下内容的完整简报：
- 黄金行业股票筛选分析
- 市场热点新闻分析
- 综合投资建议

输出文件：
- `reports/daily_report_YYYYMMDD.txt` - 文本版简报
- `reports/daily_report_YYYYMMDD.html` - HTML版简报
- `data/gold_stocks_YYYYMMDD.csv` - 黄金股票详细数据
- `data/guba_posts_YYYYMMDD.csv` - 市场新闻详细数据

### 2. 只分析黄金股票

```bash
python3 gold_stock_screener.py
```

输出：黄金行业股票筛选结果和评分

### 3. 只分析市场热点

```bash
python3 guba_analyzer.py
```

输出：市场热点新闻和讨论分析

## 核心功能详解

### 功能1: 黄金股票筛选 (`gold_stock_screener.py`)

**筛选条件**:
- 所属行业：黄金/贵金属
- 总股本：8-15亿股
- 流通市值：105-195亿元（目标150亿±30%）
- 官方资本：检测社保基金、国资委、汇金、证金等

**评分标准**:
```
总分 = 股本匹配分(25) + 官方背书分(30) + 黄金行业加分(15)
```

**使用示例**:
```python
from gold_stock_screener import GoldStockScreener

# 创建筛选器
screener = GoldStockScreener()

# 筛选黄金股票
results = screener.screen_gold_stocks()

# 打印摘要
screener.print_gold_summary(results)

# 保存结果
results.to_csv('my_gold_stocks.csv', index=False, encoding='utf-8-sig')
```

### 功能2: 市场热点分析 (`guba_analyzer.py`)

**数据来源**:
- 东方财富股票新闻
- 主力资金流向新闻

**筛选规则**:
1. **长度筛选**: 内容长度>10个字
2. **互动筛选**: 阅读量前30% 或 评论数>5（如有数据）
3. **垃圾过滤**: 排除广告、谩骂等低质量内容

**质量评分**:
```
质量评分 = 阅读量权重(40%) + 评论数权重(40%) + 内容长度权重(20%)
```

**使用示例**:
```python
from guba_analyzer import GubaAnalyzer

# 创建分析器
analyzer = GubaAnalyzer()

# 获取市场热点
posts_df = analyzer.get_guba_trends(max_pages=5)

# 查看摘要
summary = analyzer.get_filtered_posts_summary(posts_df)
print(summary)

# 查看TOP 10热点
print(posts_df[['标题', '质量评分']].head(10))
```

### 功能3: 每日简报系统 (`daily_report_system.py`)

**系统架构**:
```
DailyReportSystem
├── 模块1: 黄金股票分析
├── 模块2: 市场热点分析
└── 模块3: 综合简报生成
```

**自定义简报**:
```python
from daily_report_system import DailyReportSystem

# 创建系统实例
system = DailyReportSystem()

# 自定义生成简报
report = system.generate_daily_report(
    include_gold_stocks=True,  # 包含黄金股票分析
    include_guba=True          # 包含市场热点分析
)

# 打印简报
print(report)
```

## 定时自动化

### 方法1: Crontab (macOS/Linux)

```bash
# 编辑crontab
crontab -e

# 每天早上9点生成简报
0 9 * * * cd /path/to/project && /usr/bin/python3 daily_report_system.py >> /path/to/logs/daily_report.log 2>&1

# 每天下午3点更新数据
0 15 * * * cd /path/to/project && /usr/bin/python3 daily_report_system.py >> /path/to/logs/daily_report.log 2>&1
```

### 方法2: Python脚本定时

创建 `scheduler.py`:
```python
import schedule
import time
from daily_report_system import DailyReportSystem

def generate_report():
    print(f"开始生成简报: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    system = DailyReportSystem()
    system.generate_daily_report()
    print("简报生成完成")

# 每天9:00执行
schedule.every().day.at("09:00").do(generate_report)

# 每天15:00执行
schedule.every().day.at("15:00").do(generate_report)

print("定时任务已启动...")
while True:
    schedule.run_pending()
    time.sleep(60)
```

运行：
```bash
pip install schedule
python3 scheduler.py
```

## 输出示例

### 简报结构

```
================================================================================
每日投资简报
生成时间: 2026年01月14日 15:19:49
================================================================================

【一、黄金行业股票分析】
--------------------------------------------------------------------------------
分析股票总数: 11 只
符合筛选条件: 3 只
平均评分: 45.5 分

重点关注股票 TOP 5:

1. 600547 山东黄金
   总分: 70 | 股本: 10.5亿股 | 市值: 145.2亿元 | 价格: 13.82元
   亮点: 股本规模适中 | 有官方资本背景 | 黄金行业

2. 600489 中金黄金
   总分: 65 | 股本: 12.8亿股 | 市值: 168.5亿元 | 价格: 13.16元
   亮点: 股本规模适中 | 有官方资本背景 | 黄金行业

...

【二、市场热点分析】
--------------------------------------------------------------------------------
高质量帖子数: 10 条
平均阅读量: 0
平均评论数: 0.0

热门讨论话题 TOP 10:

1. 两融余额增加35.50亿元 杠杆资金大幅加仓283股
   阅读: 0 | 评论: 0 | 质量评分: 20.0

2. 【数据揭秘】融资客看好个股一览
   阅读: 0 | 评论: 0 | 质量评分: 19.9

...

【三、综合建议】
--------------------------------------------------------------------------------
1. 黄金板块投资建议:
   - 共发现 3 只符合条件的黄金股票
   - 重点关注: 600547 山东黄金 (评分: 70)
   - 该股有官方资本背景，相对稳健

2. 市场热点关注:
   - 当前市场讨论活跃，共 10 个热门话题
   - 热门股票: 603777, 600300

3. 风险提示:
   - 股市有风险，投资需谨慎
   - 建议结合基本面分析和技术面分析
   - 注意控制仓位，分散投资风险
   - 关注宏观经济政策和行业动态

================================================================================
注: 本简报仅供参考，不构成投资建议。投资有风险，入市需谨慎。
================================================================================
```

## 扩展开发

### 添加新的分析模块

1. 创建新的分析器类：

```python
# new_analyzer.py
class NewAnalyzer:
    def analyze(self):
        # 实现分析逻辑
        return results_df
```

2. 在主系统中集成：

```python
# daily_report_system.py
from new_analyzer import NewAnalyzer

class DailyReportSystem:
    def __init__(self):
        self.new_analyzer = NewAnalyzer()
    
    def generate_daily_report(self):
        # 添加新模块
        new_data = self.new_analyzer.analyze()
        self.report_data['新模块'] = new_data
```

### 自定义筛选条件

修改 `gold_stock_screener.py` 中的条件：

```python
def check_market_cap_criteria(self, info_dict):
    # 修改股本范围
    shares_criteria = 5 <= total_shares <= 20  # 改为5-20亿
    
    # 修改市值范围
    market_cap_criteria = 80 <= circulating_market_cap <= 250  # 改为80-250亿
    
    return shares_criteria, market_cap_criteria, total_shares, circulating_market_cap
```

## 常见问题

**Q: 如何只分析特定股票？**
```python
analyzer = GubaAnalyzer()
posts = analyzer.get_guba_trends(stock_code='600519')  # 贵州茅台
```

**Q: 如何修改简报保存路径？**
```python
# 在 daily_report_system.py 中修改
def _save_report(self, report_content):
    txt_filename = "/custom/path/daily_report.txt"
    # ...
```

**Q: 如何添加邮件发送功能？**
```python
import smtplib
from email.mime.text import MIMEText

def send_email_report(report_content):
    msg = MIMEText(report_content, 'plain', 'utf-8')
    msg['Subject'] = f'每日投资简报 - {datetime.now().strftime("%Y-%m-%d")}'
    msg['From'] = 'your_email@example.com'
    msg['To'] = 'recipient@example.com'
    
    # 发送邮件
    # ...
```

## 性能优化

1. **并行处理**: 使用多线程处理多只股票
2. **缓存机制**: 缓存当日已获取的数据
3. **增量更新**: 只更新变化的数据

## 注意事项

1. **数据源稳定性**: akshare依赖第三方数据源，可能不稳定
2. **请求频率**: 避免过于频繁的请求，已内置延时
3. **数据准确性**: 数据仅供参考，投资需谨慎
4. **异常处理**: 所有模块都有异常处理，不会因单个错误崩溃

## 技术支持

如遇问题，请检查：
1. akshare版本是否最新：`pip install --upgrade akshare`
2. 网络连接是否正常
3. Python版本是否>=3.7
4. 依赖包是否完整安装

## 更新计划

- [ ] 添加更多行业筛选器
- [ ] 集成技术指标分析
- [ ] 添加邮件/微信通知
- [ ] 支持自定义评分权重
- [ ] 添加历史数据对比
- [ ] 生成可视化图表