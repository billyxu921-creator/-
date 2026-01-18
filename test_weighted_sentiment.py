#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
加权情绪分析测试脚本
测试博主影响力加权、关键词加成、加权公式计算
"""

from weibo_sentiment_weighted import WeiboSentimentWeightedAnalyzer
import pandas as pd


def test_influence_weight():
    """测试影响力权重计算"""
    print("=" * 60)
    print("测试1: 影响力权重计算")
    print("=" * 60)
    print()
    
    analyzer = WeiboSentimentWeightedAnalyzer()
    
    test_cases = [
        (5000000, 10, "500万粉丝"),
        (1000000, 10, "100万粉丝"),
        (500000, 3, "50万粉丝"),
        (100000, 3, "10万粉丝"),
        (50000, 1, "5万粉丝"),
        (1000, 1, "1千粉丝"),
    ]
    
    print("粉丝数 → 影响力权重")
    print("-" * 40)
    
    for followers, expected_weight, desc in test_cases:
        weight = analyzer.calculate_influence_weight(followers)
        status = "✅" if weight == expected_weight else "❌"
        print(f"{status} {desc:15s} ({followers:>8,}) → 权重 ×{weight}")
    
    print()


def test_keyword_boost():
    """测试关键词加成检测"""
    print("=" * 60)
    print("测试2: 关键词加成检测")
    print("=" * 60)
    print()
    
    analyzer = WeiboSentimentWeightedAnalyzer()
    
    test_texts = [
        ("黄金价格今日涨停，市场情绪高涨", True, ["涨停"]),
        ("某公司宣布重组计划，股价大涨", True, ["重组"]),
        ("国资委入股黄金企业，利好消息", True, ["入股"]),
        ("黄金价格上涨，投资者关注", False, []),
        ("今天天气不错", False, []),
    ]
    
    print("文本内容 → 关键词加成")
    print("-" * 60)
    
    for text, expected_boost, expected_keywords in test_texts:
        has_boost, matched_kw = analyzer.detect_keyword_boost(text)
        status = "✅" if has_boost == expected_boost else "❌"
        
        print(f"{status} {text[:30]:30s}")
        print(f"   加成: {'是' if has_boost else '否':2s} | 关键词: {', '.join(matched_kw) if matched_kw else '无'}")
        print()


def test_weighted_calculation():
    """测试加权公式计算"""
    print("=" * 60)
    print("测试3: 加权公式计算")
    print("=" * 60)
    print()
    
    analyzer = WeiboSentimentWeightedAnalyzer()
    
    test_cases = [
        # (AI分数, 关键词加成, 影响力权重, 描述)
        (50, False, 1, "普通博主，无关键词"),
        (50, True, 1, "普通博主，有关键词"),
        (50, False, 3, "中影响力博主，无关键词"),
        (50, True, 3, "中影响力博主，有关键词"),
        (50, False, 10, "高影响力博主，无关键词"),
        (50, True, 10, "高影响力博主，有关键词"),
        (80, True, 10, "高影响力博主，高分+关键词"),
        (20, False, 1, "普通博主，低分"),
    ]
    
    print("AI分数 | 关键词 | 权重 | 最终分数 | 说明")
    print("-" * 80)
    
    for ai_score, has_boost, weight, desc in test_cases:
        result = analyzer.calculate_weighted_sentiment(ai_score, has_boost, weight)
        
        print(f"{ai_score:6d} | {'是':4s} | ×{weight:2d} | {result['final_score']:8.2f} | {desc}")
        print(f"       | {'否' if not has_boost else '  ':4s} |      | "
              f"(加成:{result['keyword_bonus']:5.1f}, 加权:{result['weighted_score']:6.1f})")
        print()


def test_full_workflow():
    """测试完整工作流程（使用模拟数据）"""
    print("=" * 60)
    print("测试4: 完整工作流程（模拟数据）")
    print("=" * 60)
    print()
    
    analyzer = WeiboSentimentWeightedAnalyzer()
    
    # 创建模拟数据
    mock_data = {
        '博主名': [
            '财经大V', '投资专家', '普通用户A', '黄金分析师', '普通用户B',
            '知名博主', '普通用户C', '行业专家', '普通用户D', '财经评论员'
        ],
        '粉丝数': [
            2000000, 500000, 5000, 1500000, 3000,
            800000, 2000, 300000, 1500, 1200000
        ],
        '博文内容': [
            '黄金价格今日涨停，市场情绪高涨！',
            '某黄金企业宣布重组计划，利好消息',
            '黄金价格上涨，值得关注',
            '国资委入股黄金企业，重大利好',
            '今天黄金涨了不少',
            '黄金投资机会来了，建议关注',
            '黄金价格波动较大',
            '黄金板块技术面突破，看涨',
            '黄金还会涨吗？',
            '黄金市场分析：涨停预期强烈'
        ],
        '点赞数': [5000, 1200, 50, 3000, 20, 800, 15, 600, 10, 2000],
        '转发数': [2000, 500, 10, 1500, 5, 300, 3, 200, 2, 800],
        '发布时间': ['1小时前'] * 10
    }
    
    df = pd.DataFrame(mock_data)
    
    # 计算影响力权重
    df['影响力权重'] = df['粉丝数'].apply(analyzer.calculate_influence_weight)
    
    # 检测关键词加成
    df['关键词加成'] = df['博文内容'].apply(lambda x: analyzer.detect_keyword_boost(x)[0])
    df['匹配关键词'] = df['博文内容'].apply(
        lambda x: ','.join(analyzer.detect_keyword_boost(x)[1])
    )
    
    print("【模拟数据统计】")
    print(f"总微博数: {len(df)}")
    print(f"高影响力博主: {len(df[df['影响力权重'] == 10])}")
    print(f"中影响力博主: {len(df[df['影响力权重'] == 3])}")
    print(f"普通博主: {len(df[df['影响力权重'] == 1])}")
    print(f"包含关键词加成: {len(df[df['关键词加成'] == True])}")
    print()
    
    print("【前5条微博详情】")
    print("-" * 80)
    
    for i, (_, row) in enumerate(df.head(5).iterrows(), 1):
        print(f"{i}. @{row['博主名']} (粉丝:{row['粉丝数']:,}, 权重:×{row['影响力权重']})")
        print(f"   内容: {row['博文内容']}")
        print(f"   关键词加成: {'是' if row['关键词加成'] else '否'} "
              f"({row['匹配关键词'] if row['匹配关键词'] else '无'})")
        print(f"   互动: 👍{row['点赞数']} 🔄{row['转发数']}")
        print()
    
    # 计算加权分数示例
    print("【加权分数计算示例】")
    print("-" * 80)
    
    ai_base_score = 65  # 假设AI基础分数为65
    
    print(f"假设AI基础分数: {ai_base_score}")
    print()
    
    for i, (_, row) in enumerate(df.head(3).iterrows(), 1):
        result = analyzer.calculate_weighted_sentiment(
            ai_score=ai_base_score,
            has_boost=row['关键词加成'],
            influence_weight=row['影响力权重']
        )
        
        print(f"{i}. @{row['博主名']}")
        print(f"   AI基础分数: {result['ai_score']}")
        print(f"   关键词加成: +{result['keyword_bonus']:.1f}")
        print(f"   影响力权重: ×{result['influence_weight']}")
        print(f"   加权分数: {result['weighted_score']:.1f}")
        print(f"   最终分数: {result['final_score']:.2f} (归一化后)")
        print()
    
    print("✅ 完整工作流程测试完成")
    print()


def main():
    """主函数"""
    print("\n")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║                                                          ║")
    print("║          加权情绪分析系统 - 功能测试                     ║")
    print("║                                                          ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print("\n")
    
    # 运行所有测试
    test_influence_weight()
    test_keyword_boost()
    test_weighted_calculation()
    test_full_workflow()
    
    print("=" * 60)
    print("✅ 所有测试完成！")
    print("=" * 60)
    print()
    
    print("【加权公式说明】")
    print()
    print("Final_Score = (AI_Sentiment_Score + Keyword_Bonus) × Influence_Weight")
    print()
    print("其中:")
    print("  - AI_Sentiment_Score: DeepSeek AI分析的基础分数 (0-100)")
    print("  - Keyword_Bonus: AI分数 × 20% (如果包含关键词)")
    print("  - Influence_Weight: 博主影响力权重 (1, 3, 或 10)")
    print()
    print("归一化:")
    print("  - 最大可能值: (100 + 20) × 10 = 1200")
    print("  - 归一化公式: (Final_Score / 1200) × 100")
    print("  - 确保最终分数在 0-100 之间")
    print()
    
    print("【使用方法】")
    print()
    print("运行加权优化版分析:")
    print("  python3 weibo_sentiment_weighted.py")
    print()


if __name__ == "__main__":
    main()
