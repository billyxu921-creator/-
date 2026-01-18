#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
黄金行业股票筛选和评分系统 - 最终版
专门分析黄金行业股票，满足任一条件即可进入筛选池，综合评分
"""

import akshare as ak
import pandas as pd
import numpy as np
import time
import warnings
from datetime import datetime

warnings.filterwarnings('ignore')

class GoldStockFinalScreener:
    def __init__(self):
        """初始化黄金股票筛选器"""
        self.official_capital_keywords = [
            '全国社保基金', '社保基金', '国资委', '汇金', '证金',
            '中央汇金', '证金公司', '国有资产', '国投', '中投'
        ]
        
    def get_gold_stocks(self):
        """获取黄金行业股票列表"""
        print("正在获取黄金行业股票...")
        
        try:
            # 获取行业分类
            industry_stocks = ak.stock_board_industry_name_em()
            print(f"获取到 {len(industry_stocks)} 个行业分类")
            
            # 查找黄金相关行业
            gold_industries = industry_stocks[
                industry_stocks['板块名称'].str.contains('黄金|贵金属|金矿', na=False)
            ]
            
            if not gold_industries.empty:
                print(f"找到黄金相关行业: {gold_industries['板块名称'].tolist()}")
                
                # 获取黄金行业的股票
                gold_stocks_list = []
                for _, industry in gold_industries.iterrows():
                    industry_name = industry['板块名称']
                    print(f"获取 {industry_name} 行业股票...")
                    
                    try:
                        stocks_in_industry = ak.stock_board_industry_cons_em(symbol=industry_name)
                        if not stocks_in_industry.empty:
                            stocks_in_industry['行业'] = industry_name
                            gold_stocks_list.append(stocks_in_industry)
                            print(f"  找到 {len(stocks_in_industry)} 只股票")
                    except Exception as e:
                        print(f"  获取 {industry_name} 行业股票失败: {e}")
                
                if gold_stocks_list:
                    gold_stocks = pd.concat(gold_stocks_list, ignore_index=True)
                    return gold_stocks
            
            # 备用方案：通过名称关键词筛选
            print("使用备用方案：通过股票名称关键词筛选...")
            all_stocks = ak.stock_info_a_code_name()
            gold_keywords = ['黄金', '金矿', '贵金属', '紫金', '山金', '中金黄金', '赤峰黄金', '湖南黄金']
            
            gold_stocks = all_stocks[
                all_stocks['name'].str.contains('|'.join(gold_keywords), na=False)
            ].copy()
            
            if not gold_stocks.empty:
                gold_stocks['行业'] = '黄金相关'
                return gold_stocks
            
        except Exception as e:
            print(f"获取黄金股票失败: {e}")
        
        return pd.DataFrame()
    
    def get_stock_basic_info(self, stock_code):
        """获取股票基本信息"""
        try:
            stock_info = ak.stock_individual_info_em(symbol=stock_code)
            info_dict = {}
            for _, row in stock_info.iterrows():
                info_dict[row['item']] = row['value']
            return info_dict
        except Exception as e:
            print(f"    获取基本信息失败: {e}")
            return {}
    
    def get_stock_holders_simple(self, stock_code):
        """简化版获取股东信息"""
        try:
            # 尝试获取十大股东
            holders = ak.stock_zh_a_gdhs(symbol=stock_code)
            return holders
        except:
            # 如果失败，尝试其他方法或返回空
            try:
                # 备用方法：获取股东人数变化（可能包含一些股东信息）
                holder_num = ak.stock_zh_a_gdhs_detail_em(symbol=stock_code)
                return holder_num
            except:
                return pd.DataFrame()
    
    def check_conditions(self, info_dict, holders_df):
        """检查所有筛选条件"""
        conditions = {
            '股本匹配': False,
            '市值匹配': False,
            '官方背书': False,
            '黄金行业': True  # 已经是黄金行业股票
        }
        
        details = {}
        
        try:
            # 1. 检查股本条件 (8-15亿股)
            total_shares_str = str(info_dict.get('总股本', '0'))
            if 'e' in total_shares_str.lower():
                total_shares = float(total_shares_str) / 1e8
            else:
                total_shares = float(total_shares_str) / 1e8
            
            details['总股本'] = total_shares
            if 8 <= total_shares <= 15:
                conditions['股本匹配'] = True
            
            # 2. 检查流通市值条件 (105-195亿元)
            current_price = float(info_dict.get('最新', 0))
            circulating_shares_str = str(info_dict.get('流通股', '0'))
            
            if 'e' in circulating_shares_str.lower():
                circulating_shares = float(circulating_shares_str) / 1e8
            else:
                circulating_shares = float(circulating_shares_str) / 1e8
            
            circulating_market_cap = current_price * circulating_shares
            details['流通市值'] = circulating_market_cap
            details['当前价格'] = current_price
            
            if 105 <= circulating_market_cap <= 195:
                conditions['市值匹配'] = True
            
            # 3. 检查官方资本
            if not holders_df.empty and '股东名称' in holders_df.columns:
                holder_names = holders_df['股东名称'].astype(str).tolist()
                for holder in holder_names:
                    for keyword in self.official_capital_keywords:
                        if keyword in holder:
                            conditions['官方背书'] = True
                            details['官方股东'] = holder
                            break
                    if conditions['官方背书']:
                        break
            
        except Exception as e:
            print(f"    检查条件时出错: {e}")
        
        return conditions, details
    
    def calculate_score(self, conditions, details):
        """根据条件计算评分"""
        score = 0
        score_breakdown = {
            '股本匹配分': 0,
            '官方背书分': 0,
            '市值加分': 0,
            '黄金行业分': 15
        }
        
        # 股本匹配评分 (25分)
        if conditions['股本匹配']:
            total_shares = details.get('总股本', 0)
            if 8 <= total_shares <= 12:
                score_breakdown['股本匹配分'] = 25
            elif 12 < total_shares <= 15:
                score_breakdown['股本匹配分'] = 20
        
        # 官方背书评分 (30分)
        if conditions['官方背书']:
            score_breakdown['官方背书分'] = 30
        
        # 市值匹配额外加分 (5分)
        if conditions['市值匹配']:
            score_breakdown['市值加分'] = 5
        
        # 计算总分
        total_score = sum(score_breakdown.values())
        
        return total_score, score_breakdown
    
    def analyze_gold_stock(self, stock_code, stock_name, industry):
        """分析单只黄金股票"""
        print(f"正在分析: {stock_code} - {stock_name}")
        
        # 获取基本信息
        basic_info = self.get_stock_basic_info(stock_code)
        if not basic_info:
            print(f"    跳过：无法获取基本信息")
            return None
        
        # 获取股东信息
        holders_df = self.get_stock_holders_simple(stock_code)
        
        # 检查条件
        conditions, details = self.check_conditions(basic_info, holders_df)
        
        # 计算评分
        total_score, score_breakdown = self.calculate_score(conditions, details)
        
        # 统计符合的条件
        met_conditions = [k for k, v in conditions.items() if v]
        
        # 构建结果
        result = {
            '股票代码': stock_code,
            '股票名称': stock_name,
            '所属行业': industry,
            '总股本(亿股)': round(details.get('总股本', 0), 2),
            '流通市值(亿元)': round(details.get('流通市值', 0), 2),
            '当前价格': round(details.get('当前价格', 0), 2),
            '符合条件': ', '.join(met_conditions),
            '符合条件数': len(met_conditions),
            '总分': total_score,
            **score_breakdown
        }
        
        # 显示分析结果
        print(f"    总股本: {result['总股本(亿股)']}亿股, 流通市值: {result['流通市值(亿元)']}亿元")
        print(f"    符合条件: {result['符合条件']}")
        print(f"    综合评分: {total_score}分")
        
        if conditions['官方背书'] and '官方股东' in details:
            print(f"    官方股东: {details['官方股东']}")
        
        time.sleep(0.5)  # 避免请求过频
        return result
    
    def screen_and_score(self):
        """筛选和评分黄金股票"""
        print("黄金行业股票筛选和评分系统 - 最终版")
        print("=" * 60)
        print("评分规则:")
        print("• 股本匹配 (25分): 8-15亿股")
        print("• 官方背书 (30分): 十大股东包含官方资本")
        print("• 市值匹配 (5分): 流通市值105-195亿元")
        print("• 黄金行业 (15分): 属于黄金/贵金属行业")
        print("• 满足任一条件即可进入筛选池分析")
        print("=" * 60)
        
        # 获取黄金股票
        gold_stocks = self.get_gold_stocks()
        if gold_stocks.empty:
            print("未找到黄金行业股票")
            return pd.DataFrame()
        
        print(f"\n找到 {len(gold_stocks)} 只黄金相关股票，开始分析...\n")
        
        results = []
        for idx, row in gold_stocks.iterrows():
            # 处理列名差异
            if '代码' in gold_stocks.columns:
                stock_code = row['代码']
                stock_name = row['名称']
            else:
                stock_code = row['code']
                stock_name = row['name']
            
            industry = row.get('行业', '黄金相关')
            
            try:
                result = self.analyze_gold_stock(stock_code, stock_name, industry)
                if result:
                    results.append(result)
                print(f"    完成 ({idx + 1}/{len(gold_stocks)})\n")
            except Exception as e:
                print(f"    分析失败: {e}\n")
                continue
        
        if results:
            results_df = pd.DataFrame(results)
            results_df = results_df.sort_values('总分', ascending=False)
            return results_df
        
        return pd.DataFrame()
    
    def print_final_summary(self, results_df):
        """打印最终分析摘要"""
        if results_df.empty:
            print("未找到分析结果")
            return
        
        print(f"\n{'='*80}")
        print(f"黄金行业股票最终分析报告")
        print(f"{'='*80}")
        print(f"分析股票总数: {len(results_df)}")
        print(f"平均总分: {results_df['总分'].mean():.1f}")
        print(f"最高分: {results_df['总分'].max()}")
        
        # 按评分区间统计
        high_score = len(results_df[results_df['总分'] >= 50])
        medium_score = len(results_df[(results_df['总分'] >= 30) & (results_df['总分'] < 50)])
        low_score = len(results_df[results_df['总分'] < 30])
        
        print(f"\n评分分布:")
        print(f"高分股票 (≥50分): {high_score} 只")
        print(f"中等股票 (30-49分): {medium_score} 只")
        print(f"基础股票 (<30分): {low_score} 只")
        
        print(f"\n详细排名:")
        print("-" * 120)
        print(f"{'排名':<4} {'代码':<8} {'名称':<12} {'总分':<6} {'股本(亿)':<10} {'市值(亿)':<10} {'价格':<8} {'符合条件':<20}")
        print("-" * 120)
        
        for i, (_, row) in enumerate(results_df.iterrows(), 1):
            print(f"{i:<4} {row['股票代码']:<8} {row['股票名称']:<12} "
                  f"{row['总分']:<6.0f} {row['总股本(亿股)']:<10.2f} "
                  f"{row['流通市值(亿元)']:<10.2f} {row['当前价格']:<8.2f} "
                  f"{row['符合条件']:<20}")
        
        # 重点推荐
        top_5 = results_df.head(5)
        print(f"\n🏆 重点推荐 (前5名):")
        print("-" * 60)
        for i, (_, row) in enumerate(top_5.iterrows(), 1):
            print(f"{i}. {row['股票代码']} {row['股票名称']} - {row['总分']:.0f}分")
            advantages = []
            if row['股本匹配分'] > 0:
                advantages.append(f"股本适中({row['总股本(亿股)']}亿)")
            if row['官方背书分'] > 0:
                advantages.append("官方背景")
            if row['市值加分'] > 0:
                advantages.append("市值合理")
            advantages.append("黄金行业")
            
            print(f"   优势: {', '.join(advantages)}")
            print()


def main():
    """主函数"""
    screener = GoldStockFinalScreener()
    
    # 执行筛选和评分
    results = screener.screen_and_score()
    
    if not results.empty:
        # 打印摘要
        screener.print_final_summary(results)
        
        # 保存结果
        filename = f"gold_stocks_final_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        results.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n📊 详细结果已保存到: {filename}")
        
        # 给出投资建议
        top_stock = results.iloc[0]
        print(f"\n💡 投资建议:")
        print(f"推荐关注: {top_stock['股票代码']} {top_stock['股票名称']}")
        print(f"推荐理由: 综合评分最高({top_stock['总分']:.0f}分)，{top_stock['符合条件']}")
        
    else:
        print("未找到符合条件的黄金股票")


if __name__ == "__main__":
    main()