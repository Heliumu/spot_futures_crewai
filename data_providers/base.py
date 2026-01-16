# data_providers/base.py
from abc import ABC, abstractmethod
from typing import List, Optional

class DataProvider(ABC):
    """
    所有数据提供者的抽象基类。
    必须实现以下方法：
    - get_history_data: 获取历史行情数据
    """
    
    @abstractmethod
    def get_history_data(
        self,
        asset_class: str,
        region: str,
        ticker: str,
        start_date: Optional[str],
        end_date: Optional[str]
    ) -> List:
        """
        获取历史行情数据。
        
        Args:
            asset_class: 资产类别 ('future', 'stock', 'forex', 'crypto')
            region: 市场区域 (ISO国家代码，如 'cn', 'us', 'global')
            ticker: 交易代码 (如 'rb', '600000', 'USDCNY')
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            
        Returns:
            数据列表（具体类型由子类决定）
        """
        pass
