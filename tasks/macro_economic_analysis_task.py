# tasks/macro_economic_analysis_task.py

from crewai import Task
from agents.macro_economic_agent import macro_economic_analyst
from typing import Optional

# ... (MACRO_REPORT_TEMPLATE 保持不变) ...
MACRO_REPORT_TEMPLATE = """
# {commodity_name} 宏观经济因素分析报告

## 数据来源与方法声明
本报告数据来源于公开的央行报告、政府统计局、海关总署及国际贸易组织等，时间范围为{start_date}至{end_date}。分析方法结合了时间序列趋势分析与定性政策评估。

---

## 一、汇率与通胀

### 1. 汇率走势与影响
- **主要货币对（如人民币/美元）近3-5年走势**: [在此处描述关键趋势和重要点位]
- **对进口成本的影响评估**: [分析汇率变动对{commodity_name}进口成本的具体影响]
    - 影响评估: **[正面 / 负面 / 中性]**
    - 理由: [简要说明]

### 2. 全球通胀趋势
- **主要经济体（美国、中国）通胀率趋势**: [描述CPI、PPI等关键通胀指标的变化]
- **对商品价格的系统性影响**: [分析高通胀或通缩环境对大宗商品价格的普遍影响]
    - 影响评估: **[正面 / 负面 / 中性]**
    - 理由: [简要说明]

---

## 二、贸易与产业政策

### 1. 重大贸易政策
- **近3-5年关税、进出口配额、贸易协议梳理**: [列出关键政策及其变化]
    - 影响评估: **[正面 / 负面 / 中性]**
    - 理由: [简要说明]

### 2. 主要国家产业政策
- **主要出口国（如巴西、美国）政策**: [分析出口税、补贴等政策]
    - 影响评估: **[正面 / 负面 / 中性]**
    - 理由: [简要说明]
- **主要进口国（如中国）政策**: [分析储备投放、进口补贴等政策]
    - 影响评估: **[正面 / 负面 / 中性]**
    - 理由: [简要说明]

### 3. 潜在政策风险
- **当前正在讨论或已实施的潜在政策风险**: [列出并分析未来可能影响市场的政策动向]
    - 影响评估: **[正面 / 负面 / 中性]**
    - 理由: [简要说明]

---

## 三、宏观环境总结

**最终结论**: 当前宏观环境对【{commodity_name}】市场整体影响为 **[利好 / 利空 / 中性]**。
[在此处用1-2句话总结核心判断依据]
"""

def create_macro_economic_analysis_task(
    commodity_name: str,
    start_date: str = "2020-11-01",
    end_date: str = "2025-11-30",
    report_template: Optional[str] = None,
    async_execution: bool = False
) -> Task:
    """动态生成宏观经济因素分析任务。"""
    final_template = report_template or MACRO_REPORT_TEMPLATE

    description = (
        f"对商品 {commodity_name} 进行全面的宏观经济因素分析。"
        "请严格按照以下步骤执行："
        f"1. **获取核心数据**：使用 'Data Fetching Tool' 获取从 {start_date} 到 {end_date} 的相关宏观经济数据。"
        "   - **操作 1 (汇率)**: 调用工具获取人民币兑美元汇率。"
        f"     - endpoint: '/data/macro'"
        f"     - params_json: '{{\"indicator\": \"USD_CNY_RATE\", \"country\": \"CN\", \"start_date\": \"{start_date}\", \"end_date\": \"{end_date}\"}}'"
        "     - model_name: 'MacroDataPoint'"
        "   - **操作 2 (通胀)**: 调用工具获取中美两国CPI数据。"
        f"     - endpoint: '/data/macro'"
        f"     - params_json: '{{\"indicator\": \"CPI_YOY\", \"country\": \"US\", \"start_date\": \"{start_date}\", \"end_date\": \"{end_date}\"}}'"
        "     - model_name: 'MacroDataPoint'"
        "2. **搜索补充信息**：使用 'Zhipu Web Search' 搜索以下关键信息："
        f"   - a) 搜索 '人民币兑美元汇率近五年走势及关键点位'，使用 Quark 引擎。"
        f"   - b) 搜索 '美国中国CPI PPI通胀数据'，使用 Quark 引擎。"
        f"   - c) 搜索 '{commodity_name} 关税 贸易政策'，使用 Quark 引擎。"
        f"   - d) 搜索 '巴西 美国 {commodity_name} 出口政策'，使用 Quark 引擎。"
        f"   - e) 搜索 '中国 {commodity_name} 储备投放 补贴政策'，使用 Quark 引擎。"
        "3. **撰写分析报告**：将以上所有信息整合，并严格遵循给定的 Markdown 模板格式，撰写最终的宏观分析报告。"
        "   - **至关重要**：报告开头必须包含“数据来源与方法声明”，结尾必须给出“利好/利空/中性”的最终结论。"
    )

    expected_output = final_template.format(
        commodity_name=commodity_name,
        start_date=start_date,
        end_date=end_date
    )

    return Task(
        description=description,
        expected_output=expected_output,
        agent=macro_economic_analyst,
        async_execution=async_execution
    )
