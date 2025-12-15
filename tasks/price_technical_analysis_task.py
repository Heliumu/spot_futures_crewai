from typing import Optional
from crewai import Task
from agents.price_technical_agent import price_technical_analyst

# 定义报告模板
PRICE_TECHNICAL_REPORT_TEMPLATE = """
# {commodity_name} 期货价格技术分析与展望报告 ({start_date} 至 {end_date})

## 数据来源与方法声明
本报告数据来源于期货交易所的公开行情数据及主流财经媒体，分析时间范围为 {start_date} 至 {end_date}。分析方法结合了经典技术分析理论与市场情绪解读。

---

## 一、历史价格回顾 ({start_date} - {end_date})

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

# 定义任务描述模板
DESCRIPTION_TEMPLATE = (
    "对商品 '{commodity_name}' 进行全面的期货价格技术分析。请严格按照以下步骤执行：\n\n"
    
    "1. 获取历史K线数据：使用 'Data Fetching Tool' 获取从 '{start_date}' 到 '{end_date}' 的期货历史数据。\n"
    "   - ***重要***：调用工具时，你的输入必须是一个单一的 JSON 字典，格式如下：\n"
    "   {{\n"  
    "     \"endpoint\": \"/data/futures_history\",\n"
    "     \"params_json\": '{{\"product\": \"{commodity_name}\", \"start_date\": \"{start_date}\", \"end_date\": \"{end_date}\"}}',\n"  # 修改点：内部的 { 和 } 也需要转义
    "     \"model_name\": \"FuturesHistoryDataPoint\"\n"
    "   }}\n\n"  

    "2. 获取当前市场快照：再次使用 'Data Fetching Tool' 获取该商品最新的市场数据。\n"
    "   - ***重要***：调用工具时，你的输入必须是一个单一的 JSON 字典，格式如下：\n"
    "   {{\n"  
    "     \"endpoint\": \"/data/futures_snapshot\",\n"
    "     \"params_json\": '{{\"product\": \"{commodity_name}\"}}',\n"  
    "     \"model_name\": \"FuturesSnapshotDataPoint\"\n"
    "   }}\n\n"  

    "3. 搜索市场信息：使用 'Zhipu Web Search' 搜索以下关键信息，以补充你的分析：\n"
    "   a) 搜索关键词：'{commodity_name} 期货 最新新闻 市场情绪'，使用 Quark 引擎。\n"
    "   b) 搜索关键词：'{commodity_name} USDA 月度报告' 或相关行业最新报告，使用 Quark 引擎。\n\n"

    "4. 撰写分析报告：将以上所有信息整合，并严格遵循给定的 Markdown 模板格式，撰写最终的技术分析报告。\n"
    "   - 模板中的占位符需要被替换为实际值（如商品名、日期等）。\n"
    "   - 报告的每个部分都必须基于你获取的数据和搜索到的信息进行填充。\n"
    "   - 至关重要：在报告的“未来展望”部分，必须明确给出“看涨”、“看跌”或“震荡”的交易观点，并列出至少三条核心依据。"
)

def create_price_technical_analysis_task(
    commodity_name: str,
    start_date: str = "2022-11-01",
    end_date: str = "2025-11-30",
    report_template: Optional[str] = None,
    async_execution: bool = False
) -> Task:
    """
    动态生成一个期货价格技术分析任务。
    """
    # 格式化任务描述
    final_description = DESCRIPTION_TEMPLATE.format(
    commodity_name=commodity_name,
    start_date=start_date,
    end_date=end_date
    )

    # 选择并格式化输出模板
    final_template = report_template or PRICE_TECHNICAL_REPORT_TEMPLATE
    final_expected_output = final_template.format(
        commodity_name=commodity_name,
        start_date=start_date,
        end_date=end_date
    )

    # 创建并返回 Task 实例
    return Task(
        description=final_description,
        expected_output=final_expected_output,
        agent=price_technical_analyst,
        async_execution=async_execution
    )