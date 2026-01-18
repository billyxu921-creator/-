#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DeepSeek AI 文本分析模块
使用DeepSeek API对股吧帖子进行深度分析
"""

import pandas as pd
import json
import requests
import time
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')


class DeepSeekAnalyzer:
    """DeepSeek AI分析器"""
    
    def __init__(self, api_key=None, api_base="https://api.deepseek.com/v1"):
        """
        初始化DeepSeek分析器
        
        参数:
            api_key: DeepSeek API密钥
            api_base: API基础URL
        """
        self.api_key = api_key or "YOUR_DEEPSEEK_API_KEY"  # 需要替换为实际的API Key
        self.api_base = api_base
        self.model = "deepseek-chat"  # 使用DeepSeek Chat模型
        
        # 系统提示词
        self.system_prompt = """你现在是一个资深金融博弈专家。请分析以下文本内容，并按要求输出。

分析逻辑：
1. 提取标的：识别提及的具体股票代码或简称
2. 情绪量化：给出 -1.0 (极度恐慌) 到 1.0 (极度乐观) 的分值
3. 逻辑提取：用一句话总结帖子的核心论点（如：预期重组、技术位超卖、大单压盘）
4. 置信度评分：0.0 到 1.0。包含数据支撑的给高分，纯谩骂给 0

输出格式：
请仅输出 JSON 格式，字段包含：
- stock_name: 股票名称或代码
- sentiment_score: 情绪分值 (-1.0 到 1.0)
- key_logic: 核心论点（一句话）
- confidence_level: 置信度 (0.0 到 1.0)

如果文本中提到多只股票，请为每只股票输出一个JSON对象，用数组包裹。
如果无法识别股票或文本质量太低，返回空数组 []。"""
    
    def analyze_posts(self, posts_df, batch_size=10, delay=1):
        """
        分析股吧帖子
        
        参数:
            posts_df: 包含帖子的DataFrame
            batch_size: 每批处理的帖子数量
            delay: 请求间隔（秒）
            
        返回:
            DataFrame: 包含AI分析结果的数据
        """
        if posts_df.empty:
            print("输入数据为空")
            return pd.DataFrame()
        
        print(f"开始使用DeepSeek AI分析 {len(posts_df)} 条帖子...")
        print(f"批次大小: {batch_size}, 请求间隔: {delay}秒")
        
        all_results = []
        
        # 分批处理
        for i in range(0, len(posts_df), batch_size):
            batch = posts_df.iloc[i:i+batch_size]
            batch_num = i // batch_size + 1
            total_batches = (len(posts_df) + batch_size - 1) // batch_size
            
            print(f"\n处理批次 {batch_num}/{total_batches}...")
            
            for idx, row in batch.iterrows():
                try:
                    # 准备输入文本
                    title = str(row.get('标题', ''))
                    content = str(row.get('内容', ''))
                    
                    # 调用DeepSeek API
                    result = self._analyze_single_post(title, content)
                    
                    if result:
                        # 添加原始信息
                        for item in result:
                            item['原始标题'] = title
                            item['原始内容'] = content[:100] + '...' if len(content) > 100 else content
                            item['帖子链接'] = row.get('帖子链接', '')
                            item['发布时间'] = row.get('发布时间', '')
                            all_results.append(item)
                        
                        print(f"  ✓ 第 {idx+1} 条: 识别到 {len(result)} 个标的")
                    else:
                        print(f"  × 第 {idx+1} 条: 未识别到有效信息")
                    
                    # 延时避免请求过快
                    time.sleep(delay)
                    
                except Exception as e:
                    print(f"  × 第 {idx+1} 条分析失败: {e}")
                    continue
        
        if all_results:
            result_df = pd.DataFrame(all_results)
            print(f"\n✓ 分析完成，共识别 {len(result_df)} 条有效信息")
            return result_df
        else:
            print("\n× 未识别到有效信息")
            return pd.DataFrame()
    
    def _analyze_single_post(self, title, content):
        """
        分析单条帖子
        
        参数:
            title: 帖子标题
            content: 帖子内容
            
        返回:
            list: 分析结果列表
        """
        # 构建用户输入
        user_input = f"标题: {title}\n内容: {content}"
        
        # 调用API
        try:
            response = self._call_deepseek_api(user_input)
            
            if response:
                # 解析JSON结果
                try:
                    # 尝试直接解析
                    result = json.loads(response)
                    
                    # 如果返回的是单个对象，转为数组
                    if isinstance(result, dict):
                        result = [result]
                    
                    # 验证结果格式
                    validated_results = []
                    for item in result:
                        if self._validate_result(item):
                            validated_results.append(item)
                    
                    return validated_results
                    
                except json.JSONDecodeError:
                    # 如果不是标准JSON，尝试提取
                    print(f"    警告: JSON解析失败，原始响应: {response[:100]}...")
                    return []
            
            return []
            
        except Exception as e:
            print(f"    API调用失败: {e}")
            return []
    
    def _call_deepseek_api(self, user_input):
        """
        调用DeepSeek API
        
        参数:
            user_input: 用户输入文本
            
        返回:
            str: API响应内容
        """
        url = f"{self.api_base}/chat/completions"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_input}
            ],
            "temperature": 0.3,  # 降低温度以获得更稳定的输出
            "max_tokens": 500
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            # 提取响应内容
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                return content.strip()
            
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"    API请求错误: {e}")
            return None
    
    def _validate_result(self, item):
        """验证结果格式"""
        required_fields = ['stock_name', 'sentiment_score', 'key_logic', 'confidence_level']
        
        # 检查必需字段
        for field in required_fields:
            if field not in item:
                return False
        
        # 验证数值范围
        try:
            sentiment = float(item['sentiment_score'])
            confidence = float(item['confidence_level'])
            
            if not (-1.0 <= sentiment <= 1.0):
                return False
            if not (0.0 <= confidence <= 1.0):
                return False
                
        except (ValueError, TypeError):
            return False
        
        return True
    
    def generate_analysis_report(self, analysis_df):
        """生成AI分析报告"""
        if analysis_df.empty:
            return "未获取到AI分析结果"
        
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("DeepSeek AI 深度分析报告")
        report_lines.append(f"生成时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
        report_lines.append("=" * 80)
        report_lines.append("")
        
        # 统计信息
        report_lines.append("【分析概览】")
        report_lines.append(f"分析标的总数: {len(analysis_df)}")
        report_lines.append(f"平均情绪分值: {analysis_df['sentiment_score'].mean():.2f}")
        report_lines.append(f"平均置信度: {analysis_df['confidence_level'].mean():.2f}")
        report_lines.append("")
        
        # 情绪分布
        positive = len(analysis_df[analysis_df['sentiment_score'] > 0.3])
        neutral = len(analysis_df[(analysis_df['sentiment_score'] >= -0.3) & (analysis_df['sentiment_score'] <= 0.3)])
        negative = len(analysis_df[analysis_df['sentiment_score'] < -0.3])
        
        report_lines.append("【市场情绪分布】")
        report_lines.append(f"  乐观情绪: {positive} 条 ({positive/len(analysis_df)*100:.1f}%)")
        report_lines.append(f"  中性情绪: {neutral} 条 ({neutral/len(analysis_df)*100:.1f}%)")
        report_lines.append(f"  悲观情绪: {negative} 条 ({negative/len(analysis_df)*100:.1f}%)")
        report_lines.append("")
        
        # 高置信度标的
        high_confidence = analysis_df[analysis_df['confidence_level'] >= 0.7].sort_values(
            'confidence_level', ascending=False
        )
        
        if not high_confidence.empty:
            report_lines.append("【高置信度标的 TOP 10】")
            report_lines.append("-" * 80)
            
            for idx, row in high_confidence.head(10).iterrows():
                sentiment_label = self._get_sentiment_label(row['sentiment_score'])
                
                report_lines.append(f"\n{idx+1}. {row['stock_name']}")
                report_lines.append(f"   情绪: {sentiment_label} ({row['sentiment_score']:.2f})")
                report_lines.append(f"   置信度: {row['confidence_level']:.2f}")
                report_lines.append(f"   核心逻辑: {row['key_logic']}")
                report_lines.append(f"   原始标题: {row['原始标题']}")
        
        report_lines.append("")
        report_lines.append("=" * 80)
        
        return "\n".join(report_lines)
    
    def _get_sentiment_label(self, score):
        """获取情绪标签"""
        if score >= 0.7:
            return "🔥 极度乐观"
        elif score >= 0.3:
            return "📈 乐观"
        elif score >= -0.3:
            return "➡️  中性"
        elif score >= -0.7:
            return "📉 悲观"
        else:
            return "❄️  极度恐慌"


def test_deepseek_analyzer():
    """测试DeepSeek分析器"""
    print("测试DeepSeek AI分析器...")
    print("=" * 80)
    
    # 创建测试数据
    test_data = {
        '标题': [
            '山东黄金突破60日均线，MACD金叉，主力资金大幅流入',
            '紫金矿业业绩预告超预期，社保基金增持明显',
            '黄金股要起飞了！必涨！冲冲冲！',
            '中金黄金放量突破，成交量是前日3倍',
            '某黄金股大单压盘，主力吸筹迹象明显'
        ],
        '内容': [
            '技术面看，山东黄金今日突破60日均线，MACD指标金叉向上，同时主力资金净流入1.5亿元。',
            '紫金矿业发布业绩预告，预计净利润同比增长45%，超出市场预期。社保基金增持500万股。',
            '黄金股必涨，大家赶紧上车！',
            '中金黄金今日放量上涨，成交量达到前日的3倍，突破前期箱体。',
            '观察到某黄金股有明显的大单压盘迹象，主力资金在低位吸筹。'
        ],
        '帖子链接': [''] * 5,
        '发布时间': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')] * 5
    }
    
    test_df = pd.DataFrame(test_data)
    
    # 创建分析器
    analyzer = DeepSeekAnalyzer()
    
    # 检查API Key
    if analyzer.api_key == "YOUR_DEEPSEEK_API_KEY":
        print("⚠️  警告: 未设置DeepSeek API Key")
        print("请在代码中设置 api_key 参数或设置环境变量")
        print("\n使用模拟数据进行演示...")
        
        # 创建模拟结果
        mock_results = create_mock_analysis_results()
        
        # 生成报告
        report = analyzer.generate_analysis_report(mock_results)
        print("\n" + report)
        
        # 保存结果
        filename = f"deepseek_analysis_mock_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        mock_results.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n模拟结果已保存到: {filename}")
        
        return mock_results
    
    # 实际调用API
    print("\n开始调用DeepSeek API...")
    analysis_df = analyzer.analyze_posts(test_df, batch_size=5, delay=1)
    
    if not analysis_df.empty:
        # 生成报告
        report = analyzer.generate_analysis_report(analysis_df)
        print("\n" + report)
        
        # 保存结果
        filename = f"deepseek_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        analysis_df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n结果已保存到: {filename}")
        
        return analysis_df
    else:
        print("未获取到分析结果")
        return pd.DataFrame()


def create_mock_analysis_results():
    """创建模拟分析结果（用于演示）"""
    mock_data = {
        'stock_name': [
            '山东黄金(600547)',
            '紫金矿业(601899)',
            '中金黄金(600489)',
            '某黄金股'
        ],
        'sentiment_score': [0.75, 0.80, 0.60, 0.40],
        'key_logic': [
            '技术面突破60日均线，MACD金叉，主力资金净流入1.5亿',
            '业绩预告超预期，净利润同比增长45%，社保基金增持',
            '放量突破，成交量放大3倍，突破前期箱体',
            '大单压盘，主力低位吸筹'
        ],
        'confidence_level': [0.85, 0.90, 0.75, 0.60],
        '原始标题': [
            '山东黄金突破60日均线，MACD金叉，主力资金大幅流入',
            '紫金矿业业绩预告超预期，社保基金增持明显',
            '中金黄金放量突破，成交量是前日3倍',
            '某黄金股大单压盘，主力吸筹迹象明显'
        ],
        '原始内容': [
            '技术面看，山东黄金今日突破60日均线，MACD指标金叉向上...',
            '紫金矿业发布业绩预告，预计净利润同比增长45%...',
            '中金黄金今日放量上涨，成交量达到前日的3倍...',
            '观察到某黄金股有明显的大单压盘迹象...'
        ],
        '帖子链接': [''] * 4,
        '发布时间': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')] * 4
    }
    
    return pd.DataFrame(mock_data)


if __name__ == "__main__":
    test_deepseek_analyzer()