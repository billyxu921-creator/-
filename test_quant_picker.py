#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
量化选股器测试脚本
"""

from Quant_Picker import QuantPicker
import pandas as pd


def test_quant_picker():
    """测试量化选股器"""
    
    print("=" * 60)
    print("测试量化选股器")
    print("=" * 60)
    print()
    
    print("⚠️  重要提示:")
    print("1. 需要akshare库获取实时行情数据")
    print("2. 需要DeepSeek API Key进行AI分析")
    print("3. 建议在交易时间运行（9:30-15:00）")
    print("4. 首次运行可能需要5-10分钟")
    print()
    
    response = input("是否继续测试？(y/n): ")
    
    if response.lower() != 'y':
        print("测试已取消")
        return
    
    print("\n开始测试...")
    print()
    
    try:
        # 创建选股器实例
        picker = QuantPicker()
        
        # 运行完整流程
        picker.run()
        
        print("\n✅ 测试完成！")
        print("\n请查看生成的文件:")
        print("  - AI潜力股推荐_*.md")
        print("  - quant_picker_candidates_*.csv")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断测试")
    
    except Exception as e:
        print(f"\n× 测试失败: {e}")
        import traceback
        traceback.print_exc()


def test_components():
    """测试各个组件"""
    
    print("=" * 60)
    print("测试各个组件")
    print("=" * 60)
    print()
    
    picker = QuantPicker()
    
    # 测试1: AkShare数据获取
    print("【测试1】AkShare数据获取")
    print("-" * 60)
    
    try:
        df = picker.step1_akshare_screening()
        
        if not df.empty:
            print(f"✅ 成功获取 {len(df)} 只股票")
        else:
            print("⚠️  未筛选到符合条件的股票")
    
    except Exception as e:
        print(f"❌ 失败: {e}")
    
    print()
    
    # 测试2: 舆情数据加载
    print("【测试2】舆情数据加载")
    print("-" * 60)
    
    try:
        sentiment_data = picker._load_sentiment_data()
        
        if sentiment_data:
            print(f"✅ 成功加载 {len(sentiment_data)} 条舆情数据")
        else:
            print("⚠️  未找到舆情数据")
    
    except Exception as e:
        print(f"❌ 失败: {e}")
    
    print()
    
    # 测试3: API连接
    print("【测试3】DeepSeek API连接")
    print("-" * 60)
    
    try:
        test_input = "测试输入"
        result = picker._call_deepseek_for_selection(test_input)
        
        if result:
            print("✅ API连接成功")
        else:
            print("⚠️  API返回为空")
    
    except Exception as e:
        print(f"❌ 失败: {e}")
    
    print()
    
    print("=" * 60)
    print("组件测试完成")
    print("=" * 60)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--components':
        test_components()
    else:
        test_quant_picker()
