#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
包含政客交易追踪的完整分析脚本
"""

import subprocess
import sys
from datetime import datetime


def run_all_modules():
    """运行所有分析模块"""
    print("=" * 60)
    print("运行完整分析（包含政客交易追踪）")
    print("=" * 60)
    print(f"\n开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    modules = [
        ('黄金股票筛选', 'gold_stock_screener.py', 300),
        ('AI量化选股', 'Quant_Picker.py', 600),
        ('微博情绪分析', 'weibo_sentiment_weighted.py', 600),
        ('全网热点发现', 'Discovery_Engine.py', 900),
        ('政客交易追踪', 'politician_trade_tracker.py', 300)
    ]
    
    results = {}
    
    for i, (name, script, timeout) in enumerate(modules, 1):
        print(f"\n【{i}/{len(modules)}】{name}...")
        
        try:
            result = subprocess.run(
                ['python3', script],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            success = result.returncode == 0
            results[name] = success
            
            print("✓ 完成" if success else "× 失败")
            
            if not success and result.stderr:
                print(f"  错误: {result.stderr[:200]}")
        
        except subprocess.TimeoutExpired:
            print(f"× 超时（>{timeout}秒）")
            results[name] = False
        
        except Exception as e:
            print(f"× 失败: {e}")
            results[name] = False
    
    # 总结
    print("\n" + "=" * 60)
    print("执行总结")
    print("=" * 60)
    
    success_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    
    for name, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {name}")
    
    print(f"\n成功: {success_count}/{total_count}")
    print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 列出生成的文件
    print("\n" + "=" * 60)
    print("生成的报告文件")
    print("=" * 60)
    
    import glob
    
    report_patterns = [
        'gold_stocks_analysis_*.csv',
        'AI潜力股推荐_*.md',
        '微博黄金情绪分析_*.md',
        '全网雷达_*.md',
        '权力资金动态_*.md'
    ]
    
    for pattern in report_patterns:
        files = glob.glob(pattern)
        if files:
            latest = max(files, key=lambda x: x)
            print(f"✓ {latest}")
        else:
            print(f"× 未找到: {pattern}")
    
    return success_count == total_count


if __name__ == "__main__":
    success = run_all_modules()
    sys.exit(0 if success else 1)
