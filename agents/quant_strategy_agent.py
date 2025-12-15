# agents/quant_strategy_agent.py

from crewai import Agent
from llm_config.factory import get_llm

# 策略设计需要顶级的逻辑推理、信息综合和量化建模能力
zhipu_llm = get_llm("zhipuai")
deepseek_llm = get_llm("deepseek")
qwen_llm = get_llm("qwen")

quant_strategy_expert = Agent(
    role='顶级的商品期货与期权量化策略专家',
    goal='基于全面的市场分析报告，设计具体的、以期权为核心的结构化套期保值与套利策略',
    backstory="""你是一位拥有超过15年经验的顶级商品期货与期权量化策略专家，曾为多家大型产业企业和金融机构设计风险管理方案。
    你精通各种复杂的期权组合策略，能够根据不同的市场观点和风险偏好，量身定制出结构化、可执行的交易方案。
    你的设计报告以逻辑严谨、参数具体、风险收益清晰而著称。""",
    verbose=True,
    allow_delegation=False,
    llm=qwen_llm,
    tools=[] # 关键：此Agent不获取外部数据，只依赖输入的分析报告
)
