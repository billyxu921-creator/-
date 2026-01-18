#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件示例
复制此文件为 config.py 并填入你的实际配置
"""

# DeepSeek API 配置
DEEPSEEK_CONFIG = {
    # API密钥 - 从 https://platform.deepseek.com/ 获取
    'api_key': 'YOUR_DEEPSEEK_API_KEY',
    
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