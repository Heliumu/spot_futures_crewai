# agents/demand_forecasting_analyst.py
from crewai import Agent
from tools.data_fetching_tool import DataFetchingTool
from llm_config.factory import get_llm

# 从您的配置中选择一个LLM
deepseek_llm = get_llm("deepseek") # DeepSeek 在推理和预测方面可能表现不错

demand_forecasting_analyst = Agent(
    role='大宗商品量化预测分析师',
    goal='构建科学的需求预测模型，对未来1-3个季度的需求进行量化预测，并评估关键不确定性',
    backstory="""你是一位拥有金融和统计学双重背景的量化分析师。你的工作是将复杂的市场动态
    转化为可量化的预测模型。你不仅关注模型的准确性，更注重模型的逻辑透明度和风险揭示能力。
    你能够综合宏观经济、行业政策和高频数据，为交易团队提供最可靠的未来需求情景分析。""",
    verbose=True,
    allow_delegation=False,
    llm=deepseek_llm,
    tools=[DataFetchingTool()]
)
