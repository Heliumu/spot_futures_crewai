# tasks/apparent_demand_analysis_task.py
from crewai import Task
from agents.apparent_demand_analyst import apparent_demand_analyst
from typing import Optional

# 1. 定义结构化的报告模板
APPARENT_DEMAND_ANALYSIS_REPORT_TEMPLATE = """
# {commodity_name} 表观需求历史分析报告

## 数据来源与方法声明
本报告数据来源于专业数据提供商（如Wind、iFind、钢联、卓创等）及国家统计局、海关总署等官方机构，时间范围为 {start_date} 至 {end_date}。分析方法聚焦于历史统计、季节性规律识别和驱动因素量化。

---

## 一、核心指标摘要

| 统计维度 | 数值 |
| :--- | :--- |
| 过去1年平均月度需求 | [计算并填写] |
| 过去3年平均月度需求 | [计算并填写] |
| 过去5年平均月度需求 | [计算并填写] |
| 历史年均复合增长率(CAGR) | [计算并填写] |
| 历史最高月度需求 | [填写数值和日期] |
| 历史最低月度需求 | [填写数值和日期] |

---

## 二、历史表观需求走势与趋势分析

- **长期趋势**:
    - [描述过去5年表观需求的整体趋势是增长、停滞还是下降，并解释其背后的宏观经济或行业背景。]

- **同比/环比波动**:
    - [分析需求的波动性，找出增长最快和最慢的时期，并与同期发生的重大事件（如政策变动、疫情）进行关联。]

---

## 三、季节性规律分析

- **季节性特征**:
    - [描述 {commodity_name} 需求在一年中的典型季节性模式。例如，哪几个月是传统旺季，哪几个月是淡季。]

- **季节性成因**:
    - [深入解释造成这种季节性的原因，例如：下游行业的生产周期、气候因素、节假日效应等。]

---

## 四、驱动因素深度解读

- **关键下游行业关联**:
    - [列出影响 {commodity_name} 需求的1-2个最关键的下游行业（如：螺纹钢-房地产，铜-新能源）。]
    - [分析表观需求与这些下游行业数据（如：新开工面积、汽车产量）的相关性，并解释其逻辑链条。]

---

## 五、结论

[用一段话总结 {commodity_name} 在过去几年的核心需求特征、主要驱动力以及最重要的季节性规律。]
"""

# 2. 创建“任务工厂”函数
def create_apparent_demand_analysis_task(
    commodity_name: str,
    start_date: str = "2020-01-01",
    end_date: str = "2025-12-12",
    report_template: Optional[str] = None,
    async_execution: bool = False
) -> Task:
    """
    动态生成一个商品表观需求历史分析任务。

    Args:
        commodity_name (str): 要分析的商品名称，例如 "螺纹钢"。
        start_date (str): 历史数据的开始日期，格式 'YYYY-MM-DD'。
        end_date (str): 历史数据的结束日期，格式 'YYYY-MM-DD'。
        report_template (Optional[str]): 可选的自定义报告模板。
        async_execution (bool): 是否异步执行任务。

    Returns:
        Task: 一个配置好的 CrewAI Task 实例。
    """
    
    final_template = report_template or APPARENT_DEMAND_ANALYSIS_REPORT_TEMPLATE

    description = (
        f"你是一位大宗商品市场研究员，专注于历史数据分析。"
        f"你的任务是针对【{commodity_name}】，生成一份详细的表观需求历史分析报告。"
        "请严格按照以下步骤执行："
        f"1. **获取供需数据**：使用 'Data Fetching Tool' 获取该产品从 {start_date} 到 {end_date} 的月度产量、进口量和出口量数据。"
        "   - endpoint: '/data/supply_demand' (假设的端点，请根据实际情况调整)"
        f"   - params_json: '{{\"product\": \"{commodity_name}\", \"data_type\": [\"production\", \"import\", \"export\"], \"start_date\": \"{start_date}\", \"end_date\": \"{end_date}\"}}'"
        "   - model_name: 'SupplyDemandDataPoint'"
        "2. **获取下游数据**：使用 'Data Fetching Tool' 获取该产品关键下游行业的月度数据（如房地产新开工面积、汽车产量等）。"
        "   - endpoint: '/data/downstream' (假设的端点)"
        f"   - params_json: '{{\"product\": \"{commodity_name}\", \"start_date\": \"{start_date}\", \"end_date\": \"{end_date}\"}}'"
        "3. **计算与分析**："
        "   a) **计算表观需求**：使用公式 `表观需求 = 产量 + 进口量 - 出口量` 计算出月度时间序列。"
        "   b) **执行分析**：基于所有获取的数据，进行趋势、季节性、同比/环比和驱动因素分析。"
        "4. **撰写报告**：将你的所有分析结果，严格遵循给定的 Markdown 模板格式，撰写最终的专业报告。"
        "   - 确保模板中的占位符被正确替换。"
        "   - 关键数据（如CAGR、最高值）请加粗显示。"
    )

    expected_output = final_template.format(
        commodity_name=commodity_name,
        start_date=start_date,
        end_date=end_date
    )

    return Task(
        description=description,
        expected_output=expected_output,
        agent=apparent_demand_analyst,
        async_execution=async_execution
    )

