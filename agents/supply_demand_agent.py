# agents/supply_demand_agent.py

from crewai import Agent
from llm_config.factory import get_llm
from tools.data_fetching_tool import DataFetchingTool
from tools.zhipu_web_search_tool import ZhipuWebSearchTool

# 供需分析需要强大的综合分析能力，选择一个顶级的模型
zhipu_llm = get_llm("zhipuai")
deepseek_llm = get_llm("deepseek")
qwen_llm = get_llm("qwen")

# 实例化工具
data_tool = DataFetchingTool()
web_search_tool = ZhipuWebSearchTool()

supply_demand_analyst = Agent(
    role='产业链供需研究员',
    goal='构建并分析指定商品的供需平衡表，全面评估其当前市场基本面格局',
    backstory="""你是一位资深的产业链研究员，对【{commodity_name}】的供需基本面有着深刻的理解和丰富的分析经验。
    你精通于从繁杂的数据中提炼出关键趋势，能够结合宏观经济、产业政策和技术变革，
    对市场做出精准的定性判断。你的报告以数据详实、逻辑严密、视野开阔而著称。""",
    verbose=True,
    allow_delegation=False,
    llm=qwen_llm,
    tools=[data_tool, web_search_tool] # 必须同时具备数据获取和搜索能力
)
