#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
黄金行业股票筛选和评分系统
专门分析所属行业为"黄金"的A股股票
"""

import akshare as ak
import pandas as pd
import numpy as np
import time
import warnings
from datetime import datetime, timedelta

warnings.filterwarnings('ignore')

class GoldStockScreener:
    def __init__(self):
        """初始化黄金股票筛选器"""
        self.gold_keywords = [
            '黄金', '金矿', '贵金属', '金业', '金山', '金叶', 
            '紫金', '山东黄金', '中金黄金', '赤峰黄金', '湖南黄金'
        ]
        
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
    
    def get_gold_stocks(self):
        """获取黄金行业股票列表"""
        print("正在获取黄金行业股票...")
        
        try:
            # 方法1: 通过行业分类获取
            try:
                industry_stocks = self.retry_request(lambda: ak.stock_board_industry_name_em())
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
                            stocks_in_industry = self.retry_request(
                                lambda: ak.stock_board_industry_cons_em(symbol=industry_name)
                            )
                            if not stocks_in_industry.empty:
                                stocks_in_industry['行业'] = industry_name
                                gold_stocks_list.append(stocks_in_industry)
                                print(f"  找到 {len(stocks_in_industry)} 只股票")
                        except Exception as e:
                            print(f"  获取 {industry_name} 行业股票失败: {e}")
                    
                    if gold_stocks_list:
                        gold_stocks = pd.concat(gold_stocks_list, ignore_index=True)
                        print(f"通过行业分类找到 {len(gold_stocks)} 只黄金相关股票")
                        return gold_stocks
                        
            except Exception as e:
                print(f"通过行业分类获取失败: {e}")
            
            # 方法2: 通过股票名称关键词筛选
            print("尝试通过股票名称关键词筛选...")
            all_stocks = self.retry_request(lambda: ak.stock_info_a_code_name())
            
            gold_stocks = all_stocks[
                all_stocks['name'].str.contains('|'.join(self.gold_keywords), na=False)
            ].copy()
            
            if not gold_stocks.empty:
                gold_stocks['行业'] = '黄金相关'
                print(f"通过名称关键词找到 {len(gold_stocks)} 只黄金相关股票")
                return gold_stocks
            else:
                print("未找到黄金相关股票")
                return pd.DataFrame()
                
        except Exception as e:
            print(f"获取黄金股票失败: {e}")
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
                max_retries=2,
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
                total_shares = float(total_shares_str) / 1e8
            
            # 获取当前价格和流通股计算流通市值
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
    
    def get_stock_price_info(self, stock_code):
        """获取股票价格相关信息"""
        try:
            # 获取最近的价格数据
            price_data = self.retry_request(
                lambda: ak.stock_zh_a_hist(symbol=stock_code, period="daily", 
                                         start_date="20240101", end_date="20241231", adjust="")
            )
            
            if not price_data.empty:
                latest_data = price_data.iloc[-1]
                return {
                    '最新价格': latest_data['收盘'],
                    '涨跌幅': latest_data.get('涨跌幅', 0),
                    '成交量': latest_data.get('成交量', 0),
                    '成交额': latest_data.get('成交额', 0)
                }
        except Exception as e:
            print(f"    获取价格信息失败: {e}")
        
        return {}
    
    def get_stock_announcements(self, stock_code, days=90):
        """获取股票公告信息"""
        try:
            end_date = datetime.now().strftime('%Y%m%d')
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')
            
            announcements = self.retry_request(
                lambda: ak.stock_zh_a_hist_notice(
                    symbol=stock_code,
                    start_date=start_date,
                    end_date=end_date
                ),
                max_retries=2
            )
            return announcements if announcements is not None else pd.DataFrame()
        except Exception as e:
            print(f"    获取公告信息失败: {e}")
            return pd.DataFrame()
    
    def get_dividend_info(self, stock_code):
        """获取股票分红信息"""
        try:
            dividend_info = self.retry_request(
                lambda: ak.stock_zh_a_dividend(symbol=stock_code),
                max_retries=2
            )
            return dividend_info if dividend_info is not None else pd.DataFrame()
        except Exception as e:
            print(f"    获取分红信息失败: {e}")
            return pd.DataFrame()
    
    def check_recent_buyback(self, announcements_df):
        """检查近期是否有大股东增持公告"""
        if announcements_df.empty:
            return False, []
        
        buyback_keywords = ['增持', '回购', '股份增持', '大股东增持']
        found_announcements = []
        
        try:
            for _, row in announcements_df.iterrows():
                title = str(row.get('公告标题', ''))
                for keyword in buyback_keywords:
                    if keyword in title:
                        found_announcements.append(title)
                        break
        except Exception as e:
            print(f"    检查增持公告失败: {e}")
        
        return len(found_announcements) > 0, found_announcements
    
    def check_keywords_in_announcements(self, announcements_df):
        """检查公告中是否包含关键词"""
        if announcements_df.empty:
            return {}
        
        keywords = {
            '分红': ['分红', '派息', '现金分红', '股息'],
            'IPO/上市计划': ['IPO', '上市', '发行', '首发'],
            'H股发行': ['H股', '港股', '香港上市'],
            '黄金/矿产': ['黄金', '矿产', '矿业', '金矿', '铜矿', '铁矿'],
            '化肥': ['化肥', '磷肥', '钾肥', '复合肥', '尿素'],
            '机器人/AI': ['机器人', '人工智能', 'AI', '自动化', '智能制造']
        }
        
        keyword_matches = {category: [] for category in keywords.keys()}
        
        try:
            for _, row in announcements_df.iterrows():
                title = str(row.get('公告标题', ''))
                content = str(row.get('公告摘要', ''))
                full_text = title + ' ' + content
                
                for category, category_keywords in keywords.items():
                    for keyword in category_keywords:
                        if keyword in full_text:
                            keyword_matches[category].append(title)
                            break
        except Exception as e:
            print(f"    检查关键词失败: {e}")
        
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

    def calculate_gold_stock_score(self, stock_code, stock_name, industry):
        """计算黄金股票的综合评分 - 满足任一条件即可进入筛选池"""
        print(f"正在分析黄金股票: {stock_code} - {stock_name} ({industry})")
        
        # 获取基本信息
        basic_info = self.get_stock_basic_info(stock_code)
        if not basic_info:
            print(f"    跳过：无法获取基本信息")
            return None
        
        # 检查市值和股本条件
        shares_ok, market_cap_ok, total_shares, circulating_market_cap = self.check_market_cap_criteria(basic_info)
        
        # 初始化评分详情
        score_details = {
            '股票代码': stock_code,
            '股票名称': stock_name,
            '所属行业': industry,
            '总股本(亿股)': round(total_shares, 2),
            '流通市值(亿元)': round(circulating_market_cap, 2),
            '当前价格': float(basic_info.get('最新', 0)),
            '股本匹配分': 0,
            '官方背书分': 0,
            '增持动向分': 0,
            '题材热度分': 0,
            '分红预期分': 0,
            '黄金行业分': 15,  # 黄金行业固定加分
            '总分': 0,
            '符合条件数': 0,
            '进入筛选池': '是'  # 黄金行业股票都进入筛选池
        }
        
        print(f"    总股本: {total_shares:.2f}亿股, 流通市值: {circulating_market_cap:.2f}亿元")
        
        # 统计符合的条件数量
        conditions_met = []
        
        # 1. 股本匹配评分 (25分)
        if shares_ok:
            if 8 <= total_shares <= 12:
                score_details['股本匹配分'] = 25
            elif 12 < total_shares <= 15:
                score_details['股本匹配分'] = 20
            conditions_met.append('股本匹配')
            print(f"    ✓ 股本符合条件 (8-15亿股)")
        else:
            print(f"    × 股本不符合条件 ({total_shares:.2f}亿股)")
        
        # 2. 流通市值评分 (额外加分，不在原评分体系内)
        if market_cap_ok:
            score_details['股本匹配分'] += 5  # 市值符合额外加5分
            conditions_met.append('市值匹配')
            print(f"    ✓ 流通市值符合条件 (105-195亿元)")
        else:
            print(f"    × 流通市值不符合条件 ({circulating_market_cap:.2f}亿元)")
        
        # 3. 获取股东信息并评分 (30分)
        holders_df = self.get_stock_holders(stock_code)
        has_official, official_list = self.check_official_capital(holders_df)
        if has_official:
            score_details['官方背书分'] = 30
            conditions_met.append('官方背书')
            print(f"    ✓ 发现官方资本: {official_list[:2]}...")
        else:
            print(f"    × 未发现官方资本")
        
        # 4. 获取公告信息
        announcements_df = self.get_stock_announcements(stock_code)
        
        # 检查增持公告 (20分)
        has_buyback, buyback_list = self.check_recent_buyback(announcements_df)
        if has_buyback:
            score_details['增持动向分'] = 20
            conditions_met.append('增持动向')
            print(f"    ✓ 发现增持公告: {len(buyback_list)}条")
        else:
            print(f"    × 未发现增持公告")
        
        # 检查关键词匹配 (15分)
        keyword_matches = self.check_keywords_in_announcements(announcements_df)
        keyword_score = 0
        matched_categories = []
        for category, matches in keyword_matches.items():
            if matches:
                keyword_score += 3  # 每个类别3分，最多15分
                matched_categories.append(category)
        
        score_details['题材热度分'] = min(keyword_score, 15)
        if matched_categories:
            conditions_met.append('题材热度')
            print(f"    ✓ 发现题材关键词: {matched_categories}")
        else:
            print(f"    × 未发现题材关键词")
        
        # 5. 分红评分 (10分)
        dividend_df = self.get_dividend_info(stock_code)
        dividend_score, avg_dividend_rate = self.calculate_dividend_score(dividend_df)
        score_details['分红预期分'] = dividend_score
        if dividend_score > 0:
            conditions_met.append('分红预期')
            print(f"    ✓ 平均股息率: {avg_dividend_rate:.2%}")
        else:
            print(f"    × 无分红数据或股息率较低")
        
        # 黄金行业本身就是一个条件
        conditions_met.append('黄金行业')
        
        # 记录符合条件数
        score_details['符合条件数'] = len(conditions_met)
        
        # 计算总分
        score_details['总分'] = (score_details['股本匹配分'] + 
                               score_details['官方背书分'] + 
                               score_details['增持动向分'] + 
                               score_details['题材热度分'] + 
                               score_details['分红预期分'] + 
                               score_details['黄金行业分'])
        
        print(f"    符合条件: {', '.join(conditions_met)}")
        print(f"    综合评分: {score_details['总分']}分")
        
        # 添加延时
        time.sleep(1)
        
        return score_details
    
    def screen_gold_stocks(self):
        """筛选黄金股票并评分"""
        print("开始筛选黄金行业股票...")
        print("筛选条件: 黄金行业 + 股本/市值/官方资本等综合评分")
        print("=" * 60)
        
        # 获取黄金股票列表
        gold_stocks = self.get_gold_stocks()
        if gold_stocks.empty:
            print("未找到黄金行业股票")
            return pd.DataFrame()
        
        print(f"\n找到 {len(gold_stocks)} 只黄金相关股票，开始详细分析...\n")
        
        results = []
        
        for idx, row in gold_stocks.iterrows():
            # 检查列名并获取股票代码和名称
            if '代码' in gold_stocks.columns:
                stock_code = row['代码']
                stock_name = row['名称']
            else:
                stock_code = row['code']
                stock_name = row['name']
            industry = row.get('行业', '黄金相关')
            
            try:
                score_result = self.calculate_gold_stock_score(stock_code, stock_name, industry)
                if score_result:
                    results.append(score_result)
                    
                print(f"    已完成分析 ({idx + 1}/{len(gold_stocks)})\n")
                    
            except Exception as e:
                print(f"    处理股票 {stock_code} 时出错: {e}\n")
                continue
        
        if results:
            results_df = pd.DataFrame(results)
            # 按总分排序
            results_df = results_df.sort_values('总分', ascending=False)
            return results_df
        else:
            return pd.DataFrame()
    
    def print_gold_summary(self, results_df):
        """打印黄金股票筛选结果摘要"""
        if results_df.empty:
            print("未找到符合条件的黄金股票")
            return
        
        print(f"\n{'='*80}")
        print(f"黄金行业股票综合分析结果")
        print(f"{'='*80}")
        print(f"分析股票总数: {len(results_df)}")
        print(f"平均总分: {results_df['总分'].mean():.1f}")
        print(f"最高分: {results_df['总分'].max()}")
        print(f"平均符合条件数: {results_df['符合条件数'].mean():.1f}")
        
        print(f"\n评分说明:")
        print("- 股本匹配 (25分): 8-15亿股，8-12亿得25分，12-15亿得20分")
        print("- 官方背书 (30分): 十大股东包含社保基金、国资委、汇金、证金等")
        print("- 增持动向 (20分): 近期有大股东增持公告")
        print("- 题材热度 (15分): 公告包含分红、IPO、H股、矿产、化肥、AI等关键词")
        print("- 分红预期 (10分): 股息率≥4%得10分，2-4%得5分")
        print("- 黄金行业 (15分): 属于黄金/贵金属行业固定加分")
        
        print(f"\n黄金股票详细列表 (按总分排序):")
        print("-" * 130)
        print(f"{'代码':<8} {'名称':<12} {'总分':<6} {'条件数':<8} {'股本(亿)':<10} {'市值(亿)':<10} {'价格':<8} {'主要优势':<20}")
        print("-" * 130)
        
        for _, row in results_df.iterrows():
            # 分析主要优势
            advantages = []
            if row['股本匹配分'] > 0:
                advantages.append('股本适中')
            if row['官方背书分'] > 0:
                advantages.append('官方背景')
            if row['增持动向分'] > 0:
                advantages.append('有增持')
            if row['题材热度分'] > 0:
                advantages.append('题材热点')
            if row['分红预期分'] > 0:
                advantages.append('高分红')
            advantages.append('黄金行业')
            
            main_advantages = ', '.join(advantages[:3])  # 显示前3个优势
            
            print(f"{row['股票代码']:<8} {row['股票名称']:<12} "
                  f"{row['总分']:<6.0f} {row['符合条件数']:<8} "
                  f"{row['总股本(亿股)']:<10.2f} {row['流通市值(亿元)']:<10.2f} "
                  f"{row['当前价格']:<8.2f} {main_advantages:<20}")
        
        # 显示高分股票详细信息
        top_stocks = results_df.head(5)
        print(f"\n重点推荐 (前5名黄金股票):")
        print("-" * 80)
        for i, (_, row) in enumerate(top_stocks.iterrows(), 1):
            print(f"{i}. {row['股票代码']} {row['股票名称']} - 总分: {row['总分']:.0f} (符合{row['符合条件数']}个条件)")
            
            details = []
            if row['股本匹配分'] > 0:
                details.append(f"股本规模适中({row['总股本(亿股)']}亿股)")
            if row['官方背书分'] > 0:
                details.append("有官方资本背景")
            if row['增持动向分'] > 0:
                details.append("近期有增持动向")
            if row['题材热度分'] > 0:
                details.append("涉及热点题材")
            if row['分红预期分'] > 0:
                details.append("分红表现良好")
            details.append("黄金行业龙头")
            
            for detail in details[:4]:  # 显示前4个特点
                print(f"   • {detail}")
            print()
        
        # 条件分布统计
        print("条件符合情况统计:")
        print("-" * 40)
        condition_stats = {
            '股本匹配': len(results_df[results_df['股本匹配分'] > 0]),
            '官方背书': len(results_df[results_df['官方背书分'] > 0]),
            '增持动向': len(results_df[results_df['增持动向分'] > 0]),
            '题材热度': len(results_df[results_df['题材热度分'] > 0]),
            '分红预期': len(results_df[results_df['分红预期分'] > 0]),
            '黄金行业': len(results_df)  # 所有股票都是黄金行业
        }
        
        for condition, count in condition_stats.items():
            percentage = (count / len(results_df)) * 100
            print(f"{condition}: {count}/{len(results_df)} ({percentage:.1f}%)")


def main():
    """主函数"""
    print("黄金行业股票筛选和评分系统")
    print("=" * 50)
    
    # 创建筛选器实例
    screener = GoldStockScreener()
    
    # 开始筛选
    results = screener.screen_gold_stocks()
    
    if not results.empty:
        # 打印摘要
        screener.print_gold_summary(results)
        
        # 保存结果
        filename = f"gold_stocks_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        results.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n详细结果已保存到: {filename}")
    else:
        print("\n未找到黄金行业股票数据")
        print("可能的原因:")
        print("1. 网络连接问题")
        print("2. 数据源暂时不可用")
        print("3. 行业分类方式变更")


if __name__ == "__main__":
    main()