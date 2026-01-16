# data_providers/wind_data.py
from .base import DataProvider

class WindDataProvider(DataProvider):
    name = "wind_data"  # ← 与文件名一致
    
    def __init__(self):
        # 初始化逻辑
        pass
    
    def get_history_data(self, asset_class, region, ticker, start_date, end_date):
        # 实现数据获取逻辑
        pass
