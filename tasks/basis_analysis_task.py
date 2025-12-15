# tasks/basis_analysis_task.py

from crewai import Task
from agents.basis_agent import basis_analyst
from typing import Optional

# 1. 定义结构化的报告模板 (对应 prompt 中的 "输出格式")
BASIS_ANALYSIS_REPORT_TEMPLATE = """
# {commodity_name} 基差分析报告

## 数据来源与方法声明
本报告数据来源于专业数据提供商（如Wind、iFind、钢联、卓创等）及交易所公开数据，时间范围为 {start_date} 至 {end_date}。分析方法聚焦于基差的历史统计、季节性规律、区域差异及套利机会挖掘。

---

## 一、全国基差走势分析 ({start_date} - {end_date})

- **历史统计特征**:
    - **年度均价**: [计算并填写]
    - **季度均价**: [计算并填写]
    - **历史最大值**: [填写数值和日期]
    - **历史最小值**: [填写数值和日期]
    - **主要波动区间**: [描述]

- **季节性规律**:
    - [描述基差在一年中的季节性变化规律，例如哪个季度通常走强/走弱，并分析原因。]

- **近期变化分析 (近1个月)**:
    - [描述近1个月基差的具体变化趋势。]
    - [判断当前基差水平是否偏离历史季节性规律，并解释原因。]

---

## 二、区域基差差异分析 ({start_date} - {end_date})

- **主要产销区基差对比**:
    - **华北**: [描述该区域基差的强弱特征]
    - **华南**: [描述该区域基差的强弱特征]
    - **华东**: [描述该区域基差的强弱特征]
    - [对比分析各区域间的强弱关系及其背后的物流、供需逻辑。]

- **跨区域套利机会分析**:
    - **稳定价差区域对**: [识别出价差关系稳定的区域对，例如广东与广西。]
    - **套利触发阈值**: **[计算并明确指出当A地与B地价差超过多少元/吨时，套利窗口打开]**。
    - [分析套利操作的可行性及潜在风险。]

---

## 三、基差走势预测与交易策略

- **未来1-3个月基差走势预测**:
    - [基于历史规律和当前市场状况，预测未来基差的走势方向（扩大/收窄/震荡）。]

- **交易策略与风险提示**:
    - **策略建议**: [基于基差视角，提出具体的交易策略，如期现套利、跨期套利等。]
    - **风险提示**: [指出可能影响基差走势的主要风险点，如政策变化、极端天气、物流中断等。]

---

## 四、核心总结

[用一段话总结当前 {commodity_name} 基差市场的核心特征和主要机会/风险。]
"""

# 2. 创建“任务工厂”函数
def create_basis_analysis_task(
    commodity_name: str,
    start_date: str = "2020-11-01",
    end_date: str = "2025-11-30",
    report_template: Optional[str] = None,
    async_execution: bool = False
) -> Task:
    """
    动态生成一个商品基差分析任务。

    Args:
        commodity_name (str): 要分析的商品名称，例如 "螺纹钢"。
        start_date (str): 历史数据的开始日期，格式 'YYYY-MM-DD'。
        end_date (str): 历史数据的结束日期，格式 'YYYY-MM-DD'。
        report_template (Optional[str]): 可选的自定义报告模板。如果为 None，则使用默认模板。
        async_execution (bool): 是否异步执行任务。

    Returns:
        Task: 一个配置好的 CrewAI Task 实例。
    """
    
    final_template = report_template or BASIS_ANALYSIS_REPORT_TEMPLATE

    # 使用 f-string 动态构建任务描述 (对应 prompt 中的 "角色" 和 "分析维度")
    description = (
        f"你是一位大宗商品基差分析专家，专注于市场结构研究和套利机会挖掘。"
        f"你的任务是针对【{commodity_name}】，生成一份详细的基差分析报告。"
        "请严格按照以下步骤执行："
        f"1. **获取基差数据**：使用 'Data Fetching Tool' 获取该产品从 {start_date} 到 {end_date} 的基差数据。"
        "   - endpoint: '/data/basis'"
        f"   - params_json: '{{\"product\": \"{commodity_name}\", \"start_date\": \"{start_date}\", \"end_date\": \"{end_date}\"}}'"
        "   - model_name: 'BasisDataPoint'"
        "2. **执行分析**：基于获取到的数据，你需要从以下几个核心维度进行深入分析："
        "   a) **全国基差走势**：计算年度、季度基差的均价、最大/最小值和波动区间；识别季节性规律；重点分析近1个月的变化。"
        "   b) **区域基差差异**：对比主要产销区（如华北、华南、华东）的基差强弱；识别稳定价差的区域对；计算并明确跨区域套利的触发阈值。"
        "3. **撰写报告**：将你的所有分析结果，严格遵循给定的 Markdown 模板格式，撰写最终的专业报告。"
        "   - 确保模板中的占位符（如商品名、日期）被正确替换。"
        "   - 关键数据（如均价、阈值）请加粗显示。"
        "   - 在报告开头，必须包含“数据来源与方法声明”。"
        "   - 在报告末尾，用一段话总结当前基差市场的核心特征和主要机会/风险。"
    )

    # 使用 f-string 格式化最终输出模板
    expected_output = final_template.format(
        commodity_name=commodity_name,
        start_date=start_date,
        end_date=end_date
    )

    return Task(
        description=description,
        expected_output=expected_output,
        agent=basis_analyst,
        async_execution=async_execution
    )

# 3. (可选) 为了向后兼容，可以保留一个默认的 Task 实例
# basis_analysis_task = create_basis_analysis_task(commodity_name="螺纹钢")
