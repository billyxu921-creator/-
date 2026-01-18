#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股吧情报分析模块
从股吧讨论中筛选具有实战价值的投资情报
"""

import pandas as pd
import numpy as np
import re
import warnings
from datetime import datetime

warnings.filterwarnings('ignore')


class IntelligenceAnalyzer:
    """股吧情报分析器"""
    
    def __init__(self):
        """初始化分析器"""
        
        # 股票代码和简称映射（常见股票）
        self.stock_mapping = {
            # 黄金股
            '山东黄金': '600547', '中金黄金': '600489', '紫金矿业': '601899',
            '赤峰黄金': '600988', '湖南黄金': '002155', '恒邦股份': '002237',
            '银泰黄金': '000975', '西部黄金': '601069', '荣华实业': '600311',
            '豫光金铅': '600531', '东方金钰': '600086',
            
            # 其他常见股票
            '贵州茅台': '600519', '五粮液': '000858', '宁德时代': '300750',
            '比亚迪': '002594', '隆基绿能': '601012', '中国平安': '601318',
            '招商银行': '600036', '工商银行': '601398', '建设银行': '601939',
            '中国石油': '601857', '中国石化': '600028', '中国神华': '601088',
            '长江电力': '600900', '中国联通': '600050', '中国移动': '600941',
            '格力电器': '000651', '美的集团': '000333', '海天味业': '603288',
            '伊利股份': '600887', '万科A': '000002', '保利发展': '600048'
        }
        
        # 技术派关键词
        self.technical_keywords = {
            '均线': ['均线', '5日线', '10日线', '20日线', '30日线', '60日线', '120日线', '250日线',
                   '金叉', '死叉', '多头排列', '空头排列', '均线粘合', '均线发散'],
            '成交量': ['放量', '缩量', '天量', '地量', '量价齐升', '量价背离', '成交量突破',
                     '换手率', '成交额', '巨量', '温和放量', '堆量'],
            'MACD': ['MACD', 'macd', '红柱', '绿柱', 'DIF', 'DEA', 'MACD金叉', 'MACD背离',
                    '零轴', '水上金叉', '水下金叉'],
            'KDJ': ['KDJ', 'kdj', 'K线', 'D线', 'J线', 'KDJ金叉', 'KDJ钝化', '超买', '超卖'],
            '形态': ['突破', '回踩', '支撑', '压力', '箱体', '三角形', '头肩顶', '头肩底',
                   '双底', '双顶', 'W底', 'M顶', '圆弧底', '平台突破', '缺口'],
            '趋势': ['上涨趋势', '下跌趋势', '震荡', '盘整', '拉升', '回调', '反弹', '反转',
                   '新高', '新低', '强势', '弱势']
        }
        
        # 筹码派关键词
        self.chip_keywords = {
            '大单': ['大单', '主力', '机构', '游资', '北向资金', '外资', '大资金',
                   '主力资金', '净流入', '净流出', '大单买入', '大单卖出'],
            '庄家': ['庄家', '坐庄', '洗盘', '吸筹', '出货', '拉升', '砸盘', '护盘',
                   '控盘', '建仓', '减仓', '对敲', '对倒'],
            '国家队': ['国家队', '社保', '汇金', '证金', '养老金', '国资委', '央企',
                     '国企', '社保基金', '中央汇金', '证金公司'],
            '筹码': ['筹码', '筹码集中', '筹码分散', '筹码峰', '获利盘', '套牢盘',
                   '浮筹', '锁仓', '解套', '割肉'],
            '资金': ['资金流向', '资金面', '融资', '融券', '两融', '杠杆', '配资',
                   '抄底', '逃顶', '加仓', '减仓']
        }
        
        # 基本面关键词
        self.fundamental_keywords = {
            '业绩': ['业绩', '财报', '营收', '利润', '净利润', '增长', '同比', '环比',
                   '业绩预告', '业绩快报', '年报', '季报', '中报', 'EPS', 'PE', 'PB'],
            '政策': ['政策', '利好', '利空', '扶持', '补贴', '税收', '监管', '改革',
                   '规划', '产业政策', '国家政策', '地方政策'],
            '行业': ['行业', '板块', '赛道', '风口', '景气度', '周期', '产业链',
                   '上游', '下游', '龙头', '细分领域'],
            '公告': ['公告', '重组', '并购', '收购', '增持', '回购', '分红', '送转',
                   '定增', '配股', '停牌', '复牌', '中标', '合同'],
            '事件': ['突发', '黑天鹅', '利好消息', '利空消息', '重大事项', '重大合同',
                   '订单', '产能', '扩产', '投产', '研发', '新品']
        }
        
        # 散户噪音关键词（需要剔除）
        self.noise_keywords = [
            '必涨', '必跌', '翻倍', '十倍股', '妖股', '垃圾', '骗子', '割韭菜',
            '完了', '凉了', '要起飞', '上天', '入地', '梭哈', '满仓',
            '哈哈', '呵呵', '666', '牛逼', '垃圾股', '破股',
            '看涨', '看跌', '涨涨涨', '跌跌跌', '冲冲冲'
        ]
        
    def analyze_intelligence(self, posts_df):
        """
        分析股吧帖子，提取有价值的投资情报
        
        参数:
            posts_df: 包含帖子信息的DataFrame
            
        返回:
            DataFrame: 包含分析结果的情报列表
        """
        if posts_df.empty:
            print("输入数据为空")
            return pd.DataFrame()
        
        print(f"开始分析 {len(posts_df)} 条帖子...")
        
        intelligence_list = []
        
        for idx, row in posts_df.iterrows():
            title = str(row.get('标题', ''))
            content = str(row.get('内容', ''))
            full_text = title + ' ' + content
            
            # 1. 剔除散户噪音
            if self._is_noise(full_text):
                continue
            
            # 2. 识别股票标的
            stocks = self._identify_stocks(full_text)
            if not stocks:
                continue
            
            # 3. 分类逻辑
            categories = self._classify_post(full_text)
            if not categories:
                continue
            
            # 4. 提取关键论据
            evidence = self._extract_evidence(full_text, categories)
            
            # 5. 价值评估
            score = self._evaluate_value(full_text, categories, evidence)
            
            # 构建情报记录
            intelligence = {
                '标题': title,
                '识别股票': ', '.join(stocks),
                '主要分类': categories[0] if categories else '未分类',
                '次要分类': categories[1] if len(categories) > 1 else '',
                '关键论据': evidence,
                '价值评分': score,
                '原文链接': row.get('帖子链接', ''),
                '发布时间': row.get('发布时间', ''),
                '原始内容': content[:200] + '...' if len(content) > 200 else content
            }
            
            intelligence_list.append(intelligence)
        
        if intelligence_list:
            result_df = pd.DataFrame(intelligence_list)
            # 按价值评分排序
            result_df = result_df.sort_values('价值评分', ascending=False)
            print(f"✓ 筛选出 {len(result_df)} 条有价值的情报")
            return result_df.reset_index(drop=True)
        else:
            print("× 未找到有价值的情报")
            return pd.DataFrame()
    
    def _is_noise(self, text):
        """判断是否为散户噪音"""
        text_lower = text.lower()
        
        # 检查噪音关键词
        noise_count = sum(1 for keyword in self.noise_keywords if keyword in text_lower)
        
        # 如果包含3个以上噪音关键词，判定为噪音
        if noise_count >= 3:
            return True
        
        # 检查是否只有情绪没有证据（长度太短且包含噪音词）
        if len(text) < 30 and noise_count > 0:
            return True
        
        return False
    
    def _identify_stocks(self, text):
        """识别帖子中讨论的股票"""
        identified_stocks = []
        
        # 方法1: 通过股票代码识别（6位数字）
        code_pattern = r'\b[036]\d{5}\b'
        codes = re.findall(code_pattern, text)
        identified_stocks.extend(codes)
        
        # 方法2: 通过股票简称识别
        for name, code in self.stock_mapping.items():
            if name in text:
                stock_info = f"{name}({code})"
                if stock_info not in identified_stocks:
                    identified_stocks.append(stock_info)
        
        return list(set(identified_stocks))
    
    def _classify_post(self, text):
        """分类帖子类型"""
        categories = []
        scores = {}
        
        # 技术派评分
        tech_score = 0
        for category, keywords in self.technical_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    tech_score += 1
        if tech_score > 0:
            scores['技术派'] = tech_score
        
        # 筹码派评分
        chip_score = 0
        for category, keywords in self.chip_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    chip_score += 1
        if chip_score > 0:
            scores['筹码派'] = chip_score
        
        # 基本面评分
        fundamental_score = 0
        for category, keywords in self.fundamental_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    fundamental_score += 1
        if fundamental_score > 0:
            scores['基本面'] = fundamental_score
        
        # 按得分排序
        if scores:
            sorted_categories = sorted(scores.items(), key=lambda x: x[1], reverse=True)
            categories = [cat for cat, score in sorted_categories]
        
        return categories
    
    def _extract_evidence(self, text, categories):
        """提取关键论据"""
        evidence_list = []
        
        if not categories:
            return ''
        
        main_category = categories[0]
        
        # 根据主要分类提取相关论据
        if main_category == '技术派':
            for category, keywords in self.technical_keywords.items():
                for keyword in keywords:
                    if keyword in text:
                        # 提取包含关键词的句子片段
                        sentences = re.split(r'[。！？；\n]', text)
                        for sentence in sentences:
                            if keyword in sentence and len(sentence) > 10:
                                evidence_list.append(sentence.strip())
                                break
                if evidence_list:
                    break
        
        elif main_category == '筹码派':
            for category, keywords in self.chip_keywords.items():
                for keyword in keywords:
                    if keyword in text:
                        sentences = re.split(r'[。！？；\n]', text)
                        for sentence in sentences:
                            if keyword in sentence and len(sentence) > 10:
                                evidence_list.append(sentence.strip())
                                break
                if evidence_list:
                    break
        
        elif main_category == '基本面':
            for category, keywords in self.fundamental_keywords.items():
                for keyword in keywords:
                    if keyword in text:
                        sentences = re.split(r'[。！？；\n]', text)
                        for sentence in sentences:
                            if keyword in sentence and len(sentence) > 10:
                                evidence_list.append(sentence.strip())
                                break
                if evidence_list:
                    break
        
        # 返回前3条最相关的论据
        return ' | '.join(evidence_list[:3]) if evidence_list else '无明确论据'
    
    def _evaluate_value(self, text, categories, evidence):
        """评估情报价值（1-10分）"""
        score = 0
        
        # 基础分：有分类就给3分
        if categories:
            score += 3
        
        # 论据分：有具体论据加2分
        if evidence and evidence != '无明确论据':
            score += 2
            # 论据越详细，分数越高
            if len(evidence) > 50:
                score += 1
            if len(evidence) > 100:
                score += 1
        
        # 数据分：包含具体数字加分
        number_pattern = r'\d+\.?\d*%?'
        numbers = re.findall(number_pattern, text)
        if len(numbers) >= 3:
            score += 2
        elif len(numbers) >= 1:
            score += 1
        
        # 专业度分：包含专业术语加分
        professional_terms = ['突破', '支撑', '压力', '主力', '机构', '业绩', '公告', 
                             '政策', '行业', '龙头', '资金流入', '净流入']
        professional_count = sum(1 for term in professional_terms if term in text)
        if professional_count >= 3:
            score += 1
        
        # 确保分数在1-10之间
        score = max(1, min(10, score))
        
        return score
    
    def generate_intelligence_report(self, intelligence_df):
        """生成情报分析报告"""
        if intelligence_df.empty:
            return "未发现有价值的情报"
        
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("股吧情报分析报告")
        report_lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("=" * 80)
        report_lines.append("")
        
        # 统计信息
        report_lines.append("【统计概览】")
        report_lines.append(f"有效情报总数: {len(intelligence_df)}")
        report_lines.append(f"平均价值评分: {intelligence_df['价值评分'].mean():.1f}")
        report_lines.append(f"高价值情报(≥8分): {len(intelligence_df[intelligence_df['价值评分'] >= 8])}")
        report_lines.append("")
        
        # 分类统计
        category_counts = intelligence_df['主要分类'].value_counts()
        report_lines.append("【分类分布】")
        for category, count in category_counts.items():
            report_lines.append(f"  {category}: {count} 条")
        report_lines.append("")
        
        # 热门股票
        all_stocks = []
        for stocks_str in intelligence_df['识别股票']:
            all_stocks.extend(stocks_str.split(', '))
        if all_stocks:
            from collections import Counter
            stock_counter = Counter(all_stocks)
            report_lines.append("【热门标的 TOP 5】")
            for stock, count in stock_counter.most_common(5):
                report_lines.append(f"  {stock}: 被提及 {count} 次")
            report_lines.append("")
        
        # 高价值情报详情
        high_value = intelligence_df[intelligence_df['价值评分'] >= 7].head(10)
        if not high_value.empty:
            report_lines.append("【高价值情报 TOP 10】")
            report_lines.append("-" * 80)
            
            for idx, row in high_value.iterrows():
                report_lines.append(f"\n{idx + 1}. {row['标题']}")
                report_lines.append(f"   标的: {row['识别股票']}")
                report_lines.append(f"   分类: {row['主要分类']}" + 
                                  (f" + {row['次要分类']}" if row['次要分类'] else ""))
                report_lines.append(f"   评分: {row['价值评分']}/10")
                report_lines.append(f"   论据: {row['关键论据']}")
                if row['原文链接']:
                    report_lines.append(f"   链接: {row['原文链接']}")
        
        report_lines.append("\n" + "=" * 80)
        report_lines.append("注: 评分越高代表论据越充分，仅供参考")
        report_lines.append("=" * 80)
        
        return "\n".join(report_lines)


def test_intelligence_analyzer():
    """测试情报分析器"""
    print("测试股吧情报分析器...")
    
    # 创建测试数据
    test_data = {
        '标题': [
            '山东黄金突破60日均线，MACD金叉，主力资金大幅流入',
            '紫金矿业业绩预告超预期，社保基金增持明显',
            '中金黄金放量突破，成交量是前日3倍',
            '黄金股要起飞了！必涨！冲冲冲！',
            '600547今日大单净流入2.3亿，北向资金持续买入',
            '赤峰黄金发布重大合同公告，订单金额超10亿',
            '看好黄金板块，哈哈哈，涨涨涨',
            '湖南黄金KDJ金叉，量价齐升，突破前期平台',
            '国家队进场扫货，汇金增持多只黄金股',
            '黄金行业景气度提升，政策利好频出'
        ],
        '内容': [
            '技术面看，山东黄金今日突破60日均线，MACD指标金叉向上，同时主力资金净流入1.5亿元，显示资金面配合良好。',
            '紫金矿业发布业绩预告，预计净利润同比增长45%，超出市场预期。同时社保基金在二季度增持了500万股。',
            '中金黄金今日放量上涨，成交量达到前日的3倍，突破前期箱体，技术形态良好。',
            '黄金股必涨，大家赶紧上车，要起飞了！',
            '600547山东黄金今日大单净流入2.3亿元，北向资金连续5日净买入，资金面非常强势。',
            '赤峰黄金公告中标重大合同，订单金额超过10亿元，将对未来业绩产生积极影响。',
            '看好黄金板块，涨涨涨，冲冲冲！',
            '湖南黄金KDJ指标金叉，量价齐升，突破前期平台压力位，有望开启新一轮上涨。',
            '国家队资金进场明显，汇金公司增持了山东黄金、中金黄金等多只黄金股，显示官方对板块的看好。',
            '黄金行业整体景气度提升，国家出台多项扶持政策，行业龙头有望受益。'
        ],
        '阅读量': [5000, 3000, 2000, 1000, 4000, 3500, 800, 2500, 6000, 2800],
        '评论数': [50, 30, 20, 5, 40, 35, 3, 25, 60, 28],
        '帖子链接': [''] * 10,
        '股票代码': [''] * 10,
        '发布时间': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')] * 10
    }
    
    test_df = pd.DataFrame(test_data)
    
    # 创建分析器
    analyzer = IntelligenceAnalyzer()
    
    # 分析情报
    intelligence_df = analyzer.analyze_intelligence(test_df)
    
    if not intelligence_df.empty:
        # 生成报告
        report = analyzer.generate_intelligence_report(intelligence_df)
        print("\n" + report)
        
        # 保存结果
        filename = f"intelligence_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        intelligence_df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n详细情报已保存到: {filename}")
        
        return intelligence_df
    else:
        print("未发现有价值的情报")
        return pd.DataFrame()


if __name__ == "__main__":
    test_intelligence_analyzer()