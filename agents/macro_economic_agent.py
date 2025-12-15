# agents/macro_economic_agent.py

from crewai import Agent
from llm_config.factory import get_llm
from tools.data_fetching_tool import DataFetchingTool
from tools.zhipu_web_search_tool import ZhipuWebSearchTool

# 宏观分析需要强大的逻辑推理和信息整合能力，选择一个顶级的综合模型
zhipu_llm = get_llm("zhipuai")
deepseek_llm = get_llm("deepseek")
qwen_llm = get_llm("qwen")

# 实例化工具
data_tool = DataFetchingTool()
web_search_tool = ZhipuWebSearchTool()

macro_economic_analyst = Agent(
    role='宏观经济分析师',
    goal='分析影响指定商品价格和贸易的关键宏观经济因素，并评估其市场影响',
    backstory="""你是一位资深的宏观经济分析师，对全球宏观经济形势、货币政策、财政政策及国际贸易格局有着深刻的洞察力。
    你擅长从纷繁复杂的经济数据和政策变动中，识别出对大宗商品市场具有决定性影响的核心因素。
    你的报告以视野宏大、逻辑严谨、观点明确而著称。""",
    verbose=True,
    allow_delegation=False,
    llm=deepseek_llm,
    tools=[data_tool, web_search_tool] # 必须同时具备数据获取和搜索能力
)
