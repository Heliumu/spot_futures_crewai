# agents/price_technical_agent.py

from crewai import Agent
from llm_config.factory import get_llm
from tools.data_fetching_tool import DataFetchingTool
from tools.zhipu_web_search_tool import ZhipuWebSearchTool
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
if dotenv_path:
    print(f"Loading .env file from: {dotenv_path}")
    load_dotenv(dotenv_path)
else:
    print("Warning: .env file not found!")
# 技术分析和交易决策需要强大的逻辑推理和模式识别能力
zhipu_llm = get_llm("zhipuai")
deepseek_llm = get_llm("deepseek")
qwen_llm = get_llm("qwen")
# # 加载环境变量
# load_dotenv()
# 实例化工具
data_tool = DataFetchingTool()
web_search_tool = ZhipuWebSearchTool()

price_technical_analyst = Agent(
    role='期货交易分析师',
    goal='结合技术分析和市场情绪，对指定商品的期货价格进行研判，并给出未来展望和交易观点',
    backstory="""你是一位拥有超过10年实盘经验的资深期货交易分析师。
    你精通各种技术分析理论（如道氏理论、波浪理论、江恩理论等），对K线形态、技术指标和量价关系有深刻的理解。
    同时，你对市场情绪和突发新闻对价格的短期冲击有敏锐的洞察力。
    你的分析报告以数据驱动、观点鲜明、贴近实战而著称。""",
    verbose=True,
    allow_delegation=False,
    llm=deepseek_llm,
    tools=[data_tool, web_search_tool] # 必须同时具备数据获取和搜索能力
)
