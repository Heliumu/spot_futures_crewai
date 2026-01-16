# data_providers/ifind_http_data.py
from .base import DataProvider
from .ifind_http_client import IFinDHTTPClient
from schemas.models import (
    PriceDataPoint, 
    FuturesHistoryDataPoint, 
    MacroDataPoint,
    BasisDataPoint,
    SupplyDemandDataPoint
)
from typing import Any, Dict, List, Optional
import pandas as pd
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)  # 修正：添加logger导入

class IFinDHTTPDataProvider(DataProvider):
    """
    iFinD HTTP API 数据提供者
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
        """
        获取历史数据 - 适配现有接口
        """
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
        region: str  # 修正：添加region参数
    ) -> List[PriceDataPoint]:
        """获取股票历史数据"""
        # 使用基础数据函数获取股票历史数据
        indicators = ["ths_close_price_stock", "ths_open_price_stock", 
                     "ths_high_price_stock", "ths_low_price_stock", 
                     "ths_volume_stock"]
        
        result = self.client.get_basic_data(
            codes=[ticker],
            indicators=indicators,
            start_date=start_date,
            end_date=end_date
        )
        
        data_points = []
        if "tables" in result and result["tables"]:
            for table in result["tables"]:
                if "table" in table and table["table"]:
                    for row in table["table"]:
                        try:
                            date_str = row.get("time", "")  # iFinD通常返回time字段
                            if date_str:
                                # 解析日期字符串，可能需要根据实际返回格式调整
                                date_obj = datetime.strptime(date_str.split()[0], "%Y-%m-%d").date()
                                data_point = PriceDataPoint(
                                    date=date_obj,
                                    product=ticker,
                                    price=float(row.get("ths_close_price_stock", 0)),
                                    open=float(row.get("ths_open_price_stock", 0)),
                                    high=float(row.get("ths_high_price_stock", 0)),
                                    low=float(row.get("ths_low_price_stock", 0)),
                                    volume=int(row.get("ths_volume_stock", 0)),
                                    market=region  
                                )
                                data_points.append(data_point)
                        except Exception as e:
                            logger.warning(f"股票数据转换失败: {e}, row: {row}")
                            continue
        
        return data_points
    
    def _get_future_history(
        self, 
        ticker: str, 
        start_date: str, 
        end_date: str,
        region: str  # 修正：添加region参数
    ) -> List[FuturesHistoryDataPoint]:
        """获取期货历史数据"""
        # 期货数据指标
        indicators = ["ths_close_price_fund", "ths_open_price_fund", 
                     "ths_high_price_fund", "ths_low_price_fund", 
                     "ths_volume_fund", "ths_oi_fund"]
        
        result = self.client.get_basic_data(
            codes=[ticker],
            indicators=indicators,
            start_date=start_date,
            end_date=end_date
        )
        
        data_points = []
        if "tables" in result and result["tables"]:
            for table in result["tables"]:
                if "table" in table and table["table"]:
                    for row in table["table"]:
                        try:
                            datetime_str = row.get("time", "")
                            if datetime_str:
                                dt = datetime.strptime(datetime_str.split()[0], "%Y-%m-%d").date()
                                # 创建datetime对象（假设是日频数据）
                                dt_obj = datetime.combine(dt, datetime.min.time())
                                data_point = FuturesHistoryDataPoint(
                                    datetime=dt_obj,
                                    product=ticker,
                                    symbol=ticker,
                                    open=float(row.get("ths_open_price_fund", 0)),
                                    high=float(row.get("ths_high_price_fund", 0)),
                                    low=float(row.get("ths_low_price_fund", 0)),
                                    close=float(row.get("ths_close_price_fund", 0)),
                                    volume=int(row.get("ths_volume_fund", 0)),
                                    open_interest=int(row.get("ths_oi_fund", 0))
                                )
                                data_points.append(data_point)
                        except Exception as e:
                            logger.warning(f"期货数据转换失败: {e}, row: {row}")
                            continue
        
        return data_points
    
    def _get_macro_history(
        self, 
        indicator_code: str, 
        start_date: str, 
        end_date: str,
        region: str  # 修正：添加region参数
    ) -> List[MacroDataPoint]:
        """获取宏观数据"""
        result = self.client.get_edb_data(
            codes=[indicator_code],
            start_date=start_date,
            end_date=end_date
        )
        
        data_points = []
        if "tables" in result and result["tables"]:
            for table in result["tables"]:
                if "table" in table and table["table"]:
                    for row in table["table"]:
                        try:
                            date_str = row.get("time", "")
                            if date_str:
                                date_obj = datetime.strptime(date_str.split()[0], "%Y-%m-%d").date()
                                data_point = MacroDataPoint(
                                    date=date_obj,
                                    indicator_name=indicator_code,
                                    indicator_value=float(row.get("value", 0)),
                                    region=region  # 修正：使用传入的region参数
                                )
                                data_points.append(data_point)
                        except Exception as e:
                            logger.warning(f"宏观数据转换失败: {e}, row: {row}")
                            continue
        
        return data_points
    
    def _get_generic_history(
        self, 
        ticker: str, 
        start_date: str, 
        end_date: str,
        region: str
    ) -> List:
        """通用历史数据获取"""
        # 根据ticker类型判断使用哪个函数
        if ticker.startswith(('0', '3', '6')):  # 股票代码
            return self._get_stock_history(ticker, start_date, end_date, region)
        else:
            return self._get_stock_history(ticker, start_date, end_date, region)
    
    def get_real_time_data(self, ticker: str) -> Dict[str, Any]:
        """获取实时数据"""
        result = self.client.get_real_time_quotation(codes=[ticker])
        return result
    
    def get_custom_data(
        self, 
        codes: List[str], 
        indicators: List[str], 
        start_date: str, 
        end_date: str,
        functionpara: Optional[Dict] = None
    ) -> Dict:
        """获取自定义数据"""
        return self.client.get_basic_data(
            codes=codes,
            indicators=indicators,
            start_date=start_date,
            end_date=end_date,
            functionpara=functionpara
        )
