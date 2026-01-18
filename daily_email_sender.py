#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日简报邮件推送系统
实现：自动生成简报 → 汇总报告 → 发送邮件

功能:
1. 运行所有分析模块
2. 汇总生成综合简报
3. 发送到指定邮箱
"""

import smtplib
import os
import glob
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import subprocess
import time


class DailyEmailSender:
    """每日简报邮件推送器"""
    
    def __init__(self, email_config=None):
        """
        初始化邮件推送器
        
        参数:
            email_config: 邮件配置字典
        """
        # 从配置文件读取邮件配置
        if email_config is None:
            try:
                from config import EMAIL_CONFIG
                self.email_config = EMAIL_CONFIG
            except ImportError:
                print("⚠️  警告: 未找到邮件配置，请设置EMAIL_CONFIG")
                self.email_config = {
                    'smtp_server': 'smtp.qq.com',  # QQ邮箱SMTP服务器
                    'smtp_port': 465,  # SSL端口
                    'sender_email': 'your_email@qq.com',
                    'sender_password': 'your_auth_code',  # QQ邮箱授权码
                    'receiver_emails': ['receiver@example.com']
                }
        else:
            self.email_config = email_config
        
        print("✓ 邮件推送器初始化完成")
    
    def run_all_analysis(self):
        """
        运行所有分析模块
        
        返回:
            dict: 各模块运行结果
        """
        print("\n" + "=" * 60)
        print("开始运行所有分析模块")
        print("=" * 60)
        
        results = {}
        
        # 1. 黄金股票筛选
        print("\n【1/5】运行黄金股票筛选...")
        try:
            result = subprocess.run(
                ['python3', 'gold_stock_screener.py'],
                capture_output=True,
                text=True,
                timeout=300
            )
            results['gold_stocks'] = result.returncode == 0
            print("✓ 黄金股票筛选完成" if results['gold_stocks'] else "× 黄金股票筛选失败")
        except Exception as e:
            print(f"× 黄金股票筛选失败: {e}")
            results['gold_stocks'] = False
        
        # 2. 微博情绪分析（加权版）
        print("\n【2/5】运行微博情绪分析...")
        try:
            result = subprocess.run(
                ['python3', 'weibo_sentiment_weighted.py'],
                capture_output=True,
                text=True,
                timeout=1800  # 30分钟超时
            )
            results['weibo_sentiment'] = result.returncode == 0
            print("✓ 微博情绪分析完成" if results['weibo_sentiment'] else "× 微博情绪分析失败")
        except Exception as e:
            print(f"× 微博情绪分析失败: {e}")
            results['weibo_sentiment'] = False
        
        # 3. 全网热点发现
        print("\n【3/5】运行全网热点发现...")
        try:
            result = subprocess.run(
                ['python3', 'Discovery_Engine.py'],
                capture_output=True,
                text=True,
                timeout=1800  # 30分钟超时
            )
            results['discovery'] = result.returncode == 0
            print("✓ 全网热点发现完成" if results['discovery'] else "× 全网热点发现失败")
        except Exception as e:
            print(f"× 全网热点发现失败: {e}")
            results['discovery'] = False
        
        # 4. 量化选股
        print("\n【4/5】运行量化选股...")
        try:
            result = subprocess.run(
                ['python3', 'Quant_Picker.py'],
                capture_output=True,
                text=True,
                timeout=600  # 10分钟超时
            )
            results['quant_picker'] = result.returncode == 0
            print("✓ 量化选股完成" if results['quant_picker'] else "× 量化选股失败")
        except Exception as e:
            print(f"× 量化选股失败: {e}")
            results['quant_picker'] = False
        
        # 5. 黑马发现（如果有）
        print("\n【5/5】运行黑马发现...")
        try:
            if os.path.exists('dark_horse_finder.py'):
                result = subprocess.run(
                    ['python3', 'dark_horse_finder.py'],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                results['dark_horse'] = result.returncode == 0
                print("✓ 黑马发现完成" if results['dark_horse'] else "× 黑马发现失败")
            else:
                results['dark_horse'] = None
                print("⊘ 黑马发现模块不存在，跳过")
        except Exception as e:
            print(f"× 黑马发现失败: {e}")
            results['dark_horse'] = False
        
        print("\n" + "=" * 60)
        print("所有分析模块运行完成")
        print("=" * 60)
        
        # 统计结果
        success_count = sum(1 for v in results.values() if v is True)
        total_count = sum(1 for v in results.values() if v is not None)
        
        print(f"\n成功: {success_count}/{total_count}")
        
        return results
    
    def generate_summary_report(self):
        """
        生成综合简报
        
        返回:
            str: 简报文件路径
        """
        print("\n" + "=" * 60)
        print("生成综合简报")
        print("=" * 60)
        
        today = datetime.now().strftime('%Y%m%d')
        filename = f"每日投资简报_{today}.md"
        
        report_lines = []
        
        # 标题
        report_lines.append("# 📊 每日投资简报")
        report_lines.append("")
        report_lines.append(f"**生成时间**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")
        
        # 目录
        report_lines.append("## 📑 目录")
        report_lines.append("")
        report_lines.append("1. [黄金股票筛选](#1-黄金股票筛选)")
        report_lines.append("2. [微博黄金情绪分析](#2-微博黄金情绪分析)")
        report_lines.append("3. [全网热点发现](#3-全网热点发现)")
        report_lines.append("4. [AI潜力股推荐](#4-ai潜力股推荐)")
        report_lines.append("5. [黑马发现报告](#5-黑马发现报告)")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")
        
        # 1. 黄金股票筛选
        report_lines.append("## 1. 黄金股票筛选")
        report_lines.append("")
        
        gold_csv = self._find_latest_file('gold_stocks_analysis_*.csv')
        if gold_csv:
            report_lines.append(f"**数据文件**: `{os.path.basename(gold_csv)}`")
            report_lines.append("")
            
            # 读取CSV并显示TOP 5
            try:
                import pandas as pd
                df = pd.read_csv(gold_csv, encoding='utf-8-sig')
                
                report_lines.append(f"**筛选结果**: 共 {len(df)} 只股票")
                report_lines.append("")
                report_lines.append("### TOP 5 黄金股票")
                report_lines.append("")
                report_lines.append("| 排名 | 股票名称 | 股票代码 | 综合评分 | 官方资本 |")
                report_lines.append("|------|----------|----------|----------|----------|")
                
                for i, (_, row) in enumerate(df.head(5).iterrows(), 1):
                    name = row.get('股票名称', '')
                    code = row.get('股票代码', '')
                    score = row.get('综合评分', 0)
                    official = '是' if row.get('是否包含官方资本', False) else '否'
                    report_lines.append(f"| {i} | {name} | {code} | {score:.1f} | {official} |")
                
                report_lines.append("")
            except Exception as e:
                report_lines.append(f"⚠️  数据读取失败: {e}")
                report_lines.append("")
        else:
            report_lines.append("⚠️  未找到黄金股票筛选数据")
            report_lines.append("")
        
        report_lines.append("---")
        report_lines.append("")
        
        # 2. 微博黄金情绪分析
        report_lines.append("## 2. 微博黄金情绪分析")
        report_lines.append("")
        
        weibo_md = self._find_latest_file('微博黄金情绪分析_加权版_*.md')
        if weibo_md:
            report_lines.append(f"**报告文件**: `{os.path.basename(weibo_md)}`")
            report_lines.append("")
            
            # 提取关键信息
            try:
                with open(weibo_md, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # 提取情绪指数
                    import re
                    score_match = re.search(r'加权平均分数.*?(\d+\.?\d*)\s*/\s*100', content)
                    if score_match:
                        score = float(score_match.group(1))
                        report_lines.append(f"**加权情绪指数**: {score:.2f} / 100")
                        report_lines.append("")
                    
                    # 提取风险点和机会点
                    risk_section = re.search(r'用户最担心的3个风险点(.*?)用户最期待的3个机会点', content, re.DOTALL)
                    if risk_section:
                        report_lines.append("**风险点**:")
                        risks = re.findall(r'\d+\.\s*(.+)', risk_section.group(1))
                        for risk in risks[:3]:
                            report_lines.append(f"- {risk.strip()}")
                        report_lines.append("")
                    
                    opp_section = re.search(r'用户最期待的3个机会点(.*?)(?:##|---)', content, re.DOTALL)
                    if opp_section:
                        report_lines.append("**机会点**:")
                        opps = re.findall(r'\d+\.\s*(.+)', opp_section.group(1))
                        for opp in opps[:3]:
                            report_lines.append(f"- {opp.strip()}")
                        report_lines.append("")
            
            except Exception as e:
                report_lines.append(f"⚠️  报告解析失败: {e}")
                report_lines.append("")
        else:
            report_lines.append("⚠️  未找到微博情绪分析报告")
            report_lines.append("")
        
        report_lines.append("---")
        report_lines.append("")
        
        # 3. 全网热点发现
        report_lines.append("## 3. 全网热点发现")
        report_lines.append("")
        
        radar_md = self._find_latest_file('全网雷达报告_*.md')
        if radar_md:
            report_lines.append(f"**报告文件**: `{os.path.basename(radar_md)}`")
            report_lines.append("")
            
            # 提取热门板块
            try:
                with open(radar_md, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # 提取TOP 3板块
                    import re
                    sectors = re.findall(r'###\s*\d+\.\s*(.+?)\s*🚀', content)
                    
                    if sectors:
                        report_lines.append("**热门板块 TOP 3**:")
                        report_lines.append("")
                        for i, sector in enumerate(sectors[:3], 1):
                            report_lines.append(f"{i}. {sector.strip()}")
                        report_lines.append("")
            
            except Exception as e:
                report_lines.append(f"⚠️  报告解析失败: {e}")
                report_lines.append("")
        else:
            report_lines.append("⚠️  未找到全网雷达报告")
            report_lines.append("")
        
        report_lines.append("---")
        report_lines.append("")
        
        # 4. AI潜力股推荐
        report_lines.append("## 4. AI潜力股推荐")
        report_lines.append("")
        
        quant_md = self._find_latest_file('AI潜力股推荐_*.md')
        if quant_md:
            report_lines.append(f"**报告文件**: `{os.path.basename(quant_md)}`")
            report_lines.append("")
            
            # 提取AI推荐
            try:
                with open(quant_md, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # 提取推荐股票
                    import re
                    stocks = re.findall(r'###\s*(\d+)\.\s*(.+?)\s*\((.+?)\)', content)
                    
                    if stocks:
                        report_lines.append("**AI推荐 TOP 3**:")
                        report_lines.append("")
                        report_lines.append("| 排名 | 股票名称 | 股票代码 |")
                        report_lines.append("|------|----------|----------|")
                        
                        for rank, name, code in stocks[:3]:
                            report_lines.append(f"| {rank} | {name.strip()} | {code.strip()} |")
                        
                        report_lines.append("")
            
            except Exception as e:
                report_lines.append(f"⚠️  报告解析失败: {e}")
                report_lines.append("")
        else:
            report_lines.append("⚠️  未找到AI潜力股推荐")
            report_lines.append("")
        
        report_lines.append("---")
        report_lines.append("")
        
        # 5. 黑马发现报告
        report_lines.append("## 5. 黑马发现报告")
        report_lines.append("")
        
        horse_txt = self._find_latest_file('dark_horse_report_*.txt')
        if horse_txt:
            report_lines.append(f"**报告文件**: `{os.path.basename(horse_txt)}`")
            report_lines.append("")
            report_lines.append("详见附件")
            report_lines.append("")
        else:
            report_lines.append("⚠️  未找到黑马发现报告")
            report_lines.append("")
        
        # 免责声明
        report_lines.append("---")
        report_lines.append("")
        report_lines.append("## ⚠️  免责声明")
        report_lines.append("")
        report_lines.append("本简报由AI自动生成，仅供参考，不构成投资建议。")
        report_lines.append("股票投资有风险，入市需谨慎。")
        report_lines.append("")
        
        # 写入文件
        report_content = "\n".join(report_lines)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"✓ 综合简报已生成: {filename}")
        
        return filename
    
    def _find_latest_file(self, pattern):
        """
        查找最新的文件
        
        参数:
            pattern: 文件名模式
            
        返回:
            str: 文件路径，如果未找到返回None
        """
        files = glob.glob(pattern)
        
        if files:
            # 按修改时间排序，返回最新的
            latest_file = max(files, key=os.path.getmtime)
            return latest_file
        
        return None

    
    def send_email(self, summary_file):
        """
        发送邮件
        
        参数:
            summary_file: 综合简报文件路径
            
        返回:
            bool: 是否发送成功
        """
        print("\n" + "=" * 60)
        print("发送邮件")
        print("=" * 60)
        
        try:
            # 创建邮件对象
            msg = MIMEMultipart()
            msg['From'] = self.email_config['sender_email']
            msg['To'] = ', '.join(self.email_config['receiver_emails'])
            msg['Subject'] = f"📊 每日投资简报 - {datetime.now().strftime('%Y年%m月%d日')}"
            
            # 邮件正文
            body = self._create_email_body(summary_file)
            msg.attach(MIMEText(body, 'html', 'utf-8'))
            
            # 附件1: 综合简报
            self._attach_file(msg, summary_file)
            
            # 附件2: 黄金股票筛选
            gold_csv = self._find_latest_file('gold_stocks_analysis_*.csv')
            if gold_csv:
                self._attach_file(msg, gold_csv)
            
            # 附件3: 微博情绪分析
            weibo_md = self._find_latest_file('微博黄金情绪分析_加权版_*.md')
            if weibo_md:
                self._attach_file(msg, weibo_md)
            
            # 附件4: 全网雷达报告
            radar_md = self._find_latest_file('全网雷达报告_*.md')
            if radar_md:
                self._attach_file(msg, radar_md)
            
            # 附件5: AI潜力股推荐
            quant_md = self._find_latest_file('AI潜力股推荐_*.md')
            if quant_md:
                self._attach_file(msg, quant_md)
            
            # 发送邮件
            print(f"\n正在连接SMTP服务器: {self.email_config['smtp_server']}:{self.email_config['smtp_port']}")
            
            with smtplib.SMTP_SSL(
                self.email_config['smtp_server'],
                self.email_config['smtp_port']
            ) as server:
                print("正在登录...")
                server.login(
                    self.email_config['sender_email'],
                    self.email_config['sender_password']
                )
                
                print("正在发送邮件...")
                server.send_message(msg)
            
            print("✓ 邮件发送成功")
            print(f"  收件人: {', '.join(self.email_config['receiver_emails'])}")
            
            return True
        
        except Exception as e:
            print(f"× 邮件发送失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _create_email_body(self, summary_file):
        """
        创建邮件正文（HTML格式）
        
        参数:
            summary_file: 综合简报文件路径
            
        返回:
            str: HTML格式的邮件正文
        """
        today = datetime.now().strftime('%Y年%m月%d日')
        
        html = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                .header {{
                    background-color: #4CAF50;
                    color: white;
                    padding: 20px;
                    text-align: center;
                }}
                .content {{
                    padding: 20px;
                }}
                .section {{
                    margin-bottom: 20px;
                    padding: 15px;
                    background-color: #f9f9f9;
                    border-left: 4px solid #4CAF50;
                }}
                .footer {{
                    background-color: #f1f1f1;
                    padding: 10px;
                    text-align: center;
                    font-size: 12px;
                    color: #666;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin-top: 10px;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                }}
                th {{
                    background-color: #4CAF50;
                    color: white;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📊 每日投资简报</h1>
                <p>{today}</p>
            </div>
            
            <div class="content">
                <div class="section">
                    <h2>📋 简报概览</h2>
                    <p>本简报包含以下内容：</p>
                    <ul>
                        <li>黄金股票筛选</li>
                        <li>微博黄金情绪分析（加权版）</li>
                        <li>全网热点发现</li>
                        <li>AI潜力股推荐</li>
                        <li>黑马发现报告</li>
                    </ul>
                </div>
                
                <div class="section">
                    <h2>📎 附件说明</h2>
                    <p>请查看附件获取详细报告：</p>
                    <ul>
                        <li><strong>每日投资简报.md</strong> - 综合简报</li>
                        <li><strong>gold_stocks_analysis.csv</strong> - 黄金股票数据</li>
                        <li><strong>微博黄金情绪分析_加权版.md</strong> - 微博情绪报告</li>
                        <li><strong>全网雷达报告.md</strong> - 热点板块报告</li>
                        <li><strong>AI潜力股推荐.md</strong> - AI选股报告</li>
                    </ul>
                </div>
                
                <div class="section">
                    <h2>⚠️  风险提示</h2>
                    <p style="color: #d32f2f;">
                        本简报由AI自动生成，仅供参考，不构成投资建议。<br>
                        股票投资有风险，入市需谨慎。<br>
                        请结合自身风险承受能力做出投资决策。
                    </p>
                </div>
            </div>
            
            <div class="footer">
                <p>本邮件由系统自动发送，请勿直接回复</p>
                <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _attach_file(self, msg, filepath):
        """
        添加附件
        
        参数:
            msg: 邮件对象
            filepath: 文件路径
        """
        try:
            with open(filepath, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
            
            encoders.encode_base64(part)
            
            filename = os.path.basename(filepath)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename="{filename}"'
            )
            
            msg.attach(part)
            
            print(f"  ✓ 添加附件: {filename}")
        
        except Exception as e:
            print(f"  × 添加附件失败 ({filename}): {e}")
    
    def run(self):
        """
        运行完整的每日推送流程
        """
        print("=" * 60)
        print("每日简报邮件推送系统")
        print("=" * 60)
        print(f"\n开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        start_time = time.time()
        
        # 1. 运行所有分析模块
        results = self.run_all_analysis()
        
        # 2. 生成综合简报
        summary_file = self.generate_summary_report()
        
        # 3. 发送邮件
        success = self.send_email(summary_file)
        
        # 完成
        end_time = time.time()
        duration = end_time - start_time
        
        print("\n" + "=" * 60)
        if success:
            print("✅ 每日简报推送完成！")
        else:
            print("⚠️  每日简报推送部分失败")
        print("=" * 60)
        
        print(f"\n总耗时: {duration/60:.1f} 分钟")
        print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def main():
    """主函数"""
    # 创建邮件推送器
    sender = DailyEmailSender()
    
    # 运行推送流程
    sender.run()


if __name__ == "__main__":
    main()
