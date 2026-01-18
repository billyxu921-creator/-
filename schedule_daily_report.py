#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定时任务调度器
实现每日北京时间8点自动运行简报推送

使用schedule库实现定时任务
"""

import schedule
import time
from datetime import datetime
import subprocess
import sys


def run_daily_report():
    """运行每日简报推送"""
    print("\n" + "=" * 60)
    print(f"开始运行每日简报推送")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        # 运行邮件推送脚本
        result = subprocess.run(
            ['python3', 'daily_email_sender.py'],
            capture_output=True,
            text=True,
            timeout=7200  # 2小时超时
        )
        
        if result.returncode == 0:
            print("\n✅ 每日简报推送成功")
        else:
            print("\n× 每日简报推送失败")
            print(f"错误信息: {result.stderr}")
        
        # 输出日志
        print("\n【运行日志】")
        print(result.stdout)
    
    except subprocess.TimeoutExpired:
        print("\n× 运行超时（超过2小时）")
    
    except Exception as e:
        print(f"\n× 运行失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("等待下次运行...")
    print("=" * 60)


def main():
    """主函数"""
    # 从配置文件读取运行时间
    try:
        from config import SCHEDULE_CONFIG
        run_time = SCHEDULE_CONFIG.get('daily_run_time', '08:00')
        timezone = SCHEDULE_CONFIG.get('timezone', 'Asia/Shanghai')
    except ImportError:
        run_time = '08:00'
        timezone = 'Asia/Shanghai'
    
    print("=" * 60)
    print("每日简报定时任务调度器")
    print("=" * 60)
    print(f"\n配置信息:")
    print(f"  运行时间: 每天 {run_time}")
    print(f"  时区: {timezone}")
    print(f"  当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 设置定时任务
    schedule.every().day.at(run_time).do(run_daily_report)
    
    print(f"✓ 定时任务已设置")
    print(f"  下次运行时间: {schedule.next_run()}")
    print()
    
    # 询问是否立即运行一次
    response = input("是否立即运行一次测试？(y/n): ")
    if response.lower() == 'y':
        print("\n立即运行测试...")
        run_daily_report()
    
    print("\n" + "=" * 60)
    print("定时任务运行中...")
    print("按 Ctrl+C 停止")
    print("=" * 60)
    print()
    
    # 持续运行
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # 每分钟检查一次
    
    except KeyboardInterrupt:
        print("\n\n定时任务已停止")
        sys.exit(0)


if __name__ == "__main__":
    main()
