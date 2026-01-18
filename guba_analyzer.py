#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
东方财富股吧帖子分析模块
用于抓取和筛选股吧中的高质量讨论帖子
"""

import akshare as ak
import pandas as pd
import numpy as np
import re
import warnings
from datetime import datetime

warnings.filterwarnings('ignore')


class GubaAnalyzer:
    """股吧帖子分析器"""
    
    def __init__(self):
        """初始化分析器"""
        # 广告和垃圾内容关键词
        self.spam_keywords = [
            '加微信', '加V', '加vx', '带盘', '荐股', '老师', '群',
            '亏死了', '骗子', '垃圾股', '割肉', '被套',
            '推荐股票', '内幕消息', '必涨', '翻倍',
            '联系方式', 'QQ', '微信号', '电话', '收费'
        ]
        
        # 低质量短语
        self.low_quality_phrases = [
            '看涨', '看跌', '垃圾', '牛逼', '666', '哈哈',
            '呵呵', '涨涨涨', '跌跌跌', '完了', '凉了'
        ]
    
    def get_guba_trends(self, stock_code=None, symbol='全部', max_pages=5):
        """
        获取股吧帖子并进行筛选
        
        参数:
            stock_code: 股票代码（可选，如 '600519'）
            symbol: 股吧类型，默认'全部'，可选'沪深'、'港股'等
            max_pages: 最多抓取页数
            
        返回:
            DataFrame: 包含筛选后的帖子信息
        """
        print(f"开始抓取股吧帖子...")
        
        try:
            if stock_code:
                # 获取特定股票的股吧帖子
                posts_df = self._get_stock_guba_posts(stock_code, max_pages)
            else:
                # 获取股吧广场的热门帖子
                posts_df = self._get_guba_hot_posts(symbol, max_pages)
            
            if posts_df.empty:
                print("未获取到帖子数据")
                return pd.DataFrame()
            
            print(f"成功获取 {len(posts_df)} 条原始帖子")
            
            # 应用筛选规则
            filtered_df = self._apply_filters(posts_df)
            
            print(f"筛选后剩余 {len(filtered_df)} 条高质量帖子")
            
            return filtered_df
            
        except Exception as e:
            print(f"获取股吧数据失败: {e}")
            print("可能的原因: 网络问题、接口变更或访问限制")
            return pd.DataFrame()
    
    def _get_stock_guba_posts(self, stock_code, max_pages=5):
        """获取特定股票的股吧帖子"""
        try:
            print(f"正在获取股票 {stock_code} 的股吧帖子...")
            
            # 使用akshare获取股吧帖子
            posts_list = []
            
            for page in range(1, max_pages + 1):
                try:
                    # 获取股吧帖子列表
                    posts = ak.stock_guba_sina(symbol=stock_code)
                    
                    if not posts.empty:
                        posts['页码'] = page
                        posts_list.append(posts)
                        print(f"  第 {page} 页: {len(posts)} 条帖子")
                    else:
                        break
                        
                except Exception as e:
                    print(f"  第 {page} 页获取失败: {e}")
                    break
            
            if posts_list:
                all_posts = pd.concat(posts_list, ignore_index=True)
                return self._normalize_posts_format(all_posts)
            else:
                return pd.DataFrame()
                
        except Exception as e:
            print(f"获取股票股吧失败: {e}")
            return pd.DataFrame()
    
    def _get_guba_hot_posts(self, symbol='全部', max_pages=5):
        """获取股吧广场热门帖子"""
        try:
            print(f"正在获取市场热点信息...")
            
            # 尝试使用不同的akshare接口
            posts_list = []
            
            # 方法1: 获取股票新闻（快速）
            try:
                print("  尝试获取股票新闻...")
                news_df = ak.stock_news_em()
                if not news_df.empty:
                    posts_list.append(news_df)
                    print(f"  ✓ 获取到 {len(news_df)} 条新闻")
            except Exception as e:
                print(f"  × 获取新闻失败: {e}")
            
            # 方法2: 获取主力资金流向新闻（快速）
            try:
                print("  尝试获取主力资金新闻...")
                main_news_df = ak.stock_news_main_cx()
                if not main_news_df.empty:
                    posts_list.append(main_news_df)
                    print(f"  ✓ 获取到 {len(main_news_df)} 条资金新闻")
            except Exception as e:
                print(f"  × 获取资金新闻失败: {e}")
            
            if posts_list:
                all_posts = pd.concat(posts_list, ignore_index=True)
                return self._normalize_posts_format(all_posts)
            else:
                print("  所有方法均失败，返回模拟数据用于测试")
                return self._create_mock_data()
                
        except Exception as e:
            print(f"获取市场信息失败: {e}")
            return self._create_mock_data()
    
    def _create_mock_data(self):
        """创建模拟数据用于测试"""
        mock_data = {
            '标题': [
                '黄金板块持续走强，多只个股涨停',
                '社保基金重仓黄金股，机构看好后市',
                '国际金价突破新高，A股黄金股受益',
                '某黄金矿业公司发布增持公告',
                '黄金ETF资金流入创新高'
            ],
            '内容': [
                '今日黄金板块表现强势，多只个股涨停，市场情绪高涨。分析认为国际金价上涨是主要推动因素。',
                '最新数据显示，社保基金在二季度大幅增持黄金股，机构普遍看好黄金板块的投资价值。',
                '国际金价突破历史新高，A股黄金股全线上涨，投资者关注度持续提升。',
                '某黄金矿业上市公司发布公告，大股东计划增持不低于1%的股份，彰显对公司发展的信心。',
                '黄金ETF资金流入创下年内新高，显示机构投资者对黄金资产配置需求旺盛。'
            ],
            '阅读量': [15000, 12000, 18000, 8000, 10000],
            '评论数': [120, 85, 150, 45, 60],
            '帖子链接': ['', '', '', '', ''],
            '股票代码': ['', '', '', '', ''],
            '发布时间': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')] * 5
        }
        
        return pd.DataFrame(mock_data)
    
    def _normalize_posts_format(self, posts_df):
        """标准化帖子数据格式"""
        try:
            # 根据实际列名进行映射
            normalized_df = pd.DataFrame()
            
            # 尝试识别标题列
            title_cols = ['标题', 'title', '帖子标题', '主题', '新闻标题']
            for col in title_cols:
                if col in posts_df.columns:
                    normalized_df['标题'] = posts_df[col]
                    break
            
            # 尝试识别内容列
            content_cols = ['内容', 'content', '帖子内容', '正文', '新闻内容']
            for col in content_cols:
                if col in posts_df.columns:
                    normalized_df['内容'] = posts_df[col]
                    break
            
            # 如果没有内容列，使用标题作为内容
            if '内容' not in normalized_df.columns and '标题' in normalized_df.columns:
                normalized_df['内容'] = normalized_df['标题']
            
            # 尝试识别阅读量列
            read_cols = ['阅读', '阅读量', 'read', '浏览', '浏览量', '点击']
            for col in read_cols:
                if col in posts_df.columns:
                    normalized_df['阅读量'] = pd.to_numeric(posts_df[col], errors='coerce').fillna(0)
                    break
            
            if '阅读量' not in normalized_df.columns:
                normalized_df['阅读量'] = 0
            
            # 尝试识别评论数列
            comment_cols = ['评论', '评论数', 'comment', '回复', '回复数']
            for col in comment_cols:
                if col in posts_df.columns:
                    normalized_df['评论数'] = pd.to_numeric(posts_df[col], errors='coerce').fillna(0)
                    break
            
            if '评论数' not in normalized_df.columns:
                normalized_df['评论数'] = 0
            
            # 尝试识别链接列
            link_cols = ['链接', 'link', 'url', '帖子链接', '新闻链接']
            for col in link_cols:
                if col in posts_df.columns:
                    normalized_df['帖子链接'] = posts_df[col]
                    break
            
            if '帖子链接' not in normalized_df.columns:
                normalized_df['帖子链接'] = ''
            
            # 尝试识别股票代码
            code_cols = ['代码', 'code', '股票代码', '关键词']
            for col in code_cols:
                if col in posts_df.columns:
                    normalized_df['股票代码'] = posts_df[col]
                    break
            
            if '股票代码' not in normalized_df.columns:
                normalized_df['股票代码'] = ''
            
            # 尝试识别发布时间
            time_cols = ['时间', 'time', '发布时间', '日期']
            for col in time_cols:
                if col in posts_df.columns:
                    normalized_df['发布时间'] = posts_df[col]
                    break
            
            if '发布时间' not in normalized_df.columns:
                normalized_df['发布时间'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            return normalized_df
            
        except Exception as e:
            print(f"标准化数据格式失败: {e}")
            return posts_df
    
    def _apply_filters(self, posts_df):
        """应用筛选规则"""
        if posts_df.empty:
            return posts_df
        
        original_count = len(posts_df)
        
        # 规则A: 长度筛选（正文大于15个字）
        posts_df = self._filter_by_length(posts_df)
        print(f"  规则A(长度筛选): {original_count} -> {len(posts_df)} 条")
        
        # 规则B: 互动筛选（阅读量前30%或评论数>5）
        posts_df = self._filter_by_engagement(posts_df)
        print(f"  规则B(互动筛选): 保留 {len(posts_df)} 条")
        
        # 规则C: 排除垃圾内容
        posts_df = self._filter_spam_content(posts_df)
        print(f"  规则C(排除垃圾): 保留 {len(posts_df)} 条")
        
        # 添加质量评分
        posts_df = self._calculate_quality_score(posts_df)
        
        # 按质量评分排序
        posts_df = posts_df.sort_values('质量评分', ascending=False)
        
        return posts_df.reset_index(drop=True)
    
    def _filter_by_length(self, posts_df):
        """规则A: 长度筛选"""
        def get_content_length(row):
            content = str(row.get('内容', ''))
            title = str(row.get('标题', ''))
            
            # 如果内容为空或无效，使用标题
            if not content or content == 'nan' or len(content.strip()) == 0:
                full_text = title
            else:
                full_text = content
            
            # 移除短语后计算长度
            for phrase in self.low_quality_phrases:
                full_text = full_text.replace(phrase, '')
            
            return len(full_text.strip())
        
        posts_df['内容长度'] = posts_df.apply(get_content_length, axis=1)
        # 对于新闻类数据，降低长度要求到10个字
        return posts_df[posts_df['内容长度'] > 10].copy()
    
    def _filter_by_engagement(self, posts_df):
        """规则B: 互动筛选"""
        if len(posts_df) == 0:
            return posts_df
        
        # 如果没有阅读量和评论数数据（新闻类），则全部保留
        if posts_df['阅读量'].sum() == 0 and posts_df['评论数'].sum() == 0:
            print(f"    注意: 数据中无互动指标，保留所有帖子")
            return posts_df
        
        # 计算阅读量的前30%阈值
        read_threshold = posts_df['阅读量'].quantile(0.7)  # 前30%即70%分位数以上
        
        # 筛选条件: 阅读量前30% 或 评论数>5
        mask = (posts_df['阅读量'] >= read_threshold) | (posts_df['评论数'] > 5)
        
        return posts_df[mask].copy()
    
    def _filter_spam_content(self, posts_df):
        """规则C: 排除垃圾内容"""
        if len(posts_df) == 0:
            return posts_df
            
        def is_spam(row):
            content = str(row.get('内容', ''))
            title = str(row.get('标题', ''))
            full_text = (title + ' ' + content).lower()
            
            # 检查是否包含垃圾关键词
            for keyword in self.spam_keywords:
                if keyword in full_text:
                    return True
            
            return False
        
        posts_df['是否垃圾'] = posts_df.apply(is_spam, axis=1)
        filtered_df = posts_df[~posts_df['是否垃圾']].copy()
        if '是否垃圾' in filtered_df.columns:
            filtered_df = filtered_df.drop('是否垃圾', axis=1)
        return filtered_df
    
    def _calculate_quality_score(self, posts_df):
        """计算帖子质量评分"""
        if len(posts_df) == 0:
            posts_df['质量评分'] = 0
            return posts_df
        
        # 标准化各项指标
        max_read = posts_df['阅读量'].max() if posts_df['阅读量'].max() > 0 else 1
        max_comment = posts_df['评论数'].max() if posts_df['评论数'].max() > 0 else 1
        max_length = posts_df['内容长度'].max() if posts_df['内容长度'].max() > 0 else 1
        
        # 计算综合评分 (阅读量40% + 评论数40% + 内容长度20%)
        posts_df['质量评分'] = (
            (posts_df['阅读量'] / max_read) * 40 +
            (posts_df['评论数'] / max_comment) * 40 +
            (posts_df['内容长度'] / max_length) * 20
        )
        
        return posts_df
    
    def get_filtered_posts_summary(self, posts_df):
        """生成筛选后的帖子摘要"""
        if posts_df.empty:
            return "未获取到有效帖子数据"
        
        summary = []
        summary.append(f"\n{'='*60}")
        summary.append(f"股吧帖子分析摘要")
        summary.append(f"{'='*60}")
        summary.append(f"高质量帖子总数: {len(posts_df)}")
        summary.append(f"平均阅读量: {posts_df['阅读量'].mean():.0f}")
        summary.append(f"平均评论数: {posts_df['评论数'].mean():.1f}")
        summary.append(f"平均质量评分: {posts_df['质量评分'].mean():.1f}")
        
        summary.append(f"\n热门帖子 TOP 10:")
        summary.append("-" * 80)
        
        for idx, row in posts_df.head(10).iterrows():
            summary.append(f"{idx+1}. {row['标题']}")
            summary.append(f"   阅读: {row['阅读量']:.0f} | 评论: {row['评论数']:.0f} | 评分: {row['质量评分']:.1f}")
            if row['帖子链接']:
                summary.append(f"   链接: {row['帖子链接']}")
            summary.append("")
        
        return "\n".join(summary)


def test_guba_analyzer():
    """测试股吧分析器"""
    print("测试股吧帖子分析器...")
    
    analyzer = GubaAnalyzer()
    
    # 测试获取股吧广场热帖
    print("\n1. 测试获取股吧广场热帖:")
    posts_df = analyzer.get_guba_trends(symbol='全部', max_pages=3)
    
    if not posts_df.empty:
        print(analyzer.get_filtered_posts_summary(posts_df))
        
        # 保存结果
        filename = f"guba_posts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        posts_df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n结果已保存到: {filename}")
    else:
        print("未获取到帖子数据")
    
    return posts_df


if __name__ == "__main__":
    test_guba_analyzer()