#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置测试脚本
用于验证config.py中的配置是否正确
"""

import sys


def test_config_file():
    """测试配置文件是否存在"""
    print("=" * 60)
    print("配置文件测试")
    print("=" * 60)
    print()
    
    try:
        import config
        print("✓ config.py 文件存在")
        return True
    except ImportError:
        print("× config.py 文件不存在")
        print()
        print("请执行以下步骤:")
        print("1. 复制示例配置: cp config.example.py config.py")
        print("2. 编辑config.py，填入真实配置")
        return False


def test_deepseek_config():
    """测试DeepSeek配置"""
    print()
    print("-" * 60)
    print("DeepSeek API配置测试")
    print("-" * 60)
    
    try:
        from config import DEEPSEEK_CONFIG
        
        api_key = DEEPSEEK_CONFIG.get('api_key', '')
        
        if not api_key or api_key == 'your_deepseek_api_key_here':
            print("× API Key未配置")
            print("  请在config.py中填入真实的DeepSeek API Key")
            return False
        
        if not api_key.startswith('sk-'):
            print("× API Key格式错误")
            print("  DeepSeek API Key应该以'sk-'开头")
            return False
        
        print(f"✓ API Key已配置: {api_key[:10]}...{api_key[-4:]}")
        
        # 测试API连接
        print()
        print("测试API连接...")
        
        try:
            import requests
            
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'model': DEEPSEEK_CONFIG.get('model', 'deepseek-chat'),
                'messages': [
                    {'role': 'user', 'content': '测试'}
                ],
                'max_tokens': 10
            }
            
            response = requests.post(
                f"{DEEPSEEK_CONFIG.get('api_base', 'https://api.deepseek.com/v1')}/chat/completions",
                headers=headers,
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                print("✓ API连接成功")
                return True
            else:
                print(f"× API连接失败: {response.status_code}")
                print(f"  错误信息: {response.text}")
                return False
        
        except Exception as e:
            print(f"× API连接测试失败: {e}")
            print("  请检查网络连接和API Key是否正确")
            return False
    
    except ImportError:
        print("× 未找到DEEPSEEK_CONFIG配置")
        return False


def test_email_config():
    """测试邮件配置"""
    print()
    print("-" * 60)
    print("邮件配置测试")
    print("-" * 60)
    
    try:
        from config import EMAIL_CONFIG
        
        smtp_server = EMAIL_CONFIG.get('smtp_server', '')
        smtp_port = EMAIL_CONFIG.get('smtp_port', 0)
        sender_email = EMAIL_CONFIG.get('sender_email', '')
        sender_password = EMAIL_CONFIG.get('sender_password', '')
        receiver_emails = EMAIL_CONFIG.get('receiver_emails', [])
        
        # 检查配置完整性
        issues = []
        
        if not smtp_server or smtp_server == 'smtp.qq.com':
            print("✓ SMTP服务器: smtp.qq.com")
        else:
            print(f"✓ SMTP服务器: {smtp_server}")
        
        if smtp_port == 465:
            print("✓ SMTP端口: 465 (SSL)")
        else:
            print(f"⚠  SMTP端口: {smtp_port} (建议使用465)")
        
        if not sender_email or sender_email == 'your_email@qq.com':
            print("× 发件邮箱未配置")
            issues.append("发件邮箱")
        else:
            print(f"✓ 发件邮箱: {sender_email}")
        
        if not sender_password or sender_password == 'your_qq_auth_code':
            print("× 邮箱授权码未配置")
            issues.append("邮箱授权码")
        else:
            print(f"✓ 邮箱授权码: {'*' * len(sender_password)}")
        
        if not receiver_emails or receiver_emails == ['receiver@example.com']:
            print("× 收件邮箱未配置")
            issues.append("收件邮箱")
        else:
            print(f"✓ 收件邮箱: {', '.join(receiver_emails)}")
        
        if issues:
            print()
            print(f"× 配置不完整，缺少: {', '.join(issues)}")
            return False
        
        # 测试SMTP连接
        print()
        print("测试SMTP连接...")
        
        try:
            import smtplib
            
            with smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=10) as server:
                server.login(sender_email, sender_password)
            
            print("✓ SMTP连接成功")
            return True
        
        except Exception as e:
            print(f"× SMTP连接失败: {e}")
            print()
            print("可能的原因:")
            print("1. 邮箱授权码错误（注意：不是QQ密码！）")
            print("2. SMTP服务未开启")
            print("3. 网络连接问题")
            return False
    
    except ImportError:
        print("× 未找到EMAIL_CONFIG配置")
        return False


def test_dependencies():
    """测试依赖包"""
    print()
    print("-" * 60)
    print("依赖包测试")
    print("-" * 60)
    
    required_packages = [
        'akshare',
        'pandas',
        'numpy',
        'requests'
    ]
    
    all_installed = True
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"× {package} 未安装")
            all_installed = False
    
    if not all_installed:
        print()
        print("请安装缺失的依赖:")
        print("pip install -r requirements.txt")
        return False
    
    return True


def main():
    """主函数"""
    print()
    print("🔍 开始配置测试...")
    print()
    
    results = []
    
    # 1. 测试配置文件
    if not test_config_file():
        print()
        print("=" * 60)
        print("❌ 测试失败: 配置文件不存在")
        print("=" * 60)
        sys.exit(1)
    
    # 2. 测试依赖包
    results.append(("依赖包", test_dependencies()))
    
    # 3. 测试DeepSeek配置
    results.append(("DeepSeek API", test_deepseek_config()))
    
    # 4. 测试邮件配置
    results.append(("邮件配置", test_email_config()))
    
    # 总结
    print()
    print("=" * 60)
    print("测试总结")
    print("=" * 60)
    print()
    
    all_passed = True
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{name}: {status}")
        if not passed:
            all_passed = False
    
    print()
    print("=" * 60)
    
    if all_passed:
        print("✅ 所有测试通过！")
        print()
        print("你可以开始使用系统了:")
        print("- 运行完整分析: python3 daily_email_sender.py")
        print("- 部署到GitHub: ./deploy_to_github.sh")
    else:
        print("❌ 部分测试失败")
        print()
        print("请根据上述提示修复配置问题")
    
    print("=" * 60)
    print()
    
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
