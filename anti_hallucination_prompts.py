#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
防幻觉提示词配置
用于所有DeepSeek AI调用，确保输出真实可靠
"""

# 通用防幻觉规则
ANTI_HALLUCINATION_RULES = """
【重要规则 - 防止幻觉】:
1. 你只能根据提供的搜索结果和数据回答
2. 如果搜索结果中没有相关新闻，请直接回答'未找到相关内容'
3. 禁止编造任何日期、股价或事件
4. 所有股价数据必须以akshare库中的数据为准
5. 如果新闻日期不是当日，请标注为'过往信息'
6. 严禁推荐任何非A股市场的虚构代号
7. 给出推荐理由时，必须引用搜索结果中的具体原话
8. 如果数据不足，请明确说明'数据不足，无法判断'
9. 不要编造任何技术指标、财务数据或新闻事件
10. 所有结论必须基于提供的真实数据
"""

# AI量化选股专用提示词
QUANT_PICKER_PROMPT = """
你是一位资深基金经理，请从以下股票中选出3只今日最具潜力的股票。

{anti_hallucination_rules}

【提供的真实数据】:
{stock_data}

【要求】:
1. 只能从上述列表中选择，不得推荐其他股票
2. 推荐理由必须基于提供的真实数据（涨跌幅、换手率、舆情评分）
3. 如果舆情评分为0或无数据，请说明'无舆情数据支持'
4. 止盈位计算必须基于当前价格，不得编造
5. 如果数据不足以做出判断，请明确说明
6. 严禁编造任何新闻、政策或事件
7. 所有股票代码必须是真实存在的A股代码

【输出格式】:
### 1. [股票名称] ([股票代码])

**技术面**:
- 当前价格: [从数据中获取]元
- 涨跌幅: [从数据中获取]%
- 换手率: [从数据中获取]%
- 市值: [从数据中获取]亿

**舆情面**:
- 舆情评分: [从数据中获取]/100
- [如果有舆情数据，说明来源；如果没有，说明'无舆情数据']

**推荐理由**:
[必须基于提供的真实数据，不得编造]

**止盈位**: [当前价格 × (1 + 合理涨幅)]元

**风险提示**: [基于真实数据的风险提示]
"""

# 微博情绪分析专用提示词
WEIBO_SENTIMENT_PROMPT = """
请分析以下微博内容的情绪倾向，给出0-100的情绪分数。

{anti_hallucination_rules}

【提供的真实微博内容】:
{weibo_content}

【要求】:
1. 只能基于提供的微博内容进行分析
2. 如果内容不足以判断情绪，请说明'内容不足，无法判断'
3. 不要编造任何微博内容或事件
4. 风险点和机会点必须从微博内容中提取，不得编造
5. 如果微博中没有提到具体事件，不要编造事件
6. 日期信息必须来自微博原文，不得编造

【输出格式】:
情绪分数: [0-100]

3个风险点:
1. [从微博内容中提取，如果没有则说明'未提及']
2. [从微博内容中提取，如果没有则说明'未提及']
3. [从微博内容中提取，如果没有则说明'未提及']

3个机会点:
1. [从微博内容中提取，如果没有则说明'未提及']
2. [从微博内容中提取，如果没有则说明'未提及']
3. [从微博内容中提取，如果没有则说明'未提及']
"""

# 全网热点发现专用提示词
DISCOVERY_ENGINE_PROMPT = """
请从以下热度异常升高的关键词中，识别出3个最值得关注的投资板块。

{anti_hallucination_rules}

【提供的真实数据】:
{keyword_data}

【要求】:
1. 只能从提供的关键词列表中选择
2. 升温原因必须基于真实的热度变化数据
3. 不要编造任何新闻、政策或事件
4. 相关股票必须是真实存在的A股股票
5. 如果无法确定升温原因，请说明'原因不明，需进一步观察'
6. 投资建议必须保守，不得夸大
7. 风险提示必须充分

【输出格式】:
### 1. [板块名称]

**热度变化**:
- 今日讨论: [从数据中获取]次
- 昨日讨论: [从数据中获取]次
- 增长率: [从数据中计算]%

**升温原因**:
[基于热度变化的合理推测，不得编造具体事件]

**相关股票**:
[只列出真实存在的A股股票，如果不确定则说明'需进一步研究']

**投资建议**:
[保守建议，强调风险]

**风险提示**:
[充分的风险提示]
"""

# 政客交易追踪专用提示词
POLITICIAN_TRACKER_PROMPT = """
请过滤以下Twitter推文，只保留包含具体政策、项目拨款、考察调研等实词的推文。

{anti_hallucination_rules}

【提供的真实推文】:
{tweets}

【要求】:
1. 只能从提供的推文列表中筛选
2. 必须包含以下实词之一：政策、法案、拨款、项目、考察、调研、合同、订单、投资、并购、监管、审批、基础设施、补贴、税收、关税
3. 排除包含以下口水话的推文：啊、！！、to the moon、买买买
4. 不要编造任何推文内容
5. 如果所有推文都是口水话，请返回空列表

【输出格式】:
[有价值的推文列表，每行一条]
"""


def get_prompt_with_rules(prompt_template, **kwargs):
    """
    获取包含防幻觉规则的完整提示词
    
    参数:
        prompt_template: 提示词模板
        **kwargs: 模板参数
    
    返回:
        str: 完整的提示词
    """
    # 添加防幻觉规则
    kwargs['anti_hallucination_rules'] = ANTI_HALLUCINATION_RULES
    
    # 格式化提示词
    return prompt_template.format(**kwargs)


# 数据验证函数
def validate_stock_code(code):
    """
    验证股票代码是否为有效的A股代码
    
    参数:
        code: 股票代码
    
    返回:
        bool: 是否有效
    """
    if not code:
        return False
    
    # A股代码格式：6位数字
    if not code.isdigit() or len(code) != 6:
        return False
    
    # 上海：60开头，科创板：688开头
    # 深圳：00开头，中小板：002开头，创业板：300开头
    valid_prefixes = ['60', '688', '00', '002', '300']
    
    return any(code.startswith(prefix) for prefix in valid_prefixes)


def validate_price(price):
    """
    验证价格是否合理
    
    参数:
        price: 价格
    
    返回:
        bool: 是否合理
    """
    try:
        price = float(price)
        # A股价格一般在0.01-1000之间
        return 0.01 <= price <= 1000
    except:
        return False


def validate_date(date_str):
    """
    验证日期是否为今天或过去
    
    参数:
        date_str: 日期字符串
    
    返回:
        tuple: (是否有效, 是否为今天)
    """
    from datetime import datetime
    
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        today = datetime.now().date()
        
        # 日期不能是未来
        if date.date() > today:
            return False, False
        
        # 是否为今天
        is_today = date.date() == today
        
        return True, is_today
    except:
        return False, False


def add_data_source_note(text, source):
    """
    为文本添加数据来源说明
    
    参数:
        text: 原文本
        source: 数据来源
    
    返回:
        str: 添加来源说明的文本
    """
    return f"{text}\n\n**数据来源**: {source}"


def mark_historical_info(text):
    """
    标记过往信息
    
    参数:
        text: 原文本
    
    返回:
        str: 标记后的文本
    """
    return f"【过往信息】{text}"


# 示例用法
if __name__ == "__main__":
    # 测试股票代码验证
    print("测试股票代码验证:")
    print(f"600000: {validate_stock_code('600000')}")  # True
    print(f"000001: {validate_stock_code('000001')}")  # True
    print(f"300001: {validate_stock_code('300001')}")  # True
    print(f"AAPL: {validate_stock_code('AAPL')}")      # False
    print(f"12345: {validate_stock_code('12345')}")    # False
    
    # 测试价格验证
    print("\n测试价格验证:")
    print(f"25.60: {validate_price(25.60)}")   # True
    print(f"0.01: {validate_price(0.01)}")     # True
    print(f"1000: {validate_price(1000)}")     # True
    print(f"-10: {validate_price(-10)}")       # False
    print(f"10000: {validate_price(10000)}")   # False
    
    # 测试日期验证
    print("\n测试日期验证:")
    from datetime import datetime, timedelta
    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    
    print(f"今天 {today}: {validate_date(today)}")
    print(f"昨天 {yesterday}: {validate_date(yesterday)}")
    print(f"明天 {tomorrow}: {validate_date(tomorrow)}")
