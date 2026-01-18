# 每日投资简报系统

一个自动化的股票分析和简报生成系统，每日更新市场信息并生成综合投资简报。

## 系统架构

```
每日简报系统
├── 模块1: 黄金股票筛选分析 (gold_stock_screener.py)
├── 模块2: 股吧热点分析 (guba_analyzer.py)
└── 主系统: 简报生成器 (daily_report_system.py)
```

## 功能模块

### 1. 黄金股票筛选模块 (`gold_stock_screener.py`)

**功能**:
- 自动获取黄金行业股票列表
- 筛选符合条件的股票（股本8-15亿，市值105-195亿）
- 检测官方资本背景（社保基金、国资委、汇金、证金等）
- 综合评分排序

**评分体系**:
- 股本匹配: 25分
- 官方背书: 30分
- 黄金行业: 15分
- 总分: 70分

### 2. 股吧热点分析模块 (`guba_analyzer.py`)

**功能**:
- 抓取东方财富股吧热门帖子
- 多重筛选规则过滤高质量内容
- 计算帖子质量评分

**筛选规则**:
- **规则A (长度)**: 正文必须大于15个字
- **规则B (互动)**: 阅读量前30% 或 评论数>5
- **规则C (排除)**: 过滤广告、谩骂等垃圾内容

**质量评分**:
- 阅读量: 40%
- 评论数: 40%
- 内容长度: 20%

### 3. 每日简报系统 (`daily_report_system.py`)

**功能**:
- 整合所有分析模块
- 生成结构化的每日简报
- 输出文本和HTML两种格式
- 自动保存历史数据

## 安装依赖

```bash
pip install akshare pandas numpy
```

## 使用方法

### 快速开始

```bash
# 生成每日简报
python daily_report_system.py
```

### 单独使用各模块

```bash
# 只分析黄金股票
python gold_stock_screener.py

# 只分析股吧热点
python guba_analyzer.py
```

### 自定义配置

```python
from daily_report_system import DailyReportSystem

# 创建简报系统
report_system = DailyReportSystem()

# 自定义生成简报
report_content = report_system.generate_daily_report(
    include_gold_stocks=True,  # 是否包含黄金股票分析
    include_guba=True          # 是否包含股吧热点分析
)
```

## 输出文件

系统会自动创建以下目录和文件：

```
项目目录/
├── data/                          # 原始数据
│   ├── gold_stocks_YYYYMMDD.csv  # 黄金股票数据
│   └── guba_posts_YYYYMMDD.csv   # 股吧帖子数据
├── reports/                       # 简报文件
│   ├── daily_report_YYYYMMDD.txt # 文本版简报
│   └── daily_report_YYYYMMDD.html # HTML版简报
```

## 简报内容结构

```
每日投资简报
├── 一、黄金行业股票分析
│   ├── 统计信息
│   └── 重点关注股票 TOP 5
├── 二、股吧热点分析
│   ├── 统计信息
│   └── 热门讨论话题 TOP 10
└── 三、综合建议
    ├── 黄金板块投资建议
    ├── 市场热点关注
    └── 风险提示
```

## 定时任务设置

### macOS/Linux (使用crontab)

```bash
# 编辑crontab
crontab -e

# 添加定时任务（每天早上9点执行）
0 9 * * * cd /path/to/project && python3 daily_report_system.py
```

### Windows (使用任务计划程序)

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器为每天特定时间
4. 操作选择"启动程序"，填入Python路径和脚本路径

## 核心函数说明

### `get_guba_trends()`

```python
def get_guba_trends(stock_code=None, symbol='全部', max_pages=5):
    """
    获取股吧帖子并进行筛选
    
    参数:
        stock_code: 股票代码（可选）
        symbol: 股吧类型，默认'全部'
        max_pages: 最多抓取页数
        
    返回:
        DataFrame: 包含筛选后的帖子信息
            - 标题
            - 内容
            - 阅读量
            - 评论数
            - 帖子链接
            - 质量评分
    """
```

### 使用示例

```python
from guba_analyzer import GubaAnalyzer

# 创建分析器
analyzer = GubaAnalyzer()

# 获取股吧广场热帖
posts_df = analyzer.get_guba_trends(symbol='全部', max_pages=5)

# 获取特定股票的股吧帖子
posts_df = analyzer.get_guba_trends(stock_code='600519', max_pages=3)

# 查看结果
print(posts_df[['标题', '阅读量', '评论数', '质量评分']].head())

# 生成摘要
summary = analyzer.get_filtered_posts_summary(posts_df)
print(summary)
```

## 注意事项

1. **数据源依赖**: 依赖akshare库和东方财富数据源，可能受网络和接口变更影响
2. **请求频率**: 内置延时机制，避免请求过于频繁
3. **数据时效**: 建议每日定时运行以获取最新数据
4. **异常处理**: 所有模块都有异常处理，接口失效时不会崩溃
5. **投资建议**: 本系统仅供参考，不构成投资建议

## 扩展功能

可以轻松添加更多分析模块：

```python
# 在 daily_report_system.py 中添加新模块
class DailyReportSystem:
    def __init__(self):
        # 添加新的分析器
        self.new_analyzer = NewAnalyzer()
    
    def generate_daily_report(self):
        # 添加新的分析步骤
        new_data = self._analyze_new_module()
        self.report_data['新模块'] = new_data
```

## 常见问题

**Q: 为什么获取不到股吧数据？**
A: 可能是网络问题或akshare接口变更，检查网络连接并更新akshare到最新版本。

**Q: 如何修改筛选条件？**
A: 在对应模块中修改筛选参数，如股本范围、市值范围等。

**Q: 可以分析其他行业吗？**
A: 可以，参考`gold_stock_screener.py`创建新的行业筛选器。

**Q: 如何添加更多数据源？**
A: 在对应模块中添加新的数据获取函数，并在主系统中整合。

## 更新日志

- v1.0 (2026-01-14)
  - 初始版本
  - 黄金股票筛选功能
  - 股吧热点分析功能
  - 每日简报生成功能

## 许可证

MIT License

## 联系方式

如有问题或建议，欢迎反馈。