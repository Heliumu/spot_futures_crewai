# tasks/demand_forecasting_task.py
from crewai import Task
from agents.demand_forecasting_analyst import demand_forecasting_analyst
from typing import Optional

# 1. 定义结构化的报告模板
DEMAND_FORECASTING_REPORT_TEMPLATE = """
# {commodity_name} 未来需求预测报告

## 数据来源与方法声明
本报告基于历史数据及权威机构的宏观、行业前瞻性预测。预测模型采用多因素情景分析法，旨在提供未来 {forecast_horizon} 的需求展望。

---

## 一、预测摘要

| 情景 | 未来1季度需求预测 | 未来2季度需求预测 | 未来3季度需求预测 |
| :--- | :--- | :--- | :--- |
| **基准情景** | [预测值] | [预测值] | [预测值] |
| **乐观情景** | [预测值] | [预测值] | [预测值] |
| **悲观情景** | [预测值] | [预测值] | [预测值] |

---

## 二、模型逻辑与核心假设

- **预测框架**:
    - [描述你使用的预测模型，例如：基于下游行业开工率和PMI的多元回归模型，或基于领先指标的加权评分模型。]

- **核心假设**:
    - [列出本次预测所依赖的最重要的3-5个假设，例如：假设未来GDP增速为X%，假设房地产市场投资增速为Y%，假设无重大黑天鹅事件。]

---

## 三、关键驱动变量展望

- **宏观经济指标**:
    - [分析GDP、PMI等关键宏观指标的未来预期，并说明其对需求的潜在影响。]

- **行业特定指标**:
    - [分析关键下游行业（如汽车、新能源、地产）的未来景气度预测，并说明其对需求的拉动或抑制作用。]

---

## 四、预测结果与不确定性

- **预测走势图**:
    - [描述历史需求与未来三种情景下预测需求的走势图，并解释预测区间的含义。]

- **核心风险与不确定性**:
    - [列出可能对预测结果产生重大影响的负面和正面风险，例如：地缘政治冲突导致供应链中断、超预期的财政刺激政策等。]

---

## 五、结论

[用一段话总结对未来 {forecast_horizon} {commodity_name} 需求的核心判断，以及最需要关注的变量和风险点。]
"""

# 2. 创建“任务工厂”函数
def create_demand_forecasting_task(
    commodity_name: str,
    forecast_horizon: str = "3个季度",
    report_template: Optional[str] = None,
    async_execution: bool = False
) -> Task:
    """
    动态生成一个商品未来需求预测任务。

    Args:
        commodity_name (str): 要预测的商品名称，例如 "铜"。
        forecast_horizon (str): 预测的时间跨度，例如 "2个季度"。
        report_template (Optional[str]): 可选的自定义报告模板。
        async_execution (bool): 是否异步执行任务。

    Returns:
        Task: 一个配置好的 CrewAI Task 实例。
    """
    
    final_template = report_template or DEMAND_FORECASTING_REPORT_TEMPLATE

    description = (
        f"你是一位大宗商品量化预测分析师，专注于构建前瞻性预测模型。"
        f"你的任务是针对【{commodity_name}】，生成一份未来 {forecast_horizon} 的需求预测报告。"
        "请严格按照以下步骤执行："
        "1. **获取历史与前瞻性数据**：使用 'Data Fetching Tool' 获取所需数据。"
        "   - **历史数据**: 获取过去5-10年的表观需求及关键驱动变量（如PMI、下游产量）的历史月度数据，用于模型训练。"
        "   - **前瞻性数据**: 获取权威机构（如央行、IMF、券商）对未来GDP、PMI、行业投资等的预测值。"
        "   - (提示：你可能需要多次调用工具以获取不同类型的数据)"
        "2. **构建预测模型**："
        "   a) **确定框架**：基于你对 {commodity_name} 的理解，选择合适的预测模型（如回归、时间序列等）。"
        "   b) **情景分析**：基于不同的核心假设（乐观、基准、悲观），生成三套未来需求的预测值。"
        "3. **撰写报告**：将你的模型逻辑、假设、预测结果和风险分析，严格遵循给定的 Markdown 模板格式，撰写最终的专业报告。"
        "   - 确保模板中的占位符被正确替换。"
        "   - 在摘要中清晰地用表格展示三种情景的预测值。"
    )

    expected_output = final_template.format(
        commodity_name=commodity_name,
        forecast_horizon=forecast_horizon
    )

    return Task(
        description=description,
        expected_output=expected_output,
        agent=demand_forecasting_analyst,
        async_execution=async_execution
    )
