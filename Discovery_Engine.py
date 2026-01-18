#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全网热点发现引擎 (Discovery Engine)
自动识别小红书和微博上讨论度异常升高的股票板块

功能特点:
1. 多源探测: 小红书财经频道推荐流 + 微博财经热搜榜 + 股票超话
2. 强制反爬: headless=False、随机等待5.5-12.2秒、拟人滚动、真实User-Agent
3. AI智能发现: 对比今日与昨日词频，识别动量最大的3个非预设板块
4. 生成Markdown简报: 【全网雷达：你可能错过的热门机会】
"""

import pandas as pd
import random
import time
import json
import requests
import re
import os
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright
from collections import Counter
import winsound  # Windows系统蜂鸣声（macOS需要替换为其他方案）


class DiscoveryEngine:
    """全网热点发现引擎"""
    
    def __init__(self, api_key=None):
        """
        初始化发现引擎
        
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
        
        # 真实的User-Agent列表（用于随机切换）
        self.user_agents = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0'
        ]
        
        # 历史数据存储路径
        self.history_dir = "discovery_history"
        if not os.path.exists(self.history_dir):
            os.makedirs(self.history_dir)
        
        # AI分析的系统提示词
        self.system_prompt = """你是一位资深的金融市场分析师和数据科学家。

任务: 分析今日和昨日的财经讨论文本，识别出讨论度异常升高的股票板块。

【重要规则 - 防止幻觉】:
1. 你只能根据提供的今日和昨日文本数据进行分析
2. 如果文本中没有相关板块信息，请在reason中说明'未找到相关内容'
3. 禁止编造任何新闻、政策或事件
4. 增长率必须基于提供的今日和昨日提及次数计算，不得编造
5. 如果某个板块昨日提及次数为0，请谨慎判断是否为真实热点
6. 严禁推荐任何非A股市场的板块
7. 火爆原因必须基于提供的文本内容，不得编造具体事件
8. 如果无法确定原因，请说明'原因不明，需进一步观察'
9. 关键事件必须从提供的文本中提取，不得编造
10. 所有结论必须基于提供的真实数据

分析要求:
1. 提取所有提到的行业板块关键词（如：煤炭、核电、新能源、半导体、医药等）
2. 对比今日与昨日的词频变化，计算增长率（公式：(今日-昨日)/昨日×100%）
3. 识别出动量最大的3个非预设板块（排除：黄金、大盘、A股等泛指词）
4. 分析每个板块火爆的原因（必须基于提供的文本内容，不得编造）

输出格式（JSON）:
{
    "hot_sectors": [
        {
            "sector_name": "板块名称（必须在提供的文本中出现）",
            "growth_rate": 增长率（基于提供的数据计算，如150表示增长150%）,
            "today_mentions": 今日提及次数（必须是真实统计值）,
            "yesterday_mentions": 昨日提及次数（必须是真实统计值）,
            "reason": "火爆原因分析（必须基于提供的文本内容，如果不确定则说明'原因不明'）",
            "confidence": 置信度(0.0-1.0，如果数据不足请降低置信度)
        }
    ],
    "market_sentiment": "整体市场情绪描述（基于提供的文本）",
    "key_events": ["关键事件1（从文本提取）", "关键事件2（从文本提取）", "关键事件3（从文本提取）"],
    "data_quality_note": "如果数据质量差或不足，请在此说明"
}

注意: 只返回JSON格式，不要包含其他文字。严禁编造任何数据或事件。"""

    
    def beep_alert(self):
        """
        验证码提示蜂鸣声
        macOS系统使用print提示（因为winsound仅支持Windows）
        """
        try:
            # macOS系统使用系统提示音
            os.system('afplay /System/Library/Sounds/Glass.aiff')
        except:
            # 如果失败，使用print提示
            print("\n" + "🔔" * 20)
            print("⚠️  检测到验证码！请手动处理！")
            print("🔔" * 20 + "\n")
    
    def random_wait(self, min_sec=5.5, max_sec=12.2):
        """
        随机等待（反爬策略）
        
        参数:
            min_sec: 最小等待秒数
            max_sec: 最大等待秒数
        """
        wait_time = random.uniform(min_sec, max_sec)
        print(f"  ⏳ 随机等待 {wait_time:.1f} 秒...")
        time.sleep(wait_time)
    
    def slow_scroll(self, page, distance=800):
        """
        拟人化缓慢滚动
        
        参数:
            page: Playwright页面对象
            distance: 滚动距离（像素）
        """
        # 分多次小幅度滚动，模拟真实用户
        steps = random.randint(3, 6)
        step_distance = distance // steps
        
        for i in range(steps):
            page.mouse.wheel(0, step_distance)
            time.sleep(random.uniform(0.3, 0.8))
    
    def scrape_xiaohongshu(self, target_count=50, headless=False):
        """
        抓取小红书财经频道推荐流
        
        参数:
            target_count: 目标抓取笔记数量
            headless: 是否无头模式
            
        返回:
            list: 笔记数据列表
        """
        print("=" * 60)
        print("开始抓取小红书财经频道")
        print("=" * 60)
        
        all_notes = []
        
        try:
            with sync_playwright() as p:
                # 随机选择User-Agent
                user_agent = random.choice(self.user_agents)
                
                print(f"启动浏览器 (headless={headless})...")
                browser = p.chromium.launch(headless=headless)
                
                context = browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent=user_agent
                )
                
                page = context.new_page()
                
                try:
                    # 访问小红书财经频道
                    print("\n步骤1: 访问小红书财经频道...")
                    xhs_url = "https://www.xiaohongshu.com/explore"
                    page.goto(xhs_url, timeout=30000)
                    
                    self.random_wait(5.5, 8.0)
                    
                    # 检查是否需要登录
                    if self._check_login_required(page, "小红书"):
                        print("\n⚠️  需要登录小红书")
                        print("请在浏览器中完成登录（扫码或账号密码）")
                        print("登录完成后，按回车继续...")
                        input()
                        
                        # 登录后重新访问
                        page.goto(xhs_url, timeout=30000)
                        self.random_wait(3.0, 5.0)
                    
                    # 搜索财经相关内容（包含多个热门板块关键词）
                    print("\n步骤2: 搜索财经相关内容...")
                    try:
                        search_box = page.locator('input[placeholder*="搜索"]').first
                        # 使用更广泛的搜索关键词，覆盖多个热门板块
                        search_keywords = "财经 理财 股票 投资"
                        search_box.fill(search_keywords)
                        self.random_wait(1.0, 2.0)
                        search_box.press("Enter")
                        self.random_wait(5.5, 8.0)
                    except:
                        print("  ⚠️  搜索框定位失败，使用推荐流...")
                    
                    # 开始滚动抓取推荐流
                    print(f"\n步骤3: 滚动抓取推荐流（目标{target_count}条）...")
                    
                    scroll_count = 0
                    max_scrolls = 20  # 最多滚动20次
                    
                    while len(all_notes) < target_count and scroll_count < max_scrolls:
                        scroll_count += 1
                        print(f"\n  第 {scroll_count} 次滚动 (已抓取 {len(all_notes)}/{target_count})...")
                        
                        # 检查验证码
                        if self._check_captcha(page):
                            self.beep_alert()
                            print("  请手动完成验证码，完成后按回车继续...")
                            input()
                        
                        # 提取当前页面的笔记
                        notes = self._extract_xiaohongshu_notes(page)
                        
                        # 去重添加
                        for note in notes:
                            if note not in all_notes:
                                all_notes.append(note)
                        
                        print(f"  ✓ 本次提取 {len(notes)} 条，累计 {len(all_notes)} 条")
                        
                        # 如果已达到目标，停止
                        if len(all_notes) >= target_count:
                            break
                        
                        # 拟人化滚动
                        self.slow_scroll(page, distance=random.randint(600, 1000))
                        
                        # 随机等待
                        self.random_wait(5.5, 12.2)
                    
                    print(f"\n✓ 小红书抓取完成，共获取 {len(all_notes)} 条笔记")
                
                except Exception as e:
                    print(f"\n× 小红书抓取出错: {e}")
                    import traceback
                    traceback.print_exc()
                
                finally:
                    browser.close()
        
        except Exception as e:
            print(f"\n× 小红书模块失败: {e}")
            print("  继续执行其他平台...")
        
        return all_notes

    
    def _extract_xiaohongshu_notes(self, page):
        """
        从当前页面提取小红书笔记
        
        参数:
            page: Playwright页面对象
            
        返回:
            list: 笔记数据列表
        """
        notes = []
        
        try:
            # 小红书的笔记卡片选择器（可能需要根据实际页面调整）
            note_cards = page.locator('.note-item, .cover, section').all()
            
            for card in note_cards[:20]:  # 每次最多提取20条
                try:
                    note_data = {}
                    
                    # 提取标题
                    try:
                        title = card.locator('.title, .note-title').inner_text()
                        note_data['标题'] = title.strip()
                    except:
                        note_data['标题'] = ''
                    
                    # 提取摘要/内容
                    try:
                        content = card.locator('.desc, .content').inner_text()
                        note_data['内容'] = content.strip()
                    except:
                        note_data['内容'] = ''
                    
                    # 提取点赞数
                    try:
                        likes_text = card.locator('.like, .like-count').inner_text()
                        likes = re.findall(r'\d+', likes_text)
                        note_data['点赞数'] = int(likes[0]) if likes else 0
                    except:
                        note_data['点赞数'] = 0
                    
                    # 提取评论数
                    try:
                        comments_text = card.locator('.comment, .comment-count').inner_text()
                        comments = re.findall(r'\d+', comments_text)
                        note_data['评论数'] = int(comments[0]) if comments else 0
                    except:
                        note_data['评论数'] = 0
                    
                    # 来源平台
                    note_data['平台'] = '小红书'
                    note_data['抓取时间'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    # 只保存有标题或内容的笔记
                    if note_data['标题'] or note_data['内容']:
                        notes.append(note_data)
                
                except:
                    continue
        
        except Exception as e:
            print(f"    提取笔记失败: {e}")
        
        return notes
    
    def scrape_weibo(self, headless=False):
        """
        抓取微博财经热搜榜和股票超话
        
        参数:
            headless: 是否无头模式
            
        返回:
            list: 微博数据列表
        """
        print("\n" + "=" * 60)
        print("开始抓取微博财经热搜和股票超话")
        print("=" * 60)
        
        all_posts = []
        
        try:
            with sync_playwright() as p:
                user_agent = random.choice(self.user_agents)
                
                print(f"启动浏览器 (headless={headless})...")
                browser = p.chromium.launch(headless=headless)
                
                context = browser.new_context(
                    viewport={'width': 1920, 'height': 1080},
                    user_agent=user_agent
                )
                
                page = context.new_page()
                
                try:
                    # 1. 抓取财经热搜榜
                    print("\n步骤1: 抓取微博财经热搜榜...")
                    posts_hot = self._scrape_weibo_hot_search(page)
                    all_posts.extend(posts_hot)
                    print(f"  ✓ 财经热搜: {len(posts_hot)} 条")
                    
                    self.random_wait(5.5, 8.0)
                    
                    # 2. 抓取股票超话
                    print("\n步骤2: 抓取股票超话...")
                    posts_topic = self._scrape_weibo_stock_topic(page)
                    all_posts.extend(posts_topic)
                    print(f"  ✓ 股票超话: {len(posts_topic)} 条")
                    
                    print(f"\n✓ 微博抓取完成，共获取 {len(all_posts)} 条")
                
                except Exception as e:
                    print(f"\n× 微博抓取出错: {e}")
                    import traceback
                    traceback.print_exc()
                
                finally:
                    browser.close()
        
        except Exception as e:
            print(f"\n× 微博模块失败: {e}")
            print("  继续执行其他平台...")
        
        return all_posts
    
    def _scrape_weibo_hot_search(self, page):
        """抓取微博财经热搜榜"""
        posts = []
        
        try:
            # 访问微博热搜页
            weibo_hot_url = "https://s.weibo.com/top/summary"
            page.goto(weibo_hot_url, timeout=30000)
            
            self.random_wait(3.0, 5.0)
            
            # 检查登录
            if self._check_login_required(page, "微博"):
                print("\n⚠️  需要登录微博")
                print("请在浏览器中完成登录")
                print("登录完成后，按回车继续...")
                input()
                page.goto(weibo_hot_url, timeout=30000)
                self.random_wait(3.0, 5.0)
            
            # 查找财经相关热搜
            hot_items = page.locator('tbody tr').all()
            
            for item in hot_items[:30]:  # 取前30条
                try:
                    text = item.inner_text()
                    
                    # 筛选财经相关（包含：股、金融、经济、A股、港股等关键词）
                    # 新增：肥料、战争、卫星、脑机接口等热点板块关键词
                    finance_keywords = [
                        # 基础财经关键词
                        '股', '金融', '经济', 'A股', '港股', '基金', '投资', '理财', '上市', '市值',
                        # 行业板块关键词
                        '肥料', '化肥', '磷肥', '钾肥', '氮肥',  # 肥料板块
                        '战争', '军工', '国防', '武器', '军事',  # 战争/军工板块
                        '卫星', '航天', '火箭', '太空', '北斗',  # 卫星/航天板块
                        '脑机接口', '脑机', '神经', '马斯克', 'Neuralink',  # 脑机接口板块
                        # 其他热门板块
                        '煤炭', '核电', '新能源', '光伏', '风电', '储能',
                        '半导体', '芯片', '人工智能', 'AI', '机器人',
                        '医药', '生物', '疫苗', '医疗',
                        '房地产', '地产', '建筑', '基建'
                    ]
                    
                    if any(keyword in text for keyword in finance_keywords):
                        post_data = {
                            '标题': text.strip(),
                            '内容': text.strip(),
                            '点赞数': 0,
                            '评论数': 0,
                            '平台': '微博热搜',
                            '抓取时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        }
                        posts.append(post_data)
                except:
                    continue
        
        except Exception as e:
            print(f"  财经热搜抓取失败: {e}")
        
        return posts

    
    def _scrape_weibo_stock_topic(self, page):
        """抓取微博股票超话"""
        posts = []
        
        try:
            # 访问股票超话
            stock_topic_url = "https://s.weibo.com/weibo?q=%23股票%23"
            page.goto(stock_topic_url, timeout=30000)
            
            self.random_wait(5.5, 8.0)
            
            # 检查验证码
            if self._check_captcha(page):
                self.beep_alert()
                print("  请手动完成验证码，完成后按回车继续...")
                input()
            
            # 滚动加载
            for i in range(3):
                self.slow_scroll(page, distance=800)
                self.random_wait(3.0, 5.0)
            
            # 提取微博内容
            cards = page.locator('.card-wrap').all()
            
            for card in cards[:30]:
                try:
                    post_data = {}
                    
                    # 提取内容
                    try:
                        content = card.locator('.txt').inner_text()
                        post_data['内容'] = content.strip()
                    except:
                        post_data['内容'] = ''
                    
                    # 提取标题（使用内容前50字）
                    post_data['标题'] = post_data['内容'][:50] + '...' if len(post_data['内容']) > 50 else post_data['内容']
                    
                    # 提取互动数据
                    try:
                        likes_text = card.locator('text=/赞/').inner_text()
                        likes = re.findall(r'\d+', likes_text)
                        post_data['点赞数'] = int(likes[0]) if likes else 0
                    except:
                        post_data['点赞数'] = 0
                    
                    try:
                        comments_text = card.locator('text=/评论/').inner_text()
                        comments = re.findall(r'\d+', comments_text)
                        post_data['评论数'] = int(comments[0]) if comments else 0
                    except:
                        post_data['评论数'] = 0
                    
                    post_data['平台'] = '微博超话'
                    post_data['抓取时间'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    if post_data['内容']:
                        posts.append(post_data)
                
                except:
                    continue
        
        except Exception as e:
            print(f"  股票超话抓取失败: {e}")
        
        return posts
    
    def _check_login_required(self, page, platform_name):
        """检查是否需要登录"""
        try:
            # 检查常见的登录标识
            login_indicators = ['登录', 'login', '扫码', '账号']
            
            page_text = page.content().lower()
            
            for indicator in login_indicators:
                if indicator in page_text:
                    return True
            
            return False
        except:
            return False
    
    def _check_captcha(self, page):
        """检查是否出现验证码"""
        try:
            # 检查常见的验证码标识
            captcha_indicators = ['验证', 'captcha', '滑块', '拼图']
            
            page_text = page.content().lower()
            
            for indicator in captcha_indicators:
                if indicator in page_text:
                    return True
            
            return False
        except:
            return False
    
    def save_today_data(self, data_list):
        """
        保存今日数据到历史文件
        
        参数:
            data_list: 数据列表
        """
        if not data_list:
            return
        
        today = datetime.now().strftime('%Y%m%d')
        filename = os.path.join(self.history_dir, f"discovery_{today}.json")
        
        # 合并所有文本
        all_text = []
        for item in data_list:
            text = f"{item.get('标题', '')} {item.get('内容', '')}"
            all_text.append(text)
        
        # 保存
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'date': today,
                'count': len(data_list),
                'texts': all_text
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ 今日数据已保存: {filename}")
    
    def load_yesterday_data(self):
        """
        加载昨日数据
        
        返回:
            list: 昨日文本列表
        """
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
        filename = os.path.join(self.history_dir, f"discovery_{yesterday}.json")
        
        if os.path.exists(filename):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"✓ 加载昨日数据: {data['count']} 条")
                    return data.get('texts', [])
            except:
                print("⚠️  昨日数据加载失败")
                return []
        else:
            print("⚠️  未找到昨日数据，将使用空对比")
            return []

    
    def analyze_with_ai(self, today_texts, yesterday_texts):
        """
        使用DeepSeek AI分析热点板块
        
        参数:
            today_texts: 今日文本列表
            yesterday_texts: 昨日文本列表
            
        返回:
            dict: AI分析结果
        """
        print("\n" + "=" * 60)
        print("开始AI智能发现分析")
        print("=" * 60)
        
        # 合并文本
        today_combined = "\n".join(today_texts[:200])  # 限制长度
        yesterday_combined = "\n".join(yesterday_texts[:200]) if yesterday_texts else "无昨日数据"
        
        print(f"今日文本: {len(today_texts)} 条")
        print(f"昨日文本: {len(yesterday_texts)} 条")
        
        # 构建用户输入
        user_input = f"""今日讨论内容（共{len(today_texts)}条）:
{today_combined}

---

昨日讨论内容（共{len(yesterday_texts)}条）:
{yesterday_combined}

请分析今日相比昨日，哪些板块的讨论度异常升高。"""
        
        # 调用DeepSeek API
        print("\n正在调用DeepSeek API进行智能分析...")
        
        result = self._call_deepseek_api(user_input)
        
        if result:
            print("✓ AI分析完成")
            return result
        else:
            print("× AI分析失败")
            return None
    
    def _call_deepseek_api(self, user_input):
        """
        调用DeepSeek API
        
        参数:
            user_input: 用户输入文本
            
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
                {"role": "user", "content": user_input}
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
    
    def generate_report(self, analysis_result, all_data):
        """
        生成Markdown简报
        
        参数:
            analysis_result: AI分析结果
            all_data: 所有抓取的数据
            
        返回:
            str: 报告文件路径
        """
        print("\n" + "=" * 60)
        print("生成全网雷达简报")
        print("=" * 60)
        
        today = datetime.now().strftime('%Y%m%d')
        filename = f"全网雷达报告_{today}.md"
        
        report_lines = []
        
        # 标题
        report_lines.append("# 【全网雷达：你可能错过的热门机会】")
        report_lines.append("")
        report_lines.append(f"**生成时间**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")
        
        # 数据来源
        report_lines.append("## 📡 数据来源")
        report_lines.append("")
        
        # 统计各平台数据量
        platform_stats = {}
        for item in all_data:
            platform = item.get('平台', '未知')
            platform_stats[platform] = platform_stats.get(platform, 0) + 1
        
        for platform, count in platform_stats.items():
            report_lines.append(f"- **{platform}**: {count} 条")
        
        report_lines.append(f"- **总计**: {len(all_data)} 条")
        report_lines.append("")
        
        # AI分析结果
        if analysis_result:
            # 整体市场情绪
            market_sentiment = analysis_result.get('market_sentiment', '')
            if market_sentiment:
                report_lines.append("## 🌡️ 整体市场情绪")
                report_lines.append("")
                report_lines.append(f"> {market_sentiment}")
                report_lines.append("")
            
            # 热门板块
            hot_sectors = analysis_result.get('hot_sectors', [])
            if hot_sectors:
                report_lines.append("## 🔥 讨论度异常升高的板块 TOP 3")
                report_lines.append("")
                
                for i, sector in enumerate(hot_sectors[:3], 1):
                    sector_name = sector.get('sector_name', '未知板块')
                    growth_rate = sector.get('growth_rate', 0)
                    today_mentions = sector.get('today_mentions', 0)
                    yesterday_mentions = sector.get('yesterday_mentions', 0)
                    reason = sector.get('reason', '原因未知')
                    confidence = sector.get('confidence', 0)
                    
                    report_lines.append(f"### {i}. {sector_name} 🚀")
                    report_lines.append("")
                    report_lines.append(f"**增长率**: {growth_rate:.0f}%")
                    report_lines.append("")
                    report_lines.append(f"**讨论热度**:")
                    report_lines.append(f"- 今日提及: {today_mentions} 次")
                    report_lines.append(f"- 昨日提及: {yesterday_mentions} 次")
                    report_lines.append("")
                    report_lines.append(f"**火爆原因**: {reason}")
                    report_lines.append("")
                    report_lines.append(f"**置信度**: {confidence:.0%}")
                    report_lines.append("")
                    
                    # 热度条形图
                    bar_length = min(int(growth_rate / 10), 20)
                    bar = "🟩" * bar_length
                    report_lines.append(f"```")
                    report_lines.append(f"热度增长: {bar}")
                    report_lines.append(f"```")
                    report_lines.append("")
            
            # 关键事件
            key_events = analysis_result.get('key_events', [])
            if key_events:
                report_lines.append("## 📰 今日关键事件")
                report_lines.append("")
                for i, event in enumerate(key_events, 1):
                    report_lines.append(f"{i}. {event}")
                report_lines.append("")
        
        # 热门内容样本
        report_lines.append("## 💬 热门内容样本")
        report_lines.append("")
        
        # 按点赞数排序
        sorted_data = sorted(all_data, key=lambda x: x.get('点赞数', 0), reverse=True)
        
        for i, item in enumerate(sorted_data[:10], 1):
            platform = item.get('平台', '未知')
            title = item.get('标题', '')
            content = item.get('内容', '')
            likes = item.get('点赞数', 0)
            comments = item.get('评论数', 0)
            
            report_lines.append(f"### {i}. [{platform}]")
            report_lines.append("")
            
            if title:
                report_lines.append(f"**{title}**")
                report_lines.append("")
            
            if content:
                preview = content[:150] + '...' if len(content) > 150 else content
                report_lines.append(f"> {preview}")
                report_lines.append("")
            
            report_lines.append(f"👍 {likes} | 💬 {comments}")
            report_lines.append("")
        
        # 免责声明
        report_lines.append("---")
        report_lines.append("")
        report_lines.append("## ⚠️  使用说明")
        report_lines.append("")
        report_lines.append("1. 本报告基于社交媒体公开数据和AI分析生成")
        report_lines.append("2. 讨论热度不等于投资价值，请理性判断")
        report_lines.append("3. 建议结合基本面、技术面等多维度分析")
        report_lines.append("4. 不构成任何投资建议，投资有风险")
        report_lines.append("")
        
        # 写入文件
        report_content = "\n".join(report_lines)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"✓ 简报已保存: {filename}")
        
        return filename

    
    def run(self, xhs_count=50, headless=False):
        """
        运行完整的发现流程
        
        参数:
            xhs_count: 小红书目标抓取数量
            headless: 是否无头模式
        """
        print("=" * 60)
        print("全网热点发现引擎 - Discovery Engine")
        print("=" * 60)
        print()
        
        all_data = []
        
        # 1. 抓取小红书
        print("\n【第1步】抓取小红书财经频道...")
        try:
            xhs_data = self.scrape_xiaohongshu(target_count=xhs_count, headless=headless)
            all_data.extend(xhs_data)
            print(f"✓ 小红书: {len(xhs_data)} 条")
        except Exception as e:
            print(f"× 小红书抓取失败: {e}")
            print("  继续执行...")
        
        # 2. 抓取微博
        print("\n【第2步】抓取微博财经热搜和股票超话...")
        try:
            weibo_data = self.scrape_weibo(headless=headless)
            all_data.extend(weibo_data)
            print(f"✓ 微博: {len(weibo_data)} 条")
        except Exception as e:
            print(f"× 微博抓取失败: {e}")
            print("  继续执行...")
        
        # 检查是否有数据
        if not all_data:
            print("\n× 未抓取到任何数据，程序结束")
            return
        
        print(f"\n✓ 数据抓取完成，共 {len(all_data)} 条")
        
        # 保存原始数据
        today = datetime.now().strftime('%Y%m%d_%H%M%S')
        raw_filename = f"discovery_raw_{today}.csv"
        
        df = pd.DataFrame(all_data)
        df.to_csv(raw_filename, index=False, encoding='utf-8-sig')
        print(f"✓ 原始数据已保存: {raw_filename}")
        
        # 3. 保存今日数据到历史
        print("\n【第3步】保存今日数据...")
        self.save_today_data(all_data)
        
        # 4. 加载昨日数据
        print("\n【第4步】加载昨日数据...")
        yesterday_texts = self.load_yesterday_data()
        
        # 5. AI分析
        print("\n【第5步】AI智能发现分析...")
        today_texts = [f"{item.get('标题', '')} {item.get('内容', '')}" for item in all_data]
        
        analysis_result = self.analyze_with_ai(today_texts, yesterday_texts)
        
        # 6. 生成报告
        print("\n【第6步】生成全网雷达简报...")
        report_file = self.generate_report(analysis_result, all_data)
        
        # 完成
        print("\n" + "=" * 60)
        print("✅ 全网热点发现完成！")
        print("=" * 60)
        print(f"\n生成文件:")
        print(f"  - 原始数据: {raw_filename}")
        print(f"  - 雷达简报: {report_file}")
        print()


def main():
    """主函数"""
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║          全网热点发现引擎 - Discovery Engine             ║
║                                                          ║
║  功能: 自动识别小红书和微博上讨论度异常升高的板块       ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    # 创建发现引擎实例
    engine = DiscoveryEngine()
    
    # 运行发现流程
    # xhs_count=50: 小红书抓取50条笔记
    # headless=False: 显示浏览器窗口，方便扫码登录
    engine.run(xhs_count=50, headless=False)


if __name__ == "__main__":
    main()
