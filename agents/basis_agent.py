# agents/basis_agent.py
from crewai import Agent
# from core.llm_config import get_primary_llm
from tools.data_fetching_tool import DataFetchingTool
from llm_config.factory import get_llm

# 配置示例
zhipu_llm = get_llm("zhipuai")
deepseek_llm = get_llm("deepseek")
qwen_llm = get_llm("qwen")

# llm = get_primary_llm()

basis_analyst = Agent(
    role='资深基差分析师',
    goal='对指定商品的基差数据进行深度分析，洞察其历史位置、变化趋势，并预测未来走势',
    backstory="""你是一位在商品期货市场拥有超过15年经验的资深基差分析师。
    你对现货与期货价格的联动关系有着深刻的理解，能够从复杂的基差变化中
    识别出市场情绪、供需矛盾和潜在的套利机会。你的分析报告以严谨、数据驱动和富有洞察力著称。""",
    verbose=True,
    allow_delegation=False,
    llm=zhipu_llm,
    tools=[DataFetchingTool()]
)


