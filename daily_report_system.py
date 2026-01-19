#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日股票简报系统
整合股票筛选、股吧分析等多个功能模块，生成每日投资简报
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
import os

# 导入自定义模块
from gold_stock_screener import GoldStockScreener
from guba_analyzer import GubaAnalyzer
from intelligence_analyzer import IntelligenceAnalyzer

warnings.filterwarnings('ignore')


class DailyReportSystem:
    """每日简报系统"""
    
    def __init__(self):
        """初始化简报系统"""
        self.report_date = datetime.now().strftime('%Y年%m月%d日')
        self.report_time = datetime.now().strftime('%H:%M:%S')
        self.report_data = {}
        
        # 初始化各个分析模块
        self.gold_screener = GoldStockScreener()
        self.guba_analyzer = GubaAnalyzer()
        self.intelligence_analyzer = IntelligenceAnalyzer()
    
    def generate_daily_report(self, include_gold_stocks=True, include_guba=True, include_intelligence=True):
        """
        生成每日简报
        
        参数:
            include_gold_stocks: 是否包含黄金股票分析
            include_guba: 是否包含股吧热点分析
            include_intelligence: 是否包含情报分析
        """
        print(f"{'='*80}")
        print(f"开始生成每日投资简报 - {self.report_date} {self.report_time}")
        print(f"{'='*80}\n")
        
        # 1. 黄金股票筛选分析
        if include_gold_stocks:
            print("\n【模块1】黄金行业股票筛选分析")
            print("-" * 80)
            gold_stocks_df = self._analyze_gold_stocks()
            self.report_data['黄金股票'] = gold_stocks_df
        
        # 2. 股吧热点分析
        if include_guba:
            print("\n【模块2】股吧热点帖子分析")
            print("-" * 80)
            guba_posts_df = self._analyze_guba_trends()
            self.report_data['股吧热点'] = guba_posts_df
            
            # 3. 情报深度分析
            if include_intelligence and not guba_posts_df.empty:
                print("\n【模块3】情报深度分析")
                print("-" * 80)
                intelligence_df = self._analyze_intelligence(guba_posts_df)
                self.report_data['情报分析'] = intelligence_df
        
        # 4. 生成综合简报
        print("\n【模块4】生成综合简报")
        print("-" * 80)
        report_content = self._compile_report()
        
        # 4. 保存简报
        self._save_report(report_content)
        
        print(f"\n{'='*80}")
        print(f"每日简报生成完成！")
        print(f"{'='*80}")
        
        return report_content
    
    def _analyze_gold_stocks(self):
        """分析黄金股票"""
        try:
            print("正在筛选黄金行业股票...")
            gold_stocks_df = self.gold_screener.screen_gold_stocks()
            
            if not gold_stocks_df.empty:
                print(f"✓ 成功分析 {len(gold_stocks_df)} 只黄金股票")
                
                # 保存详细数据
                filename = f"data/gold_stocks_{datetime.now().strftime('%Y%m%d')}.csv"
                os.makedirs('data', exist_ok=True)
                gold_stocks_df.to_csv(filename, index=False, encoding='utf-8-sig')
                print(f"  详细数据已保存: {filename}")
                
                return gold_stocks_df
            else:
                print("× 未获取到黄金股票数据")
                return pd.DataFrame()
                
        except Exception as e:
            print(f"× 黄金股票分析失败: {e}")
            return pd.DataFrame()
    
    def _analyze_guba_trends(self):
        """分析股吧热点"""
        try:
            print("正在分析股吧热点帖子...")
            guba_posts_df = self.guba_analyzer.get_guba_trends(max_pages=3)
            
            if not guba_posts_df.empty:
                print(f"✓ 成功筛选 {len(guba_posts_df)} 条高质量帖子")
                
                # 保存详细数据
                filename = f"data/guba_posts_{datetime.now().strftime('%Y%m%d')}.csv"
                os.makedirs('data', exist_ok=True)
                guba_posts_df.to_csv(filename, index=False, encoding='utf-8-sig')
                print(f"  详细数据已保存: {filename}")
                
                return guba_posts_df
            else:
                print("× 未获取到股吧帖子数据")
                return pd.DataFrame()
                
        except Exception as e:
            print(f"× 股吧分析失败: {e}")
            return pd.DataFrame()
    
    def _analyze_intelligence(self, guba_posts_df):
        """分析情报"""
        try:
            print("正在进行情报深度分析...")
            intelligence_df = self.intelligence_analyzer.analyze_intelligence(guba_posts_df)
            
            if not intelligence_df.empty:
                print(f"✓ 成功提取 {len(intelligence_df)} 条有价值情报")
                
                # 保存详细数据
                filename = f"data/intelligence_{datetime.now().strftime('%Y%m%d')}.csv"
                os.makedirs('data', exist_ok=True)
                intelligence_df.to_csv(filename, index=False, encoding='utf-8-sig')
                print(f"  详细数据已保存: {filename}")
                
                return intelligence_df
            else:
                print("× 未提取到有价值情报")
                return pd.DataFrame()
                
        except Exception as e:
            print(f"× 情报分析失败: {e}")
            return pd.DataFrame()
    
    def _compile_report(self):
        """编译生成简报内容"""
        report_lines = []
        
        # 简报标题
        report_lines.append("=" * 80)
        report_lines.append(f"每日投资简报")
        report_lines.append(f"生成时间: {self.report_date} {self.report_time}")
        report_lines.append("=" * 80)
        report_lines.append("")
        
        # 一、黄金股票分析部分
        if '黄金股票' in self.report_data and not self.report_data['黄金股票'].empty:
            report_lines.append("【一、黄金行业股票分析】")
            report_lines.append("-" * 80)
            report_lines.extend(self._format_gold_stocks_section())
            report_lines.append("")
        
        # 二、股吧热点分析部分
        if '股吧热点' in self.report_data and not self.report_data['股吧热点'].empty:
            report_lines.append("【二、股吧热点分析】")
            report_lines.append("-" * 80)
            report_lines.extend(self._format_guba_section())
            report_lines.append("")
        
        # 三、情报深度分析部分
        if '情报分析' in self.report_data and not self.report_data['情报分析'].empty:
            report_lines.append("【三、情报深度分析】")
            report_lines.append("-" * 80)
            report_lines.extend(self._format_intelligence_section())
            report_lines.append("")
        
        # 四、综合建议
        report_lines.append("【四、综合建议】")
        report_lines.append("-" * 80)
        report_lines.extend(self._generate_recommendations())
        report_lines.append("")
        
        # 简报结尾
        report_lines.append("=" * 80)
        report_lines.append("注: 本简报仅供参考，不构成投资建议。投资有风险，入市需谨慎。")
        report_lines.append("=" * 80)
        
        return "\n".join(report_lines)
    
    def _format_gold_stocks_section(self):
        """格式化黄金股票部分"""
        lines = []
        gold_df = self.report_data['黄金股票']
        
        # 统计信息
        total_count = len(gold_df)
        # 兼容新旧版本的列名
        if '是否符合条件' in gold_df.columns:
            qualified_count = len(gold_df[gold_df['是否符合条件'] == '是'])
        elif '进入筛选池' in gold_df.columns:
            qualified_count = len(gold_df[gold_df['进入筛选池'] == '是'])
        else:
            qualified_count = total_count  # 如果没有这些列，默认全部符合
        
        avg_score = gold_df['总分'].mean()
        
        lines.append(f"分析股票总数: {total_count} 只")
        lines.append(f"符合筛选条件: {qualified_count} 只")
        lines.append(f"平均评分: {avg_score:.1f} 分")
        lines.append("")
        
        # 重点推荐（前5名）
        lines.append("重点关注股票 TOP 5:")
        lines.append("")
        
        top_stocks = gold_df.head(5)
        for idx, row in top_stocks.iterrows():
            lines.append(f"{idx+1}. {row['股票代码']} {row['股票名称']}")
            lines.append(f"   总分: {row['总分']:.0f} | 股本: {row.get('总股本(亿股)', 'N/A')}亿股 | "
                        f"市值: {row.get('流通市值(亿元)', 'N/A')}亿元 | 价格: {row.get('当前价格', 0):.2f}元")
            
            # 亮点说明
            highlights = []
            if row.get('股本匹配分', 0) > 0:
                highlights.append("股本规模适中")
            if row.get('官方背书分', 0) > 0:
                highlights.append("有官方资本背景")
            if row.get('黄金行业分', 0) > 0 or '黄金' in str(row.get('所属行业', '')):
                highlights.append("黄金行业")
            
            if highlights:
                lines.append(f"   亮点: {' | '.join(highlights)}")
            lines.append("")
        
        return lines
    
    def _format_guba_section(self):
        """格式化股吧热点部分"""
        lines = []
        guba_df = self.report_data['股吧热点']
        
        # 统计信息
        total_posts = len(guba_df)
        avg_read = guba_df['阅读量'].mean()
        avg_comment = guba_df['评论数'].mean()
        
        lines.append(f"高质量帖子数: {total_posts} 条")
        lines.append(f"平均阅读量: {avg_read:.0f}")
        lines.append(f"平均评论数: {avg_comment:.1f}")
        lines.append("")
        
        # 热门话题（前10条）
        lines.append("热门讨论话题 TOP 10:")
        lines.append("")
        
        top_posts = guba_df.head(10)
        for idx, row in top_posts.iterrows():
            lines.append(f"{idx+1}. {row['标题']}")
            lines.append(f"   阅读: {row['阅读量']:.0f} | 评论: {row['评论数']:.0f} | "
                        f"质量评分: {row['质量评分']:.1f}")
            if row['股票代码']:
                lines.append(f"   相关股票: {row['股票代码']}")
            if row['帖子链接']:
                lines.append(f"   链接: {row['帖子链接']}")
            lines.append("")
        
        return lines
    
    def _format_intelligence_section(self):
        """格式化情报分析部分"""
        lines = []
        intel_df = self.report_data['情报分析']
        
        # 统计信息
        total_intel = len(intel_df)
        avg_score = intel_df['价值评分'].mean()
        high_value_count = len(intel_df[intel_df['价值评分'] >= 8])
        
        lines.append(f"有效情报总数: {total_intel} 条")
        lines.append(f"平均价值评分: {avg_score:.1f}/10")
        lines.append(f"高价值情报(≥8分): {high_value_count} 条")
        lines.append("")
        
        # 分类统计
        category_counts = intel_df['主要分类'].value_counts()
        lines.append("情报分类分布:")
        for category, count in category_counts.items():
            lines.append(f"  • {category}: {count} 条")
        lines.append("")
        
        # 热门标的
        all_stocks = []
        for stocks_str in intel_df['识别股票']:
            all_stocks.extend(stocks_str.split(', '))
        if all_stocks:
            from collections import Counter
            stock_counter = Counter(all_stocks)
            lines.append("热门标的 TOP 5:")
            for stock, count in stock_counter.most_common(5):
                lines.append(f"  • {stock}: 被提及 {count} 次")
            lines.append("")
        
        # 高价值情报详情（前5条）
        high_value = intel_df[intel_df['价值评分'] >= 7].head(5)
        if not high_value.empty:
            lines.append("高价值情报精选:")
            lines.append("")
            
            for idx, row in high_value.iterrows():
                lines.append(f"{idx + 1}. 【{row['主要分类']}】{row['标题']}")
                lines.append(f"   标的: {row['识别股票']}")
                lines.append(f"   评分: {row['价值评分']}/10 ⭐")
                lines.append(f"   论据: {row['关键论据'][:100]}...")
                lines.append("")
        
        return lines
    
    def _generate_recommendations(self):
        """生成综合建议"""
        lines = []
        
        # 基于黄金股票的建议
        if '黄金股票' in self.report_data and not self.report_data['黄金股票'].empty:
            gold_df = self.report_data['黄金股票']
            
            # 兼容新旧版本的列名
            if '是否符合条件' in gold_df.columns:
                qualified_stocks = gold_df[gold_df['是否符合条件'] == '是']
            elif '进入筛选池' in gold_df.columns:
                qualified_stocks = gold_df[gold_df['进入筛选池'] == '是']
            else:
                qualified_stocks = gold_df  # 如果没有这些列，默认全部符合
            
            if not qualified_stocks.empty:
                lines.append("1. 黄金板块投资建议:")
                lines.append(f"   - 共发现 {len(qualified_stocks)} 只符合条件的黄金股票")
                
                top_stock = qualified_stocks.iloc[0]
                lines.append(f"   - 重点关注: {top_stock['股票代码']} {top_stock['股票名称']} "
                           f"(评分: {top_stock['总分']:.0f})")
                
                if top_stock.get('官方背书分', 0) > 0:
                    lines.append(f"   - 该股有官方资本背景，相对稳健")
                
                lines.append("")
        
        # 基于股吧热点的建议
        if '股吧热点' in self.report_data and not self.report_data['股吧热点'].empty:
            guba_df = self.report_data['股吧热点']
            
            lines.append("2. 市场热点关注:")
            lines.append(f"   - 当前市场讨论活跃，共 {len(guba_df)} 个热门话题")
            
            # 提取热门股票代码
            hot_stocks = guba_df[guba_df['股票代码'] != '']['股票代码'].value_counts().head(3)
            if not hot_stocks.empty:
                lines.append(f"   - 热门股票: {', '.join(hot_stocks.index.tolist())}")
            
            lines.append("")
        
        # 基于情报分析的建议
        if '情报分析' in self.report_data and not self.report_data['情报分析'].empty:
            intel_df = self.report_data['情报分析']
            high_value_intel = intel_df[intel_df['价值评分'] >= 8]
            
            if not high_value_intel.empty:
                lines.append("3. 情报要点:")
                lines.append(f"   - 发现 {len(high_value_intel)} 条高价值情报(≥8分)")
                
                # 提取最高分情报
                top_intel = high_value_intel.iloc[0]
                lines.append(f"   - 最高价值情报: {top_intel['标题']}")
                lines.append(f"     标的: {top_intel['识别股票']}")
                lines.append(f"     类型: {top_intel['主要分类']}")
                lines.append(f"     评分: {top_intel['价值评分']}/10")
                
                lines.append("")
        
        # 风险提示
        risk_section = "4. 风险提示:" if '情报分析' in self.report_data else "3. 风险提示:"
        lines.append(risk_section)
        lines.append("   - 股市有风险，投资需谨慎")
        lines.append("   - 建议结合基本面分析和技术面分析")
        lines.append("   - 注意控制仓位，分散投资风险")
        lines.append("   - 关注宏观经济政策和行业动态")
        
        return lines
    
    def _save_report(self, report_content):
        """保存简报到文件"""
        try:
            # 创建reports目录
            os.makedirs('reports', exist_ok=True)
            
            # 保存文本版简报
            txt_filename = f"reports/daily_report_{datetime.now().strftime('%Y%m%d')}.txt"
            with open(txt_filename, 'w', encoding='utf-8') as f:
                f.write(report_content)
            print(f"✓ 简报已保存: {txt_filename}")
            
            # 保存HTML版简报（可选）
            html_filename = f"reports/daily_report_{datetime.now().strftime('%Y%m%d')}.html"
            html_content = self._convert_to_html(report_content)
            with open(html_filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"✓ HTML简报已保存: {html_filename}")
            
        except Exception as e:
            print(f"× 保存简报失败: {e}")
    
    def _convert_to_html(self, text_content):
        """将文本简报转换为HTML格式"""
        html_template = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>每日投资简报 - {self.report_date}</title>
    <style>
        body {{
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .report-container {{
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            border-left: 4px solid #3498db;
            padding-left: 10px;
        }}
        pre {{
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            overflow-x: auto;
            line-height: 1.6;
        }}
        .timestamp {{
            color: #7f8c8d;
            font-size: 14px;
        }}
        .warning {{
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 10px;
            margin-top: 20px;
        }}
    </style>
</head>
<body>
    <div class="report-container">
        <h1>每日投资简报</h1>
        <p class="timestamp">生成时间: {self.report_date} {self.report_time}</p>
        <pre>{text_content}</pre>
    </div>
</body>
</html>
"""
        return html_template


def main():
    """主函数"""
    print("每日投资简报系统")
    print("=" * 80)
    
    # 创建简报系统实例
    report_system = DailyReportSystem()
    
    # 生成每日简报
    report_content = report_system.generate_daily_report(
        include_gold_stocks=True,  # 包含黄金股票分析
        include_guba=True,         # 包含股吧热点分析
        include_intelligence=True  # 包含情报深度分析
    )
    
    # 打印简报内容
    print("\n" + report_content)


if __name__ == "__main__":
    main()