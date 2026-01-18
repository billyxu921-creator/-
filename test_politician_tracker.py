#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
政客交易追踪模块测试脚本
"""

from politician_trade_tracker import PoliticianTradeTracker


def test_tracker():
    """测试追踪器"""
    print("=" * 60)
    print("测试政客交易追踪模块")
    print("=" * 60)
    print()
    
    # 创建追踪器
    tracker = PoliticianTradeTracker()
    
    # 运行完整流程
    report_file = tracker.run()
    
    if report_file:
        print(f"\n✅ 测试成功！报告已生成: {report_file}")
        
        # 显示报告内容
        print("\n" + "=" * 60)
        print("报告预览")
        print("=" * 60)
        
        with open(report_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # 只显示前50行
            lines = content.split('\n')[:50]
            print('\n'.join(lines))
            
            if len(content.split('\n')) > 50:
                print("\n... (更多内容请查看完整报告)")
    else:
        print("\n× 测试失败")


if __name__ == "__main__":
    test_tracker()
