# tasks/inventory_analysis_task.py
from typing import Optional
from crewai import Task
from datetime import datetime  # 1. 导入 datetime 模块
from agents.inventory_agent import inventory_analyst

# 将你提供的模板定义为 Python 字符串，用于 expected_output
INVENTORY_REPORT_TEMPLATE = """
# {commodity_name} 库存分析报告

## 分析时间
{analysis_time}

## 一、核心观点
[在此处填写你的核心判断，1-2句话]

## 二、库存总览
- **总量与变化**: [社会库存总量及周度/月度变化]
- **主要集散地**: [列出库存量排名靠前的仓库或港口]
- **数据来源**: [用户提供 / 网络搜索]

## 三、产业链库存动态
- **上游情况**: [原料库存状态]
- **中游情况**: [贸易商库存及心态]
- **下游情况**: [加工企业原料库存水平]
- **库存传导**: [描述库存如何在上中下游间流动]

## 四、贸易、物流与价差
- **进出口影响**: [进口到港/出口情况对库存的影响]
- **物流状况**: [运输成本、瓶颈等]
- **地域价差**: [不同地区价差及其反映的供需情况]

## 五、市场展望与策略
- **库存趋势预判**: [对未来库存变化的判断]
- **价格影响评估**: [库存变化对价格的影响]
- **投资机会提示**: [基于分析发现的潜在机会]
- **风险提示**: [需要关注的风险因素]
"""

# 2. 将 description 也定义为模板字符串
DESCRIPTION_TEMPLATE = (
    "对商品 {commodity_name} 进行全面的库存分析。"
    "请严格按照以下步骤执行：\n\n"
    "1. **获取核心数据**：使用 'Data Fetching Tool' 获取该产品的库存数据。\n"
    "   - **操作**: 调用工具获取 {inventory_type} 库存数据。\n"
    "     - endpoint: '/data/inventory'\n"
    "     - params_json: '{{\"product\": \"{commodity_name}\", \"inventory_type\": \"{inventory_type}\", \"start_date\": \"{start_date}\", \"end_date\": \"{end_date}\"}}'\n"
    "     - model_name: 'InventoryDataPoint'\n\n"
    "2. **补充市场信息**：使用 'Zhipu Web Search' 搜索关于 '{commodity_name} 的最新贸易流、物流瓶颈和地域价差'。\n"
    "   - 使用 Quark 引擎（search_pro_quark）以获取最新新闻和市场信息。\n\n"
    "3. **撰写分析报告**：将以上所有信息整合，并严格遵循给定的 Markdown 模板格式，撰写最终的库存分析报告。\n"
    "   - 模板中的占位符需要被替换为实际值。"
)


def create_inventory_analysis_task(
    commodity_name: str,
    start_date: str = "2022-11-01",  # 默认值
    end_date: str = "2025-11-30",    # 默认值
    report_template: Optional[str] = None,
    async_execution: bool = False,
    inventory_type: str = "social"  # 默认库存类型
) -> Task:
    """
    动态生成一个库存分析任务。
    """
    # 3. 在函数内部，生成缺失的 analysis_time
    analysis_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 4. 选择最终使用的模板
    final_template = report_template or INVENTORY_REPORT_TEMPLATE

    # 5. 格式化 description 和 expected_output，确保所有占位符都被替换
    final_description = DESCRIPTION_TEMPLATE.format(
        commodity_name=commodity_name,
        inventory_type=inventory_type,
        start_date=start_date,
        end_date=end_date
    )

    final_expected_output = final_template.format(
        commodity_name=commodity_name,
        inventory_type=inventory_type,
        start_date=start_date,
        end_date=end_date,
        analysis_time=analysis_time  # <-- 关键：添加缺失的参数
    )

    # 6. 创建并返回 Task 实例，传入格式化后的字符串
    return Task(
        description=final_description,
        expected_output=final_expected_output,
        agent=inventory_analyst,
        async_execution=async_execution
    )

