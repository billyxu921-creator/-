#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博黄金情绪自动分析系统
使用Playwright抓取微博数据，DeepSeek AI分析情绪
"""

import pandas as pd
import random
import time
import json
import requests
from datetime import datetime
from playwright.sync_api import sync_playwright
import re


class WeiboGoldSentimentAnalyzer:
    """微博黄金情绪分析器"""
    
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
        
        # AI分析的系统提示词
        self.system_prompt = """你是一位行为金融学专家，请分析这些微博文本，给出以下内容：

1. 黄金看涨情绪指数（0-100分）
   - 0-20: 极度悲观，恐慌性抛售
   - 21-40: 悲观，看跌情绪明显
   - 41-60: 中性，观望为主
   - 61-80: 乐观，看涨情绪明显
   - 81-100: 极度乐观，追涨热情高

2. 今日微博用户最担心的3个风险点

3. 今日微博用户最期待的3个机会点

请以JSON格式输出：
{
    "sentiment_index": 数值(0-100),
    "sentiment_label": "情绪标签",
    "risk_points": ["风险点1", "风险点2", "风险点3"],
    "opportunity_points": ["机会点1", "机会点2", "机会点3"],
    "summary": "一句话总结今日黄金情绪"
}"""
    
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
        print("开始抓取微博黄金相关内容")
        print("=" * 60)
        
        all_posts = []
        
        with sync_playwright() as p:
            # 启动浏览器（headless=False方便扫码登录）
            print(f"启动浏览器 (headless={headless})...")
            browser = p.chromium.launch(headless=headless)
            
            # 创建浏览器上下文（模拟真实用户）
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            )
            
            # 创建新页面
            page = context.new_page()
            
            try:
                # 1. 导航到微博搜索页
                print("\n步骤1: 访问微博搜索页...")
                weibo_search_url = "https://s.weibo.com/weibo?q=黄金"
                page.goto(weibo_search_url, timeout=30000)
                
                # 随机等待，模拟真实用户
                wait_time = random.uniform(3, 7)
                print(f"等待 {wait_time:.1f} 秒...")
                time.sleep(wait_time)
                
                # 检查是否需要登录
                if "login" in page.url.lower() or page.locator('text=登录').count() > 0:
                    print("\n⚠️  需要登录微博")
                    print("请在浏览器中完成登录（扫码或账号密码）")
                    print("登录完成后，按回车继续...")
                    input()
                    
                    # 登录后重新访问搜索页
                    page.goto(weibo_search_url, timeout=30000)
                    time.sleep(random.uniform(3, 5))
                
                # 2. 开始抓取数据
                print(f"\n步骤2: 开始抓取数据（共{pages}页）...")
                
                for page_num in range(1, pages + 1):
                    print(f"\n正在抓取第 {page_num}/{pages} 页...")
                    
                    # 等待内容加载
                    try:
                        page.wait_for_selector('.card-wrap', timeout=10000)
                    except:
                        print("  ⚠️  页面加载超时，尝试继续...")
                    
                    # 滚动页面，触发懒加载
                    print("  滚动页面加载更多内容...")
                    for scroll in range(3):
                        page.evaluate('window.scrollBy(0, 800)')
                        time.sleep(random.uniform(1, 2))
                    
                    # 提取当前页面的微博内容
                    posts = self._extract_posts_from_page(page)
                    all_posts.extend(posts)
                    print(f"  ✓ 本页提取 {len(posts)} 条微博")
                    
                    # 如果不是最后一页，点击下一页
                    if page_num < pages:
                        try:
                            # 查找并点击"下一页"按钮
                            next_button = page.locator('a.next')
                            if next_button.count() > 0:
                                print("  点击下一页...")
                                next_button.click()
                                
                                # 随机等待，避免被识别为爬虫
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
                # 关闭浏览器
                print("\n关闭浏览器...")
                browser.close()
        
        # 转换为DataFrame
        if all_posts:
            df = pd.DataFrame(all_posts)
            return df
        else:
            return pd.DataFrame()
    
    def _extract_posts_from_page(self, page):
        """
        从当前页面提取微博内容
        
        参数:
            page: Playwright页面对象
            
        返回:
            list: 微博数据列表
        """
        posts = []
        
        try:
            # 查找所有微博卡片
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
                        # 提取数字
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
                    
                    # 只保存有内容的微博
                    if post_data['博文内容']:
                        posts.append(post_data)
                
                except Exception as e:
                    # 单条微博提取失败不影响其他
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
        
        # 2. 去除过短的内容（少于10个字）
        print("\n步骤2: 过滤过短内容...")
        before = len(df)
        df = df[df['博文内容'].str.len() >= 10].copy()
        print(f"  过滤后: {len(df)} 条 (移除 {before - len(df)} 条)")
        
        # 3. 去重（根据博文内容）
        print("\n步骤3: 去除重复内容...")
        before = len(df)
        df = df.drop_duplicates(subset=['博文内容'], keep='first')
        print(f"  去重后: {len(df)} 条 (移除 {before - len(df)} 条)")
        
        # 4. 重置索引
        df = df.reset_index(drop=True)
        
        print(f"\n✓ 清洗完成，最终保留 {len(df)} 条有效数据")
        
        return df
    
    def analyze_sentiment_with_ai(self, df):
        """
        使用DeepSeek AI分析情绪
        
        参数:
            df: 清洗后的数据DataFrame
            
        返回:
            dict: AI分析结果
        """
        print("\n" + "=" * 60)
        print("开始AI情绪分析")
        print("=" * 60)
        
        if df.empty:
            print("× 没有数据可供分析")
            return None
        
        # 1. 合并所有博文内容
        print(f"\n准备分析 {len(df)} 条微博...")
        
        # 选择点赞数和转发数较高的微博（更有代表性）
        df_sorted = df.sort_values(by=['点赞数', '转发数'], ascending=False)
        
        # 取前50条或全部（如果少于50条）
        top_posts = df_sorted.head(50)
        
        # 合并内容
        combined_text = "\n\n---\n\n".join([
            f"【微博{i+1}】{row['博文内容']}"
            for i, (_, row) in enumerate(top_posts.iterrows())
        ])
        
        print(f"选取 {len(top_posts)} 条代表性微博进行分析")
        print(f"总字数: {len(combined_text)} 字")
        
        # 2. 调用DeepSeek API
        print("\n正在调用DeepSeek API...")
        
        result = self._call_deepseek_api(combined_text)
        
        if result:
            print("✓ AI分析完成")
            return result
        else:
            print("× AI分析失败")
            return None
    
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
                
                # 尝试解析JSON
                try:
                    # 提取JSON部分（可能包含在markdown代码块中）
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
                    print(f"  原始响应: {content[:200]}...")
                    return None
            
            return None
            
        except Exception as e:
            print(f"  API调用失败: {e}")
            return None
    
    def generate_report(self, df, analysis_result):
        """
        生成Markdown格式的分析报告
        
        参数:
            df: 数据DataFrame
            analysis_result: AI分析结果
            
        返回:
            str: 报告文件路径
        """
        print("\n" + "=" * 60)
        print("生成分析报告")
        print("=" * 60)
        
        # 生成文件名（以日期命名）
        today = datetime.now().strftime('%Y%m%d')
        filename = f"微博黄金情绪分析_{today}.md"
        
        # 构建报告内容
        report_lines = []
        
        # 标题
        report_lines.append(f"# 微博黄金情绪分析报告")
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
        
        # AI分析结果
        if analysis_result:
            report_lines.append("## 🤖 AI情绪分析")
            report_lines.append("")
            
            # 情绪指数
            sentiment_index = analysis_result.get('sentiment_index', 50)
            sentiment_label = analysis_result.get('sentiment_label', '中性')
            
            report_lines.append(f"### 黄金看涨情绪指数")
            report_lines.append("")
            report_lines.append(f"**{sentiment_index} / 100** - {sentiment_label}")
            report_lines.append("")
            
            # 情绪条形图（用emoji表示）
            bar_length = int(sentiment_index / 5)
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
        
        # 热门微博
        report_lines.append("## 🔥 热门微博 TOP 10")
        report_lines.append("")
        
        top_posts = df.nlargest(10, '点赞数')
        for i, (_, row) in enumerate(top_posts.iterrows(), 1):
            report_lines.append(f"### {i}. @{row['博主名']}")
            report_lines.append(f"")
            report_lines.append(f"> {row['博文内容'][:200]}{'...' if len(row['博文内容']) > 200 else ''}")
            report_lines.append(f"")
            report_lines.append(f"- 👍 点赞: {row['点赞数']} | 🔄 转发: {row['转发数']} | 📅 {row['发布时间']}")
            report_lines.append(f"")
        
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
        运行完整的分析流程
        
        参数:
            pages: 抓取页数
            headless: 是否无头模式
        """
        print("=" * 60)
        print("微博黄金情绪自动分析系统")
        print("=" * 60)
        print()
        
        # 1. 抓取数据
        df = self.scrape_weibo_gold(pages=pages, headless=headless)
        
        if df.empty:
            print("\n× 未抓取到数据，程序结束")
            return
        
        # 保存原始数据
        raw_filename = f"weibo_raw_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(raw_filename, index=False, encoding='utf-8-sig')
        print(f"\n原始数据已保存: {raw_filename}")
        
        # 2. 清洗数据
        df_clean = self.clean_data(df)
        
        if df_clean.empty:
            print("\n× 清洗后无有效数据，程序结束")
            return
        
        # 保存清洗后的数据
        clean_filename = f"weibo_clean_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df_clean.to_csv(clean_filename, index=False, encoding='utf-8-sig')
        print(f"清洗数据已保存: {clean_filename}")
        
        # 3. AI分析
        analysis_result = self.analyze_sentiment_with_ai(df_clean)
        
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
    analyzer = WeiboGoldSentimentAnalyzer()
    
    # 运行分析
    # pages=3: 抓取3页数据
    # headless=False: 显示浏览器窗口，方便扫码登录
    analyzer.run(pages=3, headless=False)


if __name__ == "__main__":
    main()