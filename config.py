#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件
包含DeepSeek API密钥和其他配置参数
"""

# DeepSeek API 配置
DEEPSEEK_CONFIG = {
    # API密钥
    'api_key': 'sk-8b60ff11aefd4032a572f736087f175f',
    
    # API基础URL
    'api_base': 'https://api.deepseek.com/v1',
    
    # 使用的模型
    'model': 'deepseek-chat',
    
    # 温度参数 (0.0-1.0, 越低越稳定)
    'temperature': 0.3,
    
    # 最大token数
    'max_tokens': 500,
    
    # 请求超时时间(秒)
    'timeout': 30
}

# 分析参数配置
ANALYSIS_CONFIG = {
    # 每批处理的帖子数量
    'batch_size': 10,
    
    # API请求间隔(秒)
    'request_delay': 1,
    
    # 最大处理帖子数
    'max_posts': 100,
    
    # 是否启用AI分析
    'enable_ai_analysis': True,
    
    # 是否启用传统分析
    'enable_traditional_analysis': True
}

# 输出配置
OUTPUT_CONFIG = {
    # 输出目录
    'output_dir': 'reports',
    
    # 是否保存详细日志
    'save_detailed_log': True,
    
    # 是否生成HTML报告
    'generate_html_report': True
}


# 邮件配置
EMAIL_CONFIG = {
    # SMTP服务器配置
    'smtp_server': 'smtp.qq.com',  # QQ邮箱SMTP服务器
    'smtp_port': 465,  # SSL端口（QQ邮箱使用465）
    
    # 发件人信息
    'sender_email': 'your_email@qq.com',  # 替换为你的QQ邮箱
    'sender_password': 'your_auth_code',  # 替换为QQ邮箱授权码（不是QQ密码！）
    
    # 收件人列表
    'receiver_emails': [
        'receiver1@example.com',  # 替换为实际收件人邮箱
        # 'receiver2@example.com',  # 可以添加多个收件人
    ],
    
    # 邮件主题前缀
    'subject_prefix': '📊 每日投资简报',
    
    # 是否发送附件
    'attach_files': True,
    
    # 附件大小限制（MB）
    'max_attachment_size': 25
}

# 定时任务配置
SCHEDULE_CONFIG = {
    # 每日运行时间（24小时制）
    'daily_run_time': '08:00',  # 北京时间早上8点
    
    # 时区
    'timezone': 'Asia/Shanghai',
    
    # 是否启用定时任务
    'enable_schedule': True,
    
    # 失败重试次数
    'retry_times': 3,
    
    # 重试间隔（分钟）
    'retry_interval': 10
}
