# 股吧情报分析系统 - 使用指南

## 功能概述

股吧情报分析系统能够从海量股吧讨论中自动筛选出具有实战价值的投资情报，帮助投资者快速把握市场动向。

## 核心功能

### 1. 智能识别标的

自动识别帖子中讨论的股票，支持：
- **股票代码识别**: 自动识别6位股票代码（如 600547）
- **股票简称识别**: 识别常见股票简称（如"山东黄金"）
- **模糊匹配**: 即使没写完整代码也能识别

### 2. 三维分类逻辑

将帖子精准分类为三大类型：

#### 【技术派】
关注技术指标和图形形态：
- **均线系统**: 金叉、死叉、多头排列、空头排列
- **成交量**: 放量、缩量、量价齐升、量价背离
- **技术指标**: MACD、KDJ、RSI等
- **形态分析**: 突破、回踩、支撑、压力位

#### 【筹码派】
关注资金流向和主力动向：
- **大单追踪**: 主力资金、机构资金、北向资金
- **庄家行为**: 洗盘、吸筹、出货、拉升
- **国家队**: 社保基金、汇金、证金等官方资本
- **筹码分布**: 筹码集中度、获利盘、套牢盘

#### 【基本面】
关注公司业绩和行业动态：
- **业绩数据**: 财报、营收、利润增长
- **政策利好**: 行业政策、扶持政策
- **重大事件**: 公告、重组、并购、增持
- **行业趋势**: 景气度、产业链、龙头地位

### 3. 散户噪音过滤

自动剔除低质量内容：
- 纯情绪化表达（"必涨"、"翻倍"、"冲冲冲"）
- 无实质内容的短帖
- 广告和垃圾信息
- 谩骂和负面情绪

### 4. 价值评分系统

对每条情报进行1-10分评估：

```
评分维度：
├── 基础分(3分): 有明确分类
├── 论据分(4分): 有具体论据和详细说明
├── 数据分(2分): 包含具体数字和百分比
└── 专业度(1分): 使用专业术语

评分标准：
• 9-10分: 论据充分，数据详实，极具参考价值
• 7-8分: 有明确论据，逻辑清晰，值得关注
• 5-6分: 有一定参考价值，但论据不够充分
• 1-4分: 参考价值较低
```

## 使用方法

### 快速开始

```python
from guba_analyzer import GubaAnalyzer
from intelligence_analyzer import IntelligenceAnalyzer

# 1. 获取股吧帖子
guba_analyzer = GubaAnalyzer()
posts_df = guba_analyzer.get_guba_trends(max_pages=5)

# 2. 分析情报
intel_analyzer = IntelligenceAnalyzer()
intelligence_df = intel_analyzer.analyze_intelligence(posts_df)

# 3. 生成报告
report = intel_analyzer.generate_intelligence_report(intelligence_df)
print(report)

# 4. 保存结果
intelligence_df.to_csv('intelligence.csv', index=False, encoding='utf-8-sig')
```

### 集成到每日简报

```python
from daily_report_system import DailyReportSystem

# 创建简报系统（自动包含情报分析）
system = DailyReportSystem()

# 生成完整简报
report = system.generate_daily_report(
    include_gold_stocks=True,
    include_guba=True,
    include_intelligence=True  # 启用情报分析
)
```

### 命令行使用

```bash
# 测试情报分析器
python3 intelligence_analyzer.py

# 生成包含情报分析的完整简报
python3 daily_report_system.py
```

## 输出示例

### 情报分析结果

```
================================================================================
股吧情报分析报告
生成时间: 2026-01-14 15:24:15
================================================================================

【统计概览】
有效情报总数: 7
平均价值评分: 7.7
高价值情报(≥8分): 3

【分类分布】
  技术派: 3 条
  筹码派: 2 条
  基本面: 2 条

【热门标的 TOP 5】
  山东黄金(600547): 被提及 3 次
  中金黄金(600489): 被提及 2 次
  紫金矿业(601899): 被提及 1 次

【高价值情报 TOP 10】
--------------------------------------------------------------------------------

1. 山东黄金突破60日均线，MACD金叉，主力资金大幅流入
   标的: 山东黄金(600547)
   分类: 技术派 + 筹码派
   评分: 10/10
   论据: 技术面看，山东黄金今日突破60日均线，MACD指标金叉向上，
         同时主力资金净流入1.5亿元，显示资金面配合良好

2. 600547今日大单净流入2.3亿，北向资金持续买入
   标的: 山东黄金(600547)
   分类: 筹码派 + 技术派
   评分: 9/10
   论据: 600547山东黄金今日大单净流入2.3亿元，北向资金连续5日净买入，
         资金面非常强势

3. 紫金矿业业绩预告超预期，社保基金增持明显
   标的: 紫金矿业(601899)
   分类: 基本面 + 筹码派
   评分: 8/10
   论据: 紫金矿业发布业绩预告，预计净利润同比增长45%，超出市场预期。
         同时社保基金在二季度增持了500万股
```

### CSV输出字段

```
标题, 识别股票, 主要分类, 次要分类, 关键论据, 价值评分, 原文链接, 发布时间, 原始内容
```

## 实战应用场景

### 场景1: 技术面突破信号

```
情报: "山东黄金突破60日均线，MACD金叉，主力资金大幅流入"
分类: 技术派 + 筹码派
评分: 10/10

实战价值:
✓ 技术面多重确认（均线突破 + MACD金叉）
✓ 资金面配合（主力资金流入）
✓ 可作为短线介入信号
```

### 场景2: 筹码面异动

```
情报: "北向资金连续5日净买入，大单净流入2.3亿"
分类: 筹码派
评分: 9/10

实战价值:
✓ 外资持续看好
✓ 大资金持续流入
✓ 可作为中线持有依据
```

### 场景3: 基本面利好

```
情报: "业绩预告超预期，净利润同比增长45%，社保基金增持"
分类: 基本面 + 筹码派
评分: 8/10

实战价值:
✓ 业绩确定性强
✓ 官方资本背书
✓ 可作为长线配置标的
```

## 高级功能

### 自定义股票库

```python
analyzer = IntelligenceAnalyzer()

# 添加自定义股票映射
analyzer.stock_mapping.update({
    '你的股票简称': '股票代码',
    '某某科技': '300xxx'
})
```

### 自定义关键词

```python
# 添加自定义技术派关键词
analyzer.technical_keywords['自定义指标'] = ['关键词1', '关键词2']

# 添加自定义筹码派关键词
analyzer.chip_keywords['自定义类别'] = ['关键词1', '关键词2']

# 添加自定义基本面关键词
analyzer.fundamental_keywords['自定义类别'] = ['关键词1', '关键词2']
```

### 调整评分权重

```python
def custom_evaluate_value(self, text, categories, evidence):
    """自定义评分逻辑"""
    score = 0
    
    # 你的评分逻辑
    if '特定关键词' in text:
        score += 5
    
    return min(10, score)

# 替换评分函数
analyzer._evaluate_value = custom_evaluate_value
```

## 注意事项

### 1. 数据质量
- 情报质量取决于原始帖子质量
- 建议结合多个数据源交叉验证
- 高分情报也需要人工复核

### 2. 时效性
- 股吧信息更新快，建议实时抓取
- 历史情报可能已失效
- 注意查看发布时间

### 3. 风险控制
- 情报仅供参考，不构成投资建议
- 需结合自己的投资体系
- 注意控制仓位和风险

### 4. 法律合规
- 遵守数据使用规范
- 不传播虚假信息
- 不进行市场操纵

## 性能优化

### 批量处理

```python
# 分批处理大量帖子
batch_size = 100
for i in range(0, len(posts_df), batch_size):
    batch = posts_df[i:i+batch_size]
    intel_batch = analyzer.analyze_intelligence(batch)
    # 处理结果
```

### 并行处理

```python
from multiprocessing import Pool

def analyze_batch(posts_batch):
    analyzer = IntelligenceAnalyzer()
    return analyzer.analyze_intelligence(posts_batch)

# 使用多进程
with Pool(4) as pool:
    results = pool.map(analyze_batch, batches)
```

## 常见问题

**Q: 为什么有些股票识别不出来？**
A: 需要在stock_mapping中添加该股票的简称和代码映射。

**Q: 如何提高情报准确率？**
A: 1) 增加关键词库 2) 优化评分逻辑 3) 提高原始数据质量

**Q: 评分标准可以调整吗？**
A: 可以，修改_evaluate_value函数中的评分逻辑。

**Q: 如何过滤特定类型的情报？**
A: 使用DataFrame的筛选功能，如 `intel_df[intel_df['主要分类'] == '技术派']`

## 扩展开发

### 添加新的分类

```python
# 在IntelligenceAnalyzer类中添加
self.new_category_keywords = {
    '新类别': ['关键词1', '关键词2']
}

# 在_classify_post方法中添加评分逻辑
new_score = 0
for keyword in self.new_category_keywords['新类别']:
    if keyword in text:
        new_score += 1
if new_score > 0:
    scores['新类别'] = new_score
```

### 集成机器学习

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# 训练分类模型
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(training_texts)
y = training_labels

model = MultinomialNB()
model.fit(X, y)

# 在分类时使用模型
def ml_classify(text):
    X_test = vectorizer.transform([text])
    return model.predict(X_test)[0]
```

## 更新日志

- v1.0 (2026-01-14)
  - 初始版本
  - 支持三维分类（技术派、筹码派、基本面）
  - 智能评分系统
  - 散户噪音过滤

## 技术支持

如有问题或建议，欢迎反馈。

---

**免责声明**: 本系统提供的情报分析仅供参考，不构成投资建议。投资有风险，入市需谨慎。