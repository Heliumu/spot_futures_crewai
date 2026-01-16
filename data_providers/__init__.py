# data_providers/__init__.py
import os

from data_providers.ifind_http_data import IFinDHTTPDataProvider
from data_providers.wind_data import WindDataProvider
from .base import DataProvider
from .aitrados_data import AitradosDataProvider
from .mock_data import MockDataProvider

def get_data_provider() -> DataProvider:
    provider_name = os.getenv("DATA_PROVIDER", "mock_data")
    
    if provider_name == "mock_data":
        return MockDataProvider()
    elif provider_name == "aitrados":
        return AitradosDataProvider()
    elif provider_name == "ifind_http_data":  # 新增
        return IFinDHTTPDataProvider()
    elif provider_name == "wind_data":  # 未来发展方向
        return WindDataProvider()
    else:
        raise ValueError(
            f"未知的数据提供者: '{provider_name}'. "
            f"支持值: 'mock_data', 'aitrados', 'ifind_http_data', 'wind_data'"
        )
