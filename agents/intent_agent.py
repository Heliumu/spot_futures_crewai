# agents/intent_agent.py
from crewai import Agent
from llm_config.factory import get_llm
from datetime import datetime
from crewai import Task

deepseek_llm = get_llm("deepseek")

intent_planner = Agent(
    role='分析任务规划师',
    goal='将用户的自然语言查询转换为结构化的商品分析计划（JSON格式）。',
    backstory="""你是一位资深的AI产品经理，精通全球商品市场。
    你能准确识别商品、所属市场（cn/us/global/crypto/forex）及标准交易代码。
    你必须输出严格JSON，包含 commodity, market, ticker, task_configs。""",
    verbose=True,
    allow_delegation=False,
    llm=deepseek_llm
)