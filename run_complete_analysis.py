#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整分析流程示例
演示如何从股吧分析到黑马发现的完整流程
"""

from guba_analyzer import GubaAnalyzer
from intelligence_analyzer import IntelligenceAnalyzer
from dark_horse_finder import DarkHorseFinder
from datetime import datetime
import pandas as pd


def run_complete_analysis():
    """运行完整的分析流程"""
    
    print("=" * 80)
    print("股票投资智能分析系统 - 完整分析流程")
    print("=" * 80)
    print()
    
    # 步骤1: 获取股吧热点
    print("【步骤1】获取股吧热点数据")
    print("-" * 80)
    guba_analyzer = GubaAnalyzer()
    posts_df = guba_analyzer.get_guba_trends(max_pages=3)
    
    if posts_df.empty:
        print("未获取到股吧数据，使用模拟数据进行演示...")
        posts_df = create_demo_data()
    
    print(f"✓ 获取到 {len(posts_df)} 条帖子")
    print()
    
    # 步骤2: 情报分析
    print("【步骤2】情报深度分析")
    print("-" * 80)
    intel_analyzer = IntelligenceAnalyzer()
    intelligence_df = intel_analyzer.analyze_intelligence(posts_df)
    
    if intelligence_df.empty:
        print("未提取到有效情报")
        return
    
    print(f"✓ 提取到 {len(intelligence_df)} 条有价值情报")
    
    # 显示情报摘要
    print("\n情报摘要:")
    print(f"  平均评分: {intelligence_df['价值评分'].mean():.1f}/10")
    print(f"  高价值情报(≥8分): {len(intelligence_df[intelligence_df['价值评分'] >= 8])} 条")
    
    category_counts = intelligence_df['主要分类'].value_counts()
    print(f"  分类分布: {dict(category_counts)}")
    print()
    
    # 步骤3: 黑马发现
    print("【步骤3】黑马股票发现")
    print("-" * 80)
    dark_horse_finder = DarkHorseFinder()
    report = dark_horse_finder.generate_dark_horse_report(intelligence_df)
    
    # 显示报告
    print()
    print(report)
    
    # 保存所有结果
    print()
    print("【步骤4】保存分析结果")
    print("-" * 80)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 保存情报分析
    intel_file = f"intelligence_analysis_{timestamp}.csv"
    intelligence_df.to_csv(intel_file, index=False, encoding='utf-8-sig')
    print(f"✓ 情报分析已保存: {intel_file}")
    
    # 保存黑马报告
    report_file = f"dark_horse_report_{timestamp}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"✓ 黑马报告已保存: {report_file}")
    
    print()
    print("=" * 80)
    print("分析完成！")
    print("=" * 80)


def create_demo_data():
    """创建演示数据（小盘股）"""
    demo_data = {
        '标题': [
            '某小盘黄金股大单压盘明显，主力吸筹迹象',
            '这只8亿股本的黄金股筹码集中度提升，国企改革预期',
            '小盘黄金股KDJ低位金叉，MACD即将金叉',
            '某黄金股北向资金持续流入，社保增持',
            '流通市值150亿的黄金股底部放量突破',
            '小盘黄金股中字头重组传闻，资产注入预期',
            '黄金板块中的小盘股机会来了',
            '某黄金股主力建仓明显，筹码锁定',
            '小市值黄金股政策利好，行业景气度提升',
            '黄金股中的黑马，业绩拐点明确'
        ],
        '内容': [
            '今日观察到某小盘黄金股有明显的大单压盘迹象，主力资金在低位吸筹，筹码逐步集中。该股流通股本约8亿股，流通市值150亿左右，符合黑马特征。',
            '这只股本8亿的黄金股作为国企，近期有改革预期，可能涉及资产重组。筹码集中度明显提升。',
            '技术面看，KDJ指标在低位形成金叉，MACD即将金叉，底部信号明确。该股市值不大，有爆发潜力。',
            '某黄金股获北向资金持续流入，社保基金二季度增持明显。流通市值约150亿，属于中小盘。',
            '底部放量突破前期平台，主力建仓特征明显，成交量温和放大。该股流通市值150亿左右。',
            '市场传闻某小盘黄金股可能涉及中字头企业重组，资产注入预期强烈。',
            '黄金板块中的小盘股机会来了，流通股本10亿以内的标的值得关注。',
            '某黄金股主力建仓明显，筹码高度锁定，浮筹很少，一旦启动空间巨大。',
            '小市值黄金股受益于政策利好，行业景气度持续提升，业绩有望超预期。',
            '发现一只黄金股黑马，业绩拐点明确，从亏损到盈利，估值修复空间大。'
        ],
        '阅读量': [5000, 4500, 3000, 4000, 3500, 5500, 2000, 3000, 2500, 4500],
        '评论数': [50, 45, 30, 40, 35, 55, 20, 30, 25, 45],
        '帖子链接': [''] * 10,
        '股票代码': [''] * 10,
        '发布时间': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')] * 10
    }
    
    return pd.DataFrame(demo_data)


if __name__ == "__main__":
    run_complete_analysis()