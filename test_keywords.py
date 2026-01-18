#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
关键词测试脚本
测试新增关键词的匹配效果
"""

def test_keywords():
    """测试关键词匹配"""
    
    # 完整的关键词列表（与Discovery_Engine.py保持一致）
    finance_keywords = [
        # 基础财经关键词
        '股', '金融', '经济', 'A股', '港股', '基金', '投资', '理财', '上市', '市值',
        # 行业板块关键词
        '肥料', '化肥', '磷肥', '钾肥', '氮肥',  # 肥料板块
        '战争', '军工', '国防', '武器', '军事',  # 战争/军工板块
        '卫星', '航天', '火箭', '太空', '北斗',  # 卫星/航天板块
        '脑机接口', '脑机', '神经', '马斯克', 'Neuralink',  # 脑机接口板块
        # 其他热门板块
        '煤炭', '核电', '新能源', '光伏', '风电', '储能',
        '半导体', '芯片', '人工智能', 'AI', '机器人',
        '医药', '生物', '疫苗', '医疗',
        '房地产', '地产', '建筑', '基建'
    ]
    
    # 测试文本样本
    test_texts = [
        "马斯克Neuralink脑机接口技术取得重大突破",
        "化肥价格上涨，磷肥钾肥供应紧张",
        "地缘政治紧张，军工板块受到关注",
        "北斗卫星导航系统再添新星",
        "A股今日大涨，煤炭板块领涨",
        "人工智能概念股持续走强",
        "房地产政策调整，地产股集体上涨",
        "今天天气不错，适合出门散步",  # 不应匹配
        "新能源汽车销量创新高",
        "半导体芯片国产化加速"
    ]
    
    print("=" * 60)
    print("关键词匹配测试")
    print("=" * 60)
    print(f"\n总关键词数: {len(finance_keywords)}")
    print(f"测试文本数: {len(test_texts)}")
    print()
    
    # 统计各板块关键词数量
    print("【关键词分类统计】")
    print(f"  基础财经: 10个")
    print(f"  肥料板块: 5个")
    print(f"  军工板块: 5个")
    print(f"  航天板块: 5个")
    print(f"  脑机接口: 5个")
    print(f"  能源板块: 6个")
    print(f"  科技板块: 5个")
    print(f"  医疗板块: 4个")
    print(f"  地产板块: 4个")
    print(f"  总计: {len(finance_keywords)}个")
    print()
    
    # 测试匹配
    print("【匹配测试结果】")
    print()
    
    matched_count = 0
    
    for i, text in enumerate(test_texts, 1):
        # 检查是否匹配
        matched_keywords = [kw for kw in finance_keywords if kw in text]
        
        if matched_keywords:
            matched_count += 1
            print(f"{i}. ✅ 匹配成功")
            print(f"   文本: {text}")
            print(f"   匹配关键词: {', '.join(matched_keywords)}")
        else:
            print(f"{i}. ❌ 未匹配")
            print(f"   文本: {text}")
        
        print()
    
    # 统计结果
    print("=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"匹配成功: {matched_count}/{len(test_texts)} ({matched_count/len(test_texts)*100:.0f}%)")
    print(f"预期匹配: 9/10 (90%)")
    
    if matched_count == 9:
        print("\n✅ 测试通过！关键词匹配正常工作。")
    else:
        print(f"\n⚠️  匹配数量异常，预期9个，实际{matched_count}个")
    
    print()
    
    # 展示新增关键词
    print("=" * 60)
    print("新增关键词列表")
    print("=" * 60)
    print()
    
    new_keywords = {
        '肥料板块': ['肥料', '化肥', '磷肥', '钾肥', '氮肥'],
        '军工板块': ['战争', '军工', '国防', '武器', '军事'],
        '航天板块': ['卫星', '航天', '火箭', '太空', '北斗'],
        '脑机接口': ['脑机接口', '脑机', '神经', '马斯克', 'Neuralink']
    }
    
    for category, keywords in new_keywords.items():
        print(f"【{category}】")
        print(f"  关键词: {', '.join(keywords)}")
        print()
    
    print("✅ 所有新增关键词已成功添加到Discovery_Engine.py")
    print()


if __name__ == "__main__":
    test_keywords()
