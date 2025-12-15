# tasks/supply_demand_analysis_task.py

from crewai import Task
from agents.supply_demand_agent import supply_demand_analyst
from typing import Optional

# ... (SUPPLY_DEMAND_REPORT_TEMPLATE 保持不变) ...
SUPPLY_DEMAND_REPORT_TEMPLATE = """
# {commodity_name} 供需基本面分析报告

## 一、供应端分析

### 1. 国内产量与进口量
- **国内产量趋势 ({start_date} - {end_date})**: [在此处用文字描述近3-5年的变化趋势，如稳步增长、周期性波动等]
- **进口量趋势 ({start_date} - {end_date})**: [在此处用文字描述进口量的变化]
- **主要来源国及占比**: [列出主要进口来源国及其近年来的占比变化]
- **数据来源**: [明确标注数据来源，如：海关总署、国家统计局]

### 2. 全球市场动态
- **主要生产国情况**: [分析全球主要生产国的产量、库存和出口政策变化]
- **全球供需格局**: [对全球整体供需状况进行简要描述]

## 二、需求端分析

### 1. 国内表观消费量
- **消费量趋势 ({start_date} - {end_date})**: [描述国内表观消费量的变化趋势]
- **下游主要行业需求**: [分析下游主要行业（如饲料、养殖）的需求变化和驱动因素]
- **数据来源**: [明确标注数据来源，如：国家统计局、行业协会]

### 2. 长期影响因素
- **替代品影响**: [分析是否有替代品在冲击市场需求]
- **技术变革**: [分析技术变革（如低蛋白日粮）对长期需求的潜在影响]

## 三、库存状况与市场定性

### 1. 库存水平分析
- **港口/工厂/下游库存**: [分析各环节库存的近3-5年同期水平]
- **库存消费比**: [根据数据计算并分析库存消费比的变化]
- **数据来源**: [明确标注数据来源，如：Wind、我的钢铁网、行业协会]

### 2. 市场基本面定性判断
**最终结论**: [在此处从“供需宽松”、“供需紧张”、“供需基本平衡”三选一，并给出简要理由]
"""

def create_supply_demand_analysis_task(
    commodity_name: str,
    start_date: str = "2020-11-01",
    end_date: str = "2025-11-30",
    report_template: Optional[str] = None,
    async_execution: bool = False
) -> Task:
    """动态生成供需基本面分析任务。"""
    final_template = report_template or SUPPLY_DEMAND_REPORT_TEMPLATE
    
    description = (
        f"对商品 {commodity_name} 进行全面的供需基本面分析。"
        "请严格按照以下步骤执行："
        f"1. **获取核心数据**：使用 'Data Fetching Tool' 获取该商品从 {start_date} 到 {end_date} 的供需数据。"
        "   - **操作 1 (国内产量)**: "
        f"     - endpoint: '/data/supply_demand'"
        f"     - params_json: '{{\"product\": \"{commodity_name}\", \"category\": \"Supply\", \"metric\": \"Domestic_Production\", \"start_date\": \"{start_date}\", \"end_date\": \"{end_date}\"}}'"
        "     - model_name: 'SupplyDemandDataPoint'"

        "   - **操作 2 (进口量)**: "
        f"     - endpoint: '/data/supply_demand'"
        f"     - params_json: '{{\"product\": \"{commodity_name}\", \"category\": \"Trade\", \"metric\": \"Import_Volume\", \"start_date\": \"{start_date}\", \"end_date\": \"{end_date}\"}}'"
        "     - model_name: 'SupplyDemandDataPoint'"

        "2. **搜索补充信息**：使用 'Zhipu Web Search' 搜索以下关键信息："
        f"   - a) 搜索 '全球{commodity_name}主产国产量及出口政策'，使用 Quark 引擎。"
        f"   - b) 搜索 '{commodity_name}下游行业需求变化及技术变革'，使用 Quark 引擎。"
        f"   - c) 搜索 'USDA报告 {commodity_name}' 或 '中国{commodity_name}行业协会数据'。"
        
        "3. **撰写分析报告**：将以上所有信息整合，并严格遵循给定的 Markdown 模板格式，撰写最终的供需分析报告。"
        "   - **至关重要**：在报告的最后，必须明确给出“供需宽松”、“供需紧张”或“供需基本平衡”的最终定性判断。"
    )

    expected_output = final_template.format(
        commodity_name=commodity_name,
        start_date=start_date,
        end_date=end_date
    )

    return Task(
        description=description,
        expected_output=expected_output,
        agent=supply_demand_analyst,
        async_execution=async_execution
    )
