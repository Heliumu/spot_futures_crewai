# tools/ifind_http_tool.py
from crewai.tools import tool
from data_providers.ifind_http_data import IFinDHTTPDataProvider
from typing import List, Dict, Any
import json

class IFinDHTTPDataTool:
    """iFinD HTTP API 数据获取工具"""
    
    def __init__(self):
        self.provider = IFinDHTTPDataProvider()
    
    @tool("获取股票历史数据")
    def get_stock_history_data(
        self,
        ticker: str,
        start_date: str,
        end_date: str,
        indicators: str = "open,high,low,close,volume"
    ) -> str:
        """
        获取股票历史数据
        Args:
            ticker: 股票代码，如 '300033.SZ'
            start_date: 开始日期，格式 'YYYY-MM-DD'
            end_date: 结束日期，格式 'YYYY-MM-DD'
            indicators: 指标列表，逗号分隔
        """
        try:
            result = self.provider._get_stock_history(ticker, start_date, end_date)
            return f"获取到 {len(result)} 条股票历史数据: {json.dumps([d.dict() for d in result[:3]], ensure_ascii=False, default=str)}"
        except Exception as e:
            return f"获取股票历史数据失败: {str(e)}"
    
    @tool("获取实时行情")
    def get_real_time_data(self, ticker: str) -> str:
        """获取实时行情数据"""
        try:
            data = self.provider.get_real_time_data(ticker)
            return f"实时数据: {json.dumps(data, ensure_ascii=False, default=str)[:500]}..."
        except Exception as e:
            return f"获取实时数据失败: {str(e)}"
    
    @tool("获取宏观数据")
    def get_macro_data(
        self,
        indicator_code: str,
        start_date: str,
        end_date: str
    ) -> str:
        """获取宏观数据"""
        try:
            result = self.provider._get_macro_history(indicator_code, start_date, end_date)
            return f"获取到 {len(result)} 条宏观数据: {json.dumps([d.dict() for d in result[:3]], ensure_ascii=False, default=str)}"
        except Exception as e:
            return f"获取宏观数据失败: {str(e)}"
    
    @tool("获取自定义数据")
    def get_custom_data(
        self,
        codes: str,
        indicators: str,
        start_date: str,
        end_date: str,
        functionpara: str = "{}"
    ) -> str:
        """
        获取自定义数据
        Args:
            codes: 代码列表，逗号分隔
            indicators: 指标列表，逗号分隔
            start_date: 开始日期
            end_date: 结束日期
            functionpara: 函数参数，JSON字符串
        """
        try:
            codes_list = codes.split(",")
            indicators_list = indicators.split(",")
            functionpara_dict = json.loads(functionpara) if functionpara else {}
            
            result = self.provider.get_custom_data(
                codes=codes_list,
                indicators=indicators_list,
                start_date=start_date,
                end_date=end_date,
                functionpara=functionpara_dict
            )
            return f"自定义数据查询结果: {json.dumps(result, ensure_ascii=False, default=str)[:500]}..."
        except Exception as e:
            return f"获取自定义数据失败: {str(e)}"
