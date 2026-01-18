#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试DeepSeek API Key是否有效
"""

import requests
import json

def test_deepseek_api():
    """测试API连接"""
    
    print("=" * 60)
    print("DeepSeek API 连接测试")
    print("=" * 60)
    
    # 从配置文件读取
    try:
        from config import DEEPSEEK_CONFIG
        api_key = DEEPSEEK_CONFIG['api_key']
        api_base = DEEPSEEK_CONFIG['api_base']
        print(f"✓ API Key: {api_key[:20]}...{api_key[-10:]}")
        print(f"✓ API Base: {api_base}")
    except ImportError:
        print("× 错误: 未找到 config.py 文件")
        return False
    
    print("\n正在测试API连接...")
    
    # 构建测试请求
    url = f"{api_base}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": "你是一个测试助手。"
            },
            {
                "role": "user",
                "content": "请回复'测试成功'三个字。"
            }
        ],
        "temperature": 0.3,
        "max_tokens": 50
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                print(f"AI回复: {content}")
                print("\n" + "=" * 60)
                print("✅ API连接测试成功！")
                print("=" * 60)
                
                # 显示使用信息
                if 'usage' in result:
                    usage = result['usage']
                    print(f"\n使用统计:")
                    print(f"  输入tokens: {usage.get('prompt_tokens', 0)}")
                    print(f"  输出tokens: {usage.get('completion_tokens', 0)}")
                    print(f"  总计tokens: {usage.get('total_tokens', 0)}")
                
                return True
            else:
                print("× 错误: 响应格式异常")
                print(f"响应内容: {result}")
                return False
        else:
            print(f"× 错误: HTTP {response.status_code}")
            print(f"响应内容: {response.text}")
            
            if response.status_code == 401:
                print("\n可能的原因:")
                print("  1. API Key无效或已过期")
                print("  2. API Key格式错误")
                print("  3. 账户未激活")
            elif response.status_code == 429:
                print("\n可能的原因:")
                print("  1. 请求频率过高")
                print("  2. 账户额度不足")
            
            return False
            
    except requests.exceptions.Timeout:
        print("× 错误: 请求超时")
        print("请检查网络连接")
        return False
    except requests.exceptions.RequestException as e:
        print(f"× 错误: 请求失败 - {e}")
        return False
    except Exception as e:
        print(f"× 错误: {e}")
        return False


if __name__ == "__main__":
    success = test_deepseek_api()
    
    if success:
        print("\n✅ 你可以开始使用AI分析功能了！")
        print("\n运行完整分析:")
        print("  python3 run_analysis_with_ai.py")
    else:
        print("\n❌ API测试失败，请检查配置")
        print("\n排查步骤:")
        print("  1. 确认 config.py 文件存在")
        print("  2. 确认 API Key 正确")
        print("  3. 检查网络连接")
        print("  4. 访问 https://platform.deepseek.com/ 查看账户状态")