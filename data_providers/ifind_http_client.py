# data_providers/ifind_http_client.py
import requests
import json
from typing import List, Optional, Dict, Any
from datetime import datetime, date
import logging
import os

logger = logging.getLogger(__name__)

class IFinDHTTPClient:
    """
    iFinD HTTP API 客户端 - 修正版
    """
    
    def __init__(self):
        self.access_token = os.getenv("IFIND_ACCESS_TOKEN")
        self.refresh_token = os.getenv("IFIND_REFRESH_TOKEN")
        
        if not self.access_token:
            raise ValueError("请在 .env 中设置 IFIND_ACCESS_TOKEN")
        
        self.base_url = os.getenv("IFIND_BASE_URL", "https://quantapi.51ifind.com/api/v1")
        self.headers = {
            "Content-Type": "application/json",
            "access_token": self.access_token
        }
    
    def _make_request(self, endpoint: str, data: Dict) -> Dict:
        """发送HTTP请求"""
        url = f"{self.base_url}/{endpoint}"
        
        try:
            logger.info(f"发送请求到: {url}")
            logger.info(f"请求数据: {data}")
            
            response = requests.post(
                url=url,
                json=data,
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code != 200:
                error_msg = f"HTTP请求失败: {response.status_code}, {response.text}"
                logger.error(error_msg)
                raise Exception(error_msg)
            
            result = response.json()
            logger.info(f"API响应错误码: {result.get('errorcode', 'N/A')}")
            
            # 检查错误码
            if result.get('errorcode', 0) != 0:
                error_msg = f"API错误: {result.get('errmsg', 'Unknown error')}"
                logger.error(error_msg)
                raise Exception(error_msg)
            
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"网络请求失败: {e}")
            raise
        except Exception as e:
            logger.error(f"请求失败: {e}")
            raise
    
    def get_history_quotation(
        self,
        codes: List[str],
        indicators: List[str],
        start_date: str,
        end_date: str,
        functionpara: Optional[Dict] = None
    ) -> Dict:
        """历史行情服务"""
        data = {
            "codes": ",".join(codes),
            "indicators": ",".join(indicators),
            "startdate": start_date.replace("-", ""),
            "enddate": end_date.replace("-", "")
        }
        
        if functionpara:
            data["functionpara"] = functionpara
        
        return self._make_request("cmd_history_quotation", data)
    
    def get_real_time_quotation(
        self,
        codes: List[str],
        indicators: List[str] = None
    ) -> Dict:
        """实时行情服务"""
        data = {
            "codes": ",".join(codes)
        }
        
        if indicators:
            data["indicators"] = ",".join(indicators)
        else:
            data["indicators"] = "latest"
        
        return self._make_request("real_time_quotation", data)
    
    def get_basic_data(
        self,
        codes: List[str],
        indipara: List[Dict],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        functionpara: Optional[Dict] = None
    ) -> Dict:
        """基础数据服务"""
        data = {
            "codes": ",".join(codes),
            "indipara": indipara
        }
        
        if start_date:
            data["startdate"] = start_date.replace("-", "")
        if end_date:
            data["enddate"] = end_date.replace("-", "")
        if functionpara:
            data["functionpara"] = functionpara
        
        return self._make_request("basic_data_service", data)
    
    def get_date_sequence(
        self,
        codes: List[str],
        indipara: List[Dict],
        start_date: str,
        end_date: str,
        functionpara: Optional[Dict] = None
    ) -> Dict:
        """日期序列服务"""
        data = {
            "codes": ",".join(codes),
            "startdate": start_date.replace("-", ""),
            "enddate": end_date.replace("-", ""),
            "indipara": indipara
        }
        
        if functionpara:
            data["functionpara"] = functionpara
        
        return self._make_request("date_sequence", data)
    
    def get_edb_data(
        self,
        indicators: List[str],
        start_date: str,
        end_date: str
    ) -> Dict:
        """经济数据库服务"""
        data = {
            "indicators": ",".join(indicators),
            "startdate": start_date.replace("-", ""),
            "enddate": end_date.replace("-", "")
        }
        
        return self._make_request("edb_service", data)

class IFinDHTTPDataProvider:
    """
    iFinD HTTP 数据提供者 - 修正版
    """
    
    def __init__(self):
        self.client = IFinDHTTPClient()
    
    def get_history_data(
        self,
        asset_class: str,
        region: str,
        ticker: str,
        start_date: Optional[str],
        end_date: Optional[str]
    ) -> List:
        """获取历史数据 - 适配现有接口"""
        try:
            if asset_class == "stock":
                return self._get_stock_history(ticker, start_date, end_date, region)
            elif asset_class == "future":
                return self._get_future_history(ticker, start_date, end_date, region)
            elif asset_class == "macro":
                return self._get_macro_history(ticker, start_date, end_date, region)
            else:
                return self._get_generic_history(ticker, start_date, end_date, region)
        except Exception as e:
            logger.error(f"获取历史数据失败: {e}")
            return []
    
    def _get_stock_history(
        self, 
        ticker: str, 
        start_date: str, 
        end_date: str,
        region: str
    ) -> List:
        """获取股票历史数据"""
        try:
            # 使用历史行情服务
            result = self.client.get_history_quotation(
                codes=[ticker],
                indicators=["open", "high", "low", "close", "volume"],
                start_date=start_date,
                end_date=end_date,
                functionpara={"Fill": "Blank"}
            )
            
            from schemas.models import PriceDataPoint
            data_points = []
            
            if "tables" in result and result["tables"]:
                for table_data in result["tables"]:
                    # 解析数据结构
                    times = table_data.get("time", [])
                    table_values = table_data.get("table", {})
                    
                    # 确保所有指标都有相同长度的时间序列
                    if not times:
                        continue
                    
                    for i in range(len(times)):
                        try:
                            time_str = times[i]
                            
                            # 解析日期
                            if "-" in time_str:
                                date_obj = datetime.strptime(time_str.split()[0], "%Y-%m-%d").date()
                            else:
                                date_obj = datetime.strptime(time_str, "%Y%m%d").date()
                            
                            # 获取对应索引的值
                            open_val = self._safe_float_get(table_values, "open", i)
                            high_val = self._safe_float_get(table_values, "high", i)
                            low_val = self._safe_float_get(table_values, "low", i)
                            close_val = self._safe_float_get(table_values, "close", i)
                            volume_val = self._safe_int_get(table_values, "volume", i)
                            
                            data_point = PriceDataPoint(
                                date=date_obj,
                                product=ticker,
                                price=close_val,
                                open=open_val,
                                high=high_val,
                                low=low_val,
                                volume=volume_val,
                                market=region
                            )
                            data_points.append(data_point)
                            
                        except Exception as e:
                            logger.warning(f"解析第{i}条数据失败: {e}")
                            continue
            
            logger.info(f"成功解析 {len(data_points)} 条股票历史数据")
            return data_points
            
        except Exception as e:
            logger.error(f"获取股票历史数据失败: {e}")
            return []
    
    def _get_future_history(
        self, 
        ticker: str, 
        start_date: str, 
        end_date: str,
        region: str
    ) -> List:
        """获取期货历史数据"""
        return self._get_stock_history(ticker, start_date, end_date, region)
    
    def _get_macro_history(
        self, 
        indicator_code: str, 
        start_date: str, 
        end_date: str,
        region: str
    ) -> List:
        """获取宏观数据"""
        try:
            result = self.client.get_edb_data(
                indicators=[indicator_code],
                start_date=start_date,
                end_date=end_date
            )
            
            from schemas.models import MacroDataPoint
            data_points = []
            
            if "tables" in result and result["tables"]:
                for table_data in result["tables"]:
                    times = table_data.get("time", [])
                    table_values = table_data.get("table", {})
                    
                    if not times:
                        continue
                    
                    for i in range(len(times)):
                        try:
                            time_str = times[i]
                            
                            if "-" in time_str:
                                date_obj = datetime.strptime(time_str.split()[0], "%Y-%m-%d").date()
                            else:
                                date_obj = datetime.strptime(time_str, "%Y%m%d").date()
                            
                            # 对于EDB数据，值可能在不同的字段中
                            value = self._safe_float_get(table_values, indicator_code, i)
                            if value is None:
                                # 尝试其他可能的字段名
                                for key in table_values.keys():
                                    value = self._safe_float_get(table_values, key, i)
                                    if value is not None:
                                        break
                            
                            if value is not None:
                                data_point = MacroDataPoint(
                                    date=date_obj,
                                    indicator_name=indicator_code,
                                    indicator_value=value,
                                    region=region
                                )
                                data_points.append(data_point)
                                
                        except Exception as e:
                            logger.warning(f"解析宏观数据失败: {e}")
                            continue
            
            logger.info(f"成功解析 {len(data_points)} 条宏观数据")
            return data_points
            
        except Exception as e:
            logger.error(f"获取宏观数据失败: {e}")
            return []
    
    def _get_generic_history(
        self, 
        ticker: str, 
        start_date: str, 
        end_date: str,
        region: str
    ) -> List:
        """通用历史数据获取"""
        return self._get_stock_history(ticker, start_date, end_date, region)
    
    def get_real_time_data(self, ticker: str) -> Dict[str, Any]:
        """获取实时数据"""
        try:
            result = self.client.get_real_time_quotation([ticker])
            return result
        except Exception as e:
            logger.error(f"获取实时数据失败: {e}")
            return {}
    
    def _safe_float_get(self, data_dict: Dict, key: str, index: int) -> Optional[float]:
        """安全获取浮点数值"""
        try:
            values = data_dict.get(key, [])
            if isinstance(values, list) and index < len(values):
                val = values[index]
                if val is not None:
                    return float(val)
            return None
        except (ValueError, TypeError):
            return None
    
    def _safe_int_get(self, data_dict: Dict, key: str, index: int) -> Optional[int]:
        """安全获取整数值"""
        try:
            values = data_dict.get(key, [])
            if isinstance(values, list) and index < len(values):
                val = values[index]
                if val is not None:
                    return int(float(val))  # 先转float再转int，处理小数
            return None
        except (ValueError, TypeError):
            return None

class IFinDHTTPDataTool:
    """iFinD HTTP API 数据获取工具"""
    
    def __init__(self):
        self.provider = IFinDHTTPDataProvider()
    
    def get_stock_history_data(
        self,
        ticker: str,
        start_date: str,
        end_date: str,
        indicators: str = "open,high,low,close,volume"
    ) -> str:
        """获取股票历史数据"""
        try:
            result = self.provider._get_stock_history(ticker, start_date, end_date, "cn")
            return f"获取到 {len(result)} 条股票历史数据: {str([d.dict() for d in result[:3]])}"
        except Exception as e:
            return f"获取股票历史数据失败: {str(e)}"
    
    def get_real_time_data(self, ticker: str) -> str:
        """获取实时行情数据"""
        try:
            data = self.provider.get_real_time_data(ticker)
            return f"实时数据: {str(data)[:500]}..."
        except Exception as e:
            return f"获取实时数据失败: {str(e)}"
