#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全网热点发现引擎测试脚本
"""

from Discovery_Engine import DiscoveryEngine
import sys


def test_discovery_engine():
    """测试全网热点发现引擎"""
    
    print("=" * 60)
    print("测试全网热点发现引擎")
    print("=" * 60)
    print()
    
    print("⚠️  重要提示:")
    print("1. 本测试需要真实浏览器环境（headless=False）")
    print("2. 需要手动登录小红书和微博（扫码或账号密码）")
    print("3. 抓取过程较慢（5.5-12.2秒随机等待），请耐心等待")
    print("4. 如遇验证码，会发出提示音，请手动处理")
    print()
    
    # 询问用户是否继续
    response = input("是否继续测试？(y/n): ")
    
    if response.lower() != 'y':
        print("测试已取消")
        return
    
    print("\n开始测试...")
    print()
    
    try:
        # 创建发现引擎实例
        engine = DiscoveryEngine()
        
        # 运行发现流程
        # 测试时减少抓取数量，加快速度
        engine.run(
            xhs_count=20,  # 小红书抓取20条（测试用）
            headless=False  # 显示浏览器
        )
        
        print("\n✅ 测试完成！")
        print("\n请查看生成的文件:")
        print("  - discovery_raw_*.csv (原始数据)")
        print("  - 全网雷达报告_*.md (分析简报)")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断测试")
        sys.exit(0)
    
    except Exception as e:
        print(f"\n× 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_discovery_engine()
