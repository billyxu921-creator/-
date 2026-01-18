#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
量化选股器 (Quant Picker)
实现：AkShare指标初选 → 舆情碰撞 → DeepSeek终极筛选 → AI潜力股推荐

流程:
1. AkShare指标初选（市值、涨幅、换手率）
2. 舆情碰撞（微博+小红书热点匹配）
3. DeepSeek终极筛选（AI选出TOP 3）
4. 生成AI潜力股推荐报告
"""

import akshare as ak
import pandas as pd
import numpy as np
import json
import requests
import re
from datetime import datetime
import warnings
import os

warnings.filterwarnings('ignore')


class QuantPicker:
    """量化选股器"""
    
    def __init__(self, api_key=None):
        """
        初始化选股器
        
        参数:
            api_key: DeepSeek API密钥
        """
        # 从配置文件读取API Key
        if api_key is None:
            try:
                from config import DEEPSEEK_CONFIG
                self.api_key = DEEPSEEK_CONFIG['api_key']
                self.api_base = DEEPSEEK_CONFIG['api_base']
            except ImportError:
                print("⚠️  警告: 未找到配置文件，请设置API Key")
                self.api_key = "YOUR_API_KEY"
                self.api_base = "https://api.deepseek.com/v1"
        else:
            self.api_key = api_key
            self.api_base = "https://api.deepseek.com/v1"
        
        # 舆情关键词配置
        self.sentiment_keywords = {
            'high_priority': ['重组', '并购', '收购', '入股', '利好', '涨停', '突破'],
            'medium_priority': ['增持', '回购', '业绩', '盈利', '分红'],
            'low_priority': ['关注', '看好', '推荐']
        }
        
        # 历史数据目录
        self.history_dir = "discovery_history"
        
        print("✓ 量化选股器初始化完成")
    
    def step1_akshare_screening(self):
        """
        Step 1: AkShare指标初选
        
        筛选标准:
        - 60 < 市值 < 200亿
        - 2% < 涨幅 < 6%
        - 换手率 > 5%
        
        返回:
            DataFrame: 初选股票列表
        """
        print("\n" + "=" * 60)
        print("Step 1: AkShare指标初选")
        print("=" * 60)
        
        try:
            # 获取全A股实时行情
            print("\n正在获取全A股实时行情...")
            df = ak.stock_zh_a_spot_em()
            
            print(f"✓ 获取成功，共 {len(df)} 只股票")
            
            # 数据预处理
            print("\n数据预处理...")
            
            # 确保数值列为float类型
            numeric_columns = ['最新价', '涨跌幅', '换手率', '总市值', '流通市值']
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # 计算市值（亿元）
            if '总市值' in df.columns:
                df['市值_亿'] = df['总市值'] / 100000000
            elif '流通市值' in df.columns:
                df['市值_亿'] = df['流通市值'] / 100000000
            else:
                print("× 未找到市值字段")
                return pd.DataFrame()
            
            # 筛选条件
            print("\n应用筛选条件:")
            print("  - 60 < 市值 < 200亿")
            print("  - 2% < 涨幅 < 6%")
            print("  - 换手率 > 5%")
            
            # 应用筛选
            mask = (
                (df['市值_亿'] > 60) & 
                (df['市值_亿'] < 200) &
                (df['涨跌幅'] > 2) & 
                (df['涨跌幅'] < 6) &
                (df['换手率'] > 5)
            )
            
            df_filtered = df[mask].copy()
            
            # 按涨幅排序
            df_filtered = df_filtered.sort_values('涨跌幅', ascending=False)
            
            # 重置索引
            df_filtered = df_filtered.reset_index(drop=True)
            
            print(f"\n✓ 初选完成，筛选出 {len(df_filtered)} 只股票")
            
            if len(df_filtered) > 0:
                print("\n【初选股票TOP 10】")
                print("-" * 60)
                for i, (_, row) in enumerate(df_filtered.head(10).iterrows(), 1):
                    print(f"{i:2d}. {row['名称']:8s} ({row['代码']}) "
                          f"涨幅:{row['涨跌幅']:5.2f}% "
                          f"市值:{row['市值_亿']:6.1f}亿 "
                          f"换手:{row['换手率']:5.2f}%")
            
            return df_filtered
        
        except Exception as e:
            print(f"\n× AkShare数据获取失败: {e}")
            import traceback
            traceback.print_exc()
            return pd.DataFrame()
    
    def step2_sentiment_match(self, df_stocks):
        """
        Step 2: 舆情碰撞
        
        将初选股票与微博、小红书热点数据匹配
        
        参数:
            df_stocks: 初选股票DataFrame
            
        返回:
            DataFrame: 添加舆情评分的股票列表
        """
        print("\n" + "=" * 60)
        print("Step 2: 舆情碰撞 (Sentiment Match)")
        print("=" * 60)
        
        if df_stocks.empty:
            print("× 无初选股票，跳过舆情碰撞")
            return df_stocks
        
        # 加载舆情数据
        sentiment_data = self._load_sentiment_data()
        
        if not sentiment_data:
            print("⚠️  未找到舆情数据，使用默认评分")
            df_stocks['舆情评分'] = 50
            df_stocks['舆情来源'] = '无'
            df_stocks['匹配关键词'] = ''
            df_stocks['博主影响力'] = 1
            return df_stocks
        
        print(f"\n✓ 加载舆情数据: {len(sentiment_data)} 条")
        
        # 为每只股票计算舆情评分
        print("\n正在匹配舆情数据...")
        
        sentiment_scores = []
        sentiment_sources = []
        matched_keywords = []
        influencer_weights = []
        
        for _, stock in df_stocks.iterrows():
            stock_name = stock['名称']
            stock_code = stock['代码']
            
            # 匹配舆情数据
            score, source, keywords, weight = self._match_sentiment(
                stock_name, stock_code, sentiment_data
            )
            
            sentiment_scores.append(score)
            sentiment_sources.append(source)
            matched_keywords.append(keywords)
            influencer_weights.append(weight)
        
        # 添加舆情字段
        df_stocks['舆情评分'] = sentiment_scores
        df_stocks['舆情来源'] = sentiment_sources
        df_stocks['匹配关键词'] = matched_keywords
        df_stocks['博主影响力'] = influencer_weights
        
        # 计算综合得分
        # 综合得分 = 涨幅权重(30%) + 换手率权重(20%) + 舆情评分(50%)
        df_stocks['综合得分'] = (
            df_stocks['涨跌幅'] * 0.3 +
            df_stocks['换手率'] * 0.2 +
            df_stocks['舆情评分'] * 0.5
        )
        
        # 按综合得分排序
        df_stocks = df_stocks.sort_values('综合得分', ascending=False)
        df_stocks = df_stocks.reset_index(drop=True)
        
        print(f"\n✓ 舆情碰撞完成")
        
        # 显示舆情匹配结果
        matched_count = len(df_stocks[df_stocks['舆情评分'] > 50])
        print(f"  匹配到舆情: {matched_count} 只")
        
        if matched_count > 0:
            print("\n【舆情匹配TOP 5】")
            print("-" * 80)
            for i, (_, row) in enumerate(df_stocks[df_stocks['舆情评分'] > 50].head(5).iterrows(), 1):
                print(f"{i}. {row['名称']:8s} "
                      f"舆情评分:{row['舆情评分']:5.1f} "
                      f"来源:{row['舆情来源']:10s} "
                      f"关键词:{row['匹配关键词']:20s} "
                      f"影响力:×{row['博主影响力']}")
        
        return df_stocks
    
    def _load_sentiment_data(self):
        """
        加载舆情数据（微博+小红书）
        
        返回:
            list: 舆情数据列表
        """
        sentiment_data = []
        
        # 1. 加载最新的discovery数据
        try:
            if os.path.exists(self.history_dir):
                files = os.listdir(self.history_dir)
                json_files = [f for f in files if f.startswith('discovery_') and f.endswith('.json')]
                
                if json_files:
                    # 获取最新文件
                    latest_file = sorted(json_files)[-1]
                    filepath = os.path.join(self.history_dir, latest_file)
                    
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        texts = data.get('texts', [])
                        
                        for text in texts:
                            sentiment_data.append({
                                'text': text,
                                'source': '全网雷达',
                                'followers': 10000,  # 默认粉丝数
                                'platform': '小红书+微博'
                            })
                    
                    print(f"  ✓ 加载全网雷达数据: {len(texts)} 条")
        except Exception as e:
            print(f"  ⚠️  加载全网雷达数据失败: {e}")
        
        # 2. 加载微博数据
        try:
            csv_files = [f for f in os.listdir('.') if f.startswith('weibo_clean') and f.endswith('.csv')]
            
            if csv_files:
                latest_weibo = sorted(csv_files)[-1]
                df_weibo = pd.read_csv(latest_weibo, encoding='utf-8-sig')
                
                for _, row in df_weibo.iterrows():
                    sentiment_data.append({
                        'text': str(row.get('博文内容', '')),
                        'source': '微博',
                        'followers': row.get('粉丝数', 1000),
                        'platform': '微博'
                    })
                
                print(f"  ✓ 加载微博数据: {len(df_weibo)} 条")
        except Exception as e:
            print(f"  ⚠️  加载微博数据失败: {e}")
        
        return sentiment_data
    
    def _match_sentiment(self, stock_name, stock_code, sentiment_data):
        """
        匹配单只股票的舆情数据
        
        参数:
            stock_name: 股票名称
            stock_code: 股票代码
            sentiment_data: 舆情数据列表
            
        返回:
            tuple: (舆情评分, 来源, 匹配关键词, 博主影响力权重)
        """
        base_score = 50  # 基础分
        max_score = 0
        best_source = '无'
        best_keywords = ''
        max_weight = 1
        
        for item in sentiment_data:
            text = item['text']
            source = item['source']
            followers = item.get('followers', 1000)
            
            # 检查是否提及该股票
            if stock_name in text or stock_code in text:
                # 计算影响力权重
                if followers >= 1000000:  # 100万+
                    weight = 10
                elif followers >= 100000:  # 10万+
                    weight = 3
                else:
                    weight = 1
                
                # 检查关键词
                score = base_score
                matched_kw = []
                
                # 高优先级关键词 (+30分)
                for kw in self.sentiment_keywords['high_priority']:
                    if kw in text:
                        score += 30
                        matched_kw.append(kw)
                        break
                
                # 中优先级关键词 (+20分)
                if not matched_kw:
                    for kw in self.sentiment_keywords['medium_priority']:
                        if kw in text:
                            score += 20
                            matched_kw.append(kw)
                            break
                
                # 低优先级关键词 (+10分)
                if not matched_kw:
                    for kw in self.sentiment_keywords['low_priority']:
                        if kw in text:
                            score += 10
                            matched_kw.append(kw)
                            break
                
                # 应用影响力权重
                weighted_score = score * weight
                
                # 保留最高分
                if weighted_score > max_score:
                    max_score = weighted_score
                    best_source = source
                    best_keywords = ','.join(matched_kw)
                    max_weight = weight
        
        # 归一化到0-100
        final_score = min(100, max_score / 10)
        
        return final_score, best_source, best_keywords, max_weight

    
    def step3_deepseek_selection(self, df_stocks, top_n=10):
        """
        Step 3: DeepSeek终极筛选
        
        将综合得分最高的前N只股票发送给DeepSeek AI进行终极筛选
        
        参数:
            df_stocks: 带舆情评分的股票DataFrame
            top_n: 发送给AI的股票数量
            
        返回:
            dict: AI推荐结果
        """
        print("\n" + "=" * 60)
        print("Step 3: DeepSeek终极筛选")
        print("=" * 60)
        
        if df_stocks.empty:
            print("× 无股票数据，跳过AI筛选")
            return None
        
        # 选取TOP N
        top_stocks = df_stocks.head(top_n)
        
        print(f"\n选取综合得分TOP {len(top_stocks)} 只股票进行AI分析...")
        
        # 获取股票新闻
        print("\n正在获取股票新闻...")
        stocks_with_news = self._fetch_stock_news(top_stocks)
        
        # 构建AI输入
        ai_input = self._build_ai_input(stocks_with_news)
        
        print(f"\n输入字数: {len(ai_input)} 字")
        
        # 调用DeepSeek API
        print("\n正在调用DeepSeek API进行终极筛选...")
        
        ai_result = self._call_deepseek_for_selection(ai_input)
        
        if ai_result:
            print("✓ AI筛选完成")
            return ai_result
        else:
            print("× AI筛选失败")
            return None
    
    def _fetch_stock_news(self, df_stocks):
        """
        获取股票最新新闻
        
        参数:
            df_stocks: 股票DataFrame
            
        返回:
            DataFrame: 添加新闻字段的股票数据
        """
        news_list = []
        
        for _, stock in df_stocks.iterrows():
            stock_code = stock['代码']
            stock_name = stock['名称']
            
            try:
                # 尝试获取个股新闻
                news_df = ak.stock_news_em(symbol=stock_code)
                
                if not news_df.empty:
                    # 取最新3条新闻标题
                    latest_news = news_df.head(3)['新闻标题'].tolist()
                    news_summary = '; '.join(latest_news)
                else:
                    news_summary = '暂无最新新闻'
            
            except:
                news_summary = '暂无最新新闻'
            
            news_list.append(news_summary)
        
        df_stocks['最新新闻'] = news_list
        
        return df_stocks
    
    def _build_ai_input(self, df_stocks):
        """
        构建AI输入文本
        
        参数:
            df_stocks: 股票DataFrame
            
        返回:
            str: AI输入文本
        """
        lines = []
        
        lines.append("以下是今日筛选出的潜力股票列表：\n")
        
        for i, (_, stock) in enumerate(df_stocks.iterrows(), 1):
            lines.append(f"【股票{i}】{stock['名称']} ({stock['代码']})")
            lines.append(f"  涨跌幅: {stock['涨跌幅']:.2f}%")
            lines.append(f"  最新价: {stock['最新价']:.2f}元")
            lines.append(f"  市值: {stock['市值_亿']:.1f}亿")
            lines.append(f"  换手率: {stock['换手率']:.2f}%")
            lines.append(f"  成交量: {stock.get('成交量', 0)}")
            lines.append(f"  舆情评分: {stock['舆情评分']:.1f}/100")
            lines.append(f"  舆情来源: {stock['舆情来源']}")
            
            if stock['匹配关键词']:
                lines.append(f"  匹配关键词: {stock['匹配关键词']}")
            
            if stock['博主影响力'] > 1:
                lines.append(f"  博主影响力: ×{stock['博主影响力']}")
            
            lines.append(f"  最新新闻: {stock['最新新闻']}")
            lines.append(f"  综合得分: {stock['综合得分']:.2f}")
            lines.append("")
        
        return "\n".join(lines)
    
    def _call_deepseek_for_selection(self, input_text):
        """
        调用DeepSeek API进行股票筛选
        
        参数:
            input_text: 输入文本
            
        返回:
            dict: AI分析结果
        """
        system_prompt = """你是一位资深基金经理，拥有20年的A股投资经验。

请从提供的股票列表中选出3只今日最具潜力的股票。

【重要规则 - 防止幻觉】:
1. 你只能根据提供的股票数据回答，不得推荐列表外的股票
2. 所有股价数据必须以提供的akshare数据为准，不得编造
3. 如果舆情评分为0或无数据，请明确说明'无舆情数据支持'
4. 禁止编造任何新闻、政策或事件
5. 严禁推荐任何非A股市场的股票代码
6. 给出推荐理由时，必须基于提供的真实数据（涨跌幅、换手率、舆情评分）
7. 止盈位计算必须基于当前价格，使用公式：当前价格 × (1 + 合理涨幅%)
8. 如果数据不足以做出判断，请在risk_warning中说明'数据不足'
9. 不要编造任何技术指标或财务数据
10. 所有结论必须基于提供的真实数据

分析要求：
1. 综合考虑技术面（涨幅、换手率、成交量）和舆情面（社交媒体热度、关键词）
2. 找出技术面和舆情面的结合点（例如：技术突破+舆情催化）
3. 给出具体的推荐理由（必须基于提供的真实数据）
4. 预测一个短期止盈位（1-3个交易日，基于当前价格计算）

输出格式（JSON）：
{
    "recommendations": [
        {
            "rank": 1,
            "stock_name": "股票名称",
            "stock_code": "股票代码（必须是提供列表中的真实代码）",
            "reason": "推荐理由（必须基于提供的真实数据）",
            "technical_analysis": "技术面分析（基于提供的涨跌幅、换手率数据）",
            "sentiment_analysis": "舆情面分析（基于提供的舆情评分，如果为0则说明无数据）",
            "synergy_point": "技术面和舆情面的结合点",
            "target_price": "止盈位（元，基于当前价格计算）",
            "expected_return": "预期收益率（%）",
            "risk_warning": "风险提示（如果数据不足请说明）"
        }
    ],
    "market_view": "整体市场观点（基于提供的数据）",
    "strategy_suggestion": "操作策略建议（保守建议）",
    "data_source_note": "所有数据来源于akshare实时行情"
}

注意：只返回JSON格式，不要包含其他文字。严禁编造任何数据。"""
        
        url = f"{self.api_base}/chat/completions"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": input_text}
            ],
            "temperature": 0.3,
            "max_tokens": 2000
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                
                # 尝试解析JSON
                try:
                    json_match = re.search(r'\{[\s\S]*\}', content)
                    if json_match:
                        json_str = json_match.group()
                        ai_result = json.loads(json_str)
                        return ai_result
                    else:
                        print("  警告: 无法从响应中提取JSON")
                        return None
                except json.JSONDecodeError:
                    print(f"  警告: JSON解析失败")
                    print(f"  原始响应: {content[:200]}...")
                    return None
            
            return None
            
        except Exception as e:
            print(f"  API调用失败: {e}")
            return None
    
    def step4_generate_report(self, df_stocks, ai_result):
        """
        Step 4: 生成AI潜力股推荐报告
        
        参数:
            df_stocks: 股票DataFrame
            ai_result: AI分析结果
            
        返回:
            str: 报告文件路径
        """
        print("\n" + "=" * 60)
        print("Step 4: 生成AI潜力股推荐报告")
        print("=" * 60)
        
        today = datetime.now().strftime('%Y%m%d')
        filename = f"AI潜力股推荐_{today}.md"
        
        report_lines = []
        
        # 标题
        report_lines.append("# 🚀 AI其他主题潜力股推荐")
        report_lines.append("")
        report_lines.append(f"**生成时间**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")
        
        # 筛选概况
        report_lines.append("## 📊 筛选概况")
        report_lines.append("")
        report_lines.append(f"- **初选股票数**: {len(df_stocks)} 只")
        report_lines.append(f"- **舆情匹配数**: {len(df_stocks[df_stocks['舆情评分'] > 50])} 只")
        report_lines.append(f"- **AI终选数**: 3 只")
        report_lines.append("")
        
        # 筛选标准
        report_lines.append("## 🎯 筛选标准")
        report_lines.append("")
        report_lines.append("### Step 1: AkShare指标初选")
        report_lines.append("- 60 < 市值 < 200亿")
        report_lines.append("- 2% < 涨幅 < 6%")
        report_lines.append("- 换手率 > 5%")
        report_lines.append("")
        report_lines.append("### Step 2: 舆情碰撞")
        report_lines.append("- 匹配微博、小红书热点数据")
        report_lines.append("- 百万粉丝博主提及 → 高优先级")
        report_lines.append("- 关键词加权: 重组/利好/涨停等")
        report_lines.append("")
        report_lines.append("### Step 3: DeepSeek终极筛选")
        report_lines.append("- AI基金经理从TOP 10中选出TOP 3")
        report_lines.append("- 综合技术面和舆情面")
        report_lines.append("- 预测短期止盈位")
        report_lines.append("")
        
        # AI推荐结果
        if ai_result and 'recommendations' in ai_result:
            recommendations = ai_result['recommendations']
            
            report_lines.append("## 🏆 AI推荐TOP 3")
            report_lines.append("")
            
            for rec in recommendations:
                rank = rec.get('rank', 0)
                stock_name = rec.get('stock_name', '')
                stock_code = rec.get('stock_code', '')
                reason = rec.get('reason', '')
                technical = rec.get('technical_analysis', '')
                sentiment = rec.get('sentiment_analysis', '')
                synergy = rec.get('synergy_point', '')
                target = rec.get('target_price', '')
                expected_return = rec.get('expected_return', '')
                risk = rec.get('risk_warning', '')
                
                report_lines.append(f"### {rank}. {stock_name} ({stock_code})")
                report_lines.append("")
                
                # 获取实时数据
                stock_data = df_stocks[df_stocks['代码'] == stock_code]
                if not stock_data.empty:
                    stock = stock_data.iloc[0]
                    report_lines.append(f"**实时数据**:")
                    report_lines.append(f"- 最新价: {stock['最新价']:.2f}元")
                    report_lines.append(f"- 涨跌幅: {stock['涨跌幅']:.2f}%")
                    report_lines.append(f"- 换手率: {stock['换手率']:.2f}%")
                    report_lines.append(f"- 市值: {stock['市值_亿']:.1f}亿")
                    report_lines.append(f"- 舆情评分: {stock['舆情评分']:.1f}/100")
                    report_lines.append("")
                
                report_lines.append(f"**推荐理由**: {reason}")
                report_lines.append("")
                
                report_lines.append(f"**技术面分析**:")
                report_lines.append(f"> {technical}")
                report_lines.append("")
                
                report_lines.append(f"**舆情面分析**:")
                report_lines.append(f"> {sentiment}")
                report_lines.append("")
                
                report_lines.append(f"**技术+舆情结合点**:")
                report_lines.append(f"> {synergy}")
                report_lines.append("")
                
                report_lines.append(f"**止盈位**: {target}")
                report_lines.append(f"**预期收益**: {expected_return}")
                report_lines.append("")
                
                report_lines.append(f"**风险提示**: {risk}")
                report_lines.append("")
                report_lines.append("---")
                report_lines.append("")
            
            # 市场观点
            market_view = ai_result.get('market_view', '')
            if market_view:
                report_lines.append("## 📈 整体市场观点")
                report_lines.append("")
                report_lines.append(f"> {market_view}")
                report_lines.append("")
            
            # 操作策略
            strategy = ai_result.get('strategy_suggestion', '')
            if strategy:
                report_lines.append("## 💡 操作策略建议")
                report_lines.append("")
                report_lines.append(f"> {strategy}")
                report_lines.append("")
        
        else:
            report_lines.append("## ⚠️  AI分析失败")
            report_lines.append("")
            report_lines.append("未能获取AI推荐结果，请检查API连接。")
            report_lines.append("")
        
        # 候选股票列表
        report_lines.append("## 📋 候选股票列表 (TOP 10)")
        report_lines.append("")
        
        for i, (_, stock) in enumerate(df_stocks.head(10).iterrows(), 1):
            report_lines.append(f"### {i}. {stock['名称']} ({stock['代码']})")
            report_lines.append("")
            report_lines.append(f"- 涨跌幅: {stock['涨跌幅']:.2f}%")
            report_lines.append(f"- 最新价: {stock['最新价']:.2f}元")
            report_lines.append(f"- 市值: {stock['市值_亿']:.1f}亿")
            report_lines.append(f"- 换手率: {stock['换手率']:.2f}%")
            report_lines.append(f"- 舆情评分: {stock['舆情评分']:.1f}/100")
            report_lines.append(f"- 综合得分: {stock['综合得分']:.2f}")
            
            if stock['匹配关键词']:
                report_lines.append(f"- 匹配关键词: {stock['匹配关键词']}")
            
            report_lines.append("")
        
        # 免责声明
        report_lines.append("---")
        report_lines.append("")
        report_lines.append("## ⚠️  免责声明")
        report_lines.append("")
        report_lines.append("1. 本报告由AI算法自动生成，仅供参考")
        report_lines.append("2. 股票投资有风险，入市需谨慎")
        report_lines.append("3. 请结合自身风险承受能力做出投资决策")
        report_lines.append("4. 不构成任何投资建议")
        report_lines.append("")
        
        # 写入文件
        report_content = "\n".join(report_lines)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"✓ 报告已保存: {filename}")
        
        return filename
    
    def run(self):
        """
        运行完整的量化选股流程
        """
        print("=" * 60)
        print("量化选股器 (Quant Picker)")
        print("=" * 60)
        print()
        
        # Step 1: AkShare指标初选
        df_stocks = self.step1_akshare_screening()
        
        if df_stocks.empty:
            print("\n× 初选无结果，程序结束")
            return
        
        # Step 2: 舆情碰撞
        df_stocks = self.step2_sentiment_match(df_stocks)
        
        # Step 3: DeepSeek终极筛选
        ai_result = self.step3_deepseek_selection(df_stocks, top_n=10)
        
        # Step 4: 生成报告
        report_file = self.step4_generate_report(df_stocks, ai_result)
        
        # 保存候选股票数据
        csv_file = f"quant_picker_candidates_{datetime.now().strftime('%Y%m%d')}.csv"
        df_stocks.to_csv(csv_file, index=False, encoding='utf-8-sig')
        
        print("\n" + "=" * 60)
        print("✅ 量化选股完成！")
        print("=" * 60)
        print(f"\n生成文件:")
        print(f"  - AI推荐报告: {report_file}")
        print(f"  - 候选股票数据: {csv_file}")
        
        # 显示AI推荐结果
        if ai_result and 'recommendations' in ai_result:
            print("\n【AI推荐TOP 3】")
            print("-" * 60)
            for rec in ai_result['recommendations']:
                print(f"{rec['rank']}. {rec['stock_name']} ({rec['stock_code']})")
                print(f"   止盈位: {rec['target_price']} | 预期收益: {rec['expected_return']}")
                print(f"   理由: {rec['reason'][:50]}...")
                print()


def main():
    """主函数"""
    # 创建选股器实例
    picker = QuantPicker()
    
    # 运行选股流程
    picker.run()


if __name__ == "__main__":
    main()
