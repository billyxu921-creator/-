#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博黄金情绪自动分析系统 - 加权优化版
使用Playwright抓取微博数据，DeepSeek AI分析情绪
新增：博主影响力加权、关键词加成、加权公式计算
"""

import pandas as pd
import random
import time
import json
import requests
from datetime import datetime
from playwright.sync_api import sync_playwright
import re
import numpy as np


class WeiboSentimentWeightedAnalyzer:
    """微博情绪分析器 - 加权优化版"""
    
    def __init__(self, api_key=None):
        """
        初始化分析器
        
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
        
        # 营销广告关键词（用于过滤）
        self.spam_keywords = [
            '抽奖', '转运珠', '代购', '微商', '加微信', '扫码',
            '优惠', '促销', '打折', '秒杀', '拼团', '砍价',
            '免费领', '限时', '特价', '包邮', '直播间'
        ]
        
        # 关键词加成配置
        self.boost_keywords = ['涨停', '重组', '入股', '并购', '收购', '增持', '回购']
        self.boost_ratio = 0.20  # 20%加成
        
        # AI分析的系统提示词
        self.system_prompt = """你是一位行为金融学专家，请分析这些微博文本，给出以下内容：

【重要规则 - 防止幻觉】:
1. 你只能根据提供的微博内容进行分析
2. 如果微博内容不足以判断情绪，请在summary中说明'内容不足，无法判断'
3. 禁止编造任何微博内容、新闻或事件
4. 风险点和机会点必须从微博内容中提取，如果没有则说明'未提及'
5. 如果微博中没有提到具体事件，不要编造事件
6. 日期信息必须来自微博原文，不得编造
7. 所有结论必须基于提供的真实微博内容
8. 如果微博内容主要是广告或无关内容，请在summary中说明

1. 黄金看涨情绪指数（0-100分）- 必须基于提供的微博内容
   - 0-20: 极度悲观，恐慌性抛售
   - 21-40: 悲观，看跌情绪明显
   - 41-60: 中性，观望为主
   - 61-80: 乐观，看涨情绪明显
   - 81-100: 极度乐观，追涨热情高

2. 今日微博用户最担心的3个风险点（必须从微博内容中提取，如果没有则说明'未提及'）

3. 今日微博用户最期待的3个机会点（必须从微博内容中提取，如果没有则说明'未提及'）

请以JSON格式输出：
{
    "sentiment_index": 数值(0-100),
    "sentiment_label": "情绪标签",
    "risk_points": ["风险点1（从微博提取）", "风险点2（从微博提取）", "风险点3（从微博提取）"],
    "opportunity_points": ["机会点1（从微博提取）", "机会点2（从微博提取）", "机会点3（从微博提取）"],
    "summary": "一句话总结今日黄金情绪（基于提供的微博内容）",
    "data_quality_note": "如果数据不足或质量差，请在此说明"
}

注意：严禁编造任何内容，所有分析必须基于提供的真实微博文本。"""
    
    def calculate_influence_weight(self, followers_count):
        """
        计算博主影响力权重
        
        参数:
            followers_count: 粉丝数
            
        返回:
            float: 影响力权重
        """
        if followers_count >= 1000000:  # 100万+
            return 10.0
        elif followers_count >= 100000:  # 10万+
            return 3.0
        else:
            return 1.0
    
    def detect_keyword_boost(self, text):
        """
        检测关键词加成
        
        参数:
            text: 文本内容
            
        返回:
            tuple: (是否有加成, 匹配的关键词列表)
        """
        matched_keywords = [kw for kw in self.boost_keywords if kw in text]
        has_boost = len(matched_keywords) > 0
        return has_boost, matched_keywords
    
    def calculate_weighted_sentiment(self, ai_score, has_boost, influence_weight):
        """
        计算加权情绪分数
        
        公式: Final_Score = (AI_Sentiment_Score + Keyword_Bonus) * Influence_Weight
        归一化: 确保最终分数在0-100之间
        
        参数:
            ai_score: AI原始分数 (0-100)
            has_boost: 是否有关键词加成
            influence_weight: 影响力权重
            
        返回:
            dict: 包含各项分数的字典
        """
        # 1. 计算关键词加成
        keyword_bonus = ai_score * self.boost_ratio if has_boost else 0
        
        # 2. 应用加权公式
        weighted_score = (ai_score + keyword_bonus) * influence_weight
        
        # 3. 归一化到0-100
        # 最大可能值: (100 + 20) * 10 = 1200
        # 归一化公式: score / max_possible * 100
        max_possible = (100 + 100 * self.boost_ratio) * 10  # 1200
        normalized_score = min(100, (weighted_score / max_possible) * 100)
        
        return {
            'ai_score': ai_score,
            'keyword_bonus': keyword_bonus,
            'influence_weight': influence_weight,
            'weighted_score': weighted_score,
            'final_score': round(normalized_score, 2)
        }

    
    def scrape_weibo_gold(self, pages=3, headless=False):
        """
        使用Playwright抓取微博黄金相关内容
        
        参数:
            pages: 抓取页数（默认3页）
            headless: 是否无头模式（False方便扫码登录）
            
        返回:
            DataFrame: 包含微博数据
        """
        print("=" * 60)
        print("开始抓取微博黄金相关内容（加权优化版）")
        print("=" * 60)
        
        all_posts = []
        
        with sync_playwright() as p:
            print(f"启动浏览器 (headless={headless})...")
            browser = p.chromium.launch(headless=headless)
            
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            )
            
            page = context.new_page()
            
            try:
                print("\n步骤1: 访问微博搜索页...")
                weibo_search_url = "https://s.weibo.com/weibo?q=黄金"
                page.goto(weibo_search_url, timeout=30000)
                
                wait_time = random.uniform(3, 7)
                print(f"等待 {wait_time:.1f} 秒...")
                time.sleep(wait_time)
                
                # 检查是否需要登录
                if "login" in page.url.lower() or page.locator('text=登录').count() > 0:
                    print("\n⚠️  需要登录微博")
                    print("请在浏览器中完成登录（扫码或账号密码）")
                    print("登录完成后，按回车继续...")
                    input()
                    
                    page.goto(weibo_search_url, timeout=30000)
                    time.sleep(random.uniform(3, 5))
                
                print(f"\n步骤2: 开始抓取数据（共{pages}页）...")
                
                for page_num in range(1, pages + 1):
                    print(f"\n正在抓取第 {page_num}/{pages} 页...")
                    
                    try:
                        page.wait_for_selector('.card-wrap', timeout=10000)
                    except:
                        print("  ⚠️  页面加载超时，尝试继续...")
                    
                    # 滚动页面
                    print("  滚动页面加载更多内容...")
                    for scroll in range(3):
                        page.evaluate('window.scrollBy(0, 800)')
                        time.sleep(random.uniform(1, 2))
                    
                    # 提取当前页面的微博内容（包含粉丝数）
                    posts = self._extract_posts_from_page(page)
                    all_posts.extend(posts)
                    print(f"  ✓ 本页提取 {len(posts)} 条微博")
                    
                    # 翻页
                    if page_num < pages:
                        try:
                            next_button = page.locator('a.next')
                            if next_button.count() > 0:
                                print("  点击下一页...")
                                next_button.click()
                                
                                wait_time = random.uniform(4, 8)
                                print(f"  等待 {wait_time:.1f} 秒...")
                                time.sleep(wait_time)
                            else:
                                print("  未找到下一页按钮，停止抓取")
                                break
                        except Exception as e:
                            print(f"  翻页失败: {e}")
                            break
                
                print(f"\n✓ 抓取完成，共获取 {len(all_posts)} 条微博")
                
            except Exception as e:
                print(f"\n× 抓取过程出错: {e}")
                import traceback
                traceback.print_exc()
            
            finally:
                print("\n关闭浏览器...")
                browser.close()
        
        if all_posts:
            df = pd.DataFrame(all_posts)
            return df
        else:
            return pd.DataFrame()
    
    def _extract_posts_from_page(self, page):
        """
        从当前页面提取微博内容（包含粉丝数）
        
        参数:
            page: Playwright页面对象
            
        返回:
            list: 微博数据列表
        """
        posts = []
        
        try:
            cards = page.locator('.card-wrap').all()
            
            for card in cards:
                try:
                    post_data = {}
                    
                    # 提取博主名
                    try:
                        author = card.locator('.name').inner_text()
                        post_data['博主名'] = author.strip()
                    except:
                        post_data['博主名'] = '未知'
                    
                    # 提取粉丝数（新增）
                    try:
                        # 尝试多种选择器
                        followers_text = ''
                        
                        # 方法1: 查找包含"粉丝"的文本
                        followers_elem = card.locator('text=/粉丝/')
                        if followers_elem.count() > 0:
                            followers_text = followers_elem.first.inner_text()
                        
                        # 方法2: 查找info区域
                        if not followers_text:
                            info_elem = card.locator('.info')
                            if info_elem.count() > 0:
                                info_text = info_elem.inner_text()
                                if '粉丝' in info_text:
                                    followers_text = info_text
                        
                        # 解析粉丝数
                        if followers_text:
                            # 提取数字和单位（如：123万、45.6万、1234）
                            match = re.search(r'(\d+\.?\d*)\s*([万千百]?)', followers_text)
                            if match:
                                num = float(match.group(1))
                                unit = match.group(2)
                                
                                if unit == '万':
                                    followers_count = int(num * 10000)
                                elif unit == '千':
                                    followers_count = int(num * 1000)
                                elif unit == '百':
                                    followers_count = int(num * 100)
                                else:
                                    followers_count = int(num)
                                
                                post_data['粉丝数'] = followers_count
                            else:
                                post_data['粉丝数'] = 0
                        else:
                            post_data['粉丝数'] = 0
                    except:
                        post_data['粉丝数'] = 0
                    
                    # 提取博文内容
                    try:
                        content = card.locator('.txt').inner_text()
                        post_data['博文内容'] = content.strip()
                    except:
                        post_data['博文内容'] = ''
                    
                    # 提取发布时间
                    try:
                        pub_time = card.locator('.from').inner_text()
                        post_data['发布时间'] = pub_time.strip()
                    except:
                        post_data['发布时间'] = ''
                    
                    # 提取点赞数
                    try:
                        likes = card.locator('text=/赞/').inner_text()
                        like_num = re.findall(r'\d+', likes)
                        post_data['点赞数'] = int(like_num[0]) if like_num else 0
                    except:
                        post_data['点赞数'] = 0
                    
                    # 提取转发数
                    try:
                        retweets = card.locator('text=/转发/').inner_text()
                        retweet_num = re.findall(r'\d+', retweets)
                        post_data['转发数'] = int(retweet_num[0]) if retweet_num else 0
                    except:
                        post_data['转发数'] = 0
                    
                    # 计算影响力权重（新增）
                    post_data['影响力权重'] = self.calculate_influence_weight(post_data['粉丝数'])
                    
                    # 检测关键词加成（新增）
                    has_boost, matched_kw = self.detect_keyword_boost(post_data['博文内容'])
                    post_data['关键词加成'] = has_boost
                    post_data['匹配关键词'] = ','.join(matched_kw) if matched_kw else ''
                    
                    if post_data['博文内容']:
                        posts.append(post_data)
                
                except:
                    continue
        
        except Exception as e:
            print(f"    提取微博失败: {e}")
        
        return posts

    
    def clean_data(self, df):
        """
        清洗数据
        
        参数:
            df: 原始数据DataFrame
            
        返回:
            DataFrame: 清洗后的数据
        """
        print("\n" + "=" * 60)
        print("开始数据清洗")
        print("=" * 60)
        
        original_count = len(df)
        print(f"原始数据: {original_count} 条")
        
        # 1. 过滤营销广告
        print("\n步骤1: 过滤营销广告...")
        mask = df['博文内容'].apply(lambda x: not any(keyword in str(x) for keyword in self.spam_keywords))
        df = df[mask].copy()
        print(f"  过滤后: {len(df)} 条 (移除 {original_count - len(df)} 条)")
        
        # 2. 去除过短的内容
        print("\n步骤2: 过滤过短内容...")
        before = len(df)
        df = df[df['博文内容'].str.len() >= 10].copy()
        print(f"  过滤后: {len(df)} 条 (移除 {before - len(df)} 条)")
        
        # 3. 去重
        print("\n步骤3: 去除重复内容...")
        before = len(df)
        df = df.drop_duplicates(subset=['博文内容'], keep='first')
        print(f"  去重后: {len(df)} 条 (移除 {before - len(df)} 条)")
        
        # 4. 重置索引
        df = df.reset_index(drop=True)
        
        # 5. 统计加权信息
        print(f"\n✓ 清洗完成，最终保留 {len(df)} 条有效数据")
        
        if not df.empty:
            print("\n【加权统计】")
            high_influence = len(df[df['影响力权重'] == 10])
            mid_influence = len(df[df['影响力权重'] == 3])
            low_influence = len(df[df['影响力权重'] == 1])
            
            print(f"  高影响力博主(100万+粉丝): {high_influence} 条 (权重×10)")
            print(f"  中影响力博主(10万+粉丝): {mid_influence} 条 (权重×3)")
            print(f"  普通博主: {low_influence} 条 (权重×1)")
            
            boost_count = len(df[df['关键词加成'] == True])
            print(f"  包含关键词加成: {boost_count} 条 (+20%)")
        
        return df
    
    def analyze_sentiment_with_ai_weighted(self, df):
        """
        使用DeepSeek AI分析情绪（加权版本）
        
        参数:
            df: 清洗后的数据DataFrame
            
        返回:
            dict: AI分析结果（包含加权计算）
        """
        print("\n" + "=" * 60)
        print("开始AI情绪分析（加权优化版）")
        print("=" * 60)
        
        if df.empty:
            print("× 没有数据可供分析")
            return None
        
        # 1. 按影响力权重排序，优先分析高影响力博主的内容
        print(f"\n准备分析 {len(df)} 条微博...")
        df_sorted = df.sort_values(by=['影响力权重', '点赞数', '转发数'], ascending=False)
        
        # 取前50条或全部
        top_posts = df_sorted.head(50)
        
        # 合并内容（标注影响力和关键词）
        combined_text = "\n\n---\n\n".join([
            f"【微博{i+1}】(粉丝:{row['粉丝数']}, 权重:{row['影响力权重']}, "
            f"关键词:{'是' if row['关键词加成'] else '否'})\n{row['博文内容']}"
            for i, (_, row) in enumerate(top_posts.iterrows())
        ])
        
        print(f"选取 {len(top_posts)} 条代表性微博进行分析")
        print(f"总字数: {len(combined_text)} 字")
        
        # 2. 调用DeepSeek API获取基础情绪分数
        print("\n正在调用DeepSeek API...")
        ai_result = self._call_deepseek_api(combined_text)
        
        if not ai_result:
            print("× AI分析失败")
            return None
        
        print("✓ AI基础分析完成")
        
        # 3. 计算加权情绪分数
        print("\n正在计算加权情绪分数...")
        
        ai_base_score = ai_result.get('sentiment_index', 50)
        
        # 计算每条微博的加权分数
        weighted_scores = []
        
        for _, row in top_posts.iterrows():
            score_detail = self.calculate_weighted_sentiment(
                ai_score=ai_base_score,
                has_boost=row['关键词加成'],
                influence_weight=row['影响力权重']
            )
            weighted_scores.append(score_detail['final_score'])
        
        # 计算平均加权分数
        avg_weighted_score = np.mean(weighted_scores)
        
        # 4. 整合结果
        ai_result['ai_base_score'] = ai_base_score
        ai_result['weighted_sentiment_index'] = round(avg_weighted_score, 2)
        ai_result['score_details'] = {
            'min_score': round(min(weighted_scores), 2),
            'max_score': round(max(weighted_scores), 2),
            'std_score': round(np.std(weighted_scores), 2)
        }
        
        print(f"✓ 加权计算完成")
        print(f"  AI基础分数: {ai_base_score}")
        print(f"  加权平均分数: {avg_weighted_score:.2f}")
        print(f"  分数范围: {ai_result['score_details']['min_score']} - {ai_result['score_details']['max_score']}")
        
        return ai_result
    
    def _call_deepseek_api(self, text):
        """
        调用DeepSeek API
        
        参数:
            text: 要分析的文本
            
        返回:
            dict: 分析结果
        """
        url = f"{self.api_base}/chat/completions"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"请分析以下微博内容：\n\n{text}"}
            ],
            "temperature": 0.3,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                
                try:
                    json_match = re.search(r'\{[\s\S]*\}', content)
                    if json_match:
                        json_str = json_match.group()
                        analysis_result = json.loads(json_str)
                        return analysis_result
                    else:
                        print("  警告: 无法从响应中提取JSON")
                        return None
                except json.JSONDecodeError:
                    print(f"  警告: JSON解析失败")
                    return None
            
            return None
            
        except Exception as e:
            print(f"  API调用失败: {e}")
            return None

    
    def generate_report(self, df, analysis_result):
        """
        生成Markdown格式的分析报告（加权版本）
        
        参数:
            df: 数据DataFrame
            analysis_result: AI分析结果
            
        返回:
            str: 报告文件路径
        """
        print("\n" + "=" * 60)
        print("生成分析报告（加权优化版）")
        print("=" * 60)
        
        today = datetime.now().strftime('%Y%m%d')
        filename = f"微博黄金情绪分析_加权版_{today}.md"
        
        report_lines = []
        
        # 标题
        report_lines.append(f"# 微博黄金情绪分析报告（加权优化版）")
        report_lines.append(f"")
        report_lines.append(f"**生成时间**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
        report_lines.append(f"")
        report_lines.append("---")
        report_lines.append("")
        
        # 数据概况
        report_lines.append("## 📊 数据概况")
        report_lines.append("")
        report_lines.append(f"- **抓取微博数**: {len(df)} 条")
        report_lines.append(f"- **平均点赞数**: {df['点赞数'].mean():.0f}")
        report_lines.append(f"- **平均转发数**: {df['转发数'].mean():.0f}")
        report_lines.append(f"- **最高点赞**: {df['点赞数'].max()}")
        report_lines.append("")
        
        # 加权统计
        report_lines.append("## ⚖️  加权统计")
        report_lines.append("")
        
        high_influence = len(df[df['影响力权重'] == 10])
        mid_influence = len(df[df['影响力权重'] == 3])
        low_influence = len(df[df['影响力权重'] == 1])
        
        report_lines.append("### 博主影响力分布")
        report_lines.append("")
        report_lines.append(f"- **高影响力博主** (100万+粉丝, 权重×10): {high_influence} 条")
        report_lines.append(f"- **中影响力博主** (10万+粉丝, 权重×3): {mid_influence} 条")
        report_lines.append(f"- **普通博主** (权重×1): {low_influence} 条")
        report_lines.append("")
        
        boost_count = len(df[df['关键词加成'] == True])
        report_lines.append("### 关键词加成")
        report_lines.append("")
        report_lines.append(f"- **包含关键词加成**: {boost_count} 条 (+20%)")
        report_lines.append(f"- **关键词**: {', '.join(self.boost_keywords)}")
        report_lines.append("")
        
        # AI分析结果
        if analysis_result:
            report_lines.append("## 🤖 AI情绪分析（加权优化）")
            report_lines.append("")
            
            # 基础分数 vs 加权分数
            ai_base_score = analysis_result.get('ai_base_score', 50)
            weighted_score = analysis_result.get('weighted_sentiment_index', 50)
            sentiment_label = analysis_result.get('sentiment_label', '中性')
            
            report_lines.append(f"### 情绪指数对比")
            report_lines.append("")
            report_lines.append(f"| 指标 | 分数 | 说明 |")
            report_lines.append(f"|------|------|------|")
            report_lines.append(f"| AI基础分数 | {ai_base_score} / 100 | DeepSeek原始分析 |")
            report_lines.append(f"| 加权平均分数 | {weighted_score} / 100 | 考虑影响力+关键词 |")
            report_lines.append(f"| 情绪标签 | {sentiment_label} | - |")
            report_lines.append("")
            
            # 分数详情
            score_details = analysis_result.get('score_details', {})
            report_lines.append(f"**分数统计**:")
            report_lines.append(f"- 最低分: {score_details.get('min_score', 0)}")
            report_lines.append(f"- 最高分: {score_details.get('max_score', 0)}")
            report_lines.append(f"- 标准差: {score_details.get('std_score', 0)}")
            report_lines.append("")
            
            # 情绪条形图
            bar_length = int(weighted_score / 5)
            bar = "🟩" * bar_length + "⬜" * (20 - bar_length)
            report_lines.append(f"```")
            report_lines.append(f"{bar}")
            report_lines.append(f"0    20   40   60   80   100")
            report_lines.append(f"```")
            report_lines.append("")
            
            # 一句话总结
            summary = analysis_result.get('summary', '')
            if summary:
                report_lines.append(f"**今日情绪**: {summary}")
                report_lines.append("")
            
            # 风险点
            risk_points = analysis_result.get('risk_points', [])
            if risk_points:
                report_lines.append("### ⚠️  用户最担心的3个风险点")
                report_lines.append("")
                for i, risk in enumerate(risk_points, 1):
                    report_lines.append(f"{i}. {risk}")
                report_lines.append("")
            
            # 机会点
            opportunity_points = analysis_result.get('opportunity_points', [])
            if opportunity_points:
                report_lines.append("### 💡 用户最期待的3个机会点")
                report_lines.append("")
                for i, opp in enumerate(opportunity_points, 1):
                    report_lines.append(f"{i}. {opp}")
                report_lines.append("")
        
        # 高影响力博主TOP 5
        report_lines.append("## 👑 高影响力博主 TOP 5")
        report_lines.append("")
        
        top_influencers = df.nlargest(5, '粉丝数')
        for i, (_, row) in enumerate(top_influencers.iterrows(), 1):
            report_lines.append(f"### {i}. @{row['博主名']}")
            report_lines.append(f"")
            report_lines.append(f"- 👥 粉丝数: {row['粉丝数']:,}")
            report_lines.append(f"- ⚖️  影响力权重: ×{row['影响力权重']}")
            report_lines.append(f"- 🔑 关键词加成: {'是' if row['关键词加成'] else '否'}")
            if row['匹配关键词']:
                report_lines.append(f"- 📌 匹配关键词: {row['匹配关键词']}")
            report_lines.append(f"")
            report_lines.append(f"> {row['博文内容'][:150]}{'...' if len(row['博文内容']) > 150 else ''}")
            report_lines.append(f"")
            report_lines.append(f"- 👍 点赞: {row['点赞数']} | 🔄 转发: {row['转发数']} | 📅 {row['发布时间']}")
            report_lines.append(f"")
        
        # 关键词加成微博
        boost_posts = df[df['关键词加成'] == True]
        if not boost_posts.empty:
            report_lines.append("## 🔥 包含关键词加成的微博")
            report_lines.append("")
            
            for i, (_, row) in enumerate(boost_posts.head(5).iterrows(), 1):
                report_lines.append(f"### {i}. @{row['博主名']}")
                report_lines.append(f"")
                report_lines.append(f"- 📌 匹配关键词: {row['匹配关键词']}")
                report_lines.append(f"- ⚖️  影响力权重: ×{row['影响力权重']}")
                report_lines.append(f"")
                report_lines.append(f"> {row['博文内容'][:150]}{'...' if len(row['博文内容']) > 150 else ''}")
                report_lines.append(f"")
                report_lines.append(f"- 👍 点赞: {row['点赞数']} | 🔄 转发: {row['转发数']}")
                report_lines.append(f"")
        
        # 加权公式说明
        report_lines.append("---")
        report_lines.append("")
        report_lines.append("## 📐 加权公式说明")
        report_lines.append("")
        report_lines.append("### 影响力权重")
        report_lines.append("```")
        report_lines.append("粉丝数 >= 100万: 权重 = 10")
        report_lines.append("粉丝数 >= 10万:  权重 = 3")
        report_lines.append("其他:            权重 = 1")
        report_lines.append("```")
        report_lines.append("")
        report_lines.append("### 关键词加成")
        report_lines.append("```")
        report_lines.append(f"关键词: {', '.join(self.boost_keywords)}")
        report_lines.append(f"加成比例: +{self.boost_ratio * 100}%")
        report_lines.append("```")
        report_lines.append("")
        report_lines.append("### 加权公式")
        report_lines.append("```")
        report_lines.append("Final_Score = (AI_Sentiment_Score + Keyword_Bonus) × Influence_Weight")
        report_lines.append("")
        report_lines.append("其中:")
        report_lines.append("- AI_Sentiment_Score: DeepSeek AI分析的基础分数 (0-100)")
        report_lines.append("- Keyword_Bonus: AI分数 × 20% (如果包含关键词)")
        report_lines.append("- Influence_Weight: 博主影响力权重 (1, 3, 或 10)")
        report_lines.append("")
        report_lines.append("归一化:")
        report_lines.append("- 最大可能值: (100 + 20) × 10 = 1200")
        report_lines.append("- 归一化公式: (Final_Score / 1200) × 100")
        report_lines.append("- 确保最终分数在 0-100 之间")
        report_lines.append("```")
        report_lines.append("")
        
        # 免责声明
        report_lines.append("---")
        report_lines.append("")
        report_lines.append("## ⚠️  免责声明")
        report_lines.append("")
        report_lines.append("本报告基于微博公开数据和AI分析生成，仅供参考，不构成投资建议。")
        report_lines.append("社交媒体情绪具有波动性，请结合其他信息源综合判断。")
        report_lines.append("")
        
        # 写入文件
        report_content = "\n".join(report_lines)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"✓ 报告已保存: {filename}")
        
        return filename
    
    def run(self, pages=3, headless=False):
        """
        运行完整的分析流程（加权优化版）
        
        参数:
            pages: 抓取页数
            headless: 是否无头模式
        """
        print("=" * 60)
        print("微博黄金情绪自动分析系统（加权优化版）")
        print("=" * 60)
        print()
        
        # 1. 抓取数据
        df = self.scrape_weibo_gold(pages=pages, headless=headless)
        
        if df.empty:
            print("\n× 未抓取到数据，程序结束")
            return
        
        # 保存原始数据
        raw_filename = f"weibo_raw_weighted_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(raw_filename, index=False, encoding='utf-8-sig')
        print(f"\n原始数据已保存: {raw_filename}")
        
        # 2. 清洗数据
        df_clean = self.clean_data(df)
        
        if df_clean.empty:
            print("\n× 清洗后无有效数据，程序结束")
            return
        
        # 保存清洗后的数据
        clean_filename = f"weibo_clean_weighted_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df_clean.to_csv(clean_filename, index=False, encoding='utf-8-sig')
        print(f"清洗数据已保存: {clean_filename}")
        
        # 3. AI加权分析
        analysis_result = self.analyze_sentiment_with_ai_weighted(df_clean)
        
        # 4. 生成报告
        report_file = self.generate_report(df_clean, analysis_result)
        
        print("\n" + "=" * 60)
        print("✅ 分析完成！")
        print("=" * 60)
        print(f"\n生成文件:")
        print(f"  - 原始数据: {raw_filename}")
        print(f"  - 清洗数据: {clean_filename}")
        print(f"  - 分析报告: {report_file}")


def main():
    """主函数"""
    # 创建分析器实例
    analyzer = WeiboSentimentWeightedAnalyzer()
    
    # 运行分析
    analyzer.run(pages=3, headless=False)


if __name__ == "__main__":
    main()
