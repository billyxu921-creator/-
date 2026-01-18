#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整分析流程 - 集成DeepSeek AI
演示如何在股吧分析中集成AI深度分析
"""

from guba_analyzer import GubaAnalyzer
from deepseek_analyzer import DeepSeekAnalyzer
from intelligence_analyzer import IntelligenceAnalyzer
from dark_horse_finder import DarkHorseFinder
from datetime import datetime
import pandas as pd
import os


def run_analysis_with_ai(api_key=None):
    """运行包含AI分析的完整流程"""
    
    print("=" * 80)
    print("股票投资智能分析系统 - AI增强版")
    print("=" * 80)
    print()
    
    # 步骤1: 获取股吧热点
    print("【步骤1】获取股吧热点数据")
    print("-" * 80)
    guba_analyzer = GubaAnalyzer()
    posts_df = guba_analyzer.get_guba_trends(max_pages=3)
    
    if posts_df.empty:
        print("未获取到股吧数据")
        return
    
    print(f"✓ 获取到 {len(posts_df)} 条帖子")
    print()
    
    # 步骤2: DeepSeek AI深度分析 ⭐ 新增
    print("【步骤2】DeepSeek AI深度分析")
    print("-" * 80)
    deepseek_analyzer = DeepSeekAnalyzer(api_key=api_key)
    
    # 调用AI分析
    ai_analysis_df = deepseek_analyzer.analyze_posts(
        posts_df, 
        batch_size=10,  # 每批处理10条
        delay=1         # 请求间隔1秒
    )
    
    if not ai_analysis_df.empty:
        print(f"✓ AI分析完成，识别到 {len(ai_analysis_df)} 条有效信息")
        
        # 生成AI分析报告
        ai_report = deepseek_analyzer.generate_analysis_report(ai_analysis_df)
        print("\n" + ai_report)
        
        # 将AI分析结果合并到原始数据
        posts_df = merge_ai_results(posts_df, ai_analysis_df)
    else:
        print("× AI分析未返回结果，继续使用传统分析")
    
    print()
    
    # 步骤3: 传统情报分析
    print("【步骤3】传统情报分析")
    print("-" * 80)
    intel_analyzer = IntelligenceAnalyzer()
    intelligence_df = intel_analyzer.analyze_intelligence(posts_df)
    
    if intelligence_df.empty:
        print("未提取到有效情报")
        return
    
    print(f"✓ 提取到 {len(intelligence_df)} 条有价值情报")
    print()
    
    # 步骤4: 黑马发现
    print("【步骤4】黑马股票发现")
    print("-" * 80)
    dark_horse_finder = DarkHorseFinder()
    dark_horse_report = dark_horse_finder.generate_dark_horse_report(intelligence_df)
    
    print()
    print(dark_horse_report)
    
    # 步骤5: 保存所有结果
    print()
    print("【步骤5】保存分析结果")
    print("-" * 80)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    os.makedirs('reports', exist_ok=True)
    
    # 保存AI分析结果
    if not ai_analysis_df.empty:
        ai_file = f"reports/ai_analysis_{timestamp}.csv"
        ai_analysis_df.to_csv(ai_file, index=False, encoding='utf-8-sig')
        print(f"✓ AI分析结果已保存: {ai_file}")
        
        ai_report_file = f"reports/ai_report_{timestamp}.txt"
        with open(ai_report_file, 'w', encoding='utf-8') as f:
            f.write(ai_report)
        print(f"✓ AI分析报告已保存: {ai_report_file}")
    
    # 保存情报分析
    intel_file = f"reports/intelligence_{timestamp}.csv"
    intelligence_df.to_csv(intel_file, index=False, encoding='utf-8-sig')
    print(f"✓ 情报分析已保存: {intel_file}")
    
    # 保存黑马报告
    dark_horse_file = f"reports/dark_horse_{timestamp}.txt"
    with open(dark_horse_file, 'w', encoding='utf-8') as f:
        f.write(dark_horse_report)
    print(f"✓ 黑马报告已保存: {dark_horse_file}")
    
    # 生成综合对比报告
    if not ai_analysis_df.empty:
        comparison_report = generate_comparison_report(ai_analysis_df, intelligence_df)
        comparison_file = f"reports/comparison_{timestamp}.txt"
        with open(comparison_file, 'w', encoding='utf-8') as f:
            f.write(comparison_report)
        print(f"✓ 对比报告已保存: {comparison_file}")
    
    print()
    print("=" * 80)
    print("分析完成！")
    print("=" * 80)


def merge_ai_results(posts_df, ai_analysis_df):
    """将AI分析结果合并到原始帖子数据"""
    # 为每条帖子添加AI分析字段
    posts_df['AI情绪分值'] = None
    posts_df['AI核心逻辑'] = None
    posts_df['AI置信度'] = None
    
    for idx, post_row in posts_df.iterrows():
        title = post_row['标题']
        
        # 查找对应的AI分析结果
        matching_ai = ai_analysis_df[ai_analysis_df['原始标题'] == title]
        
        if not matching_ai.empty:
            ai_row = matching_ai.iloc[0]
            posts_df.at[idx, 'AI情绪分值'] = ai_row['sentiment_score']
            posts_df.at[idx, 'AI核心逻辑'] = ai_row['key_logic']
            posts_df.at[idx, 'AI置信度'] = ai_row['confidence_level']
    
    return posts_df


def generate_comparison_report(ai_analysis_df, intelligence_df):
    """生成AI分析与传统分析的对比报告"""
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("AI分析 vs 传统分析 对比报告")
    report_lines.append(f"生成时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
    report_lines.append("=" * 80)
    report_lines.append("")
    
    # 数据量对比
    report_lines.append("【数据量对比】")
    report_lines.append(f"AI分析识别标的: {len(ai_analysis_df)} 个")
    report_lines.append(f"传统分析识别情报: {len(intelligence_df)} 条")
    report_lines.append("")
    
    # AI分析优势
    report_lines.append("【AI分析优势】")
    report_lines.append("✓ 情绪量化: 提供-1.0到1.0的精确情绪分值")
    report_lines.append("✓ 置信度评估: 自动评估信息可信度")
    report_lines.append("✓ 核心逻辑提取: 一句话总结关键论点")
    report_lines.append("✓ 自然语言理解: 更好地理解复杂表述")
    report_lines.append("")
    
    # 传统分析优势
    report_lines.append("【传统分析优势】")
    report_lines.append("✓ 规则明确: 基于预定义关键词，可解释性强")
    report_lines.append("✓ 分类详细: 技术派/筹码派/基本面三维分类")
    report_lines.append("✓ 无需API: 不依赖外部服务，成本低")
    report_lines.append("✓ 响应快速: 本地处理，速度快")
    report_lines.append("")
    
    # 情绪分布对比
    if not ai_analysis_df.empty:
        avg_sentiment = ai_analysis_df['sentiment_score'].mean()
        avg_confidence = ai_analysis_df['confidence_level'].mean()
        
        report_lines.append("【AI分析洞察】")
        report_lines.append(f"市场平均情绪: {avg_sentiment:.2f}")
        
        if avg_sentiment > 0.3:
            report_lines.append("  → 市场整体偏乐观")
        elif avg_sentiment < -0.3:
            report_lines.append("  → 市场整体偏悲观")
        else:
            report_lines.append("  → 市场情绪中性")
        
        report_lines.append(f"平均置信度: {avg_confidence:.2f}")
        
        if avg_confidence > 0.7:
            report_lines.append("  → 信息质量较高，论据充分")
        elif avg_confidence > 0.5:
            report_lines.append("  → 信息质量中等")
        else:
            report_lines.append("  → 信息质量偏低，需谨慎对待")
        
        report_lines.append("")
    
    # 建议
    report_lines.append("【综合建议】")
    report_lines.append("1. 结合使用: AI分析提供情绪和置信度，传统分析提供分类和论据")
    report_lines.append("2. 交叉验证: 两种方法识别的共同标的更值得关注")
    report_lines.append("3. 优势互补: AI擅长理解语义，传统方法擅长规则匹配")
    report_lines.append("4. 成本考虑: 根据预算选择合适的分析方式")
    report_lines.append("")
    
    report_lines.append("=" * 80)
    
    return "\n".join(report_lines)


if __name__ == "__main__":
    # 从配置文件读取API Key
    try:
        from config import DEEPSEEK_CONFIG
        API_KEY = DEEPSEEK_CONFIG['api_key']
        print(f"✓ 已从配置文件加载API Key")
    except ImportError:
        # 如果没有配置文件，尝试从环境变量读取
        import os
        API_KEY = os.getenv('DEEPSEEK_API_KEY', 'YOUR_DEEPSEEK_API_KEY')
        if API_KEY == 'YOUR_DEEPSEEK_API_KEY':
            print("⚠️  警告: 未找到API Key配置")
            print("请创建 config.py 文件或设置环境变量 DEEPSEEK_API_KEY")
    
    # 运行分析
    run_analysis_with_ai(api_key=API_KEY)