# tools/edt_data_tool_enhanced.py
from crewai.tools import tool
from data_providers.ifind_http_client import IFinDHTTPClient
from config.ifind_edb_mapping import IFindEDBMapping
from typing import List, Dict, Any
import json

class EnhancedEDBDataTool:
    """
    增强版EDB数据工具
    针对您的CrewAI项目优化
    """
    
    def __init__(self):
        self.client = IFinDHTTPClient()
        self.mapping = IFindEDBMapping()
    
    @tool("获取EDB数据用于基差分析")
    def get_basis_analysis_data(
        self,
        start_date: str,
        end_date: str
    ) -> str:
        """获取基差分析所需的数据"""
        indicators = self.mapping.get_required_indicators('basis')
        return self._get_edb_data(indicators, start_date, end_date, "基差")
    
    @tool("获取EDB数据用于库存分析")
    def get_inventory_analysis_data(
        self,
        start_date: str,
        end_date: str
    ) -> str:
        """获取库存分析所需的数据"""
        indicators = self.mapping.get_required_indicators('inventory')
        return self._get_edb_data(indicators, start_date, end_date, "库存")
    
    @tool("获取EDB数据用于供需分析")
    def get_supply_demand_analysis_data(
        self,
        start_date: str,
        end_date: str
    ) -> str:
        """获取供需分析所需的数据"""
        indicators = self.mapping.get_required_indicators('supply_demand')
        return self._get_edb_data(indicators, start_date, end_date, "供需")
    
    @tool("获取EDB数据用于表观需求分析")
    def get_apparent_demand_analysis_data(
        self,
        start_date: str,
        end_date: str
    ) -> str:
        """获取表观需求分析所需的数据"""
        indicators = self.mapping.get_required_indicators('apparent_demand')
        return self._get_edb_data(indicators, start_date, end_date, "表观需求")
    
    @tool("获取EDB数据用于需求预测")
    def get_demand_forecasting_data(
        self,
        start_date: str,
        end_date: str
    ) -> str:
        """获取需求预测所需的数据"""
        indicators = self.mapping.get_required_indicators('demand_forecasting')
        return self._get_edb_data(indicators, start_date, end_date, "需求预测")
    
    @tool("获取EDB数据用于宏观经济分析")
    def get_macro_economic_data(
        self,
        start_date: str,
        end_date: str
    ) -> str:
        """获取宏观经济分析所需的数据"""
        indicators = self.mapping.get_required_indicators('macro_economic')
        return self._get_edb_data(indicators, start_date, end_date, "宏观经济")
    
    @tool("获取EDB数据用于价格技术分析")
    def get_price_technical_data(
        self,
        start_date: str,
        end_date: str
    ) -> str:
        """获取价格技术分析所需的数据"""
        indicators = self.mapping.get_required_indicators('price_technical')
        return self._get_edb_data(indicators, start_date, end_date, "价格技术")
    
    @tool("获取EDB数据用于量化策略")
    def get_quant_strategy_data(
        self,
        start_date: str,
        end_date: str
    ) -> str:
        """获取量化策略所需的数据"""
        indicators = self.mapping.get_required_indicators('quant_strategy')
        return self._get_edb_data(indicators, start_date, end_date, "量化策略")
    
    @tool("获取EDB数据用于交易执行")
    def get_trading_data(
        self,
        start_date: str,
        end_date: str
    ) -> str:
        """获取交易执行所需的数据"""
        indicators = self.mapping.get_required_indicators('trading')
        return self._get_edb_data(indicators, start_date, end_date, "交易执行")
    
    @tool("获取自定义EDB数据")
    def get_custom_edb_data(
        self,
        indicators: List[str],
        start_date: str,
        end_date: str
    ) -> str:
        """获取自定义EDB数据"""
        return self._get_edb_data(indicators, start_date, end_date, "自定义")
    
    def _get_edb_data(
        self,
        indicators: List[str],
        start_date: str,
        end_date: str,
        analysis_type: str
    ) -> str:
        """通用的EDB数据获取方法"""
        try:
            if not indicators:
                return f"❌ {analysis_type}分析：未找到相关指标"
            
            result = self.client.get_edb_data(
                indicators=indicators,
                start_date=start_date,
                end_date=end_date
            )
            
            # 解析结果并生成摘要
            summary = f"✅ {analysis_type}分析：获取到 {len(result.get('tables', []))} 个指标\n"
            
            if "tables" in result and result["tables"]:
                for table in result["tables"]:
                    if "table" in table:
                        values = list(table["table"].values())[0] if table["table"] else []
                        if isinstance(values, list) and values:
                            latest_value = values[-1]
                            avg_value = sum([v for v in values if v is not None]) / len([v for v in values if v is not None])
                            summary += f"   • 最新值: {latest_value:.2f}, 均值: {avg_value:.2f}\n"
            
            return summary
            
        except Exception as e:
            return f"❌ {analysis_type}分析：获取数据失败 - {str(e)}"
