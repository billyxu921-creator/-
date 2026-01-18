#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改进版A股股票筛选和评分系统
增加了更好的错误处理和重试机制
"""

import akshare as ak
import pandas as pd
import numpy as np
import time
import warnings
from datetime import datetime, timedelta
import re

warnings.filterwarnings('ignore')

class StockScreener:
    def __init__(self):
        """初始化股票筛选器"""
        self.keywords = {
            '分红': ['分红', '派息', '现金分红', '股息'],
            'IPO/上市计划': ['IPO', '上市', '发行', '首发'],
            'H股发行': ['H股', '港股', '香港上市'],
            '黄金/矿产': ['黄金', '矿产', '矿业', '金矿', '铜矿', '铁矿'],
            '化肥': ['化肥', '磷肥', '钾肥', '复合肥', '尿素'],
            '机器人/AI': ['机器人', '人工智能', 'AI', '自动化', '智能制造']
        }
        
        self.official_capital_keywords = [
            '全国社保基金', '社保基金', '国资委', '汇金', '证金',
            '中央汇金', '证金公司', '国有资产', '国投', '中投'
        ]
        
    def retry_request(self, func, max_retries=3, delay=1):
        """重试机制"""
        for attempt in range(max_retries):
            try:
                result = func()
                return result
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                print(f"    请求失败，{delay}秒后重试... (尝试 {attempt + 1}/{max_retries})")
                time.sleep(delay)
        return None
    
    def get_stock_list(self):
        """获取A股股票列表"""
        print("正在获取A股股票列表...")
        try:
            stock_list = self.retry_request(lambda: ak.stock_info_a_code_name())
            print(f"获取到 {len(stock_list)} 只股票")
            return stock_list
        except Exception as e:
            print(f"获取股票列表失败: {e}")
            return pd.DataFrame()
    
    def get_stock_basic_info(self, stock_code):
        """获取股票基本信息"""
        try:
            stock_individual_info = self.retry_request(
                lambda: ak.stock_individual_info_em(symbol=stock_code)
            )
            
            # 转换为字典格式便于处理
            info_dict = {}
            for _, row in stock_individual_info.iterrows():
                info_dict[row['item']] = row['value']
            
            return info_dict
        except Exception as e:
            print(f"    获取基本信息失败: {e}")
            return {}
    
    def get_stock_holders(self, stock_code):
        """获取股票十大股东信息"""
        try:
            holders = self.retry_request(
                lambda: ak.stock_zh_a_gdhs(symbol=stock_code),
                max_retries=2,  # 股东信息经常失败，减少重试次数
                delay=2
            )
            return holders
        except Exception as e:
            print(f"    获取股东信息失败: {e}")
            return pd.DataFrame()
    
    def check_market_cap_criteria(self, info_dict):
        """检查市值和股本条件"""
        try:
            # 从基本信息中提取数据
            total_shares_str = str(info_dict.get('总股本', '0'))
            
            # 处理科学计数法和单位转换
            if 'e' in total_shares_str.lower():
                total_shares = float(total_shares_str) / 1e8  # 转换为亿股
            else:
                total_shares = float(total_shares_str) / 1e8  # 假设原始数据是股数
            
            # 尝试获取流通市值（可能需要计算）
            current_price = float(info_dict.get('最新', 0))
            circulating_shares_str = str(info_dict.get('流通股', '0'))
            
            if 'e' in circulating_shares_str.lower():
                circulating_shares = float(circulating_shares_str) / 1e8
            else:
                circulating_shares = float(circulating_shares_str) / 1e8
            
            # 计算流通市值（亿元）
            circulating_market_cap = current_price * circulating_shares
            
            # 检查条件
            shares_criteria = 8 <= total_shares <= 15
            market_cap_criteria = 105 <= circulating_market_cap <= 195
            
            return shares_criteria, market_cap_criteria, total_shares, circulating_market_cap
        except Exception as e:
            print(f"    解析市值数据失败: {e}")
            return False, False, 0, 0
    
    def check_official_capital(self, holders_df):
        """检查是否包含官方资本"""
        if holders_df.empty:
            return False, []
        
        found_officials = []
        try:
            holder_names = holders_df['股东名称'].astype(str).tolist()
            
            for holder in holder_names:
                for keyword in self.official_capital_keywords:
                    if keyword in holder:
                        found_officials.append(holder)
                        break
        except Exception as e:
            print(f"    检查官方资本失败: {e}")
            return False, []
        
        return len(found_officials) > 0, found_officials
    
    def calculate_stock_score(self, stock_code, stock_name):
        """计算单只股票的综合评分"""
        print(f"正在分析股票: {stock_code} - {stock_name}")
        
        # 获取基本信息
        basic_info = self.get_stock_basic_info(stock_code)
        if not basic_info:
            print(f"    跳过：无法获取基本信息")
            return None
        
        # 检查市值和股本条件
        shares_ok, market_cap_ok, total_shares, circulating_market_cap = self.check_market_cap_criteria(basic_info)
        
        if not shares_ok:
            print(f"    跳过：股本不符合条件 ({total_shares:.2f}亿股)")
            return None
        
        if not market_cap_ok:
            print(f"    跳过：流通市值不符合条件 ({circulating_market_cap:.2f}亿元)")
            return None
        
        print(f"    ✓ 基本条件符合 - 总股本: {total_shares:.2f}亿股, 流通市值: {circulating_market_cap:.2f}亿元")
        
        # 初始化评分
        score_details = {
            '股票代码': stock_code,
            '股票名称': stock_name,
            '总股本(亿股)': round(total_shares, 2),
            '流通市值(亿元)': round(circulating_market_cap, 2),
            '股本匹配分': 0,
            '官方背书分': 0,
            '增持动向分': 0,
            '题材热度分': 0,
            '分红预期分': 0,
            '总分': 0
        }
        
        # 1. 股本匹配评分 (25分)
        if 8 <= total_shares <= 12:
            score_details['股本匹配分'] = 25
        elif 12 < total_shares <= 15:
            score_details['股本匹配分'] = 20
        
        # 2. 获取股东信息并评分 (30分)
        holders_df = self.get_stock_holders(stock_code)
        has_official, official_list = self.check_official_capital(holders_df)
        if has_official:
            score_details['官方背书分'] = 30
            print(f"    ✓ 发现官方资本: {official_list[:2]}...")  # 只显示前2个
        
        # 简化版评分：由于网络限制，暂时跳过公告和分红数据
        # 可以根据需要后续添加
        
        # 计算总分
        score_details['总分'] = (score_details['股本匹配分'] + 
                               score_details['官方背书分'] + 
                               score_details['增持动向分'] + 
                               score_details['题材热度分'] + 
                               score_details['分红预期分'])
        
        print(f"    综合评分: {score_details['总分']}分")
        
        # 添加延时避免请求过频
        time.sleep(1)
        
        return score_details
    
    def screen_stocks(self, max_stocks=50):
        """筛选股票并评分"""
        print("开始筛选A股股票...")
        print(f"筛选条件: 总股本8-15亿股, 流通市值105-195亿元")
        print(f"将处理前 {max_stocks} 只股票\n")
        
        # 获取股票列表
        stock_list = self.get_stock_list()
        if stock_list.empty:
            print("无法获取股票列表")
            return pd.DataFrame()
        
        results = []
        processed_count = 0
        
        for _, row in stock_list.iterrows():
            if processed_count >= max_stocks:
                break
                
            stock_code = row['code']
            stock_name = row['name']
            
            try:
                score_result = self.calculate_stock_score(stock_code, stock_name)
                if score_result:
                    results.append(score_result)
                    print(f"    ✓ 符合条件，已加入结果列表")
                    
                processed_count += 1
                
                # 每处理10只股票显示进度
                if processed_count % 10 == 0:
                    print(f"\n--- 进度: {processed_count}/{max_stocks}, 找到符合条件的 {len(results)} 只 ---\n")
                    
            except Exception as e:
                print(f"    处理股票 {stock_code} 时出错: {e}")
                processed_count += 1
                continue
        
        if results:
            results_df = pd.DataFrame(results)
            # 按总分排序
            results_df = results_df.sort_values('总分', ascending=False)
            return results_df
        else:
            return pd.DataFrame()
    
    def print_summary(self, results_df):
        """打印筛选结果摘要"""
        if results_df.empty:
            print("未找到符合条件的股票")
            return
        
        print(f"\n{'='*60}")
        print(f"筛选结果摘要")
        print(f"{'='*60}")
        print(f"符合条件的股票总数: {len(results_df)}")
        print(f"平均总分: {results_df['总分'].mean():.1f}")
        print(f"最高分: {results_df['总分'].max()}")
        
        print(f"\n符合条件的股票列表:")
        print("-" * 100)
        print(f"{'代码':<8} {'名称':<12} {'总分':<6} {'股本(亿)':<10} {'市值(亿)':<10} {'股本分':<8} {'官方分':<8}")
        print("-" * 100)
        
        for _, row in results_df.iterrows():
            print(f"{row['股票代码']:<8} {row['股票名称']:<12} "
                  f"{row['总分']:<6.0f} {row['总股本(亿股)']:<10.2f} "
                  f"{row['流通市值(亿元)']:<10.2f} {row['股本匹配分']:<8.0f} "
                  f"{row['官方背书分']:<8.0f}")


def main():
    """主函数"""
    print("A股股票筛选和评分系统 (改进版)")
    print("=" * 50)
    
    # 创建筛选器实例
    screener = StockScreener()
    
    # 设置要处理的股票数量
    max_stocks = 50  # 先处理50只进行测试
    
    # 开始筛选
    results = screener.screen_stocks(max_stocks=max_stocks)
    
    if not results.empty:
        # 打印摘要
        screener.print_summary(results)
        
        # 保存结果
        filename = f"stock_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        results.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n详细结果已保存到: {filename}")
    else:
        print("\n未找到符合所有条件的股票")
        print("建议:")
        print("1. 增加处理的股票数量")
        print("2. 检查网络连接")
        print("3. 稍后重试")


if __name__ == "__main__":
    main()