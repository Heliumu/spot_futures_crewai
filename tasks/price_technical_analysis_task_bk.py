# tasks/price_technical_analysis_task.py

from typing import Optional
from crewai import Task
from agents.price_technical_agent import price_technical_analyst

# 定义严格的 Markdown 输出模板
PRICE_TECHNICAL_REPORT_TEMPLATE = """
# {commodity_name} 期货价格技术分析与展望报告

## 数据来源与方法声明
本报告数据来源于期货交易所的公开行情数据及主流财经媒体，时间范围为2022年11月至2025年11月。分析方法结合了经典技术分析理论与市场情绪解读。

---

## 一、历史价格回顾 (2022.11 - 2025.11)

- **主要运行阶段**: [描述主力合约价格的主要运行阶段，如单边上涨、宽幅震荡、区间波动等，并注明大致时间区间。]
- **历史关键高低点**: [标记出历史关键高低点及其价格和时间。]

---

## 二、当前市场状况 (近1个月)

- **价格与量仓分析**: [分析当前主力合约的价格位置、成交量、持仓量的变化及其含义。]
- **技术形态与指标**:
    - **支撑/阻力位**: [指出当前价格附近的关键支撑和阻力位。]
    - **均线系统**: [描述当前价格与短期、长期均线（如MA5, MA20, MA60）的关系。]
    - **技术指标**: [分析布林带、MACD、RSI等常用技术指标的当前状态。]
- **市场情绪解读**: [解读近期重大行业报告（如USDA报告）或新闻事件对市场情绪的影响。]

---

## 三、未来展望

- **价格运行区间预测**: [基于以上分析，预测未来一个季度的价格主要运行区间（上限和下限）。]
- **市场驱动因素与风险**: [判断未来可能驱动价格变化的核心因素和潜在的风险点。]

### **交易观点**

**观点**: **[看涨 / 看跌 / 震荡]**

**核心依据**:
1. [列出支持你观点的核心依据1，如技术形态突破]
2. [列出支持你观点的核心依据2，如宏观环境利好]
3. [列出支持你观点的核心依据3，如供需基本面紧张]
"""

def create_price_technical_analysis_task(
    commodity_name: str,
    start_date: str = "2022-11-01",  # 默认值
    end_date: str = "2025-11-30",    # 默认值
    report_template: Optional[str] = None,
    async_execution: bool = False
) -> Task:
    """
    动态生成一个期货价格技术分析任务。

    Args:
        commodity_name (str): 要分析的商品名称，例如 "螺纹钢"。
        start_date (str): 历史数据的开始日期，格式 'YYYY-MM-DD'。
        end_date (str): 历史数据的结束日期，格式 'YYYY-MM-DD'。
        report_template (Optional[str]): 可选的自定义报告模板。如果为 None，则使用默认模板。
        async_execution (bool): 是否异步执行任务。

    Returns:
        Task: 一个配置好的 CrewAI Task 实例。
    """
    
    # 如果没有提供自定义模板，则使用默认模板
    final_template = report_template or PRICE_TECHNICAL_REPORT_TEMPLATE

    # 使用 f-string 动态构建任务描述
    description = (
        f"对商品 {commodity_name} 进行全面的期货价格技术分析。"
        "请严格按照以下步骤执行："
        
        f"1. **获取历史K线数据**：使用 'Data Fetching Tool' 获取该商品自{start_date}以来的期货历史数据。"
        "   - endpoint: '/data/futures_history'"
        f"   - params_json: '{{\"product\": \"{commodity_name}\", \"start_date\": \"{start_date}\", \"end_date\": \"{end_date}\"}}'"
        "   - model_name: 'FuturesHistoryDataPoint'"

        f"2. **获取当前市场快照**：使用 'Data Fetching Tool' 获取该商品最新的市场数据。"
        "   - endpoint: '/data/futures_snapshot'"
        f"   - params_json: '{{\"product\": \"{commodity_name}\"}}'"
        "   - model_name: 'FuturesSnapshotDataPoint'"

        f"3. **搜索市场信息**：使用 'Zhipu Web Search' 搜索以下关键信息，以补充分析："
        f"   - a) 搜索 '{commodity_name} 期货 最新新闻 市场情绪'，使用 Quark 引擎。"
        f"   - b) 搜索 '{commodity_name} USDA 月度报告' 或相关行业最新报告，使用 Quark 引擎。"

        "4. **撰写分析报告**：将以上所有信息整合，并严格遵循给定的 Markdown 模板格式，撰写最终的技术分析报告。"
        f"   - 模板中的占位符需要被替换为实际值（如商品名、日期等）。"
        "   - 报告的每个部分都必须基于你获取的数据和搜索到的信息进行填充。"
        "   - **至关重要**：在报告的“未来展望”部分，必须明确给出“看涨”、“看跌”或“震荡”的交易观点，并列出至少三条核心依据。"
    )

    # 使用 f-string 格式化最终输出模板，确保占位符被替换
    expected_output = final_template.format(
        commodity_name=commodity_name,
        start_date=start_date,
        end_date=end_date
    )

    return Task(
        description=description,
        expected_output=expected_output,
        agent=price_technical_analyst,
        async_execution=async_execution
    )
