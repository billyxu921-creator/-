#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股股票筛选和评分系统
使用akshare库筛选符合条件的A股股票并进行量化评分
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
        
    def get_stock_list(self):
        """获取A股股票列表"""
        print("正在获取A股股票列表...")
        try:
            stock_list = ak.stock_info_a_code_name()
            print(f"获取到 {len(stock_list)} 只股票")
            return stock_list
        except Exception as e:
            print(f"获取股票列表失败: {e}")
            return pd.DataFrame()
    
    def get_stock_basic_info(self, stock_code):
        """获取股票基本信息"""
        try:
            # 获取股票基本信息
            stock_individual_info = ak.stock_individual_info_em(symbol=stock_code)
            
            # 转换为字典格式便于处理
            info_dict = {}
            for _, row in stock_individual_info.iterrows():
                info_dict[row['item']] = row['value']
            
            return info_dict
        except Exception as e:
            print(f"获取股票 {stock_code} 基本信息失败: {e}")
            return {}
    
    def get_stock_holders(self, stock_code):
        """获取股票十大股东信息"""
        try:
            holders = ak.stock_zh_a_gdhs(symbol=stock_code)
            return holders
        except Exception as e:
            print(f"获取股票 {stock_code} 股东信息失败: {e}")
            return pd.DataFrame()
    
    def get_stock_announcements(self, stock_code, days=90):
        """获取股票公告信息"""
        try:
            end_date = datetime.now().strftime('%Y%m%d')
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')
            
            announcements = ak.stock_zh_a_hist_notice(
                symbol=stock_code,
                start_date=start_date,
                end_date=end_date
            )
            return announcements
        except Exception as e:
            print(f"获取股票 {stock_code} 公告信息失败: {e}")
            return pd.DataFrame()
    
    def get_dividend_info(self, stock_code):
        """获取股票分红信息"""
        try:
            dividend_info = ak.stock_zh_a_dividend(symbol=stock_code)
            return dividend_info
        except Exception as e:
            print(f"获取股票 {stock_code} 分红信息失败: {e}")
            return pd.DataFrame()
    
    def check_market_cap_criteria(self, info_dict):
        """检查市值和股本条件"""
        try:
            # 总股本 (亿股)
            total_shares = float(info_dict.get('总股本', 0))
            # 流通市值 (亿元)
            circulating_market_cap = float(info_dict.get('流通市值', 0))
            
            # 检查总股本是否在8-15亿区间
            shares_criteria = 8 <= total_shares <= 15
            
            # 检查流通市值是否接近150亿 (允许±30%的浮动)
            market_cap_criteria = 105 <= circulating_market_cap <= 195
            
            return shares_criteria, market_cap_criteria, total_shares, circulating_market_cap
        except:
            return False, False, 0, 0
    
    def check_official_capital(self, holders_df):
        """检查是否包含官方资本"""
        if holders_df.empty:
            return False, []
        
        found_officials = []
        holder_names = holders_df['股东名称'].astype(str).tolist()
        
        for holder in holder_names:
            for keyword in self.official_capital_keywords:
                if keyword in holder:
                    found_officials.append(holder)
                    break
        
        return len(found_officials) > 0, found_officials
    
    def check_recent_buyback(self, announcements_df):
        """检查近期是否有大股东增持公告"""
        if announcements_df.empty:
            return False, []
        
        buyback_keywords = ['增持', '回购', '股份增持', '大股东增持']
        found_announcements = []
        
        for _, row in announcements_df.iterrows():
            title = str(row.get('公告标题', ''))
            for keyword in buyback_keywords:
                if keyword in title:
                    found_announcements.append(title)
                    break
        
        return len(found_announcements) > 0, found_announcements
    
    def check_keywords_in_announcements(self, announcements_df):
        """检查公告中是否包含关键词"""
        if announcements_df.empty:
            return {}
        
        keyword_matches = {category: [] for category in self.keywords.keys()}
        
        for _, row in announcements_df.iterrows():
            title = str(row.get('公告标题', ''))
            content = str(row.get('公告摘要', ''))
            full_text = title + ' ' + content
            
            for category, keywords in self.keywords.items():
                for keyword in keywords:
                    if keyword in full_text:
                        keyword_matches[category].append(title)
                        break
        
        return keyword_matches
    
    def calculate_dividend_score(self, dividend_df, industry_avg=0.03):
        """计算分红评分"""
        if dividend_df.empty:
            return 0, 0
        
        try:
            # 获取最近3年的分红数据
            recent_dividends = dividend_df.head(3)
            
            # 计算平均股息率
            dividend_rates = []
            for _, row in recent_dividends.iterrows():
                dividend_rate = float(row.get('股息率(%)', 0)) / 100
                if dividend_rate > 0:
                    dividend_rates.append(dividend_rate)
            
            if not dividend_rates:
                return 0, 0
            
            avg_dividend_rate = np.mean(dividend_rates)
            
            # 评分逻辑：高于4%或高于行业平均水平
            if avg_dividend_rate >= 0.04 or avg_dividend_rate > industry_avg:
                return 10, avg_dividend_rate
            elif avg_dividend_rate > 0.02:
                return 5, avg_dividend_rate
            else:
                return 2, avg_dividend_rate
                
        except:
            return 0, 0
    
    def calculate_stock_score(self, stock_code, stock_name):
        """计算单只股票的综合评分"""
        print(f"正在分析股票: {stock_code} - {stock_name}")
        
        # 获取基本信息
        basic_info = self.get_stock_basic_info(stock_code)
        if not basic_info:
            return None
        
        # 检查市值和股本条件
        shares_ok, market_cap_ok, total_shares, circulating_market_cap = self.check_market_cap_criteria(basic_info)
        
        if not shares_ok:
            print(f"  股本不符合条件: {total_shares}亿股")
            return None
        
        if not market_cap_ok:
            print(f"  流通市值不符合条件: {circulating_market_cap}亿元")
            return None
        
        print(f"  基本条件符合 - 总股本: {total_shares}亿股, 流通市值: {circulating_market_cap}亿元")
        
        # 初始化评分
        score_details = {
            '股票代码': stock_code,
            '股票名称': stock_name,
            '总股本(亿股)': total_shares,
            '流通市值(亿元)': circulating_market_cap,
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
            print(f"  发现官方资本: {official_list}")
        
        # 3. 获取公告信息
        announcements_df = self.get_stock_announcements(stock_code)
        
        # 检查增持公告 (20分)
        has_buyback, buyback_list = self.check_recent_buyback(announcements_df)
        if has_buyback:
            score_details['增持动向分'] = 20
            print(f"  发现增持公告: {len(buyback_list)}条")
        
        # 检查关键词匹配 (15分)
        keyword_matches = self.check_keywords_in_announcements(announcements_df)
        keyword_score = 0
        for category, matches in keyword_matches.items():
            if matches:
                keyword_score += 3  # 每个类别3分，最多15分
                print(f"  发现{category}相关公告: {len(matches)}条")
        score_details['题材热度分'] = min(keyword_score, 15)
        
        # 4. 分红评分 (10分)
        dividend_df = self.get_dividend_info(stock_code)
        dividend_score, avg_dividend_rate = self.calculate_dividend_score(dividend_df)
        score_details['分红预期分'] = dividend_score
        if dividend_score > 0:
            print(f"  平均股息率: {avg_dividend_rate:.2%}")
        
        # 计算总分
        score_details['总分'] = (score_details['股本匹配分'] + 
                               score_details['官方背书分'] + 
                               score_details['增持动向分'] + 
                               score_details['题材热度分'] + 
                               score_details['分红预期分'])
        
        print(f"  综合评分: {score_details['总分']}分")
        
        # 添加延时避免请求过频
        time.sleep(0.5)
        
        return score_details
    
    def screen_stocks(self, max_stocks=100):
        """筛选股票并评分"""
        print("开始筛选A股股票...")
        
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
                    
                processed_count += 1
                
                # 每处理10只股票显示进度
                if processed_count % 10 == 0:
                    print(f"已处理 {processed_count} 只股票，找到符合条件的 {len(results)} 只")
                    
            except Exception as e:
                print(f"处理股票 {stock_code} 时出错: {e}")
                continue
        
        if results:
            results_df = pd.DataFrame(results)
            # 按总分排序
            results_df = results_df.sort_values('总分', ascending=False)
            return results_df
        else:
            return pd.DataFrame()
    
    def save_results(self, results_df, filename=None):
        """保存结果到文件"""
        if filename is None:
            filename = f"stock_screening_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        results_df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"结果已保存到: {filename}")
        return filename
    
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
        print(f"最低分: {results_df['总分'].min()}")
        
        print(f"\n前10名股票:")
        print("-" * 80)
        top_10 = results_df.head(10)
        for _, row in top_10.iterrows():
            print(f"{row['股票代码']} {row['股票名称']:8} | "
                  f"总分:{row['总分']:3.0f} | "
                  f"股本:{row['股本匹配分']:2.0f} | "
                  f"官方:{row['官方背书分']:2.0f} | "
                  f"增持:{row['增持动向分']:2.0f} | "
                  f"题材:{row['题材热度分']:2.0f} | "
                  f"分红:{row['分红预期分']:2.0f}")


def main():
    """主函数"""
    print("A股股票筛选和评分系统")
    print("=" * 50)
    
    # 创建筛选器实例
    screener = StockScreener()
    
    # 设置要处理的股票数量（可以根据需要调整）
    max_stocks = 200  # 处理前200只股票进行测试
    
    print(f"将处理前 {max_stocks} 只股票进行筛选...")
    print("筛选条件:")
    print("- 总股本: 8-15亿股")
    print("- 流通市值: 105-195亿元 (目标150亿±30%)")
    print("- 包含官方资本或近期增持")
    print("- 关键词匹配和分红情况")
    print()
    
    # 开始筛选
    results = screener.screen_stocks(max_stocks=max_stocks)
    
    if not results.empty:
        # 打印摘要
        screener.print_summary(results)
        
        # 保存结果
        filename = screener.save_results(results)
        
        print(f"\n详细结果已保存到 {filename}")
        print("可以使用 Excel 或其他工具打开查看完整数据")
    else:
        print("未找到符合所有条件的股票")
        print("建议:")
        print("1. 增加处理的股票数量")
        print("2. 适当放宽筛选条件")
        print("3. 检查数据源是否正常")


if __name__ == "__main__":
    main()