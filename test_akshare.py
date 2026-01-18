#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试akshare库的基本功能
"""

import akshare as ak
import pandas as pd
import sys

def test_basic_functions():
    """测试akshare基本功能"""
    print("开始测试akshare基本功能...")
    
    try:
        # 测试1: 获取股票列表
        print("1. 测试获取A股股票列表...")
        stock_list = ak.stock_info_a_code_name()
        print(f"   成功获取 {len(stock_list)} 只股票")
        print(f"   前5只股票: ")
        print(stock_list.head())
        
    except Exception as e:
        print(f"   获取股票列表失败: {e}")
        return False
    
    try:
        # 测试2: 获取单只股票信息
        print("\n2. 测试获取单只股票信息...")
        test_code = stock_list.iloc[0]['code']  # 取第一只股票
        print(f"   测试股票代码: {test_code}")
        
        stock_info = ak.stock_individual_info_em(symbol=test_code)
        print(f"   成功获取股票信息，共 {len(stock_info)} 项数据")
        print("   部分信息:")
        print(stock_info.head())
        
    except Exception as e:
        print(f"   获取股票信息失败: {e}")
        return False
    
    try:
        # 测试3: 获取股东信息
        print(f"\n3. 测试获取股东信息...")
        holders = ak.stock_zh_a_gdhs(symbol=test_code)
        print(f"   成功获取股东信息，共 {len(holders)} 条记录")
        if not holders.empty:
            print("   前3大股东:")
            print(holders.head(3))
        
    except Exception as e:
        print(f"   获取股东信息失败: {e}")
        print("   这可能是正常的，某些股票可能没有股东数据")
    
    print("\n基本功能测试完成!")
    return True

if __name__ == "__main__":
    success = test_basic_functions()
    if success:
        print("\n✅ akshare库工作正常，可以继续使用完整的筛选程序")
    else:
        print("\n❌ akshare库存在问题，请检查网络连接或稍后重试")
        sys.exit(1)