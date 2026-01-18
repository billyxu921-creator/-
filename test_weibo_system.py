#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博情绪分析系统 - 测试脚本
使用模拟数据测试系统功能（不需要真实抓取微博）
"""

import pandas as pd
from datetime import datetime
from weibo_gold_sentiment import WeiboGoldSentimentAnalyzer


def create_mock_weibo_data():
    """创建模拟微博数据"""
    mock_data = {
        '博主名': [
            '财经观察员', '黄金投资者', '市场分析师', '理财达人',
            '金融小白', '投资老手', '经济学人', '股市风云',
            '贵金属专家', '财富管理', '金融评论', '市场观察',
            '投资顾问', '理财规划师', '金融分析师'
        ],
        '博文内容': [
            '黄金突破2100美元，创历史新高！避险情绪持续升温，建议关注黄金ETF',
            '今天黄金又涨了，感觉要起飞了。美联储降息预期增强，黄金配置价值凸显',
            '技术面看，黄金已经突破关键阻力位，MACD金叉，建议逢低布局',
            '黄金涨这么多，会不会有回调风险？短期可能超买，注意控制仓位',
            '第一次买黄金，不知道现在是不是好时机？求大神指点',
            '持有黄金3年了，终于回本了！长期看好黄金的避险价值',
            '美元走弱对黄金形成支撑，地缘政治风险也在推升金价',
            '央行持续购金，这是长期利好信号。黄金作为战略储备的地位不可动摇',
            '黄金ETF资金流入创新高，机构投资者看好后市',
            '现在买黄金会不会太晚？感觉已经涨了很多了',
            '黄金和美债收益率负相关，当前环境下黄金配置价值明显',
            '短期可能有技术性回调，但长期趋势依然向上',
            '通胀预期回升，黄金作为抗通胀资产受到青睐',
            '黄金矿业股也跟着大涨，关注龙头企业',
            '建议黄金配置比例不超过总资产的10-15%，分散风险'
        ],
        '发布时间': [
            '2小时前', '3小时前', '5小时前', '6小时前',
            '8小时前', '10小时前', '12小时前', '14小时前',
            '16小时前', '18小时前', '20小时前', '22小时前',
            '1天前', '1天前', '1天前'
        ],
        '点赞数': [
            2341, 1567, 892, 654, 234, 1890, 1234, 2100,
            876, 432, 1456, 789, 1678, 543, 987
        ],
        '转发数': [
            567, 234, 123, 89, 45, 456, 234, 512,
            178, 67, 289, 134, 345, 98, 187
        ]
    }
    
    return pd.DataFrame(mock_data)


def test_system():
    """测试系统功能"""
    print("=" * 60)
    print("微博情绪分析系统 - 功能测试")
    print("=" * 60)
    print()
    print("使用模拟数据测试系统功能...")
    print()
    
    # 创建分析器
    analyzer = WeiboGoldSentimentAnalyzer()
    
    # 1. 创建模拟数据
    print("步骤1: 创建模拟微博数据...")
    df = create_mock_weibo_data()
    print(f"✓ 创建了 {len(df)} 条模拟微博")
    print()
    
    # 保存原始数据
    raw_filename = f"weibo_raw_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(raw_filename, index=False, encoding='utf-8-sig')
    print(f"原始数据已保存: {raw_filename}")
    print()
    
    # 2. 数据清洗
    print("步骤2: 数据清洗...")
    df_clean = analyzer.clean_data(df)
    print()
    
    # 保存清洗后的数据
    clean_filename = f"weibo_clean_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df_clean.to_csv(clean_filename, index=False, encoding='utf-8-sig')
    print(f"清洗数据已保存: {clean_filename}")
    print()
    
    # 3. AI分析
    print("步骤3: AI情绪分析...")
    analysis_result = analyzer.analyze_sentiment_with_ai(df_clean)
    
    if analysis_result:
        print("\nAI分析结果:")
        print(f"  情绪指数: {analysis_result.get('sentiment_index', 'N/A')}/100")
        print(f"  情绪标签: {analysis_result.get('sentiment_label', 'N/A')}")
        print(f"  一句话总结: {analysis_result.get('summary', 'N/A')}")
    print()
    
    # 4. 生成报告
    print("步骤4: 生成分析报告...")
    report_file = analyzer.generate_report(df_clean, analysis_result)
    print()
    
    # 显示报告内容
    print("=" * 60)
    print("报告预览")
    print("=" * 60)
    with open(report_file, 'r', encoding='utf-8') as f:
        content = f.read()
        # 只显示前50行
        lines = content.split('\n')[:50]
        print('\n'.join(lines))
        if len(content.split('\n')) > 50:
            print("\n... (更多内容请查看完整报告)")
    
    print()
    print("=" * 60)
    print("✅ 测试完成！")
    print("=" * 60)
    print()
    print("生成文件:")
    print(f"  - 原始数据: {raw_filename}")
    print(f"  - 清洗数据: {clean_filename}")
    print(f"  - 分析报告: {report_file}")
    print()
    print("提示: 这是使用模拟数据的测试")
    print("运行真实分析: python3 weibo_gold_sentiment.py")


if __name__ == "__main__":
    test_system()