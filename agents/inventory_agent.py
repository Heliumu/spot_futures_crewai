# agents/inventory_agent.py

from crewai import Agent
from llm_config.factory import get_llm
from tools.data_fetching_tool import DataFetchingTool
from tools.zhipu_web_search_tool import ZhipuWebSearchTool # 导入网络搜索工具

# 为库存分析选择一个擅长数据分析和逻辑推理的模型
zhipu_llm = get_llm("zhipuai")
deepseek_llm = get_llm("deepseek")
qwen_llm = get_llm("qwen")

# 实例化工具
data_tool = DataFetchingTool()
web_search_tool = ZhipuWebSearchTool()

inventory_analyst = Agent(
    role='资深库存数据分析师',
    goal='对指定商品的库存数据进行深度分析，洞察其历史水平、变化趋势，并结合贸易物流信息，判断其对价格的潜在影响',
    backstory="""你是一位在商品供应链和数据分析领域拥有超过12年经验的资深库存分析师。
    你精通各种库存数据的解读，能够从库存的细微变化中预判供需格局的演变。
    你不仅能分析结构化数据，还能通过网络搜索获取最新的市场动态、物流和贸易信息，
    从而做出更全面的判断。你的报告以数据详实、逻辑严密和富有前瞻性而闻名。""",
    verbose=True,
    allow_delegation=False,
    llm=deepseek_llm,
    tools=[data_tool, web_search_tool] # 同时拥有数据获取和网络搜索能力
)
