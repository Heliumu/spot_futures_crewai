# agents/intent_agent.py
from crewai import Agent
from llm_config.factory import get_llm

zhipu_llm = get_llm("zhipuai")
deepseek_llm = get_llm("deepseek")
qwen_llm = get_llm("qwen")

intent_planner = Agent(
    role='分析任务规划师',
    goal='将用户的自然语言查询转换为一个结构化的、可执行的商品分析计划（JSON格式）。',
    backstory="""你是一位资深的AI产品经理，精通大宗商品分析流程。
    你的任务不是分析，而是理解用户的意图，并规划出需要哪些分析师、分析哪些维度、以及分析的时间范围。
    你必须输出一个严格的JSON对象，包含 'commodity' 和 'task_configs' 字段。""",
    verbose=True,
    allow_delegation=False,
    llm=deepseek_llm
)