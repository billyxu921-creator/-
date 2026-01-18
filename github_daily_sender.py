#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Actions专用的每日简报推送脚本
简化版本，适合无浏览器环境
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


class GitHubDailySender:
    """GitHub Actions专用邮件推送器"""
    
    def __init__(self):
        """初始化"""
        try:
            from config import EMAIL_CONFIG
            self.email_config = EMAIL_CONFIG
        except ImportError:
            print("× 未找到邮件配置")
            raise
        
        print("✓ 邮件推送器初始化完成")
    
    def run_basic_analysis(self):
        """运行基础分析（不需要浏览器）"""
        print("\n" + "=" * 60)
        print("运行基础分析模块")
        print("=" * 60)
        
        results = {}
        
        # 1. 黄金股票筛选
        print("\n【1/2】黄金股票筛选...")
        try:
            result = subprocess.run(
                ['python3', 'gold_stock_screener.py'],
                capture_output=True,
                text=True,
                timeout=300
            )
            results['gold_stocks'] = result.returncode == 0
            print("✓ 完成" if results['gold_stocks'] else "× 失败")
        except Exception as e:
            print(f"× 失败: {e}")
            results['gold_stocks'] = False
        
        # 2. 量化选股
        print("\n【2/2】量化选股...")
        try:
            result = subprocess.run(
                ['python3', 'Quant_Picker.py'],
                capture_output=True,
                text=True,
                timeout=600
            )
            results['quant_picker'] = result.returncode == 0
            print("✓ 完成" if results['quant_picker'] else "× 失败")
        except Exception as e:
            print(f"× 失败: {e}")
            results['quant_picker'] = False
        
        return results
    
    def generate_simple_report(self):
        """生成简化版简报"""
        print("\n" + "=" * 60)
        print("生成简化版简报")
        print("=" * 60)
        
        today = datetime.now().strftime('%Y%m%d')
        filename = f"每日投资简报_{today}.md"
        
        report_lines = []
        
        # 标题
        report_lines.append("# 📊 每日投资简报（GitHub Actions版）")
        report_lines.append("")
        report_lines.append(f"**生成时间**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")
        
        # 说明
        report_lines.append("## 📝 说明")
        report_lines.append("")
        report_lines.append("本简报由GitHub Actions自动生成，包含以下内容：")
        report_lines.append("")
        report_lines.append("- ✅ 黄金股票筛选")
        report_lines.append("- ✅ AI量化选股")
        report_lines.append("- ⊘ 微博情绪分析（需要浏览器环境，已跳过）")
        report_lines.append("- ⊘ 全网热点发现（需要浏览器环境，已跳过）")
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("")
        
        # 1. 黄金股票筛选
        report_lines.append("## 1. 黄金股票筛选")
        report_lines.append("")
        
        gold_csv = self._find_latest_file('gold_stocks_analysis_*.csv')
        if gold_csv:
            try:
                import pandas as pd
                df = pd.read_csv(gold_csv, encoding='utf-8-sig')
                
                report_lines.append(f"**筛选结果**: 共 {len(df)} 只股票")
                report_lines.append("")
                report_lines.append("### TOP 5")
                report_lines.append("")
                report_lines.append("| 排名 | 股票名称 | 股票代码 | 综合评分 |")
                report_lines.append("|------|----------|----------|----------|")
                
                for i, (_, row) in enumerate(df.head(5).iterrows(), 1):
                    name = row.get('股票名称', '')
                    code = row.get('股票代码', '')
                    score = row.get('综合评分', 0)
                    report_lines.append(f"| {i} | {name} | {code} | {score:.1f} |")
                
                report_lines.append("")
            except Exception as e:
                report_lines.append(f"⚠️  数据读取失败: {e}")
                report_lines.append("")
        else:
            report_lines.append("⚠️  未找到数据")
            report_lines.append("")
        
        report_lines.append("---")
        report_lines.append("")
        
        # 2. AI量化选股
        report_lines.append("## 2. AI量化选股")
        report_lines.append("")
        
        quant_md = self._find_latest_file('AI潜力股推荐_*.md')
        if quant_md:
            try:
                with open(quant_md, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
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
            report_lines.append("⚠️  未找到AI推荐")
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
        
        print(f"✓ 简报已生成: {filename}")
        
        return filename
    
    def _find_latest_file(self, pattern):
        """查找最新文件"""
        files = glob.glob(pattern)
        if files:
            return max(files, key=os.path.getmtime)
        return None
    
    def send_email(self, summary_file):
        """发送邮件"""
        print("\n" + "=" * 60)
        print("发送邮件")
        print("=" * 60)
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_config['sender_email']
            msg['To'] = ', '.join(self.email_config['receiver_emails'])
            msg['Subject'] = f"📊 每日投资简报 - {datetime.now().strftime('%Y年%m月%d日')}"
            
            # 邮件正文
            body = f"""
            <html>
            <body>
                <h2>📊 每日投资简报</h2>
                <p>生成时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}</p>
                <p>本简报由GitHub Actions自动生成并推送。</p>
                <p>详细内容请查看附件。</p>
                <hr>
                <p style="color: #999; font-size: 12px;">
                    本邮件由系统自动发送，请勿直接回复<br>
                    ⚠️  投资有风险，入市需谨慎
                </p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html', 'utf-8'))
            
            # 添加附件
            self._attach_file(msg, summary_file)
            
            gold_csv = self._find_latest_file('gold_stocks_analysis_*.csv')
            if gold_csv:
                self._attach_file(msg, gold_csv)
            
            quant_md = self._find_latest_file('AI潜力股推荐_*.md')
            if quant_md:
                self._attach_file(msg, quant_md)
            
            # 发送
            print(f"\n连接SMTP服务器...")
            with smtplib.SMTP_SSL(
                self.email_config['smtp_server'],
                self.email_config['smtp_port']
            ) as server:
                print("登录...")
                server.login(
                    self.email_config['sender_email'],
                    self.email_config['sender_password']
                )
                
                print("发送邮件...")
                server.send_message(msg)
            
            print("✓ 邮件发送成功")
            return True
        
        except Exception as e:
            print(f"× 邮件发送失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _attach_file(self, msg, filepath):
        """添加附件"""
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
            print(f"  × 添加附件失败: {e}")
    
    def run(self):
        """运行完整流程"""
        print("=" * 60)
        print("GitHub Actions 每日简报推送")
        print("=" * 60)
        print(f"\n开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 1. 运行基础分析
        results = self.run_basic_analysis()
        
        # 2. 生成简报
        summary_file = self.generate_simple_report()
        
        # 3. 发送邮件
        success = self.send_email(summary_file)
        
        print("\n" + "=" * 60)
        if success:
            print("✅ 推送完成")
        else:
            print("⚠️  推送失败")
        print("=" * 60)


def main():
    sender = GitHubDailySender()
    sender.run()


if __name__ == "__main__":
    main()
