# 🏛️ 政客交易追踪模块集成说明

## 📋 集成步骤

### 1. 在每日简报中添加政客交易追踪

修改 `daily_email_sender.py`，在运行分析模块部分添加：

```python
# 5. 政客交易追踪
print("\n【5/5】政客交易追踪...")
try:
    result = subprocess.run(
        ['python3', 'politician_trade_tracker.py'],
        capture_output=True,
        text=True,
        timeout=300
    )
    results['politician_tracker'] = result.returncode == 0
    print("✓ 完成" if results['politician_tracker'] else "× 失败")
except Exception as e:
    print(f"× 失败: {e}")
    results['politician_tracker'] = False
```

### 2. 在综合简报中添加政客交易板块

在生成综合简报的函数中添加：

```python
# 5. 政客交易追踪
report_lines.append("## 5. 🏛️ 权力资金动态")
report_lines.append("")

politician_report = self._find_latest_file('权力资金动态_*.md')
if politician_report:
    try:
        with open(politician_report, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # 提取高置信度信号
            import re
            signals = re.findall(r'###\s*\d+\.\s*(.+?)\s*-\s*(.+?)\n', content)
            
            if signals:
                report_lines.append(f"**监控到 {len(signals)} 个高置信度信号**:")
                report_lines.append("")
                
                for ticker, politician in signals[:3]:  # 只显示前3个
                    report_lines.append(f"- {ticker.strip()}: {politician.strip()}")
                
                report_lines.append("")
                report_lines.append("详细分析请查看附件《权力资金动态报告》")
    except Exception as e:
        report_lines.append(f"⚠️  数据读取失败: {e}")
else:
    report_lines.append("⚠️  未找到政客交易数据")

report_lines.append("")
report_lines.append("---")
report_lines.append("")
```

### 3. 添加到邮件附件

在发送邮件函数中添加：

```python
# 添加政客交易报告
politician_report = self._find_latest_file('权力资金动态_*.md')
if politician_report:
    self._attach_file(msg, politician_report)
    print(f"  ✓ 添加附件: 权力资金动态报告")
```

---

## 🚀 快速集成脚本

创建 `run_with_politician_tracker.py`:

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
包含政客交易追踪的完整分析脚本
"""

import subprocess
import sys
from datetime import datetime


def run_all_modules():
    """运行所有分析模块"""
    print("=" * 60)
    print("运行完整分析（包含政客交易追踪）")
    print("=" * 60)
    print(f"\n开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    modules = [
        ('黄金股票筛选', 'gold_stock_screener.py', 300),
        ('AI量化选股', 'Quant_Picker.py', 600),
        ('微博情绪分析', 'weibo_sentiment_weighted.py', 600),
        ('全网热点发现', 'Discovery_Engine.py', 900),
        ('政客交易追踪', 'politician_trade_tracker.py', 300)
    ]
    
    results = {}
    
    for i, (name, script, timeout) in enumerate(modules, 1):
        print(f"\n【{i}/{len(modules)}】{name}...")
        
        try:
            result = subprocess.run(
                ['python3', script],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            success = result.returncode == 0
            results[name] = success
            
            print("✓ 完成" if success else "× 失败")
            
            if not success and result.stderr:
                print(f"  错误: {result.stderr[:200]}")
        
        except subprocess.TimeoutExpired:
            print(f"× 超时（>{timeout}秒）")
            results[name] = False
        
        except Exception as e:
            print(f"× 失败: {e}")
            results[name] = False
    
    # 总结
    print("\n" + "=" * 60)
    print("执行总结")
    print("=" * 60)
    
    success_count = sum(1 for v in results.values() if v)
    total_count = len(results)
    
    for name, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {name}")
    
    print(f"\n成功: {success_count}/{total_count}")
    print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return success_count == total_count


if __name__ == "__main__":
    success = run_all_modules()
    sys.exit(0 if success else 1)
```

---

## 📊 简报示例

集成后的每日简报将包含：

```markdown
# 📊 每日投资简报

## 1. 黄金股票筛选 TOP 5
...

## 2. AI量化选股 TOP 3
...

## 3. 微博黄金情绪指数
...

## 4. 全网热点雷达
...

## 5. 🏛️ 权力资金动态

**监控到 3 个高置信度信号**:

- NVDA: Nancy Pelosi (Technology委员会)
- XOM: Joe Manchin (Energy委员会)
- CRWD: Mark Warner (Intelligence委员会)

详细分析请查看附件《权力资金动态报告》

---

## ⚠️ 免责声明
...
```

---

## 🔧 GitHub Actions集成

由于政客交易追踪可以使用API（不需要浏览器），可以在GitHub Actions中运行。

修改 `.github/workflows/daily-report.yml`:

```yaml
- name: 运行政客交易追踪
  continue-on-error: true
  run: |
    python3 politician_trade_tracker.py || echo "政客交易追踪失败，继续执行"
```

**注意**: 如果使用Quiver API，需要在GitHub Secrets中添加：
- `QUIVER_API_KEY`

---

## 📧 邮件附件列表

集成后，邮件将包含以下附件：

1. 每日投资简报.md（综合简报）
2. gold_stocks_analysis_YYYYMMDD.csv（黄金股票数据）
3. AI潜力股推荐_YYYYMMDD.md（量化选股报告）
4. 微博黄金情绪分析_YYYYMMDD.md（情绪分析报告）
5. 全网雷达_YYYYMMDD.md（热点发现报告）
6. **权力资金动态_YYYYMMDD.md（政客交易报告）** ← 新增

---

## 🎯 使用建议

### 本地完整版

运行包含所有模块的完整分析：

```bash
python3 run_with_politician_tracker.py
```

### GitHub Actions版

- 基础模块（黄金股票、AI选股、政客交易）
- 不包含需要浏览器的模块（微博、小红书）

### 混合方案

- GitHub Actions: 每天自动运行基础版
- 本地: 每周运行一次完整版

---

## ⚠️ 注意事项

### 数据源

1. **Quiver API**: 需要付费订阅（$30-100/月）
2. **Unusual Whales**: 需要登录，可能有反爬措施
3. **官方网站**: 免费但需要解析复杂的HTML

### 法律合规

1. 跟随政客交易是合法的（公开信息）
2. 但要注意不要基于内幕信息交易
3. 自己承担投资风险

### 数据延迟

1. 议员交易披露有45天延迟
2. 市场可能已经反应
3. 仅供参考，不构成投资建议

---

## 🧪 测试集成

运行测试脚本：

```bash
# 测试政客交易追踪模块
python3 test_politician_tracker.py

# 测试完整集成
python3 run_with_politician_tracker.py
```

---

## 📚 相关文档

- [POLITICIAN_TRACKER_GUIDE.md](POLITICIAN_TRACKER_GUIDE.md) - 详细使用指南
- [README.md](README.md) - 项目总览
- [GITHUB_DEPLOYMENT_GUIDE.md](GITHUB_DEPLOYMENT_GUIDE.md) - 部署指南

---

**集成完成后，你将拥有一个包含政客交易追踪的完整投资分析系统！** 🎉

---

**最后更新**: 2026年1月15日
