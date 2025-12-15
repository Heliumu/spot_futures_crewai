# tools/zhipu_web_search_tool.py

from typing import Type, Optional
from pydantic import BaseModel, Field, PrivateAttr
from crewai.tools import BaseTool
from utils.web_search_tool import WebSearchTool, WebSearchError
import os

# 1. 输入 Schema 保持不变
class ZhipuWebSearchToolInput(BaseModel):
    """Input schema for ZhipuWebSearchTool."""
    query: str = Field(..., description="The search query string.")
    search_engine: Optional[str] = Field(
        "search_pro_quark", 
        description="The search engine to use. Options: 'search_pro', 'search_pro_quark', 'search_pro_sogou'."
    )

# 【核心改动】使用组合，而不是继承
class ZhipuWebSearchTool(BaseTool):  # 只继承 BaseTool
    name: str = "Zhipu Web Search"
    description: str = (
        "一个强大的网络搜索工具，使用智谱AI的搜索引擎。"
        "可以指定不同的搜索引擎以获取不同类型的网络信息。"
    )
    args_schema: Type[BaseModel] = ZhipuWebSearchToolInput

    # 持有一个 WebSearchTool 的实例作为私有属性
    _searcher: WebSearchTool = PrivateAttr()

    def __init__(self, **kwargs):
        # 1. 从环境变量获取 API Key
        api_key = os.getenv("ZHIPU_SEARCH_API_KEY")
        if not api_key:
            raise ValueError("ZHIPU_SEARCH_API_KEY not found in environment variables.")
        
        # 2. 创建 WebSearchTool 的实例并赋值给私有属性
        #    从 kwargs 中过滤出 WebSearchTool 需要的参数
        web_search_kwargs = {
            "api_key": api_key,
            "default_engine": kwargs.get("default_engine", "search_pro_quark"),
            "api_url": kwargs.get("api_url", "https://open.bigmodel.cn/api/paas/v4/web_search")
        }
        self._searcher = WebSearchTool(**web_search_kwargs)

        # 3. 调用父类 BaseTool 的初始化
        #    因为 name, description, args_schema 都有默认值，Pydantic 可以自动处理
        super().__init__(**kwargs)

    def _run(self, query: str, search_engine: str = "search_pro_quark") -> Optional[str]:
        """
        CrewAI Agent 调用此方法来执行搜索。
        """
        try:
            # 将任务委托给内部的 _searcher 实例
            return self._searcher.search(query=query, search_engine=search_engine)
        except WebSearchError as e:
            return f"搜索时发生错误: {e.message}"
        except Exception as e:
            return f"执行搜索时发生未知错误: {str(e)}"
