# tools/data_fetching_tool.py

from typing import List, Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field, TypeAdapter
import requests
import json

# 导入所有需要的数据模型
from schemas.models import (
    BasisDataPoint, 
    FuturesHistoryDataPoint, 
    FuturesSnapshotDataPoint,
    InventoryDataPoint, 
    MacroDataPoint,
    PriceDataPoint, 
    SupplyDemandDataPoint
)

class DataFetchingInput(BaseModel):
    endpoint: str = Field(..., description="API端点，如 '/data/basis'")
    params_json: str = Field(..., description="查询参数的JSON字符串，例如 '{\"product\": \"豆粕\"}'")
    model_name: str = Field(..., description="期望返回的数据模型名称，如 'BasisDataPoint'")

class DataFetchingTool(BaseTool):
    name: str = "Data Fetching Tool"
    description: str = "从本地数据服务API获取金融数据，如基差、价格、库存、宏观、供需等。"
    args_schema: Type[BaseModel] = DataFetchingInput

    def _run(self, endpoint: str, params_json: str, model_name: str) -> str:
        base_url = "http://localhost:8000" # 数据服务地址
        url = f"{base_url}{endpoint}"
        
        try:
            params = json.loads(params_json)
        except json.JSONDecodeError:
            return "错误：提供的参数字符串不是有效的JSON格式。"

        # 扩展模型映射表
        model_map = {
            "BasisDataPoint": BasisDataPoint,
            "PriceDataPoint": PriceDataPoint,
            "FuturesHistoryDataPoint": FuturesHistoryDataPoint,
            "FuturesSnapshotDataPoint": FuturesSnapshotDataPoint,
            "InventoryDataPoint": InventoryDataPoint,
            "MacroDataPoint": MacroDataPoint,
            "SupplyDemandDataPoint": SupplyDemandDataPoint,
        }
        
        data_point_model = model_map.get(model_name)
        if not data_point_model:
            available_models = ", ".join(model_map.keys())
            return f"错误：未知的数据模型名称 '{model_name}'。可用模型: {available_models}"

        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            json_response = response.json()
            if json_response.get('code') != 200:
                return f"API返回错误: {json_response.get('message')}"

            raw_data_list = json_response.get('data', [])
            
            adapter = TypeAdapter(List[data_point_model])
            validated_data = adapter.validate_python(raw_data_list)
            
            if not validated_data:
                return "未查询到相关数据。"
            
            # 将数据转换为易于LLM阅读的文本
            data_as_text = "\n".join([f"- {item.model_dump_json(indent=2)}" for item in validated_data])
            return f"成功获取到 {len(validated_data)} 条 '{model_name}' 数据：\n{data_as_text}"

        except requests.exceptions.RequestException as e:
            return f"获取数据时网络请求失败: {e}"
        except Exception as e:
            return f"处理数据时发生未知错误: {e}"
