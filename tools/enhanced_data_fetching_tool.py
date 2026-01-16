# tools/enhanced_data_fetching_tool.py
from crewai.tools import tool
from data_providers.ifind_http_client import IFinDHTTPClient
from config.ifind_edb_mapping import IFindEDBMapping
from typing import List, Dict, Any
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class EnhancedEDBDataTool:
    """
    完整版增强EDB数据工具 - 解决所有已知问题
    """
    
    def __init__(self):
        self.client = IFinDHTTPClient()
        self.mapping = IFindEDBMapping()
        
        # 强制启用DEBUG日志
        logger.setLevel(logging.DEBUG)
        
        # 创建文件处理器
        file_handler = logging.FileHandler('logs/data_fetch_detailed.log', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    @tool("获取EDB数据用于基差分析")
    def get_basis_analysis_data(
        self,
        start_date: str,
        end_date: str
    ) -> str:
        """获取基差分析所需的数据"""
        indicators = self.mapping.get_required_indicators('basis')
        return self._get_edb_data_safe(indicators, start_date, end_date, "基差")
    
    @tool("获取EDB数据用于库存分析")
    def get_inventory_analysis_data(
        self,
        start_date: str,
        end_date: str
    ) -> str:
        """获取库存分析所需的数据"""
        indicators = self.mapping.get_required_indicators('inventory')
        return self._get_edb_data_safe(indicators, start_date, end_date, "库存")
    
    @tool("获取EDB数据用于供需分析")
    def get_supply_demand_analysis_data(
        self,
        start_date: str,
        end_date: str
    ) -> str:
        """获取供需分析所需的数据"""
        indicators = self.mapping.get_required_indicators('supply_demand')
        return self._get_edb_data_safe(indicators, start_date, end_date, "供需")
    
    @tool("获取EDB数据用于表观需求分析")
    def get_apparent_demand_analysis_data(
        self,
        start_date: str,
        end_date: str
    ) -> str:
        """获取表观需求分析所需的数据"""
        indicators = self.mapping.get_required_indicators('apparent_demand')
        return self._get_edb_data_safe(indicators, start_date, end_date, "表观需求")
    
    @tool("获取EDB数据用于需求预测")
    def get_demand_forecasting_data(
        self,
        start_date: str,
        end_date: str
    ) -> str:
        """获取需求预测所需的数据"""
        indicators = self.mapping.get_required_indicators('demand_forecasting')
        return self._get_edb_data_safe(indicators, start_date, end_date, "需求预测")
    
    @tool("获取EDB数据用于宏观经济分析")
    def get_macro_economic_data(
        self,
        start_date: str,
        end_date: str
    ) -> str:
        """获取宏观经济分析所需的数据"""
        indicators = self.mapping.get_required_indicators('macro_economic')
        return self._get_edb_data_safe(indicators, start_date, end_date, "宏观经济")
    
    @tool("获取EDB数据用于价格技术分析")
    def get_price_technical_data(
        self,
        start_date: str,
        end_date: str
    ) -> str:
        """获取价格技术分析所需的数据"""
        indicators = self.mapping.get_required_indicators('price_technical')
        return self._get_edb_data_safe(indicators, start_date, end_date, "价格技术")
    
    @tool("获取EDB数据用于量化策略")
    def get_quant_strategy_data(
        self,
        start_date: str,
        end_date: str
    ) -> str:
        """获取量化策略所需的数据"""
        indicators = self.mapping.get_required_indicators('quant_strategy')
        return self._get_edb_data_safe(indicators, start_date, end_date, "量化策略")
    
    @tool("获取EDB数据用于交易执行")
    def get_trading_data(
        self,
        start_date: str,
        end_date: str
    ) -> str:
        """获取交易执行所需的数据"""
        indicators = self.mapping.get_required_indicators('trading')
        return self._get_edb_data_safe(indicators, start_date, end_date, "交易执行")
    
    def _get_edb_data_with_full_debug(
        self,
        indicators: List[str],
        start_date: str,
        end_date: str,
        analysis_type: str
    ) -> str:
        """带完整调试信息的EDB数据获取方法"""
        try:
            logger.info(f"=== 开始获取{analysis_type}数据 ===")
            logger.debug(f"请求参数:")
            logger.debug(f"  指标数量: {len(indicators)}")
            logger.debug(f"  指标列表: {indicators}")
            logger.debug(f"  时间范围: {start_date} 至 {end_date}")
            
            if not indicators:
                error_msg = f"❌ {analysis_type}分析：未找到相关指标"
                logger.warning(error_msg)
                return error_msg
            
            # 调用API
            result = self.client.get_edb_data(
                indicators=indicators,
                start_date=start_date,
                end_date=end_date
            )
            
            # 记录完整的API响应
            logger.info(f"API响应结构: {list(result.keys())}")
            logger.debug(f"完整API响应: {json.dumps(result, ensure_ascii=False, indent=2)[:500]}...")
            
            # 验证API响应
            if not result or 'errorcode' not in result:
                error_msg = f"❌ {analysis_type}分析：API响应不完整"
                logger.error(error_msg)
                return error_msg
            
            if result.get('errorcode', 0) != 0:
                error_msg = result.get('errmsg', '未知错误')
                final_error = f"❌ {analysis_type}分析：API错误 - {error_msg}"
                logger.error(final_error)
                return final_error
            
            # 检查是否有数据
            tables = result.get('tables', [])
            if not tables:
                warning_msg = f"⚠️ {analysis_type}分析：未查询到 {start_date} 至 {end_date} 期间的相关数据。"
                logger.warning(warning_msg)
                return warning_msg
            
            # 强制记录所有数据内容
            self._log_all_data_content(tables, analysis_type)
            
            # 构建返回摘要
            summary = self._build_data_summary(tables, analysis_type, start_date, end_date)
            
            logger.info(f"=== {analysis_type}数据获取完成 ===")
            return summary
            
        except Exception as e:
            error_msg = f"❌ {analysis_type}分析：获取数据失败 - {str(e)}"
            logger.exception(f"数据获取异常: {e}")  # 使用exception记录完整堆栈
            return error_msg
    
    def _log_all_data_content(self, tables: List[Dict], analysis_type: str):
        """强制记录所有数据内容"""
        logger.info(f"=== {analysis_type}原始数据内容 ===")
        
        for i, table in enumerate(tables[:5]):  # 记录前5个表格
            logger.info(f"表格 {i+1}:")
            logger.info(f"  THS代码: {table.get('thscode', 'N/A')}")
            logger.info(f"  数据类型: {table.get('datatype', [])}")
            logger.info(f"  时间字段: {table.get('time', [])[:10]}...")  # 前10个时间点
            
            if "table" in table and table["table"]:
                values_dict = table["table"]
                logger.info(f"  指标数量: {len(values_dict)}")
                
                for indicator_key, values in list(values_dict.items())[:3]:  # 前3个指标
                    if isinstance(values, list):
                        valid_values = [v for v in values if v is not None]
                        logger.info(f"  指标 {indicator_key}: {valid_values[:20]}...")  # 前20个值
                    else:
                        logger.info(f"  指标 {indicator_key}: {values}")
            
            logger.info(f"  表格 {i+1} 完整数据: {json.dumps(table, ensure_ascii=False, indent=2)[:1000]}...")
    
    def _build_data_summary(self, tables: List[Dict], analysis_type: str, start_date: str, end_date: str) -> str:
        """构建数据摘要返回给Agent"""
        summary_parts = [f"✅ {analysis_type}分析：获取到 {len(tables)} 个指标"]
        
        total_data_points = 0
        sample_tables = []
        
        for i, table in enumerate(tables[:3]):
            if "table" in table and table["table"]:
                values_dict = table["table"]
                if values_dict:
                    first_key = list(values_dict.keys())[0]
                    values = values_dict[first_key]
                    if isinstance(values, list):
                        valid_values = [v for v in values if v is not None]
                        if valid_values:
                            total_data_points += len(valid_values)
                            latest_value = valid_values[-1]
                            avg_value = sum(valid_values) / len(valid_values)
                            
                            # 添加样本数据
                            sample_values = valid_values[-5:]  # 最近5个值
                            sample_tables.append(f"     • 样本: {sample_values}")
                            
                            summary_parts.append(f"   • 指标{i+1}: {len(valid_values)}个数据点")
                            summary_parts.append(f"     • 最新值={latest_value:.2f}, 均值={avg_value:.2f}")
                            
                            # 添加样本数据到摘要
                            summary_parts.extend(sample_tables)
        
        summary_parts.append(f"   • 总计: {total_data_points}个有效数据点")
        summary_parts.append(f"   • 时间范围: {start_date} 至 {end_date}")
        
        return "\n".join(summary_parts)